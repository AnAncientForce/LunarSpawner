import os
import sys
import signal
import json
import pyautogui
import pygetwindow
import time
from options import Options
from interface import Interface
from PyQt5.QtWidgets import QApplication

current_directory = os.path.dirname(os.path.realpath(__file__))
logic = None

class Logic:
    def __init__(self):
        self.options = Options()

    def parse_raw_handbook_to_json(self):
        if os.path.exists(os.path.join(current_directory, "spawn.json")):
            self.spawn_json = json.load(open("spawn.json", "r"))
            print("Spawn data exists")
            return True
        if not os.path.exists(os.path.join(current_directory, "Lunar Core Handbook.txt")):
            print(f"Ensure there is a file in the directory {current_directory} named 'Lunar Core Handbook.txt'")
            return False
        category_whitelist = ["NPC Monsters (Spawnable)", "Battle Monsters", "Mazes"]
        item_blacklist = ["null", "{NICKNAME}", "{TEXTJOIN}"]
        parsed_data = {}
        with open("Lunar Core Handbook.txt", "r") as file:
            content = file.read()
            sections = content.split('# ')
            added_names = set()
            for section in sections:
                if section.strip():
                    lines = section.strip().splitlines()
                    category = lines[0].strip()
                    if len(category) > 3 and category in category_whitelist:
                        entries = [
                            line.split(" : ") for line in lines[1:] 
                            if " : " in line
                        ]
                        if entries:
                            unique_entries = []
                            for item in entries:
                                item_id = item[0].strip()
                                item_name = item[1].strip()
                                if not any(blacklisted in item_name for blacklisted in item_blacklist) and item_name not in added_names:
                                    unique_entries.append({"id": item_id, "name": item_name})
                                    added_names.add(item_name)
                            if unique_entries:
                                if category not in parsed_data:
                                    parsed_data[category] = unique_entries
                                else:
                                    parsed_data[category].extend(unique_entries)
        with open("spawn.json", "w") as json_file:
            json.dump(parsed_data, json_file, indent=4)
        
        self.spawn_json = json.load(open("spawn.json", "r"))
        return True
    
    def open_interface_loop(self):
        app = QApplication(sys.argv)
        window = Interface(self)
        window.show()
        sys.exit(app.exec_())

    def paste_command_to_java_console(self, command):
        clipboard = QApplication.clipboard()
        clipboard.setText(command.strip())
        windows = pygetwindow.getAllWindows()
        for window in windows:
            if 'java' in window.title.lower():
                window.activate()
                pyautogui.hotkey('ctrl', 'v')  
                time.sleep(0.5)
                pyautogui.press('enter')
                break

def main() -> None:
    global logic
    logic = Logic()
    if logic.parse_raw_handbook_to_json():
        logic.open_interface_loop()
    
if __name__ == '__main__':
    main()


def on_exit():
    sys.exit(0)

signal.signal(signal.SIGINT, on_exit)