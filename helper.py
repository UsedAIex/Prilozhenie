import csv
import sqlite3

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from _setting_po import Setting
from uis.for_csv import Ui_MainWindow


class Helper(QMainWindow, Ui_MainWindow):
    def __init__(self, first=None):
        self.last_winda = first
        super().__init__()
        self.setupUi(self)
        # обновление цвета
        self.color_update()
        self.for_color = QTimer()
        self.for_color.timeout.connect(self.color_update)
        self.for_color.start(1000)
        self.initUI()

    def initUI(self):
        self.chance.clicked.connect(self.chence)

    # для смены таблиц
    def chence(self):
        if self.is_istori:
            self.is_istori = False
            self.is_isnran = True
            self.write_isbr()
        elif self.is_isnran:
            self.is_istori = True
            self.is_isnran = False
            self.write_istr()

    # функция обновления цвета
    def color_update(self):
        color = Setting()
        color_text, backgroung = color.calor, color.bkgr
        self.setStyleSheet("color: {}".format(color_text) + "; \n"
                                                            "background-color: {}".format(
            backgroung) + "; \n"
                          "")

    # отображает данные в таблицу
    def loadtable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=';', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()

    # для записи данных в csv-файл из БД (история просмотра)
    def write_istr(self):
        self.is_istori = True
        self.is_isnran = False
        self.chance.setText('Сменить на \n"Посмотреть избранные"')
        self.label.setText('История')
        d_isb = sqlite3.connect("db/istr.sqlite")
        db = d_isb.cursor()
        dn = db.execute("SELECT * FROM istoria").fetchall()
        with open('cvs/for_proect_istr.csv', 'w',
                  newline='') as csvf:
            writer = csv.writer(
                csvf, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(('ID strani', "Strana", "Kogda smotrel (po msk)"))
            for id_str, country, data in dn[::-1]:
                writer.writerow((id_str, country, data))
        d_isb.close()
        self.loadtable('cvs/for_proect_istr.csv')

    # для записи данных в csv-файл из БД (избранные города)
    def write_isbr(self):
        self.is_istori = False
        self.is_isnran = True
        self.chance.setText('Сменить на \n"Посмотреть историю"')
        self.label.setText('Избранные страны')
        db_isbr = sqlite3.connect("db/istr.sqlite")
        dls = db_isbr.cursor()
        list_s_dann = dls.execute("SELECT * FROM isbrannie").fetchall()
        with open('cvs/for_proect_isbr.csv', 'w',
                  newline='') as csvf:
            writer = csv.writer(
                csvf, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(('ID isbrannoi strani', "ID strani", 'Strana'))
            for id_isbr, is_str, stra in list_s_dann[::-1]:
                writer.writerow((id_isbr + 1, is_str, stra))
        self.loadtable('cvs/for_proect_isbr.csv')

    def closeEvent(self, event):
        if self.last_winda:
            self.last_winda.show()
            self.close()
    # самый страшный файл (по моему мнению)
