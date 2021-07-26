# Author : Shaurya Mishra 
# Writer : Shaurya Mishra
# Additional support from : Github
import os
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWebEngineWidgets import *
import sys
import webbrowser
import TextArea
import LineNumberBar
import webbrowser
import ToolBar

FullScreen = "Full Screen"
disableAction = """
QAction {
		color: #999;
}
QAction:hover {
		background: #222;
}
"""

class mainWindow(QMainWindow):
	def __init__(self, parent=None):
		super(mainWindow, self).__init__(parent)
		self.setWindowTitle("untitled - SM FastEdit")
		self.setWindowIcon(QIcon("Images/txteditor.png"))
		self.resize(1000,800)
		self.setMinimumSize(500,300)
		self.path = "untitled"
		# menu bar
		self.menuBarMain = self.menuBar()
		self.setContextMenuPolicy(False)
		self.menuBarMain.setStyleSheet("""
		QMenu {
			background: #222;
			border: 2px solid #555;
			color: rgba(255,255,255,0.7);
		}
		QMenu::item {
			padding: 8px 30px;
		}

		QMenu::item:selected{
 			background-color: #444;
 			color: rgb(255, 255, 255);
 		} 
 		QMenu::separator {
 			height: 2px;
 			background: #555;
 		}
		QMenu::item:disabled {
			color: #999;
		}
		QMenu::item:disabled:selected {
			background: #222;
		}
		""")
		# file menu
		fileMenu = self.menuBarMain.addMenu("File")
		new_file = fileMenu.addAction("New File")
		new_window = fileMenu.addAction("New Window")
		fileMenu.addSeparator()
		open_file = fileMenu.addAction("Open File")
		fileMenu.addSeparator()
		save = fileMenu.addAction("Save")
		save_as = fileMenu.addAction("Save As")
		save_all = fileMenu.addAction("Save All")
		save_all.setDisabled(True)
		fileMenu.addSeparator()
		print_file = fileMenu.addAction("Print")
		close_file = fileMenu.addAction("Close File")
		close_window = fileMenu.addAction("Close Window")
		fileMenu.addSeparator()
		prefrence = fileMenu.addMenu("Prefrences")
		tools_developer = prefrence.addAction("Developer tools")
		prefrence.addSeparator()
		settings = prefrence.addAction("Settings")
		shortcuts = prefrence.addAction("Keyboard Shortcuts")
		prefrence.addSeparator()
		check_updates = prefrence.addAction("Check for updates")
		fileMenu.addSeparator()
		leave = fileMenu.addAction("Leave")
		#edit menu
		editMenu = self.menuBarMain.addMenu("Edit")
		self.undo = editMenu.addAction("Undo")
		self.redo = editMenu.addAction("Redo")
		editMenu.addSeparator()
		self.cut = editMenu.addAction("Cut")
		self.copy = editMenu.addAction("Copy")
		self.paste = editMenu.addAction("Paste")
		self.delete = editMenu.addAction("Delete")
		editMenu.addSeparator()
		self.select_all = editMenu.addAction("Select All")
		self.copy_all = editMenu.addAction("Copy All")
		editMenu.addSeparator()
		self.clear_all = editMenu.addAction("Clear Editor")
		# setting menu
		viewMenu = self.menuBarMain.addMenu("View")
		word_wrap = viewMenu.addAction("Word Wrap")
		word_wrap.setCheckable(True)
		word_wrap.setChecked(True)
		self.read_only = viewMenu.addAction("Read Only")
		self.read_only.setCheckable(True)
		self.read_only.setChecked(False)
		viewMenu.addSeparator()
		appearance = viewMenu.addMenu("Appearance")
		self.fullScreen = appearance.addAction(FullScreen)
		minimize = appearance.addAction("Minimize")
		appearance.addSeparator()
		num_bar = appearance.addAction("Show Line Bar")
		num_bar.setCheckable(True)
		num_bar.setChecked(True)
		self.status_bar = appearance.addAction("Show Status Bar")
		self.status_bar.setCheckable(True)
		self.status_bar.setChecked(True)
		side_bar = appearance.addAction("Show Side Bar")
		side_bar.setCheckable(True)
		side_bar.setChecked(True)
		editor = appearance.addAction("Show Editor Area")
		editor.setCheckable(True)
		editor.setChecked(True)
		# Run menu
		runMenu = self.menuBarMain.addMenu("Run")
		self.openInBrowser = runMenu.addAction("Open in Browser")
		self.run = runMenu.addAction("Run File")
		runMenu.addSeparator()
		runMenu.addAction("Settings")
		# help menu
		helpMenu = self.menuBarMain.addMenu("Help")
		docum = helpMenu.addAction("Documentation")
		helpMenu.addSeparator()
		tips = helpMenu.addAction("Tips and tricks")
		intro = helpMenu.addAction("Source Code")
		helpMenu.addSeparator()
		about = helpMenu.addAction("About FastEdit")

		# tool bar
		cursor = QCursor(Qt.PointingHandCursor)
		self.toolBarMain = ToolBar.FE_ToolBar()
		self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBarMain)
		self.toolBarMain.setContextMenuPolicy(False)
		a1 = QPushButton()
		a1.setCursor(cursor)
		a1.setIcon(QIcon("Images\Icons\cil-exit-to-app.png"))
		a1.setStatusTip("Leave Application")
		self.toolBarMain.addWidget(a1)
		a1.clicked.connect(self.exit)
		self.toolBarMain.addSeparator()
		a3 = QPushButton()
		a3.setCursor(cursor)
		a3.setIcon(QIcon("Images\Icons\cil-plus.png"))
		a3.setStatusTip("Create a New File")
		a3.clicked.connect(self.new_file)
		self.toolBarMain.addWidget(a3)
		a4 = QPushButton()
		a4.setCursor(cursor)
		a4.setStatusTip("Open a Existing File from Directory")
		a4.setIcon(QIcon("Images\Icons\cil-file.png"))
		a4.clicked.connect(self.open_file)
		self.toolBarMain.addWidget(a4)
		a5 = QPushButton()
		a5.setCursor(cursor)
		a5.setIcon(QIcon("Images\Icons\cil-save.png"))
		a5.setStatusTip("Save/Save as file")
		a5.clicked.connect(self.save_file)
		self.toolBarMain.addWidget(a5)

		# completer
		suggestions = [
			'html','head','meta','link','class','type','href','src','script','body','div','pre','button','a'
		]
		completer = QCompleter(suggestions)
		# text area
		self.widget = QWidget()
		self.setCentralWidget(self.widget)
		layout = QHBoxLayout(self.widget)
		layout.setContentsMargins(0,0,0,0)
		self.textArea = TextArea.TextEdit(self.widget)
		self.textArea.setContextMenuPolicy(True)
		font = self.textArea.font()
		fontMetrics = QFontMetricsF(font)
		spaceWidth = fontMetrics.width('  ')
		self.textArea.setTabStopDistance(spaceWidth * 6)
		self.textArea.setObjectName("textArea")
		self.numbers = LineNumberBar.NumberBar(self.textArea)
		layout.addWidget(self.numbers)
		layout.addWidget(self.textArea)
		layout.setSpacing(0)

		self.darkMode()
		self.textArea.cursorPositionChanged.connect(self.cursorPosition)

		self.statusBarMain = self.statusBar()
		self.statusBarMain.setStyleSheet("""
		QStatusBar {
			background: #333; 
			color: #ccc;
		}
		QStatusBar:hover {
			background: rgba(51, 51, 51,0.99);
		}
		QStatusBar::item {
			border: none;
		}
		QPushButton{
			border: none;
			padding: 5px 10px;
			font-size: 15px;
			color: #fff;
		}
		QPushButton:hover {
			background: #444;
		}
		QPushButton:pressed {
			background: #555;
		}
		QLabel{
			border: none;
			padding: 5px 10px;
			font-size: 15px;
			color: #fff;
		}
		
		QPushButton::menu-indicator{
			width:0px;
			image: none;
		}
		QLineEdit {
                  background: #333;
                  border: none;
                  padding: 5px 10px;
                  color: #fff;
                  font-size: 16px;
                  font-family: verdana;
            }
            QLineEdit:hover {
                  background: #444;
            }
            QLineEdit:focus {
                  background: #555;
            }
		""")
		self.a2 = QLineEdit()
		self.a2.setPlaceholderText("Find...")
		self.a2.setClearButtonEnabled(True)
		self.a2.setFixedWidth(150)
		self.a2_text = self.a2.text()
		self.a2.returnPressed.connect(self.find_text)
		self.statusBarMain.addPermanentWidget(self.a2)
		self.a = QLabel("Ln 1, Col 1")
		self.statusBarMain.addPermanentWidget(self.a)
		self.b = QLabel(".txt")
		self.c = QLabel("Tab Size: 6")
		self.d = QPushButton()
		self.d.setIcon(QIcon("Images/icon_more.png"))
		moreMenu = QMenu()
		moreMenu.setStyleSheet("""
		QMenu {
			background: #222;
			border: 2px solid #555;
			color: rgba(255,255,255,0.7);
		}
		QMenu::item {
			padding: 8px 30px;
		}

		QMenu::item:selected{
 			background-color: #444;
 			color: rgb(255, 255, 255);
 		} 
 		QMenu::separator {
 			height: 2px;
 			background: #555;
 		}
		""")
		hideStatusBar = moreMenu.addAction("Hide Status Bar")
		moreMenu.addSeparator()
		showHideLine = moreMenu.addAction("Line/Column")
		showHideLine.setCheckable(True)
		showHideLine.setChecked(True)
		showTabSize = moreMenu.addAction("Tab Size")
		showTabSize.setCheckable(True)
		showTabSize.setChecked(True)
		showEditorLang = moreMenu.addAction("Editor Language")
		showEditorLang.setCheckable(True)
		showEditorLang.setChecked(True)
		self.d.setMenu(moreMenu)
		self.statusBarMain.addPermanentWidget(self.c)
		self.statusBarMain.addPermanentWidget(self.b)
		self.statusBarMain.addPermanentWidget(self.d)
	# shortcuts
		new_file.setShortcut("Ctrl+N")
		new_file.setStatusTip("Create a New File")
		new_window.setShortcut("Ctrl+Shift+N")
		new_window.setStatusTip("Create a New Window")
		open_file.setShortcut("Ctrl+O")
		open_file.setStatusTip("Open an Existing File from any Folder.")
		save.setShortcut("Ctrl+S")
		save.setStatusTip("Save file")
		save_as.setShortcut("Ctrl+Shift+S")
		save_as.setStatusTip("Save file as")
		print_file.setShortcut("Ctrl+Shift+P")
		print_file.setStatusTip("Print Current File")
		leave.setStatusTip("Leave Application")

		self.undo.setShortcut("Ctrl+U")
		self.undo.setStatusTip("Undo last action")
		self.redo.setShortcut("Ctrl+Y")
		self.redo.setStatusTip("Redo last action")
		self.cut.setShortcut("Ctrl+X")
		self.cut.setStatusTip("Cut")
		self.copy.setShortcut("Ctrl+C")
		self.copy.setStatusTip("Copy")
		self.paste.setShortcut("Ctrl+V")
		self.paste.setStatusTip("Paste")
		self.delete.setShortcut("Del")
		self.delete.setStatusTip("Delete")
		self.select_all.setShortcut("Ctrl+A")
		self.select_all.setStatusTip("Select All Text")
		self.copy_all.setShortcut("Ctrl+Alt+C")
		self.copy_all.setStatusTip("Copy All Text")
		self.clear_all.setShortcut("Alt+X")
		self.clear_all.setStatusTip("Clear Editor's Text")

		self.read_only.setShortcut("Ctrl+Shift+R")
		self.fullScreen.setShortcut("F11")

		self.run.setShortcut("F5")

		docum.setShortcut("Ctrl+?")
	# functions
		leave.triggered.connect(self.exit)
		new_window.triggered.connect(self.new_window)
		new_file.triggered.connect(self.new_file)
		open_file.triggered.connect(self.open_file)
		save.triggered.connect(self.save_file)
		save_as.triggered.connect(self.save_as_file)
		close_file.triggered.connect(self.close_file)
		print_file.triggered.connect(self.print_file)
		close_window.triggered.connect(self.exit)
		shortcuts.triggered.connect(self.keyboardShortcuts)
		tools_developer.triggered.connect(self.developer_tools)

		self.undo.triggered.connect(self.Undo)
		self.redo.triggered.connect(self.Redo)
		self.cut.triggered.connect(self.textArea.cut)
		self.copy.triggered.connect(self.Copy)
		self.paste.triggered.connect(self.Paste)
		self.delete.triggered.connect(self.textArea.cut)
		self.select_all.triggered.connect(self.SelectAll)
		self.copy_all.triggered.connect(self.CopyAll)
		self.clear_all.triggered.connect(self.textArea.clear)

		word_wrap.triggered.connect(self.toggle_wrap)
		self.read_only.triggered.connect(self.readOnly)
		self.fullScreen.triggered.connect(self.full_screen)
		minimize.triggered.connect(self.showMinimized)
		num_bar.triggered.connect(self.toggle_num_bar)
		self.status_bar.triggered.connect(self.toggle_status_bar)
		side_bar.triggered.connect(self.toggle_side_bar)
		editor.triggered.connect(self.toggle_editor)
		self.openInBrowser.triggered.connect(self.open_in_browser)

		docum.triggered.connect(self.documentation)
		
		showHideLine.triggered.connect(self.showLineCol)
		showTabSize.triggered.connect(self.showTabSize)
		hideStatusBar.triggered.connect(self.showStatusBar)
		showEditorLang.triggered.connect(self.showEditorLang)

		self.textArea.textChanged.connect(self.unsaved)

		about.triggered.connect(self.about)
		intro.triggered.connect(self.intro)
	def intro(self):
		self.introWindow = QWidget()
		self.introWindow.setWindowTitle("Source Code - Github.com - SM FastEdit")
		layout = QVBoxLayout(self.introWindow)
		webView = QWebEngineView()
		webView.setZoomFactor(1.4)
		webView.setUrl(QUrl("https://github.com/codeguru-eng/SM-FastEdit"))
		layout.addWidget(webView)
		layout.setContentsMargins(0,0,0,0)
		self.introWindow.showMaximized()
	def toggle_side_bar(self):
		if self.toolBarMain.isVisible():
			self.toolBarMain.hide()
		elif self.toolBarMain.isHidden():
			self.toolBarMain.show()
	def find_text(self):
		word = self.a2.text()
		if self.textArea.find(word):
			linenumber = self.textArea.textCursor().blockNumber() + 1
			self.statusBar().showMessage("Found " + self.a2.text() + "'at Line: " + str(linenumber))
			self.textArea.centerCursor()
		else:
			self.statusBar().showMessage(self.a2.text() + " not found")
			self.textArea.moveCursor(QTextCursor.Start)
			if self.textArea.find(word):
				linenumber = self.textArea.textCursor().blockNumber() + 1
				self.statusBar().showMessage("Found '" + self.a2.text() + "' at Line: " + str(linenumber))
				self.textArea.centerCursor()
	def unsaved(self):
		self.statusBarMain.showMessage("File is unsaved.")
	def showEditorLang(self):
		if self.b.isHidden():
			self.b.show()
		elif self.b.isVisible():
			self.b.hide()
			self.statusBarMain.showMessage("Editor Language widget is removed. Go to settings to show it again.", 5000)
	def showStatusBar(self):
		if self.statusBarMain.isVisible() and self.status_bar.isChecked():
			self.statusBarMain.hide()
			self.status_bar.setChecked(False)
		elif self.statusBarMain.isHidden() and self.status_bar.isChecked(False):
			self.statusBarMain.show()
			self.status_bar.setChecked(True)
	def showTabSize(self):
		if self.c.isHidden():
			self.c.show()
		elif self.c.isVisible():
			self.c.hide()
			self.statusBarMain.showMessage("Tab Size widget is removed. Go to settings to show it again.", 5000)
	def showLineCol(self):
		if self.a.isHidden():
			self.a.show()
		elif self.a.isVisible():
			self.a.hide()
			self.statusBarMain.showMessage("Line and Column widget is removed. Go to settings to show it again.", 5000)
	def cursorPosition(self):
		cursor = self.textArea.textCursor()
		x = cursor.blockNumber() +1
		y = cursor.columnNumber() + 1
		self.a.setText(f"Ln {x}, Col {y}")
	def toggle_editor(self):
		if self.textArea.isVisible():
			self.textArea.hide()
			self.numbers.hide()
		elif self.textArea.isHidden():
			self.textArea.show()
			self.numbers.show()
	def toggle_status_bar(self):
		if self.statusBarMain.isVisible():
			self.statusBarMain.hide()
		elif self.statusBarMain.isHidden():
			self.statusBarMain.show()
	def toggle_num_bar(self):
		if self.numbers.isVisible():
			self.numbers.hide()
		elif self.numbers.isHidden():
			self.numbers.show()
	def full_screen(self):
		if self.isMaximized():
			self.showFullScreen()
			self.fullScreen.setText("Normal")
		elif self.isFullScreen():
			self.showMaximized()
			self.fullScreen.setText(FullScreen)
	def Undo(self):
		if self.textArea.undoAvailable:
			self.textArea.undo()
	def Redo(self):
		if self.textArea.redoAvailable:
			self.textArea.redo()
	def Copy(self):
		if self.textArea.copyAvailable:
			self.textArea.copy()
	def Paste(self):
		if self.textArea.canPaste:
			self.textArea.paste()
	def SelectAll(self):
		self.textArea.selectAll()
	def CopyAll(self):
		if self.textArea.copyAvailable:
			self.textArea.selectAll()
			self.textArea.copy()

	def developer_tools(self):
		webbrowser.open_new_tab("https://github.com/codeguru-eng/SM-FastEdit")
	def about(self):
		aboutDlg = QMessageBox()
		aboutDlg.setIcon(QMessageBox.Information)
		text = f"""
FastEdit is a open source texteditor created and maintained by SM Technology. It is only for PYTHON programmers.
Visit smtechnology.com/applications to know more.
	Version: 1.0

© Copyright 2021 SM Technology
		"""
		font1 = QFont()
		font1.setPointSize(10)
		font1.setFamily("Verdana")
		aboutDlg.setFont(font1)
		aboutDlg.setText(text)
		aboutDlg.show()
		aboutDlg.exec_()
	def keyPressEvent(self, event):
		options = {"[": "]", "'": "'", '"': '"', "{": "}", "(": ")", "<": ">"}
		option = options.get(event.text())
		if option is not None:
			tc = self.textArea.textCursor()
			p = tc.position()
			self.textArea.insertPlainText(option)
			tc.setPosition(p)
			self.textArea.setTextCursor(tc)
	def keyboardShortcuts(self):
		self.shortcutTip = QWidget()
		self.shortcutTip.setWindowTitle("Documentation - SM FastEdit")
		self.shortcutTip.setMinimumSize(800,500)
		layout = QVBoxLayout(self.shortcutTip)
		area = QTextEdit()
		area.setReadOnly(True)
		area.setObjectName("area")
		area.setStyleSheet("#area{ background: #222;color: #fff;border: none;font-size: 22px;font-family: consolas;selection-background-color: rgba(255,255,255,0.2);}")
		htmlText = """
		<h1> Keyboard Shortcuts</h1>
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
		"""
		area.setHtml(htmlText)
		area.verticalScrollBar().setStyleSheet("""
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
		layout.addWidget(area)
		layout.setContentsMargins(0,0,0,0)
		self.shortcutTip.showMaximized()

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
		<p> FastEdit is a open source texteditor created and maintained by SM Technology. It is only for PYTHON programmers. Dark mode of editor makes it perfect environment for coding.</p>
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
		<h3>Here is the list of all keyboard shortcuts</h3>
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
		area.verticalScrollBar().setStyleSheet("""
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
		layout.addWidget(area)
		layout.setContentsMargins(0,0,0,0)
		self.docmtation.showMaximized()

	def open_in_browser(self):
		self.statusBarMain.showMessage("Opening....",5000)
		webbrowser.open_new_tab(self.path)
		self.statusBarMain.showMessage("Opened in browser",5000)
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
		self.textArea.setFocus()
		self.update_title()
		self.statusBar().showMessage("Created a New File", 5000)
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
				self.statusBar().showMessage(f"Opened {self.path}", 5000)
				split_tUp = os.path.splitext(self.path)
				file_ext = split_tUp[1]
				self.b.setText(file_ext)
	def save_file(self):
		if self.path is "untitled":
			return self.save_as_file()
		self._save_to_path(self.path)
		self.statusBar().showMessage("Saved file", 5000)
	def save_as_file(self):
		path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
							 "All files (*.*)")
		if not path:
			return
		self._save_to_path(path)
		split_tUp = os.path.splitext(path)
		file_ext = split_tUp[1]
		self.b.setText(file_ext)
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
		self.close()
	def closeEvent(self, e):
		self.save_file()
	def update_title(self):
		self.setWindowTitle(f"{self.path} - SM FastEdit")
	def toggle_wrap(self):
		self.textArea.setLineWrapMode(1 if self.textArea.lineWrapMode() == 0 else 0 )
	def darkMode(self):
		self.widget.setStyleSheet("background: #222;")
		self.textArea.setStyleSheet("""
		#textArea { 
			border: none;
			color: #fff;
			font-size: 22px;
			font-family: consolas;
			selection-background-color: rgba(255,255,255,0.2);
		}
		""")
	def readOnly(self):
		self.textArea.setReadOnly(True if self.textArea.isReadOnly() == False else False)
	def print_file(self):
		printDlg = QPrintDialog()
		if printDlg.exec_():
			self.textArea.print(printDlg.printer())
	def set_numbers_visible(self, value = True):
		self.numbers.setVisible(True)
	def paintEvent(self, event):
		highlighted_line = QTextEdit.ExtraSelection()
		highlighted_line.format.setBackground(LineNumberBar.lineHighlightColor)
		highlighted_line.format.setProperty(QTextFormat.FullWidthSelection,QVariant(True))
		highlighted_line.cursor = self.textArea.textCursor()
		highlighted_line.cursor.clearSelection()
		self.textArea.setExtraSelections([highlighted_line])

if __name__ == "__main__":
	app = QApplication(sys.argv)
	Window = mainWindow()
	Window.showMaximized()
	app.exec_()
