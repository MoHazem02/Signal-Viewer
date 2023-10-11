from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QPushButton, QScrollBar
import wfdb
import os

class TimeLine(QtCore.QObject):
    frameChanged = QtCore.pyqtSignal(int)

    def __init__(self, interval=60, loopCount=1, parent=None):
        super(TimeLine, self).__init__(parent)
        self._startFrame = 0
        self._endFrame = 0
        self._loopCount = loopCount
        self._timer = QtCore.QTimer(self, timeout=self.on_timeout)
        self._counter = 0
        self._loop_counter = 0
        self.setInterval(interval)

    def on_timeout(self):
        if self._startFrame <= self._counter < self._endFrame:
            self.frameChanged.emit(self._counter)
            self._counter += 1
        else:
            self._counter = 0
            self._loop_counter += 1

        if self._loopCount > 0: 
            if self._loop_counter >= self.loopCount():
                self._timer.stop() 

    def setLoopCount(self, loopCount):
        self._loopCount = loopCount

    def loopCount(self):
        return self._loopCount

    interval = QtCore.pyqtProperty(int, fget=loopCount, fset=setLoopCount)

    def setInterval(self, interval):
        self._timer.setInterval(interval)

    def interval(self):
        return self._timer.interval()

    interval = QtCore.pyqtProperty(int, fget=interval, fset=setInterval)

    def setFrameRange(self, startFrame, endFrame):
        self._startFrame = startFrame
        self._endFrame = endFrame

    @QtCore.pyqtSlot()
    def start(self):
        self._counter = 0
        self._loop_counter = 0
        self._timer.start()

    @QtCore.pyqtSlot()
    def pause(self):
        self._timer.stop()


class Gui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        pg.setConfigOption('background', 0.95)
        pg.setConfigOptions(antialias=True)
        self.plot = pg.PlotWidget()
        self.plot.setAspectLocked(lock=True, ratio=0.01)
        self.plot.setYRange(-3, 3)
        widget_layout = QtWidgets.QVBoxLayout(self)
        widget_layout.addWidget(self.plot)

        self._plots = [self.plot.plot([], [], pen=pg.mkPen(color=color, width=2)) for color in ("g", "r", "y")]
        self._timeline = TimeLine(loopCount=0, interval=10)
        self._timeline.setFrameRange(0, 720)
        self._timeline.frameChanged.connect(self.generate_data)
        
        File_Path, _ = QFileDialog.getOpenFileName(None, "Browse Signal", "D:\Education\Digital Signal Processing\Tasks\Task 1\Signal-Viewer\Signals", "All Files (*)")
        Record = wfdb.rdrecord(os.path.splitext(File_Path)[0])
        self.Y_Coordinates = list(Record.p_signal[:, 0])
        self.X_Coordinates = list(np.arange(len(self.Y_Coordinates)))

        self.play_pause_button = QPushButton("Play/Pause", self)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        widget_layout.addWidget(self.play_pause_button)

        self.hide_unhide_button = QPushButton("Hide/Unhide Signal", self)
        self.hide_unhide_button.clicked.connect(self.toggle_hide_unhide)
        widget_layout.addWidget(self.hide_unhide_button)

        self.remove_signal_button = QPushButton("Remove Signal", self)
        self.remove_signal_button.clicked.connect(self.remove_signal)
        widget_layout.addWidget(self.remove_signal_button)

        self.scrollbar = QScrollBar(QtCore.Qt.Horizontal, self)
        self.scrollbar.setMinimum(0)
        self.scrollbar.setMaximum(len(self.X_Coordinates) - 720)
        self.scrollbar.valueChanged.connect(self.on_scroll)
        widget_layout.addWidget(self.scrollbar)
        
        self._timeline.start()

    def plot_data(self, data):
        for plt, val in zip(self._plots, data):
            plt.setData(range(len(val)), val)

    @QtCore.pyqtSlot(int)
    def generate_data(self, i):
        self.plot_data([self.X_Coordinates[i:i+720], self.Y_Coordinates[i:i+720]])

    def toggle_play_pause(self):
        if self._timeline._timer.isActive():
            self._timeline.pause()
        else:
            self._timeline.start()

    def toggle_hide_unhide(self):
        for plt in self._plots:
            plt.setVisible(not plt.isVisible())

    def remove_signal(self):
        for plt in self._plots:
            self.plot.removeItem(plt)
        self._plots = []

    def on_scroll(self, value):
        self._timeline.pause()
        self._timeline.setFrameRange(value, value + 720)
        self.generate_data(value)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gui = Gui()
    gui.show()
    sys.exit(app.exec_())