"""Тесты первого этапа эмулятора оболочки."""

import unittest

from src.emulator import make_prompt, parse_command, run_command


class ShellEmulatorTests(unittest.TestCase):
    """Проверяет парсер, команды, ошибки и завершение работы."""

    def test_quoted_argument(self):
        """Проверяет, что текст в кавычках остаётся одним аргументом."""
        result = parse_command('ls "папка с пробелами"')
        self.assertEqual(result, ["ls", "папка с пробелами"])

    def test_ls_stub(self):
        """Проверяет команду-заглушку ls."""
        result, should_exit = run_command("ls один два")
        self.assertEqual(result, "ls: ['один', 'два']")
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
        """Проверяет формат приглашения к вводу."""
        prompt = make_prompt()
        self.assertIn("@", prompt)
        self.assertTrue(prompt.endswith(":~$ "))


if __name__ == "__main__":
    unittest.main()
