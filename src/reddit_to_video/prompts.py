from reddit_to_video.utility import can_write_to_file


from os.path import exists as path_exists


def prompt_list(options: list[tuple], prompt_char: str = ">") -> any:
    for i, option in enumerate(options):
        print(f"[{i + 1}] {option[0]}")

    while True:
        try:
            choice = int(input(f"{prompt_char} "))
            if choice < 1 or choice > len(options):
                raise ValueError
            return options[choice - 1][1]
        except ValueError:
            print("Invalid choice")


def prompt_bool(prompt: str) -> bool:
    while True:
        try:
            choice = input(prompt)
            if choice.lower() == "y":
                return True
            if choice.lower() == "n":
                return False
            raise ValueError
        except ValueError:
            print("Invalid choice")


def prompt_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid choice")


def prompt_str(prompt: str) -> str:
    while True:
        try:
            return input(prompt)
        except ValueError:
            print("Invalid choice")


def prompt_write_file(prompt: str, overwrite=False) -> str:
    while True:
        file = input(prompt)

        if path_exists(file) and not overwrite:
            print("File already exists, try again")
            continue

        if not can_write_to_file(file):
            print("Can't write to that file location, try again")
            continue

        return file


def prompt_file(prompt: str) -> str:
    while True:
        file = input(prompt)

        if not path_exists(file):
            print("File not found, try again")
            continue

        return file
