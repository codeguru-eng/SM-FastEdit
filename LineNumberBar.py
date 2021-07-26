from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

lineBarColor = QColor("#f1f1f1")
lineHighlightColor = QColor.fromRgbF(255,255,255,0.1)

class NumberBar(QWidget):
	def __init__(self, parent = None):
		super(NumberBar, self).__init__(parent)
		self.textArea = parent
		layout = QVBoxLayout()
		self.setLayout(layout)
		self.textArea.blockCountChanged.connect(self.update_width)
		self.textArea.updateRequest.connect(self.update_on_scroll)
		self.update_width('1')

	def update_on_scroll(self, rect, scroll):
		if self.isVisible():
			if scroll:
				self.scroll(0, scroll)
			else:
				self.update()

	def update_width(self, string):
		width = self.fontMetrics().width(str(string)) + 12
		if self.width() != width:
			self.setFixedWidth(width)

	def paintEvent(self, event):
		if self.isVisible():
			block = self.textArea.firstVisibleBlock()
			height = self.fontMetrics().height()
			number = block.blockNumber()
			painter = QStylePainter(self)
			painter.fillRect(event.rect(), lineBarColor)
			painter.drawRoundedRect(0, 0, event.rect().width(), event.rect().height(), 1, 1)
			font = painter.font()
			font.setPointSize(8)

			current_block = self.textArea.textCursor().block().blockNumber() + 1

			condition = True
			while block.isValid() and condition:
				block_geometry = self.textArea.blockBoundingGeometry(block)
				offset = self.textArea.contentOffset()
				block_top = block_geometry.translated(offset).top()
				number += 1

				rect = QRect(0, block_top, self.width() - 5, height)

				if number == current_block:
					font.setBold(True)
				else:
					font.setBold(False)

				painter.setFont(font)
				painter.drawText(rect, Qt.AlignmentFlag.AlignRight, '%i'%number)

				if block_top > event.rect().bottom():
					condition = False
				block = block.next()
			painter.end()