import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator

from datetime import date

import dbConnector as db


class AddWindow(QtWidgets.QWidget):
    def __init__(self, parent, obj_name,  window_title):
        super().__init__()
        self.widgets = []
        self.parent = parent
        self.setObjectName(obj_name)
        self.setWindowTitle(window_title)

        self.general_ui_setup()

    def general_ui_setup(self):
        self.lnedit_name = QtWidgets.QLineEdit()
        self.lnedit_name.setPlaceholderText(f'*Enter {self.windowTitle().lower()} name')

        self.widgets.append(self.lnedit_name)
        self.lnedit_name.setProperty('mandatoryField',True)

        self.btn_clear_all = QtWidgets.QPushButton('clear all')
        self.btn_clear_all.setObjectName('btn_reset')
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
    def __init__(self, parent, obj_name,  window_title):
        super().__init__(parent,obj_name,  window_title)
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
        phone = ''.join([digit for digit in self.lnedit_phone.text().strip() if digit.isdigit()])
        email = self.lnedit_email.text().strip()

        db.add_client(name, phone, email)
        print('added')


class RentalAddWindow(AddWindow):

    def __init__(self,parent,obj_name,  window_title):
        super().__init__(parent,obj_name,  window_title)
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
            client_id = db.get_obj_single(client_name).client_id
        except Exception as ex:
            print(f'client_id [ERROR]: {ex}')

        description = self.text_description.toPlainText().strip()
        status = bool(self.rental_status.currentIndex())

        db.add_rental(rent_name,client_id,description,rent_date,status)
        print('added')


class CategoryAddWindow(AddWindow):
    def __init__(self,parent,obj_name,  window_title):
        super().__init__(parent,obj_name,  window_title)
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


class ItemAddWindow(AddWindow):
    def __init__(self,parent,obj_name, window_title):
        super().__init__(parent,obj_name, window_title)
        self.widgets_setup()

    def widgets_setup(self):
        self.cbox_category = QtWidgets.QComboBox()

        # ___________TESTING CODE___________
        data_loader = db.DataLoader(db.CategoryDB)
        self.objects_for_cbox = data_loader.load_all()
        for i, el in enumerate(self.objects_for_cbox):
            self.cbox_category.insertItem(i, el.category_name, el)

        # ___________TESTING CODE___________

        self.lnedit_amount = QtWidgets.QLineEdit()
        self.lnedit_amount.setPlaceholderText('Enter amount')
        self.lnedit_amount.setValidator(QIntValidator())
        self.widgets.append(self.lnedit_amount)

        self.layout_2.addWidget(self.cbox_category)
        self.layout_2.addWidget(self.lnedit_amount)

        self.layout_main.addLayout(self.layout_1)
        self.layout_main.addLayout(self.layout_2)
        self.layout_main.addLayout(self.layout_4)

        self.setLayout(self.layout_main)

    # _____________________________ functions _____________________________________
    def btn_save_clicked(self):
        name = self.lnedit_name.text().strip().capitalize()
        cat_item = self.cbox_category.itemData(self.cbox_category.currentIndex())
        amount = int(self.lnedit_amount.text().strip())

        db.add_item(name, cat_item.category_id,amount)
        print('added')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ItemAddWindow('Item')
    window.show()
    sys.exit(app.exec_())

