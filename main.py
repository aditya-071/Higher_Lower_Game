"""Entry point for Higher-Lower game.

This file implements a console version of the game following the user's
original comment dividers and also lets the player launch the Tkinter GUI
from `gui.py`.
"""

import random
import sys
import os

try:
	import art
	LOGO = getattr(art, "logo", "")
except Exception:
	LOGO = ""

import gui
from game_data import data


# Display art
def show_logo():
	if LOGO:
		print(LOGO)


# Generate a random account from the game data
def get_random_account(exclude=None):
	choice = random.choice(data)
	while exclude and choice["name"] == exclude["name"]:
		choice = random.choice(data)
	return choice


# Format account data into printable format
def format_account(acc):
	return f"{acc['name']}, a {acc['description']}, from {acc['country']}"


# check if user is correct (helper)
def is_guess_correct(guess, a_count, b_count):
	guess = guess.upper()
	return (guess == "A" and a_count >= b_count) or (guess == "B" and b_count >= a_count)


def clear_console():
	os.system("cls" if os.name == "nt" else "clear")


def play_console():
	score = 0
	account_a = get_random_account()
	account_b = get_random_account(exclude=account_a)

	while True:
		clear_console()
		show_logo()
		print(f"Score: {score}\n")

		# Display the two accounts
		print("Compare A:")
		print(format_account(account_a))
		print("\nvs\n")
		print("Against B:")
		print(format_account(account_b))
		print()

		# ask user for a guess
		choice = input("Who has more followers? Type 'A' or 'B' (or 'G' to open GUI, 'Q' to quit): ").strip().upper()
		if choice == "G":
			# launch GUI and exit console loop
			print("Launching GUI...")
			gui.main()
			return
		if choice == "Q":
			print(f"Goodbye — final score: {score}")
			return
		if choice not in ("A", "B"):
			print("Please type 'A' or 'B' (or 'G' for GUI, 'Q' to quit).")
			input("Press Enter to continue...")
			continue

		# get follower count of each account
		a_count = account_a["follower_count"]
		b_count = account_b["follower_count"]

		# check if user is correct
		if is_guess_correct(choice, a_count, b_count):
			# give user feedback on their guess
			score += 1
			print(f"You're right! Current score: {score}")
			# making account at position B become the next account at position A (keep winner)
			if b_count > a_count:
				account_a = account_b
			# pick a new B
			account_b = get_random_account(exclude=account_a)
			input("Press Enter for the next round...")
			continue
		else:
			print(f"Sorry, that's wrong. Final score: {score}.")
			print(f"A: {a_count}M — B: {b_count}M")
			again = input("Play again? (Y/N): ").strip().upper()
			if again == "Y":
				score = 0
				account_a = get_random_account()
				account_b = get_random_account(exclude=account_a)
				continue
			else:
				print("Thanks for playing!")
				return


if __name__ == "__main__":
	# Allow quick GUI launch via command-line flag
	if len(sys.argv) > 1 and sys.argv[1] in ("--gui", "-g"):
		gui.main()
	else:
		try:
			play_console()
		except KeyboardInterrupt:
			print("\nInterrupted — goodbye.")
