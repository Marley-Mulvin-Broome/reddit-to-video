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
