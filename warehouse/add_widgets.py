from PyQt5 import QtWidgets

from datetime import date
import dbConnector as db


class AddWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.widgets = []
        self.setWindowTitle('Add Window')

        self.common_widget_setup()

    def common_widget_setup(self):
        self.lnedit_name = QtWidgets.QLineEdit()
        self.lnedit_name.setPlaceholderText(f'Enter name')
        self.widgets.append(self.lnedit_name)

        self.btn_clear_all = QtWidgets.QPushButton('clear all')
        self.btn_clear_all.setObjectName('btn_clear_all')
        self.btn_clear_all.clicked.connect(self.btn_clear_all_clicked)
        self.btn_save = QtWidgets.QPushButton('Save')
        self.btn_save.clicked.connect(self.btn_save_clicked)

        self.layout_1 = QtWidgets.QHBoxLayout()
        self.layout_2 = QtWidgets.QHBoxLayout()
        self.layout_3 = QtWidgets.QHBoxLayout()
        self.layout_4 = QtWidgets.QHBoxLayout()

        self.layout_1.addWidget(self.lnedit_name)

        self.layout_4.addWidget(self.btn_clear_all)
        self.layout_4.addWidget(self.btn_save)

        self.layout_main = QtWidgets.QVBoxLayout()

    def btn_clear_all_clicked(self):
        for widget in self.widgets:
            widget.clear()

    def btn_save_clicked(self):
        raise NotImplementedError('Should be redefined in subclass ')


class ClientAddWindow(AddWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Client')
        self.widgets_setup()

    def widgets_setup(self):
        self.lnedit_phone = QtWidgets.QLineEdit()
        self.lnedit_phone.setPlaceholderText('Enter phone number')

        self.lnedit_email = QtWidgets.QLineEdit()
        self.lnedit_email.setPlaceholderText('Enter email')

        self.layout_2.addWidget(self.lnedit_phone)
        self.layout_3.addWidget(self.lnedit_email)

        self.layout_main.addLayout(self.layout_1)
        self.layout_main.addLayout(self.layout_2)
        self.layout_main.addLayout(self.layout_3)
        self.layout_main.addLayout(self.layout_4)

        self.setLayout(self.layout_main)

    def btn_save_clicked(self):
        name = self.lnedit_name.text().strip().capitalize()
        # todo валидация телефона и имейла
        phone = ''.join([digit for digit in self.lnedit_phone.text().strip() if digit.isdigit()])
        email = self.lnedit_email.text().strip()

        db.add_client(name, phone, email)
        print('added')


class RentalAddWindow(AddWindow):

    def __init__(self):
        super().__init__()
        self.widgets_setup()

    def widgets_setup(self):
        self.lnedit_client = QtWidgets.QLineEdit()
        self.lnedit_client.setPlaceholderText('Enter client name')
        self.widgets.append(self.lnedit_client)

        self.text_description = QtWidgets.QTextEdit()
        self.text_description.setPlaceholderText('Enter Description')
        self.widgets.append(self.text_description)

        self.date_widget = QtWidgets.QDateEdit()
        self.date_widget.setDate(date.today())

        self.rental_status = QtWidgets.QComboBox()
        self.rental_status.addItems(['False', 'True'])

        self.layout_1.addWidget(self.date_widget)
        self.layout_2.addWidget(self.lnedit_client)
        self.layout_2.addWidget(self.rental_status)
        self.layout_3.addWidget(self.text_description)

        self.layout_main.addLayout(self.layout_1)
        self.layout_main.addLayout(self.layout_2)
        self.layout_main.addLayout(self.layout_3)
        self.layout_main.addLayout(self.layout_4)

        self.setLayout(self.layout_main)
# _____________________________ functions _____________________________________


    def btn_save_clicked(self):
        rent_name = self.lnedit_name.text().strip().capitalize()
        rent_date = str(self.date_widget.date().toPyDate())

        client_name = self.lnedit_client.text().strip().capitalize()
        client_id = None
        try:
            client_id = db.get_client_model(client_name).client_id
        except Exception as ex:
            print(f'client_id [ERROR]: {ex}')

        description = self.text_description.toPlainText().strip()
        status = bool(self.rental_status.currentIndex())

        db.add_rental(rent_name,client_id,description,rent_date,status)
        print('added')


class CategoryAddWindow(AddWindow):
    def __init__(self):
        super().__init__()
        self.widgets_setup()

    def widgets_setup(self):
        self.layout_main.addLayout(self.layout_1)
        self.layout_main.addLayout(self.layout_4)

        self.setLayout(self.layout_main)

    # _____________________________ functions _____________________________________
    def btn_save_clicked(self):
        name = self.lnedit_name.text().strip().capitalize()
        db.add_category(name)
        print('added')


def main():
    pass


if __name__ == '__main__':
    pass
