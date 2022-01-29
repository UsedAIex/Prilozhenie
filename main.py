import sys
import traceback
from datetime import datetime

import pytz
from PyQt5 import QtCore, QtMultimedia
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QInputDialog

from _setting_po import Setting
from help_for_db import Help_db
from helper import Helper
from uis.obrazech import Ui_MainWindow


class Proekt(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.helper = Help_db()
        self.initUI()
        self.player = QtMultimedia.QMediaPlayer()
        self.seting = Setting(self)
        self.po_umolch(self.seting.pit)
        self.update_all()
        # создаю таймер что бы выполнял функцию каждую секунду
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_all)
        self.timer2.start(1000)
        self.flag_for_isbr = False
        self.flag_for_istr = False
        self.time = QTimer(self)
        # проверка запущен был будильник до этого или нет
        self.budilnik_on()

    def initUI(self):
        self.mirov_time.clicked.connect(self.show_mirov_time)
        self.budiln.clicked.connect(self.budilinik)
        # ставлю картинку на кнопку
        self.setting_but.setIcon(QIcon('settings_icon_3.png'))
        self.add_isbr.clicked.connect(self.add_isbrann)
        self.setting_but.clicked.connect(self.setting)
        self.izbrann.clicked.connect(self.isbr)
        self.sh_istoria.clicked.connect(self.show_istoria)
        self.delete_istr.clicked.connect(self.delete)
        self.del_isbr.clicked.connect(self.delete_isbr)
        self.bud_off.clicked.connect(self.not_budilnik)

    # эта функция создана для того, чтобы обновлялись время, путь к аудиофайлу(для будильника), цвет теста
    # и заднего фона
    def update_all(self):
        self.update_color()
        self.otobr()
        self.otobrazhenie()
        self.po_umolch(self.seting.pit)
        self.update_time_now()

    # для отключения будильника вручную
    def not_budilnik(self):
        self.time.stop()
        self.bud_off.hide()
        self.bud_text.setText('Будильник не установлен')
        asistent = QMessageBox()
        asistent.setIcon(QMessageBox.Information)
        asistent.setText('Будильник отключен вручную')
        asistent.setWindowTitle('Отключение')
        asistent.setStyleSheet("color: {}".format(self.seting.calor) + "; \n"
                                                                       "background-color: {}".format(
            self.seting.bkgr) + "; \n"
                                "")
        asistent.exec_()
        self.helper.bu_nik_off()

    # для отображения времени по МСК(московскому)
    def update_time_now(self):
        time = str(datetime.now().time())[:8]
        self.time_nw.setText(time)

    # если будильник был запущен до этого
    def budilnik_on(self):
        if self.helper.bud_now()[2]:
            if self.helper.bud_now()[1] < 10:
                self.bud_text.setText(
                    'Будильник установлен на: ' + str(self.helper.bud_now()[0]) + ':0' + str(self.helper.bud_now()[1]))
            else:
                self.bud_text.setText(
                    'Будильник установлен на: ' + str(self.helper.bud_now()[0]) + ':' + str(self.helper.bud_now()[1]))
            self.time.timeout.connect(self.hello)
            self.time.start(1000)
        else:
            self.bud_off.hide()

    # обновляю цвет текста и фона(если оно было)
    def update_color(self):
        # проверяем были изменение цвета или нет
        if self.seting.up_cl:
            self.seting.up_cl = False
            self.setStyleSheet("color: {}".format(self.seting.calor) + "; \n"
                                                                       "background-color: {}".format(
                self.seting.bkgr) + "; \n"
                                    "")

    # изменяю путь к аудиофайлу (если оно было)
    def po_umolch(self, filename):
        if self.seting.ok_for_music:
            self.seting.ok_for_music = False
            media = QtCore.QUrl.fromLocalFile(filename)
            content = QtMultimedia.QMediaContent(media)
            self.player.setMedia(content)

    # Удаление истории полностью
    def delete(self):
        name, ok_pressed = QInputDialog.getText(self, "Очистить историю",
                                                "Нажми 'ДА' чтобы очистить всю историю?\n"
                                                "(Можешь написать любой текст, но это не поможет)")
        # если пользователь нажал "Отмена" то ничего не стирается
        if not ok_pressed:
            return
        self.helper.delete_db('istoria')
        # прячем таблицу (если она была открыта)
        uvedoml = QMessageBox()
        uvedoml.setIcon(QMessageBox.Information)
        uvedoml.setWindowTitle('История почищена')
        uvedoml.setText('Готово. История очищена')
        uvedoml.setStandardButtons(QMessageBox.Ok)
        uvedoml.setStyleSheet("color: {}".format(self.seting.calor) + "; \n"
                                                                      "background-color: {}".format(
            self.seting.bkgr) + "; \n"
                                "")
        uvedoml.exec_()

    # удаление всех избранных городов
    def delete_isbr(self):
        name, ok_pressed = QInputDialog.getText(self, "Очистить историю",
                                                "Нажми 'ДА' чтобы очистить все избранные города? \n"
                                                "(Можешь написать любой текст, но это не поможет)")
        # если пользователь нажал "Отмена" то ничего не стирается
        if not ok_pressed:
            return
        self.helper.delete_db('isbrannie')
        # прячем таблицу
        # выводим уведомление что все хорошо
        uvedoml_for_you = QMessageBox()
        uvedoml_for_you.setIcon(QMessageBox.Information)
        uvedoml_for_you.setWindowTitle('Ты оказался не избранным')
        uvedoml_for_you.setText('Готово')
        uvedoml_for_you.setStandardButtons(QMessageBox.Ok)
        uvedoml_for_you.setStyleSheet("color: {}".format(self.seting.calor) + "; \n"
                                                                              "background-color: {}".format(
            self.seting.bkgr) + "; \n"
                                "")
        uvedoml_for_you.exec_()

    # для отображения настроек
    def setting(self):
        self.seting.show()
        self.hide()

    # для добавления избранных
    def add_isbrann(self):
        country, ok_pressed = QInputDialog.getItem(
            self, "Избранный", "Какую страну добавить в избранное?",
            (pytz.all_timezones), 1, True)
        if ok_pressed:
            # пока не будет выбранного города (или пока пользователь не нажмет 'отмена') окно будет всплывать
            while country not in pytz.all_timezones:
                country, ok_pressed = QInputDialog.getItem(
                    self, "Избранный", "Какую страну добавить в избранное?",
                    (pytz.all_timezones), 1, True)
            if ok_pressed:
                self.flag_for_isbr = True
                # если выбранный город есть в избранных то выводится уведомление и город не заносится в БД
                if self.helper.add_db('isbrannie', country) == "YES":
                    uvedoml = QMessageBox()
                    uvedoml.setIcon(QMessageBox.Information)
                    uvedoml.setWindowTitle('Невозможно добавить этот город в избранное')
                    uvedoml.setText('Этот город уже в избранных')
                    uvedoml.setStandardButtons(QMessageBox.Ok)
                    uvedoml.setStyleSheet("color: {}".format(self.seting.calor) + "; \n"
                                                                                  "background-color: {}".format(
                        self.seting.bkgr) + "; \n"
                                            "")
                    uvedoml.exec_()

    # отображение избранных стран
    def otobr(self):
        db = self.helper.otobrazh('isbrannie')
        schet = True
        count = 1
        # происходит если в БД небыло ни одного избранного города/часового пояса
        if not bool(db):
            self.izbr_str_1.setText('----------')
            self.izbr_time_1.setText('----------')
            self.izbr_str_2.setText('----------')
            self.izbr_time_2.setText('----------')
        else:
            for is_id1, id_str1, country1 in db[::-1]:
                if count == 3:
                    break
                if schet:
                    self.izbr_str_1.setText(country1)
                    now = str(datetime.now(pytz.timezone(country1)).time())[:8]
                    self.izbr_time_1.setText(now)
                    schet = False
                elif not schet:
                    self.izbr_str_2.setText(country1)
                    now = str(datetime.now(pytz.timezone(country1)).time())[:8]
                    self.izbr_time_2.setText(now)
                    schet = True
                count += 1
        self.helper.con.close()

    # показывать все избранные пользователем страны в отдельном окне
    def isbr(self):
        self.help_to_me = Helper(self)
        self.help_to_me.show()
        # для перезаписи csv и корректного отображения
        self.help_to_me.write_isbr()
        self.hide()

    # просмотр истории в отдельном окне
    def show_istoria(self):
        self.help_to_me = Helper(self)
        self.help_to_me.show()
        # для перезаписи csv и корректного отображения
        self.help_to_me.write_istr()
        self.hide()

    # отображение последних 3 просмотренных городов
    def otobrazhenie(self):
        se = self.helper.otobrazh("istoria")
        count = 1
        # происходит если ничего не было в БД
        if not bool(se):
            self.perv_strana.setText('----------')
            self.perv_time.setText('----------')
            self.vtor_str.setText('----------')
            self.vtor_time.setText('----------')
            self.tret_str.setText('----------')
            self.tret_time.setText('----------')
        else:
            for id_str, country, data in se[::-1]:
                if count == 4:
                    break
                else:
                    if count == 1:
                        self.perv_strana.setText(country)
                        now = str(datetime.now(pytz.timezone(country)).time())[:8]
                        self.perv_time.setText(now)
                    elif count == 2:
                        self.vtor_str.setText(country)
                        now = str(datetime.now(pytz.timezone(country)).time())[:8]
                        self.vtor_time.setText(now)
                    elif count == 3:
                        self.tret_str.setText(country)
                        now = str(datetime.now(pytz.timezone(country)).time())[:8]
                        self.tret_time.setText(now)
                count += 1
        self.helper.con.close()

    # показать время в любом городе
    def show_mirov_time(self):
        country, ok_pressed = QInputDialog.getItem(
            self, "Выберите город", "Выберете город, в котором хотите посмотреть время",
            (pytz.all_timezones), 1, True)
        if ok_pressed:
            while country not in pytz.all_timezones:
                country, ok_pressed = QInputDialog.getItem(
                    self, "Выберите город", "Выберете город, в котором хотите посмотреть время",
                    (pytz.all_timezones), 1, True)
            if ok_pressed:
                self.flag_for_istr = True
                self.helper.add_db('istoria', country)

    # поставить будильник
    def budilinik(self):
        time, ok_pressed = QInputDialog.getText(
            self, "(Установите) Будильник", "Во сколько вас подревожить? \nФормат: HH(любой ОДИН символ)MM)")
        if ok_pressed:
            val = validate_time(time)
            while val != 'ok':
                time, ok_pressed = QInputDialog.getText(
                    self, "Введите время", str(val))
                # реализовывается выход из программы если пользователь не хотел ставить будильник
                if not ok_pressed:
                    return
                val = validate_time(time)
        else:
            return
        if len(time) == 4:
            hour = int(str(time)[0:1])
            mini = int(str(time)[2:5])
        else:
            hour = int(str(time)[0:2])
            mini = int(str(time)[3:5])
        # если минут < 10 приписываем 0 для правильного отображения
        if mini <= 10:
            mini = '0' + str(mini)
        else:
            mini = str(mini)
        self.bud_text.setText('Будильник установлен на: ' + str(hour) + ':' + mini)
        # записывается в БД часы и минуты
        self.helper.budilnik(hour, mini, True)
        # создаем таймер для проверки ...
        self.time.timeout.connect(self.hello)
        self.time.start(1000)
        self.bud_off.show()

    # совпадает выставленное время пользователем с текущим
    def hello(self):
        hou, mini, uslovie = self.helper.bud_now()
        now_h = datetime.now().hour
        now_m = datetime.now().minute
        if now_h == hou:
            if now_m == mini:
                self.time.stop()
                self.player.play()
                name = QMessageBox()
                name.setIcon(QMessageBox.NoIcon)
                name.setWindowTitle('Прозвучал будильник')
                name.setText('Сам думай выключать или нет')
                name.setStandardButtons(QMessageBox.Ok)
                name.setStyleSheet("color: {}".format(self.seting.calor) + "; \n"
                                                                           "background-color: {}".format(
                    self.seting.bkgr) + "; \n"
                                        "")
                name.exec_()
                self.player.stop()
                self.bud_text.setText('Будильник не установлен')
                self.helper.bu_nik_off()
                self.bud_off.hide()

    # проверка на правильность времени


def validate_time(time):
    try:
        if len(str(time)) == 4:
            print(time[0:1])
            if int(time[0:1]) > 23:
                print(34)
                return "Неверный формат, попробуйте снова"
            elif int(time[2:4]) > 59:
                print(56)
                return "Неверный формат, попробуйте снова"
            else:
                print(time[3:5])
                return 'ok'
        elif len(str(time)) != 5:
            return "Неверный формат, попробуйте снова"
        else:
            if int(time[0:2]) > 23:
                return "Неверный формат, попробуйте снова"
            elif int(time[3:5]) > 59:
                return "Неверный формат, попробуйте снова"
            else:
                return 'ok'
    except ValueError:
        return "Неверный формат, попробуйте снова"


# для ловли ошибок
def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error catched!:")
    print("error message:\n", tb)
    msgbox = QMessageBox()
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setText("Произошла непредвиденная серьезная ошибка. Больше так не делай ;)")
    msgbox.setWindowTitle("Пасхалка (это ошибка гений)")
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.exec_()


sys.excepthook = excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Proekt()
    ex.show()
    sys.exit(app.exec())
