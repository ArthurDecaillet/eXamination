from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from ORM import *
from correction import *
import re
from socket_client import *
from correction_prof import *
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("./assets")

    return os.path.join(base_path, relative_path)

class App(object):        
    def setupUi(self, MainWindow):
        '''
        Setup function for the window and all its graphic elements
        '''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(847, 743)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setBold(True)
        font.setWeight(75)
        self.__list_question = []

        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(90, 0, 751, 711))
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_accueil = QtWidgets.QWidget()
        self.page_accueil.setObjectName("page_accueil")

        self.lbl_home = QtWidgets.QLabel(self.page_accueil)
        self.lbl_home.setGeometry(QtCore.QRect(190, 70, 301, 111))
        self.lbl_home.setObjectName("lbl_home")

        self.stackedWidget.addWidget(self.page_accueil)

        
        # ========================= subject page start ============================

        self.page_subject = QtWidgets.QWidget()
        self.page_subject.setObjectName("page_subject")
        self.lbl_subject = QtWidgets.QLabel(self.page_subject)
        self.lbl_subject.setGeometry(QtCore.QRect(280, 40, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_subject.setFont(font)
        self.lbl_subject.setObjectName("lbl_subject")
        self.lst_subject = QtWidgets.QListWidget(self.page_subject)
        self.lst_subject.setGeometry(QtCore.QRect(130, 110, 471, 431))
        self.lst_subject.setObjectName("lst_subject")


        

        self.btn_subject_create = QtWidgets.QPushButton(self.page_subject)
        self.btn_subject_create.setGeometry(QtCore.QRect(340, 570, 75, 23))
        self.btn_subject_create.setObjectName("btn_subject_create")
        self.btn_subject_create.setFixedSize(60,60)
        

        create_icon = QtGui.QIcon(resource_path("plus.png"))

        self.btn_subject_create.setIcon(QtGui.QIcon(create_icon))
        self.btn_subject_create.setIconSize(QtCore.QSize(60,60))
        self.btn_subject_create.setStyleSheet("QPushButton {"
            "   border-radius: 30px;"
            "   background-color: transparent;"
            "}"
            "QPushButton:hover {"
            "   background-color: lightgray;"
            "}")
        
        self.btn_subject_create.clicked.connect(self.handle_subject_create)

        self.lst_subject.itemDoubleClicked.connect(self.handle_subject_Dclick)
        
        self.stackedWidget.addWidget(self.page_subject)

        self.list_subject = get_all_subject()

        # ========================= subject page end ============================

        
        self.page_examen = QtWidgets.QWidget()
        self.page_examen.setObjectName("page_examen")

        # Page exam creation

        self.lbl_exam = QtWidgets.QLabel(self.page_examen)
        self.lbl_exam.setGeometry(QtCore.QRect(260, 50, 221, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_exam.setFont(font)
        self.lbl_exam.setObjectName("lbl_exam")

        self.grp_teacher = QtWidgets.QGroupBox(self.page_examen)
        self.grp_teacher.setGeometry(QtCore.QRect(200, 120, 261, 131))
        self.grp_teacher.setObjectName("grp_teacher")

        self.widget1 = QtWidgets.QWidget(self.grp_teacher)
        self.widget1.setGeometry(QtCore.QRect(10, 30, 201, 91))
        self.widget1.setObjectName("widget1")

        self.teacher_layout = QtWidgets.QFormLayout(self.widget1)
        self.teacher_layout.setContentsMargins(0, 0, 0, 0)
        self.teacher_layout.setObjectName("teacher_layout")

        self.lbl_teacher_lastname = QtWidgets.QLabel(self.widget1)
        self.lbl_teacher_lastname.setObjectName("lbl_teacher_lastname")

        self.teacher_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_teacher_lastname)

        self.txt_teacher_lastname = QtWidgets.QLineEdit(self.widget1)
        self.txt_teacher_lastname.setObjectName("txt_teacher_lastname")

        self.teacher_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_teacher_lastname)

        self.lbl_teacher_firstname = QtWidgets.QLabel(self.widget1)
        self.lbl_teacher_firstname.setObjectName("lbl_teacher_firstname")

        self.teacher_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_teacher_firstname)

        self.txt_teacher_firstname = QtWidgets.QLineEdit(self.widget1)
        self.txt_teacher_firstname.setObjectName("txt_teacher_firstname")

        self.teacher_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_teacher_firstname)

        self.lbl_teacher_email = QtWidgets.QLabel(self.widget1)
        self.lbl_teacher_email.setObjectName("lbl_teacher_email")

        self.teacher_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_teacher_email)

        self.txt_teacher_email = QtWidgets.QLineEdit(self.widget1)
        self.txt_teacher_email.setObjectName("txt_teacher_email")

        self.teacher_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_teacher_email)

        self.btn_exam_save = QtWidgets.QPushButton(self.page_examen)
        self.btn_exam_save.setGeometry(QtCore.QRect(320, 570, 75, 23))
        self.btn_exam_save.setObjectName("btn_exam_save")
        self.btn_exam_save.clicked.connect(self.handle_btn_exam_save_click)

        self.grp_questions = QtWidgets.QGroupBox(self.page_examen)
        self.grp_questions.setGeometry(QtCore.QRect(200, 350, 261, 171))
        self.grp_questions.setObjectName("grp_questions")

        self.cmb_exam_type = QtWidgets.QComboBox(self.grp_questions)
        self.cmb_exam_type.setGeometry(QtCore.QRect(140, 60, 111, 20))
        self.cmb_exam_type.setObjectName("cmb_exam_type")
        self.cmb_exam_type.addItem("")
        self.cmb_exam_type.addItem("")

        self.lbl_exam_type = QtWidgets.QLabel(self.grp_questions)
        self.lbl_exam_type.setGeometry(QtCore.QRect(22, 60, 92, 20))
        self.lbl_exam_type.setObjectName("lbl_exam_type")

        self.lbl_number_questions = QtWidgets.QLabel(self.grp_questions)
        self.lbl_number_questions.setGeometry(QtCore.QRect(20, 90, 121, 20))
        self.lbl_number_questions.setObjectName("lbl_number_questions")

        self.txt_number_questions = QtWidgets.QSpinBox(self.grp_questions)
        self.txt_number_questions.setGeometry(QtCore.QRect(170, 90, 42, 22))
        self.txt_number_questions.setObjectName("txt_number_questions")

        self.btn_add = QtWidgets.QPushButton(self.grp_questions)
        self.btn_add.setGeometry(QtCore.QRect(170, 130, 75, 23))
        self.btn_add.setObjectName("btn_add")
        self.btn_add.clicked.connect(self.add_question)

        self.btn_see_questions = QtWidgets.QPushButton(self.grp_questions)
        self.btn_see_questions.setGeometry(QtCore.QRect(54, 130, 101, 23))
        self.btn_see_questions.setObjectName("btn_see_questions")
        self.btn_see_questions.clicked.connect(self.show_list_question)

        self.lbl_exam_subject = QtWidgets.QLabel(self.grp_questions)
        self.lbl_exam_subject.setGeometry(QtCore.QRect(20, 30, 61, 16))
        self.lbl_exam_subject.setObjectName("lbl_exam_subject")

        self.cmb_exam_subject = QtWidgets.QComboBox(self.grp_questions)
        self.cmb_exam_subject.setGeometry(QtCore.QRect(140, 30, 111, 20))
        self.cmb_exam_subject.setObjectName("cmb_exam_subject")
        self.cmb_exam_subject.addItem("")
        self.cmb_exam_subject.addItem("")

        self.widget2 = QtWidgets.QWidget(self.page_examen)
        self.widget2.setGeometry(QtCore.QRect(210, 260, 211, 61))
        self.widget2.setObjectName("widget2")

        self.exam_layout = QtWidgets.QFormLayout(self.widget2)
        self.exam_layout.setContentsMargins(0, 0, 0, 0)
        self.exam_layout.setObjectName("exam_layout")

        self.lbl_title = QtWidgets.QLabel(self.widget2)
        self.lbl_title.setObjectName("lbl_title")

        self.exam_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_title)

        self.txt_title = QtWidgets.QLineEdit(self.widget2)
        self.txt_title.setObjectName("txt_title")

        self.exam_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_title)

        self.lbl_date = QtWidgets.QLabel(self.widget2)
        self.lbl_date.setObjectName("lbl_date")

        self.exam_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_date)

        self.txt_date = QtWidgets.QDateEdit(self.widget2)
        self.txt_date.setObjectName("txt_date")

        self.exam_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_date)

        self.stackedWidget.addWidget(self.page_examen)

        self.btn_home = QtWidgets.QPushButton(self.centralwidget)
        self.btn_home.setGeometry(QtCore.QRect(0, 20, 75, 23))
        self.btn_home.setObjectName("btn_home")
        self.btn_home.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_accueil))

        self.btn_questions = QtWidgets.QPushButton(self.centralwidget)
        self.btn_questions.setGeometry(QtCore.QRect(0, 50, 75, 23))
        self.btn_questions.setObjectName("btn_questions")
        self.btn_questions.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_subject))


        self.btn_exam = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exam.setGeometry(QtCore.QRect(0, 80, 75, 23))
        self.btn_exam.setObjectName("btn_exam")
        self.btn_exam.clicked.connect(lambda:self.handle_btn_exam_click())

        self.list_input_exam_creation=[self.txt_teacher_firstname,self.txt_teacher_lastname,self.txt_title]

        # ========================================== end of exam creation page ================================================

        self.page_correction = QtWidgets.QWidget()
        self.page_correction.setObjectName("page_correction")

        self.btn_correction = QtWidgets.QPushButton(self.centralwidget)
        self.btn_correction.setGeometry(QtCore.QRect(0, 110, 75, 23))
        self.btn_correction.setObjectName("btn_correction")
        self.btn_correction.clicked.connect(self.handle_correction_page_open)

        self.stackedWidget.addWidget(self.page_correction)
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 847, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.refresh_list()
        self.get_cmb_subject()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        '''
        Method which sets all the graphic element's text
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_home.setText(_translate("MainWindow", "Bienvenue sur l\'application eXamination"))

        # start of subject page

        self.lbl_subject.setText(_translate("MainWindow", "Liste des matières"))
        self.lbl_exam_subject.setText(_translate("MainWindow", "Matière"))
        

        # =============== end of subject page ================

        
        self.lbl_exam.setText(_translate("MainWindow", "Création d\'examen"))
        self.grp_teacher.setTitle(_translate("MainWindow", "Informations du professeur"))
        self.lbl_teacher_lastname.setText(_translate("MainWindow", "nom"))
        self.lbl_teacher_firstname.setText(_translate("MainWindow", "prénom"))
        self.lbl_teacher_email.setText(_translate("MainWindow", "email"))
        self.btn_exam_save.setText(_translate("MainWindow", "Enregistrer"))
        self.grp_questions.setTitle(_translate("MainWindow", "Informations des questions"))
        self.cmb_exam_type.setItemText(0, _translate("MainWindow", "définition"))
        self.cmb_exam_type.setItemText(1, _translate("MainWindow", "qcm"))
        self.lbl_exam_type.setText(_translate("MainWindow", "Type de question"))
        self.lbl_number_questions.setText(_translate("MainWindow", "nombre de questions"))
        self.btn_add.setText(_translate("MainWindow", "ajouter"))
        self.btn_see_questions.setText(_translate("MainWindow", "voir les questions"))
        self.lbl_title.setText(_translate("MainWindow", "titre de l\'examen"))
        self.lbl_date.setText(_translate("MainWindow", "date de l\'examen"))
        self.btn_home.setText(_translate("MainWindow", "Accueil"))
        self.btn_correction.setText(_translate("Mainwindow","Corrections"))

        self.btn_questions.setText(_translate("MainWindow", "Matières"))
        
        self.btn_exam.setText(_translate("MainWindow", "Examens"))



    def handle_btn_exam_click(self):
        '''
            Mathod which handles the functions to start when btn_exam is pressed
        '''
        self.stackedWidget.setCurrentWidget(self.page_examen)

        self.get_cmb_subject()

    def get_questions (self):
        '''
            Getter method which returns the list_question
        '''
        return self.__list_question
               
    def add_question(self):
        '''
            Method which adds a certain number of questions to the list
        '''
        self.__list_question += random_question(self.txt_number_questions.value(),self.cmb_exam_subject.currentText(),self.cmb_exam_type.currentText())
        
    def create_exam(self):
        '''
            Method that allows the programm to create an Exam document within the database according to the user informations.
        '''
        list_question_id = []
        list_element_used = [self.txt_teacher_firstname,self.txt_teacher_lastname,self.txt_teacher_email,self.txt_title]
        new_teacher = Teacher(self.txt_teacher_firstname.text(),self.txt_teacher_lastname.text(),self.txt_teacher_email.text())
        for question in self.__list_question:
            list_question_id.append(str(question.get_id()))
        
        new_exam = Exam(self.txt_title.text(),new_teacher,list_question_id,self.date_format())
        new_exam.db_insert()
        self.list_question = []
        for element in list_element_used:
            element.clear()
        self.created_exam = new_exam

    def date_format(self):
        '''
            Method that format the date to a YYYY-MM-DD string
        '''
        return f"{self.txt_date.date().getDate()[0]}-{self.txt_date.date().getDate()[1]}-{self.txt_date.date().getDate()[2]}"

    def show_list_question(self):
        '''
            Method which opens a new window from the UI_list_question class on the click of a button.
        '''
        
        self.window = QtWidgets.QMainWindow()
        self.ui = UI_list_question()
        self.ui.setupUi(self.window)
        self.window.show()

    def refresh_list(self):
        '''
            Method that refresh the display of the list of subject within the QListWidget, and it additionnaly adds buttons to the list elements
            for deleting or updating them.
        '''
        self.list_subject = get_all_subject()
        self.lst_subject.clear()
        for subject in self.list_subject:
            item = QtWidgets.QListWidgetItem(subject.get_name(),self.lst_subject)

            container_widget = QtWidgets.QWidget()

            layout = QtWidgets.QHBoxLayout()

            btn_subject_edit = QtWidgets.QPushButton(self.centralwidget)
            btn_subject_edit.setIcon(QtGui.QIcon(resource_path("edit-icon.png")))
            btn_subject_edit.setFixedSize(60,30)
            btn_subject_edit.subject_name = subject.get_name()
            btn_subject_edit.clicked.connect(lambda checked, subject=item: self.handle_subject_edit(subject))
            
            btn_subject_delete = QtWidgets.QPushButton(self.centralwidget)
            btn_subject_delete.setIcon(QtGui.QIcon(resource_path("delete-icon.png")))
            btn_subject_delete.setFixedSize(60,30)
            btn_subject_delete.clicked.connect(lambda checked, subject=item: self.handle_subject_delete(subject))

            layout.addWidget(btn_subject_delete)
            layout.addWidget(btn_subject_edit)

            container_widget.setLayout(layout)
   
            item.setSizeHint(container_widget.sizeHint())
            self.lst_subject.setItemWidget(item,container_widget)

    def handle_subject_create(self):
        '''
            Method which handles the creation of a subject by opening a UI_win_subject_create window
            => open a little window with the subject creation inputs
        '''
        self.window_subject_create = QtWidgets.QMainWindow()
        self.ui = Ui_win_subject_create()
        self.ui.setupUi(self.window_subject_create)
        self.ui.get_mainwindow(self)
        self.window_subject_create.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_subject_create.show()

       
    def handle_subject_edit(self,subject):
        '''
            Method which handles the modification / update of a subject by opening a [class name] window
        '''
        self.window_subject_update = QtWidgets.QMainWindow()
        self.ui = Subject_update_UI()
        self.ui.setupUi(self.window_subject_update,subject)
        self.ui.get_mainwindow(self)
        self.window_subject_update.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window_subject_update.show()

        

    def handle_subject_delete(self,subject):
        '''
            Method which handles the deletion of a subject by deleting it from the list_subject and then refreshing the page
        '''
        for element in self.list_subject:
            if element.get_name() == subject.text():
                element.delete_db()
        self.refresh_list()

    def handle_subject_Dclick(self,subject):
        '''
            Method which handles the double click event on a subject item and opening the UI_win_question_list window
            => shows the page with all the questions from one subject.
        '''
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_win_question_list()
        self.ui.setupUi(self.window,subject.text())
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window.show()
        
    

    def get_subjects(self):
        '''
        Method to get all the subject of the database and changing the self.list_subject variable to it.
        '''
        self.list_subject = get_all_subject()

    def get_cmb_subject(self):
        '''
            Method which gets all the subjects of the database and puts them inside the needing combobox
        '''
        self.get_subjects()
        self.cmb_exam_subject.clear()
        for subject in self.list_subject:
            item = subject.get_name()
            self.cmb_exam_subject.addItem(item)

    def handle_btn_exam_save_click(self):
        '''
        Method which handles the click of the save exam button. It also checks if the inputs are valid or not.
        It also starts the process of sending the exams.
        '''
        can_continue = True
        for input in self.list_input_exam_creation:
            if not basic_input_checker(input):
                can_continue=False
        if not email_checked(self.txt_teacher_email):
            can_continue=False
        
        if can_continue:
            self.create_exam()
            json_to_send = self.created_exam.get_json()
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_correction_ui()
            connection_client(json_to_send,self.ui)
            
            self.ui.setupUi(self.window,"",self.created_exam)
            
            self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
            self.window.show()
    def handle_correction_page_open(self):
        '''
        Method which handles to opening of the correction window
        '''
        self.window = QtWidgets.QMainWindow()
        self.ui = Correction_main_ui()
        self.ui.setupUi(self.window)
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window.show()

            


    
class UI_list_question(object):
    '''
        Class representing the list of questions selected for the exam
    '''
    def setupUi(self, MainWindow):
        '''
        Setup method for the window and all its graphic elements
        '''
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(567, 438)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lste_question = ui.get_questions()

        self.lbl_list_questions = QtWidgets.QLabel(self.centralwidget)
        self.lbl_list_questions.setGeometry(QtCore.QRect(240, 20, 91, 16))
        self.lbl_list_questions.setObjectName("lbl_list_questions")

        self.lst_questions = QtWidgets.QListWidget(self.centralwidget)
        self.lst_questions.setGeometry(QtCore.QRect(160, 90, 256, 192))
        self.lst_questions.setObjectName("lst_questions")

        

        self.btn_close = QtWidgets.QPushButton(self.centralwidget)
        self.btn_close.setGeometry(QtCore.QRect(330, 360, 75, 23))
        self.btn_close.setObjectName("btn_close")
        self.btn_close.clicked.connect(MainWindow.close)

        self.btn_delete = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delete.setGeometry(QtCore.QRect(170, 360, 75, 23))
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.clicked.connect(self.delete_question)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 567, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)


        self.refresh_list()


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        '''
        Method which sets all the graphic element's text
        '''
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "liste de questions"))
        self.lbl_list_questions.setText(_translate("MainWindow", "Liste des questions"))
        
        self.btn_close.setText(_translate("MainWindow", "fermer"))
        self.btn_delete.setText(_translate("MainWindow", "Supprimer"))

    def delete_question(self):
        '''
            Method which delete the selected element of the list of question on the click of a button
        '''
        
        self.lste_question.pop(self.lst_questions.currentRow())
        self.refresh_list()


    def refresh_list(self):
        '''
            Method that refresh the display of the list of question within the QListWidget
        '''
        self.lst_questions.clear()
        for question in self.lste_question:
            self.lst_questions.addItem(question.get_content())
    



class Ui_win_question_list(object):
    '''
        Class representing the page with all the question of a subject
    '''
    def setupUi(self, win_question_list,subject_name):
        '''
        Setup method for the window and all its graphic elements
        '''
        win_question_list.setObjectName("win_question_list")
        win_question_list.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(win_question_list)
        self.centralwidget.setObjectName("centralwidget")
        self.lst_subject_questions = QtWidgets.QListWidget(self.centralwidget)
        self.lst_subject_questions.setGeometry(QtCore.QRect(230, 70, 351, 421))
        self.lst_subject_questions.setObjectName("lst_subject_questions")

        self.btn_subject_questions_create = QtWidgets.QPushButton(self.centralwidget)
        self.btn_subject_questions_create.setGeometry(QtCore.QRect(270, 520, 75, 23))
        self.btn_subject_questions_create.setObjectName("btn_subject_questions_create")
        self.btn_subject_questions_create.clicked.connect(self.handle_question_create)

        self.btn_subject_questions_close = QtWidgets.QPushButton(self.centralwidget)
        self.btn_subject_questions_close.setGeometry(QtCore.QRect(450, 520, 75, 23))
        self.btn_subject_questions_close.setObjectName("btn_subject_questions_close")
        self.btn_subject_questions_close.clicked.connect(win_question_list.close)

        self.lbl_subject_questions = QtWidgets.QLabel(self.centralwidget)
        self.lbl_subject_questions.setGeometry(QtCore.QRect(360, 30, 91, 16))
        self.lbl_subject_questions.setObjectName("lbl_subject_questions")

        win_question_list.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(win_question_list)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        win_question_list.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(win_question_list)
        self.statusbar.setObjectName("statusbar")
        win_question_list.setStatusBar(self.statusbar)

        self.lst_questions = get_questions_by_subject(subject_name)
        self.subject = subject_name
        self.refresh_lst()
        self.retranslateUi(win_question_list)
        QtCore.QMetaObject.connectSlotsByName(win_question_list)

    def retranslateUi(self, win_question_list):
        '''
        Method which sets all the graphic element's text
        '''
        _translate = QtCore.QCoreApplication.translate
        win_question_list.setWindowTitle(_translate("win_question_list", "MainWindow"))
        self.btn_subject_questions_create.setText(_translate("win_question_list", "Créer"))
        self.btn_subject_questions_close.setText(_translate("win_question_list", "Fermer"))
        self.lbl_subject_questions.setText(_translate("win_question_list", "Liste des questions"))    

    def refresh_lst(self):
        '''
            Method which refreshes all the questions present in the subject list
        '''
        self.lst_questions = get_questions_by_subject(self.subject)
        self.lst_subject_questions.clear()
        for questions in self.lst_questions:
            for question in questions:
                
        
                item = QtWidgets.QListWidgetItem(self.lst_subject_questions)

                container_widget = QtWidgets.QWidget()
                container_layout = QtWidgets.QHBoxLayout()

                lbl_question = QtWidgets.QLabel()
                lbl_question.setText(question.get_content())


                btn_question_edit = QtWidgets.QPushButton()
                btn_question_edit.setIcon(QtGui.QIcon(resource_path("edit-icon.png")))
                btn_question_edit.setFixedSize(60,30)
                btn_question_edit.clicked.connect(lambda checked, question=lbl_question.text(): self.handle_question_edit(question))

                btn_question_delete = QtWidgets.QPushButton()
                btn_question_delete.setIcon(QtGui.QIcon(resource_path("delete-icon.png")))
                btn_question_delete.setFixedSize(60,30)
                btn_question_delete.clicked.connect(lambda checked, question=lbl_question.text(): self.handle_question_delete(question))

                container_layout.addWidget(lbl_question)
                container_layout.addWidget(btn_question_delete)
                container_layout.addWidget(btn_question_edit)

                container_widget.setLayout(container_layout)

                item.setSizeHint(container_widget.sizeHint())
                self.lst_subject_questions.setItemWidget(item,container_widget)

    def handle_question_create(self):
        '''
            Method which handles the creation of a question by opening a Question_create_UI window.
            => open a window with all the inputs to create a question
        '''
        self.window = QtWidgets.QMainWindow()
        self.ui = Question_create_UI()
        self.ui.setupUi(self.window,self.subject)
        self.ui.get_mainwindow(self)
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window.show()

    def handle_question_edit(self,question):
        '''
            Method which handles the update of the question according to its content when a button is pressed.
            @parameter question => (string) content of the question
        '''
        for elements in self.lst_questions:
            for element in elements:
                if element.get_content() == question:

                    self.window = QtWidgets.QMainWindow()
                    self.ui = Question_update_UI()
                    self.ui.setupUi(self.window,self.subject,element)
                    self.ui.get_mainwindow(self)
                    self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
                    self.window.show()
        
    def handle_question_delete(self,question):
        '''
            Method which handles the deletion of a question according to its content.
            @parameter question => content of the question (string)
        '''
        
        for elements in self.lst_questions:
            for element in elements:
                if element.get_content() == question:
                    element.db_delete()
        self.refresh_lst()

class Ui_win_subject_create(object):
    '''
        Class that represents the subject creation window.
    '''
    def setupUi(self, win_subject_create):
        '''
        Setup method for the window and all its graphic elements
        '''
        win_subject_create.setObjectName("win_subject_create")
        win_subject_create.resize(397, 294)
        self.centralwidget = QtWidgets.QWidget(win_subject_create)
        self.centralwidget.setObjectName("centralwidget")

        self.lbl_subject_create = QtWidgets.QLabel(self.centralwidget)
        self.lbl_subject_create.setGeometry(QtCore.QRect(160, 30, 101, 16))
        self.lbl_subject_create.setObjectName("lbl_subject_create")

        self.txt_subject_name = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_subject_name.setGeometry(QtCore.QRect(190, 120, 113, 20))
        self.txt_subject_name.setObjectName("txt_subject_name")

        self.lbl_subject_name = QtWidgets.QLabel(self.centralwidget)
        self.lbl_subject_name.setGeometry(QtCore.QRect(140, 120, 47, 13))
        self.lbl_subject_name.setObjectName("lbl_subject_name")

        self.btn_subject_create = QtWidgets.QPushButton(self.centralwidget)
        self.btn_subject_create.setGeometry(QtCore.QRect(160, 200, 75, 23))
        self.btn_subject_create.setObjectName("btn_subject_create")
        self.btn_subject_create.clicked.connect(self.handle_subject_create)

        win_subject_create.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(win_subject_create)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 397, 21))
        self.menubar.setObjectName("menubar")
        win_subject_create.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(win_subject_create)
        self.statusbar.setObjectName("statusbar")
        win_subject_create.setStatusBar(self.statusbar)

        self.retranslateUi(win_subject_create)
        QtCore.QMetaObject.connectSlotsByName(win_subject_create)

    def retranslateUi(self, win_subject_create):
        '''
        Method which sets all the graphic element's text
        '''
        _translate = QtCore.QCoreApplication.translate
        win_subject_create.setWindowTitle(_translate("win_subject_create", "MainWindow"))
        self.lbl_subject_create.setText(_translate("win_subject_create", "Création de matière"))
        self.lbl_subject_name.setText(_translate("win_subject_create", "nom"))
        self.btn_subject_create.setText(_translate("win_subject_create", "Créer"))

    def get_mainwindow(self,mainwindow):
        '''
            Method which gets the window in which this function is situated
        '''
        self.mainwindow = mainwindow

    def handle_subject_create(self):
        '''
            Method which handles the creation of a subject and refreshes the list of the subjects of the previously opened window.
        '''
        if basic_input_checker(self.txt_subject_name):
            new_subject = Subject(self.txt_subject_name.text())
            new_subject.insert_db()
            self.txt_subject_name.setText("")
            self.mainwindow.refresh_list()
        


class Question_create_UI(object):
    '''
        Class that represents the question creation window.
    '''
    def setupUi(self, Question_create_UI,subject):
        '''
        Setup method for the window and all its graphic elements
        '''
        Question_create_UI.setObjectName("Question_create_UI")
        Question_create_UI.resize(800, 625)

        self.window = Question_create_UI

        self.centralwidget = QtWidgets.QWidget(Question_create_UI)
        self.centralwidget.setObjectName("centralwidget")

        self.btn_question_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_question_save.setGeometry(QtCore.QRect(340, 560, 75, 23))
        self.btn_question_save.clicked.connect(self.create_question)

        

        self.lbl_options = QtWidgets.QLabel(self.centralwidget)
        self.lbl_options.setEnabled(True)
        self.lbl_options.setGeometry(QtCore.QRect(200, 420, 47, 13))
        self.lbl_questions = QtWidgets.QLabel(self.centralwidget)
        self.lbl_questions.setGeometry(QtCore.QRect(280, 0, 221, 61))

        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.lbl_questions.setFont(font)
        self.lbl_solution = QtWidgets.QLabel(self.centralwidget)
        self.lbl_solution.setEnabled(True)
        self.lbl_solution.setGeometry(QtCore.QRect(200, 490, 61, 16))

        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(200, 150, 356, 248))

        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget_2)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.lbl_type_2 = QtWidgets.QLabel(self.layoutWidget_2)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_type_2)

        self.cmb_type = QtWidgets.QComboBox(self.layoutWidget_2)
        self.cmb_type.addItem("")
        self.cmb_type.addItem("")
        self.cmb_type.currentTextChanged.connect(self.show_qcm)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cmb_type)

        self.lbl_content = QtWidgets.QLabel(self.layoutWidget_2)

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_content)

        self.txt_content = QtWidgets.QTextEdit(self.layoutWidget_2)

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_content)

        self.txt_option_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_1.setEnabled(False)
        self.txt_option_1.setGeometry(QtCore.QRect(220, 450, 71, 20))
        self.txt_option_1.textChanged.connect(self.show_solution)

        self.txt_option_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_2.setEnabled(False)
        self.txt_option_2.setGeometry(QtCore.QRect(300, 450, 71, 20))
        self.txt_option_2.textChanged.connect(self.show_solution)

        self.txt_option_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_3.setEnabled(False)
        self.txt_option_3.setGeometry(QtCore.QRect(380, 450, 71, 20))
        self.txt_option_3.textChanged.connect(self.show_solution)

        self.txt_option_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_4.setEnabled(False)
        self.txt_option_4.setGeometry(QtCore.QRect(460, 450, 71, 20))
        self.txt_option_4.textChanged.connect(self.show_solution)

        self.cbx_solution_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_1.setEnabled(False)
        self.cbx_solution_1.setGeometry(QtCore.QRect(200, 520, 70, 17))
        self.cbx_solution_1.setText("")

        self.cbx_solution_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_3.setEnabled(False)
        self.cbx_solution_3.setGeometry(QtCore.QRect(370, 520, 70, 17))
        self.cbx_solution_3.setText("")

        self.cbx_solution_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_2.setEnabled(False)
        self.cbx_solution_2.setGeometry(QtCore.QRect(290, 520, 70, 17))
        self.cbx_solution_2.setText("")

        self.cbx_solution_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_4.setEnabled(False)
        self.cbx_solution_4.setGeometry(QtCore.QRect(450, 520, 70, 17))
        self.cbx_solution_4.setText("")

        self.list_solution_object = [self.cbx_solution_1,self.cbx_solution_2,self.cbx_solution_3,self.cbx_solution_4]
        self.list_options_object = [self.txt_option_1,self.txt_option_2,self.txt_option_3,self.txt_option_4]
        self.subject = subject
        

        Question_create_UI.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(Question_create_UI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        Question_create_UI.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(Question_create_UI)
        self.statusbar.setObjectName("statusbar")

        Question_create_UI.setStatusBar(self.statusbar)

        self.retranslateUi(Question_create_UI)
        QtCore.QMetaObject.connectSlotsByName(Question_create_UI)

    def retranslateUi(self, Question_create_UI):
        '''
        Method which sets all the graphic element's text
        '''
        _translate = QtCore.QCoreApplication.translate
        Question_create_UI.setWindowTitle(_translate("Question_create_UI", "MainWindow"))
        self.btn_question_save.setText(_translate("Question_create_UI", "Enregister"))
        self.lbl_options.setText(_translate("Question_create_UI", "options"))
        self.lbl_questions.setText(_translate("Question_create_UI", "Création de questions"))
        self.lbl_solution.setText(_translate("Question_create_UI", "solution(s)"))
        self.lbl_type_2.setText(_translate("Question_create_UI", "Type de question"))
        self.cmb_type.setItemText(0, _translate("Question_create_UI", "définition"))
        self.cmb_type.setItemText(1, _translate("Question_create_UI", "qcm"))
        self.lbl_content.setText(_translate("Question_create_UI", "contenu"))

    def show_qcm(self):
        '''
            Method that changes the state of the text input concerning the options and the checkboxs concerning the solutions.
            This method shows the elements if the combobox content is equal to qcm, otherwise it hides them.
        '''
        if self.cmb_type.currentText() == "qcm":
            for element in self.list_options_object:
                element.setEnabled(True)
            
            for element in self.list_solution_object:
                element.setEnabled(True)
        else:
            for element in self.list_options_object:
                element.setEnabled(False)
            
            for element in self.list_solution_object:
                element.setEnabled(False)

    def create_question(self):
        '''
            Method that allows the programm to create a question document containing the user infos within the database 
        '''
        if self.input_checker():
            if self.cmb_type.currentText() == "qcm": 
                
                list_options = [self.txt_option_1.text(),self.txt_option_2.text(),self.txt_option_3.text(),self.txt_option_4.text()]
                list_solutions = []
                for solution in self.list_solution_object:
                    if solution.isChecked():
                        list_solutions.append(solution.text())
                new_question = QCM(self.cmb_type.currentText(),self.txt_content.toPlainText(),self.subject, list_options, list_solutions)
                
            elif self.cmb_type.currentText() == "définition":
                new_question = DEF(self.cmb_type.currentText(),self.txt_content.toPlainText(),self.subject)
            new_question.db_insert()
            self.handle_subject_change(self.subject, new_question)
            for element in self.list_solution_object:
                element.setText("")
                element.setCheckState(QtCore.Qt.Unchecked)
            for element in self.list_options_object:
                element.clear()
            self.txt_content.clear()
            self.window.close()
            self.mainwindow.refresh_lst()

    def show_solution(self):
        '''
            Method that changes the checkbox's text content to what is written in the option text input. This method activates when the content
            of an input is changed.
        '''
        self.cbx_solution_1.setText(self.txt_option_1.text())
        self.cbx_solution_2.setText(self.txt_option_2.text())
        self.cbx_solution_3.setText(self.txt_option_3.text())
        self.cbx_solution_4.setText(self.txt_option_4.text())

    def handle_subject_change(self,name, question):
        '''
            Method which handles the the adding of a new question to a subject.
        '''
        subject = get_subject_by_name(name)
        new_question_id = get_question_by_content(question.get_content())
        subject.add_question(new_question_id)

    def get_mainwindow(self,mainwindow):
        '''
            Method which gets the window in which this function is located.
        '''
        self.mainwindow = mainwindow

    def input_checker(self):
        '''
        Method which checks all this page's input's validity and return True if they are valid and False if they aren't
        @return Boolean => True if the inputs are valid and False if not
        '''
        can_continue = True
        if not textArea_input_checker(self.txt_content):
            can_continue = False
        if self.cmb_type.currentText()=="qcm":
            for option in self.list_options_object:
                if not basic_input_checker(option):
                    can_continue = False
        return can_continue


class Question_update_UI(object):
    '''
        Class that represents the question update window.
    '''
    def setupUi(self, Question_update_UI,subject,question):
        '''
        Setup method for the window and all its graphic elements
        '''
        Question_update_UI.setObjectName("Question_update_UI")
        Question_update_UI.resize(800, 625)

        self.window = Question_update_UI

        self.centralwidget = QtWidgets.QWidget(Question_update_UI)
        self.centralwidget.setObjectName("centralwidget")

        self.btn_question_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_question_save.setGeometry(QtCore.QRect(340, 560, 75, 23))
        self.btn_question_save.clicked.connect(self.handle_question_edit)

        

        self.lbl_options = QtWidgets.QLabel(self.centralwidget)
        self.lbl_options.setEnabled(True)
        self.lbl_options.setGeometry(QtCore.QRect(200, 420, 47, 13))
        self.lbl_questions = QtWidgets.QLabel(self.centralwidget)
        self.lbl_questions.setGeometry(QtCore.QRect(280, 0, 221, 61))

        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.lbl_questions.setFont(font)
        self.lbl_solution = QtWidgets.QLabel(self.centralwidget)
        self.lbl_solution.setEnabled(True)
        self.lbl_solution.setGeometry(QtCore.QRect(200, 490, 61, 16))

        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(200, 150, 356, 248))

        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget_2)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.lbl_type_2 = QtWidgets.QLabel(self.layoutWidget_2)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_type_2)

        self.cmb_type = QtWidgets.QComboBox(self.layoutWidget_2)
        self.cmb_type.addItem("")
        self.cmb_type.addItem("")
        self.cmb_type.currentTextChanged.connect(self.show_qcm)

        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cmb_type)

        self.lbl_content = QtWidgets.QLabel(self.layoutWidget_2)

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_content)

        self.txt_content = QtWidgets.QTextEdit(self.layoutWidget_2)

        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_content)

        self.txt_option_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_1.setEnabled(False)
        self.txt_option_1.setGeometry(QtCore.QRect(220, 450, 71, 20))
        self.txt_option_1.textChanged.connect(self.show_solution)

        self.txt_option_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_2.setEnabled(False)
        self.txt_option_2.setGeometry(QtCore.QRect(300, 450, 71, 20))
        self.txt_option_2.textChanged.connect(self.show_solution)

        self.txt_option_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_3.setEnabled(False)
        self.txt_option_3.setGeometry(QtCore.QRect(380, 450, 71, 20))
        self.txt_option_3.textChanged.connect(self.show_solution)

        self.txt_option_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_option_4.setEnabled(False)
        self.txt_option_4.setGeometry(QtCore.QRect(460, 450, 71, 20))
        self.txt_option_4.textChanged.connect(self.show_solution)

        self.cbx_solution_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_1.setEnabled(False)
        self.cbx_solution_1.setGeometry(QtCore.QRect(200, 520, 70, 17))
        self.cbx_solution_1.setText("")

        self.cbx_solution_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_3.setEnabled(False)
        self.cbx_solution_3.setGeometry(QtCore.QRect(370, 520, 70, 17))
        self.cbx_solution_3.setText("")

        self.cbx_solution_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_2.setEnabled(False)
        self.cbx_solution_2.setGeometry(QtCore.QRect(290, 520, 70, 17))
        self.cbx_solution_2.setText("")

        self.cbx_solution_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.cbx_solution_4.setEnabled(False)
        self.cbx_solution_4.setGeometry(QtCore.QRect(450, 520, 70, 17))
        self.cbx_solution_4.setText("")

        self.list_solution_object = [self.cbx_solution_1,self.cbx_solution_2,self.cbx_solution_3,self.cbx_solution_4]
        self.list_options_object = [self.txt_option_1,self.txt_option_2,self.txt_option_3,self.txt_option_4]
        self.subject = subject
        self.question = question

        self.refresh_page()
        

        Question_update_UI.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(Question_update_UI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        Question_update_UI.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(Question_update_UI)
        self.statusbar.setObjectName("statusbar")

        Question_update_UI.setStatusBar(self.statusbar)

        self.retranslateUi(Question_update_UI)
        QtCore.QMetaObject.connectSlotsByName(Question_update_UI)

    def retranslateUi(self, Question_update_UI):
        '''
        Method which sets all the graphic element's text
        '''
        _translate = QtCore.QCoreApplication.translate
        Question_update_UI.setWindowTitle(_translate("Question_update_UI", "MainWindow"))
        self.btn_question_save.setText(_translate("Question_update_UI", "Enregister"))
        self.lbl_options.setText(_translate("Question_update_UI", "options"))
        self.lbl_questions.setText(_translate("Question_update_UI", "Mise à jour de la question"))
        self.lbl_solution.setText(_translate("Question_update_UI", "solution(s)"))
        self.lbl_type_2.setText(_translate("Question_update_UI", "Type de question"))
        self.cmb_type.setItemText(0, _translate("Question_update_UI", "définition"))
        self.cmb_type.setItemText(1, _translate("Question_update_UI", "qcm"))
        self.lbl_content.setText(_translate("Question_update_UI", "contenu"))

    def refresh_page(self):
        '''
        Method which refreshes the éost of options and the graphic user interface.
        '''
        self.txt_content.setText(self.question.get_content())
        if self.question.get_type()=="qcm":
            self.cmb_type.setCurrentIndex(1)
            options = self.question.get_options()
            
            self.txt_option_1.setText(options[0])
            self.txt_option_2.setText(options[1])
            self.txt_option_3.setText(options[2])
            self.txt_option_4.setText(options[3])
        else:
            self.cmb_type.setCurrentIndex(0)
        

    def show_qcm(self):
        '''
            Method that changes the state of the text input concerning the options and the checkboxs concerning the solutions.
            This method shows the elements if the combobox content is equal to qcm, otherwise it hides them.
        '''
        if self.cmb_type.currentText() == "qcm":
            for element in self.list_options_object:
                element.setEnabled(True)
            
            for element in self.list_solution_object:
                element.setEnabled(True)
        else:
            for element in self.list_options_object:
                element.setEnabled(False)
            
            for element in self.list_solution_object:
                element.setEnabled(False)

    def handle_question_edit(self):
        '''
            Method that allows the programm to create a question document containing the user infos within the database 
        '''
        if self.cmb_type.currentText() == "qcm": 
            list_options = [self.txt_option_1.text(),self.txt_option_2.text(),self.txt_option_3.text(),self.txt_option_4.text()]
            list_solutions = []
            for solution in self.list_solution_object:
                if solution.isChecked():
                    list_solutions.append(solution.text())

            if self.question.get_type() == "définition":
                self.question.db_delete()
                new_question = QCM(self.cmb_type.currentText(),self.txt_content.toPlainText(),self.subject,list_options, list_solutions)
                new_question.db_insert()
                self.handle_subject_change(self.subject, new_question)
                self.question = new_question
            else:
                self.question.update_data(self.txt_content.toPlainText(),self.cmb_type.currentText(),self.subject,list_options, list_solutions)
                self.question.db_update()
        
            
        elif self.cmb_type.currentText() == "définition":
            self.question.update_data(self.txt_content.toPlainText(),self.cmb_type.currentText(),self.subject)
            self.question.db_update()

        
        for element in self.list_solution_object:
            element.setText("")
            element.setCheckState(QtCore.Qt.Unchecked)
        for element in self.list_options_object:
            element.clear()
        self.txt_content.clear()
        self.window.close()
        self.mainwindow.refresh_lst()

    def show_solution(self):
        '''
            Method that changes the checkbox's text content to what is written in the option text input. This method activates when the content
            of an input is changed.
        '''
        self.cbx_solution_1.setText(self.txt_option_1.text())
        self.cbx_solution_2.setText(self.txt_option_2.text())
        self.cbx_solution_3.setText(self.txt_option_3.text())
        self.cbx_solution_4.setText(self.txt_option_4.text())

    def handle_subject_change(self,name, question):
        '''
            Method which handles the adding of a new question to a subject.
        '''
        subject = get_subject_by_name(name)
        new_question_id = get_question_by_content(question.get_content())
        subject.add_question(new_question_id)

    def get_mainwindow(self,mainwindow):
        '''
            Method which gets the window in which this function is located.
        '''
        self.mainwindow = mainwindow


    
class Subject_update_UI(object):
    '''
        Class representing the page which updates the subject's name
    '''
    def setupUi(self, Subject_update_UI,subject):
        '''
        Setup method for the window and all its graphic elements
        '''
        Subject_update_UI.setObjectName("Subject_update_UI")
        Subject_update_UI.resize(401, 220)
        self.centralwidget = QtWidgets.QWidget(Subject_update_UI)
        self.centralwidget.setObjectName("centralwidget")
        self.subject = subject

        self.window = Subject_update_UI

        self.lbl_subject_update = QtWidgets.QLabel(self.centralwidget)
        self.lbl_subject_update.setGeometry(QtCore.QRect(140, 20, 121, 16))
        self.lbl_subject_update.setObjectName("lbl_subject_update")

        self.lbl_subject_name = QtWidgets.QLabel(self.centralwidget)
        self.lbl_subject_name.setGeometry(QtCore.QRect(100, 70, 31, 16))
        self.lbl_subject_name.setObjectName("lbl_subject_name")

        self.txt_subject_name = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_subject_name.setGeometry(QtCore.QRect(150, 70, 113, 20))
        self.txt_subject_name.setObjectName("txt_subject_name")

        self.btn_subject_update_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_subject_update_save.setGeometry(QtCore.QRect(170, 130, 75, 23))
        self.btn_subject_update_save.setObjectName("btn_subject_update_save")
        self.btn_subject_update_save.clicked.connect(self.handle_btn_save)

        Subject_update_UI.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Subject_update_UI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 401, 21))
        self.menubar.setObjectName("menubar")
        Subject_update_UI.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Subject_update_UI)
        self.statusbar.setObjectName("statusbar")
        Subject_update_UI.setStatusBar(self.statusbar)

        

        self.retranslateUi(Subject_update_UI)
        QtCore.QMetaObject.connectSlotsByName(Subject_update_UI)

    def retranslateUi(self, Subject_update_UI):
        '''
        Method which sets all the graphic element's text
        '''
        _translate = QtCore.QCoreApplication.translate
        Subject_update_UI.setWindowTitle(_translate("Subject_update_UI", "MainWindow"))
        self.lbl_subject_update.setText(_translate("Subject_update_UI", "Mise à jour de la matière"))
        self.lbl_subject_name.setText(_translate("Subject_update_UI", "nom"))
        self.btn_subject_update_save.setText(_translate("Subject_update_UI", "Enregistrer"))

    def get_mainwindow(self,mainwindow):
        '''
            Method which gets the window in which this function is situated
        '''
        self.mainwindow = mainwindow

    def handle_btn_save(self):
        '''
            Method which handles the click of the save button. It updates the subject and closes the active page.
        '''
        old_subject = get_subject_by_name(self.subject.text())
        subject_id = get_subject_id(old_subject.get_name())
        if self.txt_subject_name.text() != "" and self.txt_subject_name.text() != " ":
        
            old_subject.update_db_with_id(subject_id,self.txt_subject_name.text(),old_subject.get_questions_id())
        self.window.close()
        self.mainwindow.refresh_list()
        self.txt_subject_name.setText("")
        
        

def basic_input_checker(input):
    '''
    Function which checks if the given input is empty or contains only a space. If its the case the placeholder is replaced with an error message
    and the function returns False. If everything is fine the function returns True.
    @returns Boolean => represent if the test are passed correctly (True) or not (False)
    '''
    if not input.text() or input.text()==" " or input.text()=="":
        input.setText("")
        input.setPlaceholderText("Insérer une valeur valable")
        return False
    else:
        return True
    
def textArea_input_checker(input):
    '''
    Function which checks if the given input is empty or contains only a space. If its the case the placeholder is replaced with an error message
    and the function returns False. If everything is fine the function returns True.
    @returns Boolean => represent if the test are passed correctly (True) or not (False)
    '''
    if not input.toPlainText() or input.toPlainText()==" " or input.toPlainText()=="":
        input.setText("")
        input.setPlaceholderText("Insérer une valeur valable")
        return False
    else:
        return True
    
def email_checked(input):
    '''
    Function which checks the input's validity for an email.
    '''
    email_regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(email_regex,input.text()):
        
        return True
    else:
        input.setText("")
        input.setPlaceholderText("Votre email est invalide.")
        return False



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
