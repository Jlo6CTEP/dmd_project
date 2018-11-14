import sys
import task_list
from PyQt5.QtGui import QIcon

import query
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QScrollArea, QLabel, QPushButton, QComboBox, \
    QVBoxLayout, QHBoxLayout, QFrame


class MainWindow(QWidget):
    def __init__(self):
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

        task_label.setFrameShape(QFrame.Panel)
        task_scroll.setWidget(task_label)
        task_scroll.setWidgetResizable(True)
        task_layout.addWidget(task_scroll)
        task_frame.setFrameShape(QFrame.Panel)

        query_button = QPushButton('Do the Query')

        selector = QComboBox()
        selector.addItems(task_list.task.keys())
        task_label.setText(task_list.task[selector.currentText()])

        result_scroll = QScrollArea()
        result_label = QLabel()

        result_label.setFrameShape(QFrame.Panel)
        result_scroll.setWidget(result_label)
        result_scroll.setWidgetResizable(True)

        v_layout = QVBoxLayout()

        v_layout.addWidget(task_scroll)
        v_layout.addWidget(query_button)
        v_layout.addWidget(selector)
        v_layout.addWidget(result_scroll)

        v_layout.setStretchFactor(task_scroll, 1)
        v_layout.setStretchFactor(result_scroll, 3)

        query_button.clicked.connect(lambda: query.do_query(selector.currentText()))
        selector.currentIndexChanged.connect(lambda: task_label.setText(task_list.task[selector.currentText()]))

        self.setLayout(v_layout)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
