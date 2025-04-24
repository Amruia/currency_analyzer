from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class WidgetGrafu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(5, 3)) # Mensi graf
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.figure.tight_layout() # Aby se vesly popisky

    def vykresli_data(self, dataframe, mena_od, mena_do):
        self.ax.clear()
        if not dataframe.empty:
            self.ax.plot(dataframe.index, dataframe['Kurz'], marker='o', linestyle='-')
            self.ax.set_title(f'Historický vývoj kurzu {mena_od}/{mena_do}')
            self.ax.set_xlabel('Datum')
            self.ax.set_ylabel('Kurz')
            self.ax.grid(True)

            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            self.figure.autofmt_xdate()
        else:
            self.ax.set_title('Žádná data k zobrazení')
            self.ax.set_xlabel('Datum')
            self.ax.set_ylabel('Kurz')
        self.figure.tight_layout()
        self.canvas.draw()