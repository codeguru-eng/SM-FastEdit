from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from form import *
class FE_ToolBar(QToolBar):
      def __init__(self, parent=None):
            super(FE_ToolBar, self).__init__(parent)
            self.setMovable(False)
            self.setStyleSheet("""
            QToolBar {
                  background: #333;
                  color: #fff;
                  border: none;
            }
            QPushButton {
                  background: #333;
                  border: none;
                  padding: 15px;
            }
            QPushButton:hover {
                  background: #555;
            }
            QPushButton:pressed {
                  background: #222;
            }
            QToolBar::separator {
 			height: 4px;
 			background: #333;
 		}
            """)
