import random
import time
from typing import Any
import sys
import select

import colorama
from colorama import Fore, Style

from tabulate import tabulate

# Initialize colorama for color feedback
colorama.init()

# Define important squares and cubes for SAT
important_squares = {i: i * i for i in range(1, 13)}  # Squares until 12^2
important_cubes = {i: i * i * i for i in range(1, 5)}  # Cubes until 4^3
important_power = {**important_squares, **important_cubes}  # Combine squares and cubes


def print_welcome_message():
    print("Welcome to the Multiplication Table Trainer!")
    print("This game will help you master multiplication up to 20x20, and important squares and cubes.")
    print("You have 3 seconds to answer each question. Let's get started!\n")
    input("Press Enter to proceed...")

    def print_multiplication_table():
        print("Multiplication Table (1 to 20):")
        print("    ", end="")
        for i in range(1, 21):
            print(f"{i:4}", end="")
        print("\n" + "-" * 85)
        for i in range(1, 21):
            print(f"{i:2} |", end="")
            for j in range(1, 21):
                product = i * j
                if (i in range(7, 13) and j in range(7, 13)) or (i in range(13, 21) and j in range(13, 21)):
                    print(f"\033[1m{product:4}\033[0m", end="")  # Bold text
                else:
                    print(f"{product:4}", end="")
            print()
        print()

    def print_powers_table():
        print("Important Squares and Cubes:")
        print("Number | Square | Cube")
        print("-----------------------")
        for i in range(1, 13):
            square = important_squares[i]
            cube = important_cubes[i] if i in important_cubes else ""
            print(f"{i:6} | {square:6} | {cube:4}")
        print()

    print_multiplication_table()  # Print the multiplication table at the beginning
    print_powers_table()  # Print the important squares and cubes at the beginning

    # Print rules and instructions
    print("Rules:")
    print("1. You will be asked to multiply two numbers or find the square/cube of a number.")
    print("2. You have 3 seconds to answer each question.")
    print("3. Enter 'q' to quit the game at any time.")
    print("4. Let's see how many questions you can answer correctly!\n")
    input("Press Enter to start the game...")



def get_random_numbers():
    r = random.random()
    # Give priority to harder numbers, e.g., from 7 to 12
    if r < 0.6:  # 60% chance of picking from higher range
        return random.randint(13, 20), random.randint(1, 20)
    elif r < 0.9:  # 20% chance of picking
        return random.randint(7, 12), random.randint(1, 20)
    elif r < 0.95:  # 5% chance of picking
        return random.randint(1, 12), random.randint(1, 12)
    else:
        if random.random() < 0.5:
            return random.choice(list(important_squares.keys())), 'square'
        else:
            return random.choice(list(important_cubes.values())), 'cube'


def get_user_input(timeout=3):
    start_time = time.time()
    print("Your answer: ", end='', flush=True)
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        answer = sys.stdin.readline().strip()
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            return None, elapsed_time
        return answer, elapsed_time
    return None, timeout

# Usage in ask_question function
def ask_question(performance_tracker):
    num1, num2 = get_random_numbers()

    if num2 == 'square':
        print("\nThe number {num2} is square of:")
        correct_answer = important_squares[num1]
    elif num2 == 'cube':
        print("\nThe number {num1} is cube of:")
        correct_answer = important_cubes[num1]
    else:
        print(f"\nMultiply: {num1} x {num2}")
        correct_answer = num1 * num2

    answer, elapsed_time = get_user_input(timeout=3)

    if answer is None:
        print(Fore.YELLOW + "Too slow!" + Style.RESET_ALL)
        print(Fore.RED + f"The correct answer was: {correct_answer}" + Style.RESET_ALL)
        update_performance(num1, num2, False, performance_tracker)
        return

    # End game if user enters 'q'
    if answer == 'q':
        print_performance(performance_tracker)
        print("Exiting the game...")
        exit()

    try:
        answer = int(answer)
    except ValueError:
        answer = None  # In case of non-numeric input

    # Check if the user answered correctly and within 2.5 seconds
    if elapsed_time > 2.5:
        print(Fore.YELLOW + f"Too slow! ({elapsed_time:.2f}s)" + Style.RESET_ALL)
        print(Fore.RED + f"The correct answer was: {correct_answer}" + Style.RESET_ALL)
    elif answer == correct_answer:
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
        update_performance(num1, num2, True, performance_tracker)
    else:
        print(Fore.RED + f"Incorrect! The correct answer was: {correct_answer}" + Style.RESET_ALL)
        update_performance(num1, num2, False, performance_tracker)


# def ask_question(performance_tracker):
#     num1, num2 = get_random_numbers()
#
#     if num2 == 'square':
#         print("\nThe number {num2} is square of:")
#         correct_answer = important_squares[num1]
#     elif num2 == 'cube':
#         print("\nThe number {num1} is cube of:")
#         correct_answer = important_cubes[num1]
#     else:
#         print(f"\nMultiply: {num1} x {num2}")
#         correct_answer = num1 * num2
#     start_time = time.time()
#
#     # Get user input with a timer
#     try:
#         # wait for user input only for 3 seconds
#         print("Your answer: ", end='', flush=True)
#         ready, _, _ = select.select([sys.stdin], [], [], 3)
#         if ready:
#             answer = sys.stdin.readline().strip()
#             elapsed_time = time.time() - start_time
#         else:
#             print(Fore.YELLOW + "Too slow!" + Style.RESET_ALL)
#             print(Fore.RED + f"The correct answer was: {correct_answer}" + Style.RESET_ALL)
#             update_performance(num1, num2, False, performance_tracker)
#             return
#         # End game if user enters 'q'
#         if answer == 'q':
#             print_performance(performance_tracker)
#             print("Exiting the game...")
#             exit()
#         answer = int(answer)
#     except ValueError:
#         answer = None  # In case of non-numeric input
#
#     # Check if the user answered correctly and within 2.5 seconds
#     if elapsed_time > 2.5:
#         print(Fore.YELLOW + f"Too slow! ({elapsed_time:.2f}s)" + Style.RESET_ALL)
#         print(Fore.RED + f"The correct answer was: {correct_answer}" + Style.RESET_ALL)
#     elif answer == correct_answer:
#         print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
#         update_performance(num1, num2, True, performance_tracker)
#     else:
#         print(Fore.RED + f"Incorrect! The correct answer was: {correct_answer}" + Style.RESET_ALL)
#         update_performance(num1, num2, False, performance_tracker)


def initialize_performance_tracker():
    performance_tracker: dict[Any, Any] = {}  # Tracks how many correct/incorrect per multiplication/power

# Populate performance tracker with all pairs, squares, and cubes
    for i in range(1, 21):
        for j in range(i, 21):  # Ensure (i, j) and (j, i) are treated the same
            performance_tracker[(i, j)] = {'correct': 0, 'incorrect': 0}
    for i in range(1, 14):
        performance_tracker[(i, 'square')] = {'correct': 0, 'incorrect': 0}
    for i in range(1, 6):
        performance_tracker[(i, 'cube')] = {'correct': 0, 'incorrect': 0}

    return performance_tracker


def update_performance(num1, num2, is_correct, performance_tracker):
    # Update the performance tracker based on the user's response
    if num2 == 'square':
        pair = (num1, 'square')
    elif num2 == 'cube':
        pair = (num1, 'cube')
    else:
        pair = tuple(sorted([num1, num2]))  # Sorting to treat (8x7) and (7x8) as the same

    if is_correct:
        performance_tracker[pair]['correct'] += 1
    else:
        performance_tracker[pair]['incorrect'] += 1


def print_performance(performance_tracker):
    # Print the performance of the user
    print("\nPerformance:")
    # Print the Multiplication Table and mark the number of correct/incorrect answers
    # in every cell.


    for pair, performance in performance_tracker.items():
        if performance['correct'] + performance['incorrect'] > 0:
            print(f"{pair}: {performance['correct']} correct, {performance['incorrect']} incorrect")
    print()

    # Prepare data for tabulation
    table_data = []
    for pair, performance in performance_tracker.items():
        if performance['correct'] + performance['incorrect'] > 0:
            table_data.append([pair, performance['correct'], performance['incorrect']])

    # Print the performance table
    print("\nPerformance:")
    print(tabulate(table_data, headers=["Pair", "Correct", "Incorrect"], tablefmt="grid"))
    print()


def main():
    print_welcome_message()  # Print the welcome message at the beginning
    performance_tracker = initialize_performance_tracker()

    # Main loop for the trainer
    while True:
        ask_question(performance_tracker)
        time.sleep(1)  # Give a brief pause between questions


if __name__ == "__main__":
    main()
