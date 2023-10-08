import sys
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from pyqtgraph.Qt import QtCore


class LiveSignalPlot(QWidget):
    def __init__(self):
        super().__init__()

        # Create a layout for the widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a plot widget
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Set up the data buffer
        self.max_data_points = 100
        self.data = np.zeros(self.max_data_points)
        self.x_data = np.arange(self.max_data_points)

        # Create a plot curve
        self.plot_curve = self.plot_widget.plot(self.x_data, self.data)

        # Set up the timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)

    def update_plot(self):
        # Generate random data for demonstration
        new_data = np.random.normal()

        # Update the data buffer
        self.data[:-1] = self.data[1:]
        self.data[-1] = new_data

        # Update the plot curve data
        self.plot_curve.setData(self.x_data, self.data)

    def start_plotting(self, signal_data):
        self.data = np.array(signal_data)
        self.timer.start(100)  # Timer interval in milliseconds


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("Live Signal Browser")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create the live signal plot widget
        self.live_plot_widget = LiveSignalPlot()

        # Set up a layout for the central widget
        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.live_plot_widget)

        # Create a push button to open a signal file
        self.open_button = QPushButton("Open Signal")
        layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_signal_file)

    def open_signal_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open Signal File", "", "Text Files (*.txt)")

        if file_path:
            with open(file_path, "r") as file:
                signal_data = file.readlines()
                signal_data = [float(data.strip()) for data in signal_data]

            self.live_plot_widget.start_plotting(signal_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())