import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from functions import new_user, check_in_db


class MainWindow(QMainWindow):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        self.setFixedSize(612, 600)
        uic.loadUi('welcome_window.ui', self)
        self.welcome.clicked.connect(self.open_entry_form)

    def open_entry_form(self):
        self.hide()
        self.app_context["entry"].show()


class Entry(QMainWindow):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        self.setFixedSize(600, 420)
        uic.loadUi('entry_window.ui', self)
        self.open_registration_window.clicked.connect(self.open_registration_form)
        self.open_market.clicked.connect(self.work_in_db)

    def open_registration_form(self):
        self.hide()
        self.app_context["registration"].show()

    def open_market_for_entry_form(self):
        self.hide()
        self.app_context["market"].show()

    def work_in_db(self):
        flag = check_in_db(self.login_entry.text(), self.password_entry.text())
        if flag:
            self.open_market_for_entry_form()
        else:
            if self.login_entry.text() != '':
                self.error_label.setText('Такого пользователя не существует или не верный пароль!')
            elif self.login_entry.text() == '':
                self.error_label.setText('Введите логин!')


class Registration(QMainWindow):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        self.setFixedSize(600, 420)
        uic.loadUi('registration_form_main_window.ui', self)
        self.login_register.sizeHint()
        self.password_register.sizeHint()
        self.password_register_check.sizeHint()
        self.registration_button.clicked.connect(self.check_login_and_password)
        self.open_entry_window.clicked.connect(self.open_entry_form_for_registration)

    def open_entry_form_for_registration(self):
        self.hide()
        self.app_context["entry"].show()

    def open_market(self):
        self.hide()
        self.app_context["market"].show()

    def check_login_and_password(self):
        password = len(self.password_register.text())
        if 3 <= len(self.login_register.text()) <= 12 and self.login_register.text().isalpha():
            if 8 <= password <= 16:
                if self.password_register.text() == self.password_register_check.text():
                    check = new_user(self.login_register.text(), self.password_register.text())
                    if check:
                        self.open_market()
                    else:
                        self.error_label.setText('Такой пользователь уже зарегистрирован, попробуйте еще раз!')
                else:
                    self.error_label.setText('У вас не совпадают пароли, попробуйте еще раз!')
            else:
                if password < 8:
                    self.error_label.setText('У вас слишком короткий пароль, попробуйте еще раз!')
                else:
                    self.error_label.setText('У вас слишком длинный пароль, попробуйте еще раз!')
        else:
            if len(self.login_register.text()) < 3:
                if self.login_register.text() != '':
                    self.error_label.setText('У вас слишком короткий логин, попробуйте еще раз!')
                else:
                    self.error_label.setText('Введите логин!')
            elif len(self.login_register.text()) > 12:
                self.error_label.setText('У вас слишком длинный логин, попробуйте еще раз!')
            elif not self.login_register.text().isalpha():
                self.error_label.setText('У вас есть цифры в логине, попробуйте еще раз!')


class Market(QMainWindow):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        self.setFixedSize(700, 650)
        uic.loadUi('market_window.ui', self)
        self.names = ['Шоколадный торт', 'Ягодная тарталетка', 'Конфеты ручной работы', 'Клубничные пирожные']
        self.counts = [self.chocolate_cake_count, self.tartlet_count, self.candies_count, self.cupcakes_count]
        self.prices = [3000, 250, 25, 400]
        self.bin_button.clicked.connect(self.open_bin)

    def open_bin(self):
        open("score.txt", 'w').close()
        score = open("score.txt", 'w', encoding='utf-8')
        if int(self.chocolate_cake_count.value()) > 0 or int(self.tartlet_count.value()) > 0 or \
                int(self.candies_count.value()) > 0 or int(self.cupcakes_count.value()) > 0:
            score.write('Ваш заказ')
            score.write('\n')
            mainprice = 0

            for (elem, value, price) in zip(self.names, self.counts, self.prices):
                if value.value() > 0:
                    score.write(f'{elem}-----{value.value()} шт.-----{int(value.value()) * price} руб.')
                    score.write('\n')
                    mainprice += int(value.value()) * price

            score.write('\n')
            score.write(f'Итого: {mainprice} руб.')
        else:
            score.write('Вы ничего не заказали!')
        score.close()
        self.hide()
        self.app_context["bin"].show()


class Bin(QMainWindow):
    def __init__(self, app_context):
        super().__init__()
        self.app_context = app_context
        self.setFixedSize(500, 500)
        uic.loadUi('bin_window.ui', self)
        self.market_button.clicked.connect(self.open_market_for_bin)
        self.score_file = open('score.txt', 'r', encoding='utf-8')
        self.read_from_file()

    def open_market_for_bin(self):
        self.hide()
        self.app_context["market"].show()

    def read_from_file(self):
        score_lines = self.score_file.read().splitlines()
        self.all_products.setPlainText('')
        for elem in score_lines:
            self.all_products.appendPlainText(elem)
        self.score_file.close()



if __name__ == '__main__':
    app_context = {}
    app = QApplication(sys.argv)
    main_window = MainWindow(app_context)
    registration = Registration(app_context)
    entry = Entry(app_context)
    market = Market(app_context)
    bin = Bin(app_context)
    app_context["main_window"] = main_window
    app_context["registration"] = registration
    app_context["entry"] = entry
    app_context["market"] = market
    app_context["bin"] = bin
    main_window.show()
    sys.exit(app.exec())
