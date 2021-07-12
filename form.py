
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys
import webbrowser

class mainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)
        self.setWindowTitle("untitled - SM FastEdit")
        self.setWindowIcon(QIcon("txteditor.png"))
        self.resize(1000,800)
        self.path = "untitled"
        # menu bar
        menuBar = self.menuBar()
        # file menu
        fileMenu = menuBar.addMenu("File")
        new_file = fileMenu.addAction("New File")
        new_window = fileMenu.addAction("New Window")
        fileMenu.addSeparator()
        open_file = fileMenu.addAction("Open File")
        open_recent = fileMenu.addMenu("Open Recent")
        fileMenu.addSeparator()
        save = fileMenu.addAction("Save")
        save_as = fileMenu.addAction("Save As")
        save_all = fileMenu.addAction("Save All")
        fileMenu.addSeparator()
        print_file = fileMenu.addAction("Print")
        close_file = fileMenu.addAction("Close File")
        close_window = fileMenu.addAction("Close Window")
        fileMenu.addSeparator()
        prefrence = fileMenu.addMenu("Prefrences")
        settings = prefrence.addAction("Settings")
        shortcuts = prefrence.addAction("Keyboard Shortcuts")
        fileMenu.addSeparator()
        leave = fileMenu.addAction("Leave")
        #edit menu
        editMenu = menuBar.addMenu("Edit")
        undo = editMenu.addAction("Undo")
        redo = editMenu.addAction("Redo")
        editMenu.addSeparator()
        cut = editMenu.addAction("Cut")
        copy = editMenu.addAction("Copy")
        paste = editMenu.addAction("Paste")
        editMenu.addSeparator()
        find = editMenu.addAction("Find")
        replace = editMenu.addAction("Replace")
        editMenu.addSeparator()
        select_all = editMenu.addAction("Select All")
        # setting menu
        settingMenu = menuBar.addMenu("View")
        word_wrap = settingMenu.addAction("Word Wrap")
        word_wrap.setCheckable(True)
        word_wrap.setChecked(True)
        self.read_only = settingMenu.addAction("Read Only")
        self.read_only.setCheckable(True)
        self.read_only.setChecked(False)
        zoom = settingMenu.addMenu("Zoom")
        zoom_in = zoom.addAction("Zoom In")
        zoom_out = zoom.addAction("Zoom Out")
        reset_zoom = zoom.addAction("Reset Zoom")
        # Run menu
        runMenu = menuBar.addMenu("Run")
        self.openInBrowser = runMenu.addAction("Open in Browser")
        self.run = runMenu.addAction("Run")
        runMenu.addSeparator()
        runMenu.addAction("Settings")
        # help menu
        helpMenu = menuBar.addMenu("Help")
        docum = helpMenu.addAction("Documentation")
        helpMenu.addSeparator()
        tips = helpMenu.addAction("Tips and tricks")
        intro = helpMenu.addAction("Introduction")
        helpMenu.addSeparator()
        about = helpMenu.addAction("About us")
        # text area
        widget = QWidget()
        widget.setStyleSheet("background: #222;")
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        self.textArea = QPlainTextEdit(widget)
        self.textArea.setContextMenuPolicy(False)
        self.textArea.setObjectName("textArea")
        self.textArea.verticalScrollBar().setStyleSheet("""
        QScrollBar:vertical {
            background: #000;
            width: 15px;
            margin: 0;
            border: none;
        }
        QScrollBar::handle:vertical {
            background: #333;
            min-height: 0px;
        }
        QScrollBar::handle:vertical:hover {
            background: #444;
            min-height: 0px;
        }
        QScrollBar::add-line:vertical {
            background: #222;
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            background: #222;
            height: 0px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        """)
        self.textArea.horizontalScrollBar().setStyleSheet("""
        QScrollBar:horizontal {
            background: #000;
            width: 15px;
            margin: 0;
            border: none;
        }
        QScrollBar::handle:horizontal {
            background: #333;
            min-width: 0px;
        }
        QScrollBar::handle:horizontal:hover {
            background: #444;
            min-width: 0px;
        }
        """)

        self.textArea.setStyleSheet("""
        #textArea { 
            border: none;
            color: #fff;
            font-size: 22px;
            font-family: consolas;
            selection-background-color: rgba(255,255,255,0.2);
        }
        QPlainTextEdit:QMenu {
            background: #ccc;
            color: #000;
        }
        """)
        layout.addWidget(self.textArea)
    
    # shortcuts
        new_file.setShortcut("Ctrl+N")
        new_window.setShortcut("Ctrl+Shift+N")
        open_file.setShortcut("Ctrl+O")
        save.setShortcut("Ctrl+S")
        save_as.setShortcut("Ctrl+Shift+S")
        print_file.setShortcut("Ctrl+Shift+P")

        leave.setShortcut("Esc")

        undo.setShortcut("Ctrl+U")
        redo.setShortcut("Ctrl+Y")
        cut.setShortcut("Ctrl+X")
        copy.setShortcut("Ctrl+C")
        paste.setShortcut("Ctrl+V")
        select_all.setShortcut("Ctrl+A")
        find.setShortcut("Ctrl+F")

        self.read_only.setShortcut("Ctrl+Shift+R")
        zoom_in.setShortcut("Ctrl++")
        zoom_out.setShortcut("Ctrl+-")

        about.setShortcut("Ctrl+?")
    # functions
        leave.triggered.connect(self.exit)
        new_window.triggered.connect(self.new_window)
        new_file.triggered.connect(self.new_file)
        open_file.triggered.connect(self.open_file)
        save.triggered.connect(self.save_file)
        save_as.triggered.connect(self.save_as_file)
        save_all.setDisabled(True)
        close_file.triggered.connect(self.close_file)
        print_file.triggered.connect(self.print_file)
        close_window.triggered.connect(self.exit)
        undo.triggered.connect(self.textArea.undo)
        redo.triggered.connect(self.textArea.redo)
        cut.triggered.connect(self.textArea.cut)
        copy.triggered.connect(self.textArea.copy)
        paste.triggered.connect(self.textArea.paste)
        select_all.triggered.connect(self.textArea.selectAll)

        word_wrap.triggered.connect(self.toggle_wrap)
        self.read_only.triggered.connect(self.readOnly)
        self.openInBrowser.triggered.connect(self.open_in_browser)
        zoom_in.triggered.connect(self.textArea.zoomIn)
        zoom_out.triggered.connect(self.textArea.zoomOut)

        docum.triggered.connect(self.documentation)

        self.textArea.setPlaceholderText("Start typing here....")
        about.triggered.connect(self.about)
    def about(self):
        aboutDlg = QMessageBox()
        aboutDlg.setIcon(QMessageBox.Information)
        text = """
FastEdit is a open source texteditor created and maintained by SM Technology. It is best for SPL, JS and PYTHON programmers.
Visit smtechnology.com/applications to know more.
        """
        font1 = QFont()
        font1.setPointSize(10)
        font1.setFamily("Verdana")
        aboutDlg.setFont(font1)
        aboutDlg.setText(text)
        aboutDlg.show()
        aboutDlg.exec_()
    def documentation(self):
        self.docmtation = QWidget()
        self.docmtation.setWindowTitle("Documentation - SM FastEdit")
        self.docmtation.setMinimumSize(800,500)
        layout = QVBoxLayout(self.docmtation)
        area = QTextEdit()
        area.setReadOnly(True)
        area.setObjectName("area")
        area.setStyleSheet("#area{ background: #222;color: #fff;border: none;font-size: 22px;font-family: consolas;selection-background-color: rgba(255,255,255,0.2);}")
        htmlText = """
        <h1> SM FastEdit </h1>
        <p> FastEdit is a open source texteditor created and maintained by SM Technology. It is best for JS and PYTHON programmers. Dark mode of editor makes it perfect environment for coding.</p>
        <h2><u>Features that make editor perfect are:</u></h2>
        <ul>
            <li>Read only mode.</li>
            <li>Full screen mode.</li>
            <li>Undo and Redo feature.</li>
            <li>Easy shortcuts and tips.</li>
            <li>File path in title bar.</li>
            <li>Printing supported.</li>
            <li>Multi Window mode to edit more than one file.</li>
            <li>Open in browser feature to open certain file in web browser or in default editor.</li>
            <li>Dark background for eye protection.</li>
        </ul>
        <h2><u>Keyboard Shortcuts</u></h2>
        FastEdit provides easy keyboard shortcuts to save time from clicking any menuitem.
        <h3>Here is the list of keyboard shortcuts</h3>
        <ul>
            <li><b>Ctrl+N</b> to create a new file.</li>
            <li><b>Ctrl+O</b> to open a existing file from directory.</li>
            <li><b>Ctrl+Shift+N</b> to create a new window.</li>
            <li><b>Ctrl+S</b> to save current file.</li>
            <li><b>Ctrl+Shift+S</b> to save file in a specific folder.</li>
            <li><b>Ctrl+Shift+P</b> to print current file.</li>
            <li><b>Ctrl+U</b> to undo last action.</li>
            <li><b>Ctrl+Y</b> to redo last action.</li>
            <li><b>Ctrl+X</b> for cut action</li>
            <li><b>Ctrl+C</b> for copy action.</li>
            <li><b>Ctrl+P</b> for paste action.</li>
            <li><b>Ctrl+A</b> to select all text.</li>
            <li><b>Ctrl+F</b> to find any text in editor.</li>
            <li><b>Ctrl+Shift+R</b> to make editor readonly.</li>
            <li><b>Ctrl+?</b> for help.</li>
        </ul>
        <style>
            a {
                color: yellow;
                text-decoration: none;
            }
        </style>
        <p>For more help go to <a href="https://google.com">google.com</a>.</p>
        <p></p>
        <p></p>
        <h2><u>Source code</u></h2>
        <p>FastEdit is a open source and free texteditor. SM FastEdit is written in python language and used HTML for minor components of application.</p>
        <ul>
            <li><b>Author:</b> Shaurya Mishra</li>
            <li><b>Written in:</b> Python, HTML, CSS</li>
            <li><b>Programmer:</b> Shaurya Mishra</li>
            <li><b>Application type:</b> Text editor</li>
        </ul>
        """
        area.setHtml(htmlText)
        layout.addWidget(area)
        layout.setContentsMargins(0,0,0,0)
        self.docmtation.showMaximized()

    def open_in_browser(self):
        webbrowser.open_new_tab(self.path)
    def new_window(self):
        self.w = mainWindow()
        self.w.showMaximized()
    
    def dialog_critical(self):
        dlg = QMessageBox(self)
        dlg.setText("Error! Cannot open such type of files.")
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
    def new_file(self):
        self.path = "untitled"
        self.textArea.clear()
        self.update_title()
    def close_file(self):
        self.path = "untitled"
        self.textArea.clear()
        self.update_title()
    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "","All files (*.*)")
        if path:
            try:
                with open(path, 'rU') as f:
                    self.text = f.read()
            except Exception as e:
                self.dialog_critical()
            else:
                self.path = path
                self.textArea.setPlainText(self.text)
                self.update_title()
    def save_file(self):
        if self.path is "untitled":
            return self.save_as_file()
        self._save_to_path(self.path)
    def save_as_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                             "All files (*.*)")
        if not path:
            return
        self._save_to_path(path)
    def _save_to_path(self, path):
        text = self.textArea.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical()
        else:
            self.path = path
            self.update_title()
    def exit(self):
        self.save_file()
        self.close()
    def update_title(self):
        self.setWindowTitle(f"{self.path} - SM FastEdit")
    def toggle_wrap(self):
        self.textArea.setLineWrapMode(1 if self.textArea.lineWrapMode() == 0 else 0 )
    def readOnly(self):
        self.textArea.setReadOnly(True if self.textArea.isReadOnly() == False else False)
    def print_file(self):
        printDlg = QPrintDialog()
        if printDlg.exec_():
            self.textArea.print(printDlg.printer())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = mainWindow()
    Window.showMaximized()
    app.exec_()