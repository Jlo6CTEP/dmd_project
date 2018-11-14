import ctypes
import sys
import task_list
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import query
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QScrollArea, QLabel, QPushButton, QComboBox, \
    QVBoxLayout, QHBoxLayout, QFrame


class MainWindow(QWidget):
    def __init__(self):

        my_app_id = 'InnoUI.DMD_project.ez_A_for_course.101'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

        super().__init__()
        self.screen_size = QDesktopWidget().screenGeometry()
        self.resize(self.screen_size.width() / 2, self.screen_size.height() / 2)
        self.setWindowIcon(QIcon("../images/db"))
        self.setWindowTitle("Course DB project")
        self.update_ui()

    def update_ui(self):
        task_frame = QFrame()
        task_scroll = QScrollArea()
        task_label = QLabel()
        task_layout = QHBoxLayout()

        task_label.setWordWrap(True)
        task_label.setFrameShape(QFrame.Panel)
        task_scroll.setWidget(task_label)
        task_scroll.setWidgetResizable(True)
        task_layout.addWidget(task_scroll)
        task_frame.setFrameShape(QFrame.Panel)

        query_button = QPushButton('Do the Query')

        selector = QComboBox()
        selector.addItems(task_list.task.keys())

        task_label.setText(task_list.task[selector.currentText()])
        task_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        result_scroll = QScrollArea()
        result_label = QLabel()

        result_label.setFrameShape(QFrame.Panel)
        result_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        result_scroll.setWidget(result_label)
        result_scroll.setWidgetResizable(True)

        v_layout = QVBoxLayout()

        v_layout.addWidget(task_scroll)
        v_layout.addWidget(query_button)
        v_layout.addWidget(selector)
        v_layout.addStretch()

        h_layout = QHBoxLayout()
        h_layout.addLayout(v_layout)
        h_layout.addWidget(result_scroll)
        h_layout.setStretchFactor(v_layout, 1)
        h_layout.setStretchFactor(result_scroll, 5)

        query_button.clicked.connect(lambda: query.do_query(selector.currentText()))
        selector.currentIndexChanged.connect(lambda: task_label.setText(task_list.task[selector.currentText()]))

        self.setLayout(h_layout)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
