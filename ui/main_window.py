from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from .hub_screen import HubScreen
from .viewer_screen import ViewerScreen
from .multi_viewer import MultiViewerScreen
from .constants import DEFAULT_PROJECT_NAME, DEFAULT_WEATHER_TEXT, DEFAULT_TAGLINE, DEFAULT_LOGO_PATH

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Hub")
        self.project_name = DEFAULT_PROJECT_NAME
        self.weather_text = DEFAULT_WEATHER_TEXT
        self.tagline = DEFAULT_TAGLINE
        self.logo_path = DEFAULT_LOGO_PATH
        self.viewer_instances = {}      # key: URL for ViewerScreen instances
        self.page_instances = {}        # key: URL for persistent QWebEnginePage instances
        self.multi_view_instances = {}  # key: tuple(sorted(selected.items()))
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        self.initUI()

    def initUI(self):
        self.hub_screen = HubScreen(
            open_viewer_callback=self.open_viewer,
            open_settings_callback=self.open_settings,
            open_multi_view_callback=self.open_multi_viewer
        )
        self.stack.addWidget(self.hub_screen)
        self.resize(1200, 800)
        self.show()

    def open_viewer(self, url):
        if url not in self.page_instances:
            page = QWebEnginePage(self)
            page.setUrl(QUrl(url))
            self.page_instances[url] = page
        else:
            page = self.page_instances[url]

        if url in self.viewer_instances:
            viewer = self.viewer_instances[url]
        else:
            viewer = ViewerScreen(url, self.return_to_hub, page=page)
            self.viewer_instances[url] = viewer
            self.stack.addWidget(viewer)
        self.stack.setCurrentWidget(viewer)

    def open_multi_viewer(self, selected_websites):
        key = tuple(sorted(selected_websites.items()))
        persistent_dict = {}
        for name, url in selected_websites.items():
            if url not in self.page_instances:
                page = QWebEnginePage(self)
                page.setUrl(QUrl(url))
                self.page_instances[url] = page
            else:
                page = self.page_instances[url]
            persistent_dict[name] = (url, page)

        if key in self.multi_view_instances:
            multi_viewer = self.multi_view_instances[key]
        else:
            multi_viewer = MultiViewerScreen(persistent_dict, self.return_to_hub)
            self.multi_view_instances[key] = multi_viewer
            self.stack.addWidget(multi_viewer)
        self.stack.setCurrentWidget(multi_viewer)

    def return_to_hub(self):
        self.stack.setCurrentWidget(self.hub_screen)

    def open_settings(self):
        from PyQt5.QtWidgets import QDialog
        from .settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.project_name, self.weather_text, self.tagline, self.logo_path, self)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.getValues()
            self.project_name = values["project_name"]
            self.weather_text = values["weather_text"]
            self.tagline = values["tagline"]
            self.logo_path = values["logo_path"]
            self.hub_screen.updateHeader(self.project_name, self.weather_text)
            self.hub_screen.updateFooter(self.logo_path, self.tagline)
