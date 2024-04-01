import os
import re
import argparse
from enum import Enum
import subprocess


def _get_user_home():
    return os.path.expanduser("~")


SEARCHING_RANGES = [
    os.path.join(_get_user_home(), "Library/Preferences"),
    os.path.join(_get_user_home(), "Library/Application Support"),
    os.path.join(_get_user_home(), "Library/Caches"),
    "/Library/LaunchDaemons",
    "/Library/LaunchAgents",
    os.path.join(_get_user_home(), "Library/LaunchAgents"),
]


class Color(str, Enum):
    Red = ("\033[91m",)
    Red_BOLD = ("\033[1;91m",)
    Green = ("\033[92m",)
    Green_BOLD = ("\033[1;92m",)
    Yellow = ("\033[93m",)
    Yellow_BOLD = ("\033[1;93m",)
    Blue = ("\033[94m",)
    Purple = ("\033[95m",)
    Cyan = ("\033[96m",)
    White = ("\033[97m",)
    BOLD = "\033[1m"


def search_folders(root_path, keyword):
    matched_list = []
    for root, dirs, files in os.walk(root_path):
        for dir_name in dirs:
            if re.search(keyword, dir_name, re.IGNORECASE):
                matched_list.append(os.path.join(root, dir_name))
        for file_name in files:
            if re.search(keyword, file_name, re.IGNORECASE):
                matched_list.append(os.path.join(root, file_name))

    return matched_list


def print_with_color(text, color=None):
    if color != None:
        reset_color = "\033[0m"
        print(color.value + text + reset_color)
    else:
        print(text)


def parse_args():
    arg_parser = argparse.ArgumentParser(
        description="Clean the remaining files of an App on macOS. "
        "The searching ranges are: ~/Library/Preferences, ~/Library/Application Support, ~/Library/Caches."
    )
    arg_parser.add_argument(
        "--keyword",
        type=str,
        required=True,
        help="Keyword to search for. Can be the name, author, distributor of the app you want to clean. Case-insensitive.",
    )
    return arg_parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    keyword = args.keyword

    results = []  # may contain file or
    for path in SEARCHING_RANGES:
        results.extend(search_folders(path, keyword))

    if len(results) == 0:
        print_with_color(
            f'No folders found with the name containing "{keyword}"', Color.Green
        )
        exit(0)

    print_with_color(f"Folders found with the name containing '{keyword}':", Color.BOLD)
    for folder in results:
        print(folder)
    print("\n")

    print_with_color("Do you want to delete these folders? (y/n)", Color.Yellow_BOLD)
    user_input_0 = input()
    if user_input_0.lower() == "y":
        print_with_color(
            "Warning: This action is irreversible! Are you sure you want to delete these folders? (y/n)",
            color=Color.Red_BOLD,
        )
        user_input_1 = input()
        if user_input_1.lower() == "y":
            for item in results:
                os.system(f"echo {item}")
                subprocess.run(
                    ["rm", "-rf", item]
                )  # if fails, try sudo run this script

        print_with_color("Files or folders deleted successfully!", Color.Green_BOLD)
    else:
        print_with_color("Nothing deleted!", Color.BOLD)
        print_with_color("Exit.", Color.BOLD)
