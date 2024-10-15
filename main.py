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
important_squares = {i: i ** 2 for i in range(1, 13)}  # Squares until 12^2
important_cubes = {i: i ** 3 for i in range(1, 5)}  # Cubes until 4^3
important_power = {**important_squares, **important_cubes}  # Combine squares and cubes


def print_welcome_message():
    print("Welcome to the Multiplication Table Trainer!")
    print("This game will help you master multiplication up to 20x20, and important squares and cubes.")
    print("You have 3 seconds to answer each question. Let's get started!\n")
    input("Press Enter to proceed...")

    def print_multiplication_table():
        print("\nMultiplication Table (1 to 20):")

        # print(tabulate([[i] + [i * j for j in range(1, 21)] for i in range(1, 21)], headers=[str(i) for i in range(1, 21)], tablefmt="grid"))

        # Print the header row with correct formatting and consistent width
        print("{:<5}".format(""), end="")  # First empty space
        for i in range(1, 21):
            print("{:>5}".format(i), end="")
        print("\n" + "-" * 105)  # Separator line

        # Print each row of the table
        for i in range(1, 21):
            print("{:>2} | ".format(i), end="")  # The row number, formatted properly
            for j in range(1, 21):
                product = i * j
                print("{:>5}".format(product), end="")  # Each product formatted to fit 4-character wide columns
            print()  # Newline after each row
        print()

    def print_powers_table():
        print("Important Squares and Cubes:")
        # print(tabulate([[i, i ** 2, i ** 3 if i <= 4 else ''] for i in range(1, 13)], headers=["Number", "Square", "Cube"], tablefmt="grid"))
        print("{:<6} | {:<6} | {:<6}".format("Number", "Square", "Cube"))
        print("-" * 24)

        for i in range(1, 13):
            square = i ** 2
            cube = i ** 3 if i <= 4 else ""
            print("{:<6} | {:<6} | {:<6}".format(i, square, cube))
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
