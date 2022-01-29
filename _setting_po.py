import sqlite3

from PIL.ImageColor import getcolor
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QMainWindow, QFileDialog

from uis.setting_ui import Ui_MainWindow


class Setting(QMainWindow, Ui_MainWindow):
    def __init__(self, previ=None):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        self.last_window = previ
        self.ok_for_music = True
        self.up_cl = True
        # узнать данные, т.е. путь к аудиофайлу, цвет текста и цвет фона
        net = sqlite3.connect('db/dls_setting.sqlite')
        ku = net.cursor()
        dannie = ku.execute("SELECT * FROM ne_ozhidanno_i_priatno").fetchall()
        for put, calor, bkgr in dannie:
            self.pit = put
            self.calor = calor
            self.bkgr = bkgr
        net.close()
        self.update_all()

    def initUI(self):
        # присваиване кнопок
        self.chance.clicked.connect(self.chance_pitan)
        self.chance_color.clicked.connect(self.color1)
        self.chance_background.clicked.connect(self.color2)

    # обновить все (путь к файлу, цвет текста, цвет фона) в текстовом формате
    def update_all(self):
        self.update_1()
        self.update_2()
        self.update_3()

    # доп. функция для перевода из HEX в PGB
    def hex(self, arg):
        return getcolor(arg, 'RGB')

    # обновление текста (путь к аудиофайлу)
    def update_1(self):
        self.putin.setText('Путь к аудиофайлу: \n' + self.pit)
        self.ok_for_music = True

    # обновление текста (цвет текста в PGB)
    def update_2(self):
        self.color.setText('Цвет текста: : ' + str(self.hex(self.calor)))
        self.update_for_color()

    # обновление теста (цвет заднего фона в PGB)
    def update_3(self):
        self.label_2.setText('Цвет заднего фона: ' + str(self.hex(self.bkgr)))
        self.update_for_color()

    # (46, 255, 185) очень, ОЧЕНЬ красивый цвет

    # обновить цвет окна (не основного)
    def update_for_color(self):
        self.up_cl = True
        self.setStyleSheet("color: {}".format(self.calor) + "; \n"
                                                            "background-color: {}".format(
            self.bkgr) + "; \n"
                         "")

    # изменить путь к файлу и перезапись в БД
    def chance_pitan(self):
        net = sqlite3.connect('db/dls_setting.sqlite')
        self.pit = QFileDialog.getOpenFileName(self, 'Выбрать аудиофайл', '',
                                               'Музыка (*.mp3);;Не музыка (*.mp3)')[0]
        if self.pit == "":
            return
        ku = net.cursor()
        self.pit = str(self.pit[2:])
        ku.execute("""UPDATE ne_ozhidanno_i_priatno
                            SET put = ?""", (self.pit,))
        net.commit()
        net.close()
        self.update_1()

    # изменить цвет текста и перезапись в БД
    def color1(self):
        color3 = QColorDialog.getColor()
        if not color3.isValid():
            return
        self.setStyleSheet("color: {}".format(color3.name()) + "; \n"
                                                               "background-color: {}".format(
            self.bkgr) + "; \n"
                         "")
        aaa = sqlite3.connect('db/dls_setting.sqlite')
        a1 = aaa.cursor()
        print(color3.name()[1:])

        a1.execute('''UPDATE ne_ozhidanno_i_priatno
SET color = ?''', (color3.name(),))
        self.calor = color3.name()
        aaa.commit()
        aaa.close()
        self.update_2()

    # изменить цвет фона и перезапись в БД
    def color2(self):
        color3 = QColorDialog.getColor()
        if not color3.isValid():
            return
        self.setStyleSheet("color: {}".format(self.calor) + "; \n"
                                                            "background-color: {}".format(
            color3.name()) + "; \n"
                             "")
        zzz = sqlite3.connect('db/dls_setting.sqlite')
        abv = zzz.cursor()
        abv.execute('''UPDATE ne_ozhidanno_i_priatno
    SET bkgr_color = ?''', (color3.name(),))
        self.bkgr = color3.name()
        zzz.commit()
        zzz.close()
        self.update_3()

    def closeEvent(self, event):
        if self.last_window:
            self.last_window.show()
            self.close()
