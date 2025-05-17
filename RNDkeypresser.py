import tkinter as tk
from tkinter import ttk, filedialog
import keyboard
import random
import time
import threading
import configparser  # For handling INI files

from pynput import mouse


class KeyPresserGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Key and Mouse Presser")

        # Configuration
        self.config = configparser.ConfigParser()
        self.config_file = "config.ini"
        self.load_config()

        # Key Press Settings
        ttk.Label(master, text="Keys to Press (space-separated):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.keys_entry = ttk.Entry(master)
        self.keys_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.keys_entry.insert(0, self.config.get("settings", "keys", fallback=""))

        ttk.Label(master, text="Delay (seconds):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.delay_slider = tk.Scale(master, from_=0.01, to=5.0, resolution=0.05, orient=tk.HORIZONTAL, label="Delay", command=self.update_delay_label)
        try:
            self.delay_slider.set(float(self.config.get("settings", "delay", fallback="0.3")))
        except ValueError:
            self.delay_slider.set(0.3)
        self.delay_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.delay_label_var = tk.StringVar(value=f"{self.delay_slider.get():.2f} s")
        ttk.Label(master, textvariable=self.delay_label_var).grid(row=2, column=1, padx=5, pady=2, sticky="e")

        ttk.Label(master, text="Press Duration (seconds):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(master)
        self.duration_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.duration_entry.insert(0, self.config.get("settings", "duration", fallback="0.0"))

        # Konami Code Settings
        self.konami_var = tk.BooleanVar(value=self.config.getboolean("konami", "enabled", fallback=False))
        ttk.Checkbutton(master, text="Enable Konami Code", variable=self.konami_var).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(master, text="Konami Chance (0.0-1.0):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.konami_chance_entry = ttk.Entry(master)
        self.konami_chance_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.konami_chance_entry.insert(0, self.config.get("konami", "chance", fallback="0.01"))

        # Mouse Click Settings
        self.mouse_click_var = tk.BooleanVar(value=self.config.getboolean("mouse", "enabled", fallback=False))
        ttk.Checkbutton(master, text="Enable Mouse Clicks", variable=self.mouse_click_var).grid(row=6, column=0, padx=5, pady=5, sticky="w")

        # Load and Save Buttons
        self.load_button = ttk.Button(master, text="Load Config", command=self.load_config_gui)
        self.load_button.grid(row=7, column=0, padx=5, pady=10)
        self.save_button = ttk.Button(master, text="Save Config", command=self.save_config_gui)
        self.save_button.grid(row=7, column=1, padx=5, pady=10)

        # Start/Stop Buttons and Status
        self.start_button = ttk.Button(master, text="Start", command=self.start_pressing)
        self.start_button.grid(row=8, column=0, padx=5, pady=10)
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_pressing, state=tk.DISABLED)
        self.stop_button.grid(row=8, column=1, padx=5, pady=10)

        self.status_label = ttk.Label(master, text="Status: Stopped")
        self.status_label.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        master.grid_columnconfigure(1, weight=1)

        self.running = False
        self.thread = None
        self.konami_code = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a']
        self.mouse_controller = mouse.Controller

    def load_config(self):
        try:
            self.config.read(self.config_file)
        except configparser.Error as e:
            tk.messagebox.showerror("Config Error", f"Error reading config file: {e}")

    def save_config(self):
        try:
            self.config["settings"] = {
                "keys": self.keys_entry.get(),
                "delay": self.delay_slider.get(),
                "duration": self.duration_entry.get()
            }
            self.config["konami"] = {
                "enabled": self.konami_var.get(),
                "chance": self.konami_chance_entry.get()
            }
            self.config["mouse"] = {
                "enabled": self.mouse_click_var.get()
            }
            with open(self.config_file, "w") as configfile:
                self.config.write(configfile)
        except configparser.Error as e:
            tk.messagebox.showerror("Config Error", f"Error writing config file: {e}")

    def load_config_gui(self):
        file_path = filedialog.askopenfilename(defaultextension=".ini", filetypes=[("INI files", "*.ini"), ("All files", "*.*")])
        if file_path:
            self.config_file = file_path
            self.load_config()
            self.keys_entry.delete(0, tk.END)
            self.keys_entry.insert(0, self.config.get("settings", "keys", fallback=""))
            try:
                self.delay_slider.set(float(self.config.get("settings", "delay", fallback="0.3")))
            except ValueError:
                self.delay_slider.set(0.3)
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, self.config.get("settings", "duration", fallback="0.0"))
            self.konami_var.set(self.config.getboolean("konami", "enabled", fallback=False))
            self.konami_chance_entry.delete(0, tk.END)
            self.konami_chance_entry.insert(0, self.config.get("konami", "chance", fallback="0.01"))
            self.mouse_click_var.set(self.config.getboolean("mouse", "enabled", fallback=False))
            self.update_delay_label(self.delay_slider.get())
            tk.messagebox.showinfo("Config Loaded", f"Configuration loaded from '{file_path}'")

    def save_config_gui(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ini", filetypes=[("INI files", "*.ini"), ("All files", "*.*")])
        if file_path:
            self.config_file = file_path
            self.save_config()
            tk.messagebox.showinfo("Config Saved", f"Configuration saved to '{file_path}'")

    def update_delay_label(self, value):
        self.delay_label_var.set(f"{float(value):.2f} s")

    def press_key(self, key, duration=0.0):
        """Presses and releases a single key with a specified duration."""
        keyboard.press(key)
        time.sleep(duration)
        keyboard.release(key)
        print(f"Pressed: {key} (Duration: {duration:.2f}s)")

    def press_sequence(self, sequence, duration=0.0):
        """Presses a sequence of keys with a short delay and specified duration."""
        print(f"Executing Konami Code: {sequence} (Duration: {duration:.2f}s)")
        for key in sequence:
            self.press_key(key, 0.1 + duration) # Adding a small delay between sequence keys
            time.sleep(0.05)

    def perform_mouse_click(self):
        """Performs a random mouse click."""
        button = random.choice([mouse.Button.left, mouse.Button.right, mouse.Button.middle])
        self.mouse_controller.press(button)
        self.mouse_controller.release(button)
        print(f"Mouse Click: {button}")

    def random_action_loop(self):
        while self.running:
            keys = self.keys_entry.get().lower().split()
            delay = self.delay_slider.get()
            duration_str = self.duration_entry.get()
            konami_enabled = self.konami_var.get()
            konami_chance_str = self.konami_chance_entry.get()
            mouse_click_enabled = self.mouse_click_var.get()

            try:
                duration = float(duration_str)
                if duration < 0:
                    self.update_status("Error: Invalid press duration.")
                    self.stop_pressing()
                    break
                konami_chance = float(konami_chance_str)
                if not 0.0 <= konami_chance <= 1.0:
                    self.update_status("Error: Invalid Konami Chance.")
                    self.stop_pressing()
                    break
            except ValueError:
                self.update_status("Error: Invalid input format.")
                self.stop_pressing()
                break

            if konami_enabled and random.random() < konami_chance:
                self.press_sequence(self.konami_code, duration)
            elif mouse_click_enabled and keys and random.random() < 0.5: # 50% chance of mouse click if enabled and keys are defined
                self.perform_mouse_click()
            elif keys:
                random_key = random.choice(keys)
                self.press_key(random_key, duration)

            time.sleep(delay)
            if keyboard.is_pressed('enter'):
                self.update_status("Stopped by Enter key.")
                self.stop_pressing()

    def start_pressing(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Running")
            self.thread = threading.Thread(target=self.random_action_loop)
            self.thread.start()

    def stop_pressing(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Stopped")
            if self.thread and self.thread.is_alive():
                self.thread.join()
            self.thread = None

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = KeyPresserGUI(root)
    root.mainloop()