#!/usr/bin/env python

import sys
from board import Board, Direction

from PyQt4.QtCore import *
from PyQt4.QtGui import *

DMAP = {
    Qt.Key_Up   : Direction.up   ,
    Qt.Key_Down : Direction.down ,
    Qt.Key_Left : Direction.left ,
    Qt.Key_Right: Direction.right,
}

class BoardWidget(QWidget):
    def __init__(self, board, parent=None):
        super(BoardWidget, self).__init__(parent)
        self.board = board

        layout = QGridLayout()
        self.labels = []
        for r, row in enumerate(board.data):
            row_labels = []
            for c, col in enumerate(row):
                label = QLabel()
                row_labels.append(label)
                layout.addWidget(label, r, c)
            self.labels.append(row_labels)
        self.setLayout(layout)

        self.update()

    def update(self):
        for r, row in enumerate(self.board.data):
            for c, col in enumerate(row):
                self.labels[r][c].setText(str(col) if col else '')

    def keyPressEvent(self, event):
        key = event.key()
        if key in DMAP:
            event.accept()
            self.board.move(DMAP[key])
            self.update()
        elif key == Qt.Key_Escape:
            event.accept()
            self.close()
        elif key == Qt.Key_F:
            event.accept()
            self.board.flip_left_right()
            self.update()
        elif key == Qt.Key_R:
            event.accept()
            self.board.rows_to_cols()
            self.update()
        elif key == Qt.Key_N:
            event.accept()
            self.board.initialize()
            self.update()
        else:
            event.ignore()



def main():
    app = QApplication(sys.argv)
    b = Board()
    bw = BoardWidget(b)
    bw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
