def prompt(options: list, prompt_char: str = ">") -> int:
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")

    while True:
        try:
            choice = int(input(f"{prompt_char} "))
            if choice < 1 or choice > len(options):
                raise ValueError
            return choice
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
