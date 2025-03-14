from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QDialogButtonBox, QFileDialog

class SettingsDialog(QDialog):
    def __init__(self, project_name, weather_text, tagline, logo_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self._project_name = project_name
        self._weather_text = weather_text
        self._tagline = tagline
        self._logo_path = logo_path
        self.initUI()

    def initUI(self):
        layout = QFormLayout()
        self.project_name_edit = QLineEdit(self._project_name)
        self.weather_edit = QLineEdit(self._weather_text)
        self.tagline_edit = QLineEdit(self._tagline)
        self.logo_edit = QLineEdit(self._logo_path)
        logo_button = QPushButton("Browse Logo...")
        logo_button.clicked.connect(self.browse_logo)
        layout.addRow("Project Name:", self.project_name_edit)
        layout.addRow("Weather Text:", self.weather_edit)
        layout.addRow("Tagline:", self.tagline_edit)
        layout.addRow("Logo Path:", self.logo_edit)
        layout.addRow("", logo_button)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        self.setLayout(layout)

    def browse_logo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.jpeg *.gif)")
        if file_name:
            self.logo_edit.setText(file_name)

    def getValues(self):
        return {
            "project_name": self.project_name_edit.text().strip(),
            "weather_text": self.weather_edit.text().strip(),
            "tagline": self.tagline_edit.text().strip(),
            "logo_path": self.logo_edit.text().strip()
        }
