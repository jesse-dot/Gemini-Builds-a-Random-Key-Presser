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
- **`pynput`:** For simulating keyboard and mouse input.
- **`configparser`:** For handling the configuration file (standard with Python).

## How to Install

1.  **Ensure Python is Installed:** Make sure you have Python 3 installed on your system. You can download it from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Clone the Repository (Optional but Recommended):** If you want to keep the project files organized and easily updatable, clone the GitHub repository:
    ```bash
    git clone [repository URL]
    ```
    Navigate to the repository directory:
    ```bash
    cd [repository name]
    ```

3.  **Install `pynput`:** Open your terminal or command prompt and install the `pynput` library using pip:
    ```bash
    pip install pynput
    ```

## Usage

1.  Run the main Python script (e.g., `main.py` or the name of your script).
2.  A graphical user interface will appear.
3.  Enter the keys you want to be pressed randomly in the "Keys to Press" field (separated by spaces).
4.  Adjust the "Delay" slider to control the interval between actions.
5.  Set the "Press Duration" and "Hold Duration" as needed.
6.  Check the "Enable Konami Code" box if you want to include the easter egg and adjust its "Konami Chance".
7.  In the "Mouse Control" section, enable "Mouse Clicks" and select the desired buttons.
8.  Enable "Random Mouse Movement" and configure the "Max Move X," "Max Move Y," and "Move Frequency".
9.  Click the "Start" button to begin the simulation.
10. Click the "Stop" button to halt the simulation.
11. Use the "Load Config" and "Save Config" buttons to manage your settings.

## Contributing

Contributions to this project are welcome. Feel free to submit bug reports, feature requests, or pull requests.


[Your License Here - e.g., MIT License]
