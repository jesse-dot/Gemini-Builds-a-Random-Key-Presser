# Random Key and Mouse Presser with GUI

This Python tool provides a graphical user interface (GUI) for simulating random keyboard key presses and mouse clicks. It offers a variety of configurable options for automating basic input tasks.

## Features

- **Configurable Keys:** Enter a space-separated list of keys you want the program to randomly press.
- **Adjustable Delay:** Use a slider to set the delay (in seconds) between each action.
- **Press Duration:** Specify how long a key is held down after being pressed (in seconds).
- **Hold Duration:** Set the duration (in seconds) for which a key is held down before being released.
- **Konami Code Easter Egg:** Enable a feature that randomly triggers the famous Konami Code sequence. You can also set the probability of this occurring.
- **Mouse Click Simulation:** Enable random left, right, or middle mouse clicks. The program will randomly choose one of the enabled buttons to click.
- **Random Mouse Movement:** Simulate small, random movements of the mouse cursor within a configurable X and Y range, with adjustable frequency.
- **Load/Save Configuration:** Save your preferred settings to a `.ini` file and load them later for convenience.
- **User-Friendly GUI:** An intuitive graphical interface built using Tkinter, making it easy to configure and use the tool.

## Dependencies

This project requires the following Python libraries:

- **`tkinter`:** For the graphical user interface (standard with Python).
- **`pynput`:** For simulating keyboard and mouse input. You can install it using pip:
  ```bash
  pip install pynput
