from PyQt5.QtCore import Qt

import models
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QAction, QDialog, QTableWidget, QVBoxLayout, QPushButton, \
    QHeaderView, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QTableWidgetItem, QComboBox


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('HAVAN - Sistema de Vendas')

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        file_menu = menubar.addMenu('Arquivo')
        cruds_menu = menubar.addMenu('Cadastros')
        process_menu = menubar.addMenu('Processos')
        about_menu = menubar.addMenu('Sobre')

        # file_menu action
        action_exit = QAction('Sair', self)
        action_exit.triggered.connect(self.close)

        file_menu.addAction(action_exit)

        # cruds menu actions
        action_department = QAction('Departamento', self)
        action_department.triggered.connect(self.open_department_list)
        action_employee = QAction('Funcionário', self)
        action_employee.triggered.connect(self.open_employee_list)
        action_marital_status = QAction('Estado civil', self)
        action_branch = QAction('Filial', self)
        cruds_menu.addAction(action_department)
        cruds_menu.addAction(action_employee)
        cruds_menu.addAction(action_marital_status)
        cruds_menu.addAction(action_branch)

        # about menu action
        action_info = QAction('Informações', self)
        action_info.triggered.connect(self.show_about_message)
        about_menu.addAction(action_info)

    def show_about_message(self):
        QMessageBox.about(self, "Sobre", "Sistema de vendas da Loja Havan")

    def open_department_list(self):
        form = DepartmentList(self)
        form.exec_()

    def open_employee_list(self):
        form = EmployeeList(self)
        form.exec_()


class DepartmentList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Listagem dos departamentos')
        self.resize(600, 400)

        self.button_new = QPushButton('Novo', self)
        self.button_new.clicked.connect(self.open_department_item)
        self.button_new.setStyleSheet('background-color: black; color: white')
        self.button_new.setMinimumHeight(40)

        self.button_refresh = QPushButton('Atualizar dados', self)
        self.button_refresh.clicked.connect(self.populate_table)
        self.button_refresh.setStyleSheet('background-color: green; color: white')
        self.button_refresh.setMinimumHeight(40)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.button_new)
        vertical_layout.addWidget(self.button_refresh)
        vertical_layout.addWidget(self.table)

        self.setLayout(vertical_layout)

        self.populate_table()

    def open_department_item(self):
        form = DepartmentItem(self)
        form.exec_()

    def populate_table(self):
        departments = models.Department.get_all()
        self.table.setRowCount(len(departments))

        for linha, d in enumerate(departments):
            column_id = QTableWidgetItem()
            column_id.setText(str(d.id))
            column_id.setData(Qt.UserRole, d.name)

            column_name = QTableWidgetItem()
            column_name.setText(d.name)

            self.table.setItem(linha, 0, column_id)
            self.table.setItem(linha, 1, column_name)


class DepartmentItem(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Cadastro de departamento')
        self.resize(300, 200)

        self.label_name = QLabel('Nome')

        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMaximumHeight(40)

        self.button_save = QPushButton('Salvar', self)
        self.button_save.clicked.connect(self.save)
        self.button_save.setStyleSheet('background-color: #87CEFA; color: black')
        self.button_save.setMinimumHeight(40)

        spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.label_name)
        vertical_layout.addWidget(self.line_edit_name)
        vertical_layout.addWidget(self.button_save)
        vertical_layout.addItem(spacer)

        self.setLayout(vertical_layout)

    def save(self):
        if self.line_edit_name.text() == '':
            QMessageBox.about(self, "Erro", "Campo de nome do departamento é obrigatório")
        else:
            department = models.Department()
            department.name = self.line_edit_name.text()
            department.save()


class EmployeeList(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Listagem dos Funcionários')
        self.resize(800, 600)

        self.button_new = QPushButton('Novo', self)
        self.button_new.clicked.connect(self.open_employee_item)
        self.button_new.setStyleSheet('background-color: black; color: white')
        self.button_new.setMinimumHeight(40)

        self.button_refresh = QPushButton('Atualizar dados', self)
        self.button_refresh.clicked.connect(self.populate_table)
        self.button_refresh.setStyleSheet('background-color: green; color: white')
        self.button_refresh.setMinimumHeight(40)

        self.table = QTableWidget(self)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'Nome', 'Departamento', 'Estado Civil', 'Distrito', 'Salário', 'Data de Admissão', 'Data de Nascimento', 'Gênero'])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.button_new)
        vertical_layout.addWidget(self.button_refresh)
        vertical_layout.addWidget(self.table)

        self.setLayout(vertical_layout)
        self.populate_table()

    def open_employee_item(self):
        form = EmployeeItem(self)
        form.exec_()

    def populate_table(self):
        employees = models.Employee.get_all()
        self.table.setRowCount(len(employees))

        for linha, e in enumerate(employees):
            column_id = QTableWidgetItem()
            column_id.setText(str(e.id))
            column_id.setData(Qt.UserRole, e.name)

            column_name = QTableWidgetItem()
            column_name.setText(e.name)

            column_department = QTableWidgetItem()
            column_department.setText(str(e.id_department))

            column_marital_status = QTableWidgetItem()
            column_marital_status.setText(str(e.id_marital_status))

            column_district = QTableWidgetItem()
            column_district.setText(str(e.id_district))

            column_salary = QTableWidgetItem()
            column_salary.setText(str(e.salary))

            column_admission_date = QTableWidgetItem()
            column_admission_date.setText(str(e.admission_date))

            column_birth_date = QTableWidgetItem()
            column_birth_date.setText(str(e.birth_date))

            column_gender = QTableWidgetItem()
            column_gender.setText(e.gender)

            self.table.setItem(linha, 0, column_id)
            self.table.setItem(linha, 1, column_name)
            self.table.setItem(linha, 2, column_department)
            self.table.setItem(linha, 3, column_marital_status)
            self.table.setItem(linha, 4, column_district)
            self.table.setItem(linha, 5, column_salary)
            self.table.setItem(linha, 6, column_admission_date)
            self.table.setItem(linha, 7, column_birth_date)
            self.table.setItem(linha, 8, column_gender)


class EmployeeItem(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle('Cadastro de Funcionário')
        self.resize(300, 400)

        self.label_name = QLabel('Nome')
        self.label_department = QLabel('Departamento')
        self.label_marital_status = QLabel('Estado Civil')
        self.label_district = QLabel('Distrito')
        self.label_salary = QLabel('Salário')
        self.label_admission_date = QLabel('Data de Admissão')
        self.label_birth_date = QLabel('Data de Nascimento')
        self.label_gender = QLabel('Gênero')

        self.line_edit_name = QLineEdit(self)
        self.line_edit_name.setMaximumHeight(40)

        self.combo_box_department = QComboBox(self)
        self.combo_box_department.setMaximumHeight(40)
        self.populate_combo_box(self.combo_box_department, models.Department.get_all(), 'id', 'name')

        self.combo_box_marital_status = QComboBox(self)
        self.combo_box_marital_status.setMaximumHeight(40)
        self.populate_combo_box(self.combo_box_marital_status, models.MaritalStatus.get_all(), 'id', 'name')

        self.combo_box_district = QComboBox(self)
        self.combo_box_district.setMaximumHeight(40)
        self.populate_combo_box(self.combo_box_district, models.District.get_all(), 'id', 'name')

        self.combo_box_gender = QComboBox(self)
        self.combo_box_gender.addItems(['M', 'F',])
        self.combo_box_gender.setMaximumHeight(40)

        self.line_edit_salary = QLineEdit(self)
        self.line_edit_salary.setMaximumHeight(40)

        self.line_edit_admission_date = QLineEdit(self)
        self.line_edit_admission_date.setMaximumHeight(40)

        self.line_edit_birth_date = QLineEdit(self)
        self.line_edit_birth_date.setMaximumHeight(40)

        self.button_save = QPushButton('Salvar', self)
        self.button_save.clicked.connect(self.save)
        self.button_save.setStyleSheet('background-color: #87CEFA; color: black')
        self.button_save.setMinimumHeight(40)

        spacer = QSpacerItem(0, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(15)
        vertical_layout.addWidget(self.label_name)
        vertical_layout.addWidget(self.line_edit_name)

        vertical_layout.addWidget(self.label_department)
        vertical_layout.addWidget(self.combo_box_department)

        vertical_layout.addWidget(self.label_marital_status)
        vertical_layout.addWidget(self.combo_box_marital_status)

        vertical_layout.addWidget(self.label_district)
        vertical_layout.addWidget(self.combo_box_district)

        vertical_layout.addWidget(self.label_salary)
        vertical_layout.addWidget(self.line_edit_salary)

        vertical_layout.addWidget(self.label_admission_date)
        vertical_layout.addWidget(self.line_edit_admission_date)

        vertical_layout.addWidget(self.label_birth_date)
        vertical_layout.addWidget(self.line_edit_birth_date)

        vertical_layout.addWidget(self.label_gender)
        vertical_layout.addWidget(self.combo_box_gender)

        vertical_layout.addWidget(self.button_save)
        vertical_layout.addItem(spacer)

        self.setLayout(vertical_layout)

    def populate_combo_box(self, combo_box, items, id_attr, display_attr):
        for item in items:
            combo_box.addItem(getattr(item, display_attr), getattr(item, id_attr))

    def save(self):
        if self.line_edit_name.text() == '':
            QMessageBox.about(self, "Erro", "Campo de nome do funcionário é obrigatório")
        else:
            employee = models.Employee()
            employee.name = self.line_edit_name.text()
            employee.id_department = self.combo_box_department.currentData()
            employee.id_marital_status = self.combo_box_marital_status.currentData()
            employee.id_district = self.combo_box_district.currentData()
            employee.salary = self.line_edit_salary.text()
            employee.admission_date = self.line_edit_admission_date.text()
            employee.birth_date = self.line_edit_birth_date.text()
            employee.gender = self.combo_box_gender.currentText()
            employee.save()
