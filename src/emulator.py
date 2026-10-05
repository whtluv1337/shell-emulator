"""Простой CLI-эмулятор оболочки для первого этапа."""

import getpass
import shlex
import socket


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


def repl():
    """Запускает интерактивный ввод команд."""
    prompt = make_prompt()

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
    """Запускает эмулятор."""
    repl()


if __name__ == "__main__":
    main()
