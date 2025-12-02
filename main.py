import pyotp
import time
import os
import pyperclip
import configparser

CONFIG_FILE = 'settings.ini'
CONFIG_SECTION = 'Settings'

def clear_console():
	os.system('cls' if os.name == 'nt' else 'clear')

def check_first_run():
	if os.path.exists('secrets.csv'):
		return False
	return True

def generate_totp(secret):
	totp = pyotp.TOTP(secret)
	return totp.now()

def display_accounts():
	with open('secrets.csv', 'r') as file:
		lines = file.readlines()
		if len(lines) <= 1:
			return

	number = 1
	with open('secrets.csv', 'r') as file:
		lines = file.readlines()[1:]
		for line in lines:
			service, account_name, secret_key = line.strip().split(',')
			print(f"{number}. {service} ({account_name})")
			number += 1

def remove_account(index):
	with open('secrets.csv', 'r') as file:
		lines = file.readlines()
		
	if 0 < index < len(lines):
		del lines[index]
		with open('secrets.csv', 'w') as file:
			file.writelines(lines)
		print("✅ Account removed successfully!")
	else:
		print(f"❌ Invalid account number ({index}).")

def edit_account(index):
	temp_input = input("What would you like to edit? (service/account name/secret key): \n").strip()
	if temp_input.lower() not in ['service', 'account name', 'secret key']:
		print("❌ Invalid field. Please enter 'service', 'account name', or 'secret key'.")
		return
	with open('secrets.csv', 'r') as file:
		lines = file.readlines()
	if 0 < index < len(lines):
		service, account_name, secret_key = lines[index].strip().split(',')
		if temp_input.lower() == 'service':
			new_value = input("Enter new service name: ").strip()
			service = new_value
		elif temp_input.lower() == 'account name':
			new_value = input("Enter new account name: ").strip()
			account_name = new_value
		elif temp_input.lower() == 'secret key':
			new_value = input("Enter new secret key: ").strip()
			secret_key = new_value
		lines[index] = f"{service},{account_name},{secret_key}\n"
		with open('secrets.csv', 'w') as file:
			file.writelines(lines)
		print("✅ Account updated successfully!")

def load_clipboard_setting():
	config = configparser.ConfigParser()
	config.read(CONFIG_FILE)
	
	if CONFIG_SECTION in config:
		return config.getboolean(CONFIG_SECTION, 'copy_to_clipboard', fallback=False)
	else:
		return False
	
def save_clipboard_setting(is_enabled):
	config = configparser.ConfigParser()
	config.read(CONFIG_FILE)
		
	# Create the section if it doesn't exist
	if CONFIG_SECTION not in config:
		config[CONFIG_SECTION] = {}
			
	config[CONFIG_SECTION]['copy_to_clipboard'] = str(is_enabled)
		
	with open(CONFIG_FILE, 'w') as f:
		config.write(f)

def main():
	empty = False
	copy_to_clipboard = load_clipboard_setting()

	if check_first_run():
		print("Creating secrets.csv for the first time...")
		with open('secrets.csv', 'w') as file:
			file.write("Service,Account Name,Secret key\n")
	clear_console() 
	print("Welcome to the TOTP Manager! 🔑")
	print("If you'd like to add a new account, type 'add'. To view your accounts, type 'view'. To exit, type 'exit'.")

	with open('secrets.csv', 'r') as file:
		lines = file.readlines()
		if len(lines) <= 1:
			empty = True
	if not empty:
		print("\nYour current TOTP accounts: ")
		display_accounts()
	print("-" * 30)

	while True:
		print(f"Clipboard copy is {'enabled' if copy_to_clipboard else 'disabled'}. Type 'copy' to {'disable' if copy_to_clipboard else 'enable'} it.")
		command = input("Enter command (type commands for a list): ").strip().lower()

		clear_console() 
		if command == 'copy':
			copy_to_clipboard = not copy_to_clipboard
			save_clipboard_setting(copy_to_clipboard)
			print(f"📋 Clipboard copy has been {'enabled' if copy_to_clipboard else 'disabled'}.")
			print("-" * 30)

		elif command == 'commands':
			print("Available commands:")
			print(" add      - Add a new TOTP account")
			print(" view     - View all TOTP accounts")
			print(" remove   - Remove a TOTP account")
			print(" copy     - Toggle clipboard copy on/off")
			print(" commands - View all available commands")
			print(" edit     - Edit an existing TOTP account (not implemented)")
			print(" exit     - Exit the TOTP Manager")
			print("-" * 30)

		elif command == 'add':
			print("--- Add New Account ---")
			service = input("Enter service name: ").strip()
			if service == "exit" or service == "":
				clear_console()
				print("Returning to main menu...")
				time.sleep(1)
				clear_console()
				continue
			account_name = input("Enter account name: ").strip()
			secret_key = input("Enter secret key: ").strip()
			with open('secrets.csv', 'a') as file:
				file.write(f"{service},{account_name},{secret_key}\n")
			
			clear_console() 
			print("✅ Account added successfully!")
			empty = False
			print("\nYour updated TOTP accounts: ")
			display_accounts()
			print("-" * 30)

		elif command =="remove":
			print("--- Remove Account ---")
			if empty:
				print("No accounts to remove. Please add an account first.")
			else:
				print("Your TOTP accounts: ")
				display_accounts()
				try:
					index = int(input("Enter the account number to remove: ").strip())
					remove_account(index)
					with open('secrets.csv', 'r') as file:
						lines = file.readlines()
						if len(lines) <= 1:
							empty = True
					if not empty:
						print("\nYour updated TOTP accounts: ")
						display_accounts()
					else:
						print("No accounts left. Please add a new account.")
				except ValueError:
					print("❌ Invalid input. Please enter a valid account number.")
			print("-" * 30)

		elif command == 'view':
			print("--- Viewing Accounts ---")
			if empty:
				print("No accounts to display. Please add an account first.")
			else:
				print("Your TOTP accounts: ")
				display_accounts()
			print("-" * 30)

		elif command == 'edit':
			print("--- Edit Account ---")
			if empty:
				print("No accounts to edit. Please add an account first.")
			else:
				print("Your TOTP accounts: ")
				display_accounts()
				try:
					index = int(input("Enter the account number to edit: ").strip())
					edit_account(index)
				except ValueError:
					print("❌ Invalid input. Please enter a valid account number.")
			print("-" * 30)

		elif command.isdigit():
			index = int(command)
			with open('secrets.csv', 'r') as file:
				lines = file.readlines()
				if 0 < index < len(lines):
					service, account_name, secret_key = lines[index].strip().split(',')
					totp_code = generate_totp(secret_key)
					if copy_to_clipboard:
						pyperclip.copy(totp_code)
						print(f"🔐 TOTP code for {service} ({account_name}) and has been copied to your clipboard: {totp_code}")
						print(f"\nThe code is time-sensitive and has {30 - int(time.time()) % 30} seconds left.")
						print(f"Press Enter to return to the main menu.")
						input()
					else:
						print(f"🔐 TOTP code for {service} ({account_name}): {totp_code}")
						print(f"\nThe code is time-sensitive and has {30 - int(time.time()) % 30} seconds left.")
						print(f"Press Enter to return to the main menu.")
						input()
					clear_console()
					print("Welcome to the TOTP Manager! 🔑")
					print("If you'd like to add a new account, type 'add'. To view your accounts, type 'view'. To exit, type 'exit'.")
					print("\nYour current TOTP accounts: ")
					display_accounts()
					print("-" * 30)
				else:
					print(f"❌ Invalid account number ({index}).")		

		elif command == 'exit':
			print("Exiting the TOTP Manager. Goodbye! 👋")
			break
		
		else:
			print("❌ Invalid command. Please try again.")
			print("\nIf you'd like to add a new account, type 'add'. To view your accounts, type 'view'. To exit, type 'exit'.")
			if not empty:
				print("\nYour current TOTP accounts: ")
				display_accounts()
			print("-" * 30)


if __name__ == "__main__":
	main()
