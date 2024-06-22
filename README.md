# Tic-Tac-Toe AI and Game

This repository contains a versatile Tic-Tac-Toe game that supports both single-player (against an AI bot) and multiplayer modes. It allows for customizable board sizes up to 10x10 and the option to set the number of pieces in a row required to win (k).

![hippo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDJncXcyM3Q5Zjd6OXdxMjBxdzdlODZtM2N5Zmt3NGdrM3c3cWR3cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bUkAb0QdnLR7CSUZVu/giphy.gif)

## Features

- Single-player mode against a sophisticated AI bot
- Multiplayer mode for two players
- Customizable board size (up to 10x10) and dynamic win conditions
- Rectangular boards supported
- Minimax algorithm with alpha-beta pruning and Zobrist hashing for efficient AI decision-making
- GUI and Command-line interface versions available

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

This project has been implemented with `python` 3.11.5. To install python please navigate to https://www.python.org/downloads/. Once `python` has been installed, please install `pygame` and `pygame_gui` to run the GUI interface. Note: these packages are not required for the Command-line interface. Install these packages with the following two commands:
```bash
pip install pygame
```

```bash
pip install pygame_gui
```

### Installation

To run this application, you'll need to clone the repository from GitHub and then execute one of the main program files. Here's a step-by-step guide:

1. **Clone the repository**

Open your terminal (Command Prompt or Bash) and enter the following command:

```bash
git clone https://github.com/arnavmazumder/Tic-Tac-Toe_Engine.git
```

1. **Navigate to the repository**

Change directory to the repository you just cloned:

```bash
cd Tic-Tac-Toe_Engine
```

1. **Run the application**

To run the **GUI interface**, execute `GameGUI.py` with:

```bash
python3 GameGUI.py
```

The GUI may include 6 dropdown menus for the following options: gamemode (multiplayer or singleplayer), n (board's number of rows), m (board's number of columns), k (number of pieces in a row required to win), bot-level (easy, medium, or hard), and your piece (X or O). After selecting these options, select the "play" button to begin the game.

To run the **Command-line interface**, execute `Gamerunner.py` with:

```bash
python3 Gamerunner.py
```

Upon executing the Gamerunner, you will be prompted with some options in the following format: --OptionName command. Please type in the corresponding command of the option you would like to select and follow any displayed instructions accordingly. You may exit the main menu with the command `q`. To exit at any point during the program, use the standard `^C`.


