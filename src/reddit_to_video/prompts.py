"""Module containing various functions for prompting the user for input
Functions:
    prompt_list(options: list[tuple], prompt_char: str = ">") -> any:
        Prompts the user to choose from a list of options
    
    prompt_bool(prompt: str) -> bool:
        Prompts the user to choose yes or no
    
    prompt_int(prompt: str) -> int:
        Prompts the user to enter an integer

    prompt_str(prompt: str) -> str:
        Prompts the user to enter a string

    prompt_file(prompt: str, file_type: str, default: str = "") -> str:
        Prompts the user to enter a file path

    prompt_dir(prompt: str, default: str = "") -> str:
        Prompts the user to enter a directory path

    prompt_video(prompt: str, default: str = "") -> str:
        Prompts the user to enter a video file path

    prompt_write_file(prompt: str, overwrite=False) -> str:
        Prompts the user to enter a file path to write to

    prompt_preview_vid(output_location: str):
        Prompts the user if they want to preview the video
        and opens the video in default player if yes
"""
from os import getcwd
from os.path import isfile as file_exists
from os.path import join as path_join

from reddit_to_video.utility import can_write_to_file, preview_video
from reddit_to_video.exceptions import OsNotSupportedError


def prompt_list(options: list[tuple], prompt_char: str = ">") -> any:
    """Prompts the user to choose from a list of options"""
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
    """Prompts the user to choose yes or no"""
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
    """Prompts the user to enter an integer"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid choice")


def prompt_str(prompt: str) -> str:
    """Prompts the user to enter a string"""
    return input(prompt)


def prompt_write_file(prompt: str, overwrite=False) -> str:
    """Prompts the user to enter a file path to write to"""
    while True:
        file = input(prompt)

        if file_exists(file) and not overwrite:
            print("File already exists, try again")
            continue

        if not can_write_to_file(file):
            print("Can't write to that file location, try again")
            continue

        return file


def prompt_file(prompt: str) -> str:
    """Prompts the user to enter a file path to read from"""
    while True:
        file = input(prompt)

        if not file_exists(file):
            print("File not found, try again")
            continue

        return file


def prompt_preview_vid(output_location: str):  # pragma: no cover
    """Prompts the user if they want to preview the video"""
    will_preview = prompt_bool("Preview video? (y/n): ")

    if not will_preview:
        return

    try:
        preview_video(path_join(getcwd(), output_location))
    except FileNotFoundError:
        print("Failed to preview video, file not found")
    except OsNotSupportedError:
        print("Failed to preview video, operating system not supported")
