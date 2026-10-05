"""Тесты первого и второго этапов эмулятора оболочки."""

import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from src.emulator import (
    make_prompt,
    print_configuration,
    read_arguments,
    run_command,
    run_script,
)


class ShellEmulatorTests(unittest.TestCase):
    """Проверяет команды, параметры и стартовый скрипт."""

    def test_quoted_argument(self):
        """Проверяет аргумент в кавычках."""
        result, should_exit = run_command('ls "папка с пробелами"')
        self.assertEqual(result, "ls: ['папка с пробелами']")
        self.assertFalse(should_exit)

    def test_cd_stub(self):
        """Проверяет команду-заглушку cd."""
        result, should_exit = run_command('cd "Моя папка"')
        self.assertEqual(result, "cd: ['Моя папка']")
        self.assertFalse(should_exit)

    def test_unknown_command(self):
        """Проверяет ошибку для неизвестной команды."""
        result, should_exit = run_command("неизвестная")
        expected = "ошибка: неизвестная команда: неизвестная"
        self.assertEqual(result, expected)
        self.assertFalse(should_exit)

    def test_unclosed_quote(self):
        """Проверяет ошибку при незакрытых кавычках."""
        result, should_exit = run_command('ls "сломано')
        self.assertEqual(result, "ошибка: незакрытые кавычки")
        self.assertFalse(should_exit)

    def test_exit(self):
        """Проверяет завершение работы командой exit."""
        result, should_exit = run_command("exit")
        self.assertEqual(result, "")
        self.assertTrue(should_exit)

    def test_prompt(self):
        """Проверяет формат приглашения."""
        prompt = make_prompt()
        self.assertIn("@", prompt)
        self.assertTrue(prompt.endswith(":~$ "))

    def test_parameters(self):
        """Проверяет чтение двух параметров запуска."""
        values = [
            "emulator.py",
            "--vfs",
            "данные.xml",
            "--script",
            "старт.txt",
        ]
        with patch("sys.argv", values):
            arguments = read_arguments()

        self.assertEqual(arguments.vfs, "данные.xml")
        self.assertEqual(arguments.script, "старт.txt")

    def test_configuration_output(self):
        """Проверяет отладочный вывод параметров."""
        output = StringIO()

        with redirect_stdout(output):
            print_configuration("данные.xml", "старт.txt")

        text = output.getvalue()
        self.assertIn("данные.xml", text)
        self.assertIn("старт.txt", text)

    def test_script_stops_on_error(self):
        """Проверяет остановку скрипта на первой ошибке."""
        content = "ls один\nнеизвестная\ncd два\n"

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "сценарий.txt"
            path.write_text(content, encoding="utf-8")
            output = StringIO()

            with redirect_stdout(output):
                result, should_exit = run_script(
                    str(path),
                    "user@pc:~$ ",
                )

        text = output.getvalue()
        self.assertFalse(result)
        self.assertFalse(should_exit)
        self.assertIn("ls один", text)
        self.assertIn("неизвестная", text)
        self.assertNotIn("cd два", text)

    def test_script_shows_input_and_output(self):
        """Проверяет отображение команд и результатов скрипта."""
        content = 'ls "Моя папка"\nexit\n'

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "сценарий.txt"
            path.write_text(content, encoding="utf-8")
            output = StringIO()

            with redirect_stdout(output):
                result, should_exit = run_script(
                    str(path),
                    "user@pc:~$ ",
                )

        text = output.getvalue()
        self.assertTrue(result)
        self.assertTrue(should_exit)
        self.assertIn('ls "Моя папка"', text)
        self.assertIn("ls: ['Моя папка']", text)
        self.assertIn("exit", text)


if __name__ == "__main__":
    unittest.main()
