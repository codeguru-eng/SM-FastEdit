from PyQt5.QtWidgets import *
from syntax import *

class TextEdit(QPlainTextEdit):
    """TextEdit widget for App"""
    #Auto complete brackets and tags
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        tags = {"[": "]", "'": "'", '"': '"', "{": "}", "(": ")", "<": ">"}
        tags = tags.get(event.text())
        if tags is not None:
            cursor = self.textCursor()
            p = cursor.position()
            self.insertPlainText(tags)
            cursor.setPosition(p)
            self.setTextCursor(cursor)
    def __init__(self, parent = None):
        super(TextEdit,self).__init__(parent)
        self.setPlaceholderText("Start typing...")
        self.highlighter = Highlighter(self.document())
        self.setContextMenuPolicy(False)
        self.verticalScrollBar().setStyleSheet("""
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
        self.horizontalScrollBar().setStyleSheet("""
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
