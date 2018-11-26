import ctypes
import sys
import task_list
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from query import do_query
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QScrollArea, QLabel, QPushButton, QComboBox, \
    QVBoxLayout, QHBoxLayout, QFrame, QMainWindow, QDockWidget, QFormLayout, QLineEdit, QSizePolicy

from sys import platform

input_labels = [['color', 'sign letters'], ['date'], [], [], ['date'], [], [], ['date'], [], []]


class MainWindow(QMainWindow):
    def __init__(self):
        if sys.platform != 'linux':
            my_app_id = 'InnoUI.DMD_project.ez_A_for_course.101'  # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

        super().__init__()
        self.screen_size = QDesktopWidget().screenGeometry()
        self.resize(self.screen_size.width() / 2, self.screen_size.height() / 2)
        self.setWindowIcon(QIcon("../images/db"))
        self.setWindowTitle("Course DB project")
        self.docks = [QDockWidget("Query {}".format(str(x + 1))) for x in range(10)]
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

        f = QMainWindow()

        for x in self.docks:
            f.addDockWidget(Qt.TopDockWidgetArea, x)
            v_dock_layout = QVBoxLayout()
            dock_label = QLabel()
            dock_scroll = QScrollArea()
            dock_label.setText(task_list.task[x.windowTitle()])
            dock_label.setWordWrap(True)
            dock_scroll.setWidget(dock_label)
            dock_scroll.setWidgetResizable(True)

            frame_layout = QFormLayout()

            v_dock_layout.addWidget(dock_scroll)
            v_dock_layout.addWidget(QLabel("Inputs:"))
            v_dock_layout.addLayout(frame_layout)

            docked_widget = QWidget()
            docked_widget.setLayout(v_dock_layout)
            x.setWidget(docked_widget)
            x.hide()
        self.docks[0].show()

        docks_inputs = [[] for x in range(10)]
        self.fill_dockables(docks_inputs)

        f.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        v_layout_left = QVBoxLayout()
        v_layout_left.addWidget(query_button)
        v_layout_left.addWidget(selector)
        v_layout_left.addStretch()

        v_layout_right = QVBoxLayout()
        v_layout_right.addWidget(f)
        v_layout_right.addWidget(result_scroll)

        frame_left = QFrame()
        frame_left.setLayout(v_layout_left)
        frame_left.setFrameShape(QFrame.Panel)
        frame_right = QFrame()
        frame_right.setLayout(v_layout_right)
        frame_right.setFrameShape(QFrame.Panel)

        h_layout = QHBoxLayout()
        h_layout.addWidget(frame_left)
        h_layout.addWidget(frame_right)
        h_layout.setStretchFactor(frame_left, 1)
        h_layout.setStretchFactor(frame_right, 5)

        # query_button.clicked.connect(lambda: query.do_query(selector.currentText()))
        query_button.clicked.connect(lambda: self.send_request(docks_inputs))
        selector.currentIndexChanged.connect(lambda: self.change_dock(selector.currentText()))

        main_widget = QWidget()
        main_widget.setLayout(h_layout)
        self.setCentralWidget(main_widget)

        self.show()

    def change_dock(self, name):
        index = [x.windowTitle() for x in self.docks].index(name)
        for x in self.docks:
            x.hide()
        self.docks[index].show()

    def fill_dockables(self, inputs):
        for x in range(10):
            layout = self.docks[x].widget().layout().itemAt(2).layout()
            if not input_labels[x]:
                self.docks[x].widget().layout().itemAt(1).widget().hide()
            for f in range(len(input_labels[x])):
                inputs[x].append([QLabel(input_labels[x][f]), QLineEdit()])
                layout.addRow(*inputs[x][f])

    def send_request(self, inputs):
        tgt_dock = [(self.docks[x].windowTitle(), x) for x in range(len(self.docks)) if not self.docks[x].isHidden()][0]
        do_query(tgt_dock[0], ([x[1].text() for x in inputs[tgt_dock[1]]]))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
