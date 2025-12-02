# 🔑 TOTP Manager (Console Application)

A simple, console-based application built in Python for generating **Time-based One-Time Passwords (TOTP)**, commonly used for Two-Factor Authentication (2FA). This tool allows you to securely store your secret keys locally in a `secrets.csv` file and quickly generate codes when needed.

## ✨ Features

* **Local Storage:** Saves service details and secret keys to a local `secrets.csv` file.
* **TOTP Generation:** Uses the `pyotp` library to generate 6-digit TOTP codes reliably.
* **Time Remaining:** Displays the countdown for the time-sensitive code.
* **Persistent Settings:** Saves user preference for clipboard copying to a **`settings.ini`** file.
* **Clipboard Copying:** Automatically copies the generated TOTP code to the system clipboard when enabled.
* **Cross-Platform Clearing:** Clears the console for a clean user experience on both Windows (`cls`) and Linux/macOS (`clear`).

---

## 🚀 Installation & Setup

This project requires **Python 3.x**.

### 1. Clone the Repository

```bash
git clone https://github.com/shigeosapsycho/PyOTP
cd PyOTP
````

### 2\. Set up the Environment

It's highly recommended to use a virtual environment.

```bash
# Create a virtual environment
python -m venv venv 

# Activate the environment (Windows)
.\venv\Scripts\activate

# Activate the environment (Linux/macOS)
source venv/bin/activate
```

### 3\. Install Dependencies

The necessary dependencies are listed in `requirements.txt`. Note that this includes **`pyperclip`** for clipboard functionality.

```bash
pip install -r requirements.txt
```

-----

## 🛠️ Usage

### Running the Script

Once the dependencies are installed, you can run the application directly:

```bash
python main.py
```

### Commands

The application is command-line driven. When prompted, you can enter the following:

| Command | Description |
| :--- | :--- |
| `add` | Enter a new service name, account name, and secret key to store. |
| `copy` | **Toggles** the automatic copying of the TOTP code to your system clipboard (On/Off). |
| `view` | Display the list of all stored accounts. |
| `[number]` | Enter the number corresponding to an account to generate its TOTP code. |
| `remove` | Removes a line from the .csv file, resulting in a removal of a TOTP/line |
| `edit` | Edit a line's service, account name, or replacae the secret key |
| `exit` | Close the application. |

-----

## ⚙️ Configuration

The application automatically creates and manages a file named **`settings.ini`** in the project directory to store your preferences.

The primary setting is controlled by the `copy` command:

| Setting | Default Value | Description |
| :--- | :--- | :--- |
| `copy_to_clipboard` | `False` | Determines whether the generated TOTP code is automatically copied to the clipboard. |

-----

## 📦 Building an Executable (recommended)

You can easily convert this Python script into a standalone executable (`.exe` on Windows) using **PyInstaller**.

**Note:** PyInstaller is included in your `requirements.txt` file.

### 1\. Compile the Application

Run the following command from the root directory of the project:

```bash
pyinstaller --onefile --name "TOTP_Manager" main.py
```

  * `--onefile`: Packages everything into a single executable file.
  * `--name`: Sets the name of the final executable file.

### 2\. Locate the Executable

The executable file (`TOTP_Manager.exe`) will be created in the newly generated **`dist`** folder.

You can now distribute this single executable file to use the TOTP Manager without installing Python or any dependencies.

-----

## ⚠️ Important Notes on Security

  * The `secrets.csv` file stores your secret keys in **plain text**.
  * This application is intended for use in a **secure, local environment** where you are the sole user.
  * Do **not** upload the `secrets.csv` file to GitHub or any public location.

## 🤝 Contributing

Feel free to open issues or submit pull requests if you have suggestions for new features or bug fixes\!
