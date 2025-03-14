from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MultiViewerScreen(QWidget):
    def __init__(self, websites_dict, return_callback, parent=None):
        """
        :param websites_dict: dict of {display_name: (url, page)}
                                where page is a persistent QWebEnginePage.
        :param return_callback: function to call when the user clicks "Return"
        """
        super().__init__(parent)
        self.return_callback = return_callback
        self.initUI(websites_dict)

    def initUI(self, websites_dict):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Make the overall MultiViewerScreen expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # A grid to hold all the viewers
        self.grid = QGridLayout()
        main_layout.addLayout(self.grid)

        # Lay out the viewers in a grid
        positions = self.calculatePositions(len(websites_dict))
        row_count = max(r for r, _ in positions) + 1
        col_count = max(c for _, c in positions) + 1

        # Force rows/columns to expand equally
        for row in range(row_count):
            self.grid.setRowStretch(row, 1)
        for col in range(col_count):
            self.grid.setColumnStretch(col, 1)

        # Create a ViewerWidget for each site
        for (row, col), (name, (url, page)) in zip(positions, websites_dict.items()):
            viewer_widget = ViewerWidget(url, page)
            # Make the viewer widget expand
            viewer_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.grid.addWidget(viewer_widget, row, col)

        # A "Return" button at the bottom
        return_button = QPushButton("Return")
        return_button.clicked.connect(self.return_callback)
        main_layout.addWidget(return_button)

    def calculatePositions(self, count):
        if count == 1:
            return [(0, 0)]
        elif count == 2:
            return [(0, 0), (0, 1)]
        elif count == 3:
            return [(0, 0), (0, 1), (1, 0)]
        else:
            return [(0, 0), (0, 1), (1, 0), (1, 1)]

class ViewerWidget(QWidget):
    """
    A mini-browser widget that accepts an optional persistent QWebEnginePage.
    """
    def __init__(self, url, page=None, parent=None):
        super().__init__(parent)
        self.url = url
        self.page = page
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Let the widget expand in its grid cell
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.webview = QWebEngineView()
        self.webview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if self.page:
            self.webview.setPage(self.page)
        else:
            self.webview.load(QUrl(self.url))
        layout.addWidget(self.webview)
        
        # Create the web view; if a persistent page is given, use it.
        self.webview = QWebEngineView()
        if self.page:
            self.webview.setPage(self.page)
        else:
            self.webview.load(QUrl(self.url))
        layout.addWidget(self.webview)

        # Navigation buttons: Home, Back, Forward.
        nav_layout = QHBoxLayout()
        self.home_btn = QPushButton("Home")
        self.back_btn = QPushButton("Back")
        self.fwd_btn = QPushButton("Forward")
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.fwd_btn)
        layout.addLayout(nav_layout)

        # Connect signals.
        self.home_btn.clicked.connect(self.go_home)
        self.back_btn.clicked.connect(self.webview.back)
        self.fwd_btn.clicked.connect(self.webview.forward)

        # Auto-refresh timer (5 minutes)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.webview.reload)
        self.timer.start(300000)

    def go_home(self):
        if self.page:
            self.webview.setUrl(QUrl(self.url))
        else:
            self.webview.load(QUrl(self.url))

    # Adaptive refresh: pause when mouse enters, resume on leave.
    def enterEvent(self, event):
        if self.timer.isActive():
            self.timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.timer.isActive():
            self.timer.start(300000)
        super().leaveEvent(event)
