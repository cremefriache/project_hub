import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QCheckBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from .constants import DARK_BLUE, WHITE, DEFAULT_PROJECT_NAME, DEFAULT_WEATHER_TEXT, DEFAULT_TAGLINE, DEFAULT_WEBSITES

class HubScreen(QWidget):
    def __init__(self, open_viewer_callback, open_settings_callback, open_multi_view_callback, parent=None):
        super().__init__(parent)
        self.open_viewer_callback = open_viewer_callback
        self.open_settings_callback = open_settings_callback
        self.open_multi_view_callback = open_multi_view_callback
        self.websites = DEFAULT_WEBSITES
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Header
        self.header_widget = QWidget()
        self.header_layout = QHBoxLayout()
        self.header_widget.setLayout(self.header_layout)
        self.project_name_label = QLabel(DEFAULT_PROJECT_NAME)
        self.project_name_label.setStyleSheet(f"color: {WHITE}; font-size: 18px;")
        self.datetime_label = QLabel("")
        self.datetime_label.setStyleSheet(f"color: {WHITE}; font-size: 18px;")
        self.weather_label = QLabel(DEFAULT_WEATHER_TEXT)
        self.weather_label.setStyleSheet(f"color: {WHITE}; font-size: 18px;")
        self.header_layout.addWidget(self.project_name_label, 1, alignment=Qt.AlignLeft)
        self.header_layout.addWidget(self.datetime_label, 1, alignment=Qt.AlignCenter)
        self.header_layout.addWidget(self.weather_label, 1, alignment=Qt.AlignRight)
        self.header_widget.setStyleSheet(
            f"""
            background-color: {DARK_BLUE};
            border: none;
            border-radius: 10px;
            padding: 10px;
            """
        )
        self.main_layout.addWidget(self.header_widget)

        # Dashboard Tiles
        self.tiles_widget = QWidget()
        self.tiles_layout = QGridLayout()
        self.tiles_widget.setLayout(self.tiles_layout)
        self.checkbox_dict = {}
        row_col_positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for (name, url), (r, c) in zip(self.websites.items(), row_col_positions):
            container_widget = QWidget()
            container_layout = QVBoxLayout()
            container_widget.setLayout(container_layout)
            checkbox = QCheckBox("Select")
            self.checkbox_dict[name] = checkbox
            tile_button = QPushButton(name)
            tile_button.setStyleSheet(
                f"""
                background-color: {DARK_BLUE};
                color: {WHITE};
                font-size: 20px;
                border: 2px solid white;
                border-radius: 10px;
                padding: 20px;
                """
            )
            tile_button.clicked.connect(lambda checked, u=url: self.open_viewer_callback(u))
            container_layout.addWidget(checkbox, alignment=Qt.AlignCenter)
            container_layout.addWidget(tile_button)
            self.tiles_layout.addWidget(container_widget, r, c)
        self.main_layout.addWidget(self.tiles_widget)

        # Multi-View Button
        multi_view_button = QPushButton("Open Selected in Multi-View")
        multi_view_button.clicked.connect(self.handle_open_multi_view)
        self.main_layout.addWidget(multi_view_button, alignment=Qt.AlignCenter)

        # Footer
        self.footer_widget = QWidget()
        self.footer_layout = QHBoxLayout()
        self.footer_widget.setLayout(self.footer_layout)
        self.logo_label = QLabel()
        self.logo_label.setStyleSheet("background: transparent;")
        self.tagline_label = QLabel(DEFAULT_TAGLINE)
        self.tagline_label.setStyleSheet(f"color: {DARK_BLUE}; font-size: 18px;")
        self.footer_layout.addWidget(self.logo_label, 0, alignment=Qt.AlignRight)
        self.footer_layout.addWidget(self.tagline_label, 0, alignment=Qt.AlignLeft)
        self.main_layout.addWidget(self.footer_widget)

        # Settings Button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings_callback)
        self.main_layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)

        # Date/Time Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(60000)
        self.updateDateTime()

    def updateDateTime(self):
        now = datetime.datetime.now()
        datetime_str = now.strftime("%A, %B %d %Y | %I:%M %p")
        self.datetime_label.setText(datetime_str)

    def updateHeader(self, project_name, weather_text):
        self.project_name_label.setText(project_name)
        self.weather_label.setText(weather_text)

    def updateFooter(self, logo_path, tagline):
        self.tagline_label.setText(tagline)
        if logo_path:
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.logo_label.setPixmap(pixmap)
            else:
                self.logo_label.clear()
        else:
            self.logo_label.clear()

    def handle_open_multi_view(self):
        selected = {}
        for name, url in self.websites.items():
            if self.checkbox_dict[name].isChecked():
                selected[name] = url
        if selected:
            self.open_multi_view_callback(selected)
