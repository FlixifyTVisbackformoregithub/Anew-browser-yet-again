import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QLineEdit, QAction, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserTab(QWebEngineView):
    def __init__(self, url=""):
        super().__init__()
        self.setUrl(QUrl(url))
        self.loadStarted.connect(self.show_loading)
        self.loadFinished.connect(self.hide_loading)

    def show_loading(self):
        print("Loading...")  # You can replace this with any additional loading actions

    def hide_loading(self):
        print("Loading finished!")  # You can replace this with post-load actions

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Futuristic Browser")
        self.setGeometry(300, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # Load custom HTML home page
        home_url = QUrl.fromLocalFile(os.path.abspath("templates/home.html"))
        self.add_new_tab(home_url, "Home")

        # Toolbar
        self.navbar = QToolBar()
        self.addToolBar(self.navbar)

        # Back button
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        self.navbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        self.navbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        self.navbar.addAction(reload_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.navbar.addWidget(self.url_bar)

        # New tab button
        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        self.navbar.addAction(new_tab_btn)

        # Connect signals
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

    def add_new_tab(self, qurl=QUrl(""), label="New Tab"):
        browser_tab = BrowserTab(qurl)
        idx = self.tabs.addTab(browser_tab, label)
        self.tabs.setCurrentIndex(idx)
        browser_tab.urlChanged.connect(lambda qurl, browser_tab=browser_tab: self.update_tab_title(browser_tab))

    def update_tab_title(self, browser_tab):
        idx = self.tabs.indexOf(browser_tab)
        self.tabs.setTabText(idx, browser_tab.title())

    def close_current_tab(self, idx):
        if self.tabs.count() > 1:
            self.tabs.removeTab(idx)

    def navigate_to_url(self):
        url = QUrl(self.url_bar.text())
        if url.scheme() == "":
            url.setScheme("http")
        self.tabs.currentWidget().setUrl(url)

    def update_url_bar(self, idx):
        qurl = self.tabs.currentWidget().url()
        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

# Run the application
app = QApplication(sys.argv)
browser = WebBrowser()
browser.show()
sys.exit(app.exec_())
