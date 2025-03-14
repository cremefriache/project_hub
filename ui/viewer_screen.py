from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

class ViewerScreen(QWidget):
    """
    A full-screen viewer that can accept a persistent QWebEnginePage.
    """
    def __init__(self, url, return_callback, page=None, parent=None):
        super().__init__(parent)
        self.initial_url = url
        self.return_callback = return_callback
        self.page = page
        self.initUI()
        self.startAutoRefresh()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Create the web view; if a persistent page exists, use it.
        self.webview = QWebEngineView()
        if self.page:
            self.webview.setPage(self.page)
        else:
            self.webview.load(QUrl(self.initial_url))
        main_layout.addWidget(self.webview)

        # Navigation buttons.
        nav_layout = QHBoxLayout()
        self.home_btn = QPushButton("Home")
        self.back_btn = QPushButton("Back")
        self.forward_btn = QPushButton("Forward")
        self.return_btn = QPushButton("Return")

        self.home_btn.clicked.connect(self.go_home)
        self.back_btn.clicked.connect(self.webview.back)
        self.forward_btn.clicked.connect(self.webview.forward)
        self.return_btn.clicked.connect(self.return_callback)

        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.return_btn)
        main_layout.addLayout(nav_layout)

        self.setLayout(main_layout)

    def go_home(self):
        if self.page:
            self.webview.setUrl(QUrl(self.initial_url))
        else:
            self.webview.load(QUrl(self.initial_url))

    def startAutoRefresh(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.webview.reload)
        self.timer.start(300000)

    def showEvent(self, event):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        super().showEvent(event)

    def hideEvent(self, event):
        if hasattr(self, 'timer') and not self.timer.isActive():
            self.timer.start(300000)
        super().hideEvent(event)
