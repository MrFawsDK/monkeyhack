# MonkeyHack

A small Python and Selenium project that reads the active words on a typing test and automatically types them in Google Chrome.

> Based partly on [fin-github/monkeytype-hack](https://github.com/fin-github/monkeytype-hack), with significant modifications and rewritten functionality.

> [!WARNING]
> This project was created for educational and testing purposes only. Using automation on Monkeytype or other third-party services may violate their Terms of Service and can result in rejected scores or account restrictions. Do not use this project to submit fake results, compete on leaderboards, or misrepresent your typing speed.

## Features

- Opens the test in Google Chrome
- Reads the currently active word
- Types each word automatically
- Supports random, fixed, and fast typing modes
- Configurable delay between keystrokes
- Waits for the next active word before continuing
- Does not store passwords, cookies, words, or account information

## Requirements

- Python 3.10 or newer
- Google Chrome
- Selenium

## Installation

Clone the repository:

```powershell
git clone https://github.com/MrFawsDK/monkeyhack.git
cd monkeyhack
```

Install the dependencies:

```powershell
py -m pip install -r requirements.txt
```

Run the program:

```powershell
py main.py
```

## Credits

This project is based partly on code from [fin-github/monkeytype-hack](https://github.com/fin-github/monkeytype-hack).

The original project provided the initial concept and parts of the codebase. The code has since been rewritten and modified with updated Selenium handling, Chrome support, active-word detection, safer configuration parsing, and improved error handling.

Credit goes to [fin-github](https://github.com/fin-github) for the original implementation.
