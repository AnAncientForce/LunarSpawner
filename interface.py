import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton

class Interface(QWidget):
    def __init__(self, logic):
        super().__init__()
        self.logic = logic
        self.parsed_data = self.logic.spawn_json
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.label = QLabel("", self)
        layout.addWidget(self.label)
        
        self.amount_label = QLabel("Amount", self)
        self.amount_combo = QComboBox(self)
        self.amount_combo.addItems([str(i) for i in range(1, 6)])
        self.amount_combo.setCurrentText("1")
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_combo) 

        self.radius_label = QLabel("Radius", self)
        self.radius_combo = QComboBox(self)
        self.radius_combo.addItems([str(i) for i in range(0, 6)])
        self.radius_combo.setCurrentText("2")
        layout.addWidget(self.radius_label)
        layout.addWidget(self.radius_combo)

        self.lv_label = QLabel("Level", self)
        self.lv_combo = QComboBox(self)
        self.lv_combo.addItems([str(i) for i in range(1, 81)])
        self.lv_combo.setCurrentText("80")
        layout.addWidget(self.lv_label) 
        layout.addWidget(self.lv_combo)

        self.prop_label = QLabel("Prop", self)
        self.prop_combo = QComboBox(self)
        for item in self.parsed_data["NPC Monsters (Spawnable)"]:
            self.prop_combo.addItem(item["name"], item["id"])
        layout.addWidget(self.prop_label) 
        layout.addWidget(self.prop_combo)

        self.enemy_label = QLabel("Enemy", self)
        self.enemy_combo = QComboBox(self)
        for item in self.parsed_data["NPC Monsters (Spawnable)"]:
            self.enemy_combo.addItem(item["name"], item["id"])
        layout.addWidget(self.enemy_label) 
        layout.addWidget(self.enemy_combo)

        self.maze_label = QLabel("Scene", self)
        self.maze_combo = QComboBox(self)
        for item in self.parsed_data["Mazes"]:
            self.maze_combo.addItem(item["name"], item["id"])
        layout.addWidget(self.maze_label) 
        layout.addWidget(self.maze_combo)
        
        self.randomize_button = QPushButton("Randomize Enemy + Location", self)
        self.randomize_button.clicked.connect(self.randomize_enemy_and_location)
        layout.addWidget(self.randomize_button)

        self.copy_scene_button = QPushButton("Copy Scene", self)
        self.copy_scene_button.clicked.connect(self.copy_scene)
        layout.addWidget(self.copy_scene_button)

        self.randomize_button = QPushButton("Randomize Enemy", self)
        self.randomize_button.clicked.connect(self.randomize_enemy)
        layout.addWidget(self.randomize_button)

        self.copy_button = QPushButton("Copy Spawn", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        self.setLayout(layout)
        self.setWindowTitle('Spawner')
        self.setGeometry(1000, 1000, 400, 200)
    
    def display_ids(self):
        combo = self.sender()
        print(combo.currentData(), combo.currentText())
    

    def copy_to_clipboard(self):
        if self.logic.options.heal_before_battle:
            self.logic.paste_command_to_java_console(f"/heal @{self.logic.options.uid}")
        self.logic.paste_command_to_java_console(f"/spawn @{self.logic.options.uid} {self.prop_combo.currentData()} x{self.amount_combo.currentText()} lv{self.lv_combo.currentText()} {self.radius_combo.currentText()} {self.enemy_combo.currentData()}")
        self.label.setText('Success!')

    def copy_scene(self):
        self.logic.paste_command_to_java_console(f"/scene @{self.logic.options.uid} {self.maze_combo.currentData()}")


    def randomize_enemy_and_location(self):
        if self.logic.options.randomize_prop:
            self.prop_combo.setCurrentIndex(random.randint(1, self.prop_combo.count() - 1))
        self.enemy_combo.setCurrentIndex(random.randint(1, self.enemy_combo.count() - 1))
        self.maze_combo.setCurrentIndex(random.randint(1, self.maze_combo.count() - 1))
       
    
    def randomize_enemy(self):
        self.enemy_combo.setCurrentIndex(random.randint(1, self.enemy_combo.count() - 1))