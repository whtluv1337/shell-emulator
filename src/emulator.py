"""Простой CLI-эмулятор оболочки для первого и второго этапов."""

import argparse
import getpass
import shlex
import socket
from pathlib import Path


ERROR_PREFIX = "ошибка:"
STUB_COMMANDS = {"ls", "cd"}


def make_prompt():
    """Создаёт приглашение из реальных данных операционной системы."""
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"{username}@{hostname}:~$ "


def parse_command(command_line):
    """Разбирает строку и сохраняет текст в кавычках одним аргументом."""
    try:
        return shlex.split(command_line)
    except ValueError as error:
        raise ValueError("незакрытые кавычки") from error


def run_command(command_line):
    """Выполняет одну команду и возвращает ответ и признак выхода."""
    try:
        parts = parse_command(command_line)
    except ValueError as error:
        return f"{ERROR_PREFIX} {error}", False

    if not parts:
        return "", False

    command = parts[0]
    arguments = parts[1:]

    if command in STUB_COMMANDS:
        return f"{command}: {arguments}", False

    if command == "exit":
        if arguments:
            message = "команда exit не принимает аргументы"
            return f"{ERROR_PREFIX} {message}", False
        return "", True

    message = f"неизвестная команда: {command}"
    return f"{ERROR_PREFIX} {message}", False


def read_arguments():
    """Читает путь к VFS и путь к стартовому скрипту."""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС, вариант 23",
    )
    parser.add_argument(
        "--vfs",
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        help="путь к стартовому скрипту",
    )
    return parser.parse_args()


def print_configuration(vfs_path, script_path):
    """Показывает параметры, переданные при запуске."""
    print("Параметры запуска:")
    print(f"  Путь к VFS: {vfs_path or 'не указан'}")
    print(f"  Стартовый скрипт: {script_path or 'не указан'}")


def run_script(script_path, prompt):
    """Выполняет стартовый скрипт до первой ошибки."""
    if not script_path:
        return True, False

    path = Path(script_path)

    if not path.is_file():
        print(f"{ERROR_PREFIX} стартовый скрипт не найден")
        return False, False

    lines = path.read_text(encoding="utf-8").splitlines()

    for line in lines:
        command_line = line.strip()

        if not command_line:
            continue

        print(f"{prompt}{command_line}")
        result, should_exit = run_command(command_line)

        if result:
            print(result)

        if result.startswith(ERROR_PREFIX):
            return False, False

        if should_exit:
            return True, True

    return True, False


def repl(prompt):
    """Запускает интерактивный ввод команд."""
    while True:
        try:
            command_line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            break

        result, should_exit = run_command(command_line)

        if result:
            print(result)

        if should_exit:
            break


def main():
    """Показывает настройки, запускает скрипт и затем REPL."""
    arguments = read_arguments()
    prompt = make_prompt()

    print_configuration(arguments.vfs, arguments.script)
    script_ok, script_exit = run_script(arguments.script, prompt)

    if script_ok and not script_exit:
        repl(prompt)


if __name__ == "__main__":
    main()
