from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

class WidgetGrafu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(5, 3)) # Menší výchozí velikost grafu
        self.canvas = FigureCanvas(self.figure) # Plátno pro vykreslení grafu
        self.ax = self.figure.add_subplot(111) # Jeden podgraf (subplot) na celé ploše

        layout = QVBoxLayout()
        layout.addWidget(self.canvas) # Vložíme plátno do layoutu
        self.setLayout(layout)
        self.figure.tight_layout() # Automaticky upraví rozložení, aby se vešly popisky

    def vykresli_data(self, dataframe, mena_od, mena_do):
        self.ax.clear() # Vyčistíme starý graf
        if not dataframe.empty:
            # Vykreslení čáry s body
            self.ax.plot(dataframe.index, dataframe['Kurz'], marker='o', linestyle='-')
            self.ax.set_title(f'Historický vývoj kurzu {mena_od}/{mena_do}') # Titulek grafu
            self.ax.set_xlabel('Datum') # Popisek osy X
            self.ax.set_ylabel('Kurz')  # Popisek osy Y
            self.ax.grid(True) # Zobrazí mřížku v grafu

            # Formátování data na ose X
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            self.figure.autofmt_xdate() # Automatické natočení datumových popisků
        else:
            # Pokud nejsou data, nastavíme základní popisky bez dat
            self.ax.set_title('Žádná data k zobrazení')
            self.ax.set_xlabel('Datum')
            self.ax.set_ylabel('Kurz')
        self.figure.tight_layout() # Upraví rozložení
        self.canvas.draw() # Aktualizuje vykreslení grafu
