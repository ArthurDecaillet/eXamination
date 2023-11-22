
from PyQt5 import QtCore, QtGui, QtWidgets
from ORM import *
from random import shuffle



class Student_UI(object):
    def setupUi(self, Correction_UI,json):
        Correction_UI.setObjectName("Correction_UI")
        Correction_UI.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Correction_UI)
        self.centralwidget.setObjectName("centralwidget")
        self.mainwindow = Correction_UI
        self.json = json
        self.is_correcting = True
        self.json_returned = ""

        self.question_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.question_scroll.setGeometry(QtCore.QRect(30, 30, 741, 511))
        self.question_scroll.setWidgetResizable(True)
        self.question_scroll.setObjectName("correction_scroll")
        self.question_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.question_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.question_scroll.setWidgetResizable(True)

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.btn_exam_save=QtWidgets.QPushButton()
        
        self.btn_exam_save.setText("Enregistrer")
        
        self.btn_exam_save.clicked.connect(self.handle_btn_exam_save)
        
        


        self.handle_questions_display()
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 3, 121, 20))
        self.label.setText(f"{self.json['nom']}")

        Correction_UI.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(Correction_UI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        Correction_UI.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(Correction_UI)
        self.statusbar.setObjectName("statusbar")

        Correction_UI.setStatusBar(self.statusbar)

        self.retranslateUi(Correction_UI)
        QtCore.QMetaObject.connectSlotsByName(Correction_UI)

    def retranslateUi(self, Correction_UI):
        _translate = QtCore.QCoreApplication.translate
        Correction_UI.setWindowTitle(_translate("Correction_UI", "MainWindow"))

    def handle_questions_display(self):
        '''
        Method which manages the display of the different questions from each and every exam
        '''
        scrollContent = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout()
        student_layout = QtWidgets.QFormLayout()
        student_widget = QtWidgets.QWidget()

        lbl_student_infos = QtWidgets.QLabel()
        lbl_student_infos.setText("informations de l'éléve")
        
        self.lbl_student_firstname = QtWidgets.QLabel()
        self.lbl_student_firstname.setText("Prénom:")

        self.txt_student_firstname = QtWidgets.QLineEdit()
        self.txt_student_firstname.setFixedWidth(150)
        
        self.lbl_student_lastname = QtWidgets.QLabel()
        self.lbl_student_lastname.setText("Nom:")

        self.txt_student_lastname = QtWidgets.QLineEdit()
        self.txt_student_lastname.setFixedWidth(150)

        self.lbl_student_email = QtWidgets.QLabel()
        self.lbl_student_email.setText("Email:")

        self.txt_student_email = QtWidgets.QLineEdit()
        self.txt_student_email.setFixedWidth(200)

        self.lbl_student_class = QtWidgets.QLabel()
        self.lbl_student_class.setText("Classe:")

        self.txt_student_class = QtWidgets.QLineEdit()
        self.txt_student_class.setFixedWidth(150)

        self.option_widget_list = []
        self.student_answer_dict = {}

        student_layout.setWidget(0,QtWidgets.QFormLayout.LabelRole,self.lbl_student_firstname)
        student_layout.setWidget(0,QtWidgets.QFormLayout.FieldRole,self.txt_student_firstname)
        student_layout.setWidget(1,QtWidgets.QFormLayout.LabelRole,self.lbl_student_lastname)
        student_layout.setWidget(1,QtWidgets.QFormLayout.FieldRole,self.txt_student_lastname)
        student_layout.setWidget(2,QtWidgets.QFormLayout.LabelRole,self.lbl_student_email)
        student_layout.setWidget(2,QtWidgets.QFormLayout.FieldRole,self.txt_student_email)
        student_layout.setWidget(3,QtWidgets.QFormLayout.LabelRole,self.lbl_student_class)
        student_layout.setWidget(3,QtWidgets.QFormLayout.FieldRole,self.txt_student_class)
        
        scroll_layout.addWidget(lbl_student_infos)
        student_widget.setLayout(student_layout)
        scroll_layout.addWidget(student_widget)
        counter = 0
        
        shuffled_question_list = self.json["questions"].copy()
        shuffle(shuffled_question_list)
        for question_id in shuffled_question_list:
            db_question = get_question_by_id(question_id)
            question = db_question[0]
            
            question_widget = QtWidgets.QWidget()
            question_layout = QtWidgets.QVBoxLayout()
            lbl_content = QtWidgets.QLabel()
            
            counter += 1
            
            lbl_content.setText(f"Question n°{counter} : " + question.get_content())
            question_layout.addWidget(lbl_content)
            
            
            if question.get_type() == "qcm":
                qcm_layout = QtWidgets.QVBoxLayout()
                qcm_widget=QtWidgets.QWidget()
                
                for option in question.get_options():
                    
                    ckb_option = QtWidgets.QCheckBox()
                    ckb_option.setText(option)
                    self.option_widget_list.append(ckb_option)
                    qcm_layout.addWidget(ckb_option)
                qcm_widget.setLayout(qcm_layout)
                question_layout.addWidget(qcm_widget)
                self.student_answer_dict[question] = self.option_widget_list

            else:
                
                txt_student_answer = QtWidgets.QLineEdit()
                question_layout.addWidget(txt_student_answer)
                self.student_answer_dict[question] = txt_student_answer

            question_widget.setLayout(question_layout)
            
            scroll_layout.addWidget(question_widget)
            
            scroll_layout.addWidget(self.btn_exam_save)
            scrollContent.setLayout(scroll_layout)
            self.question_scroll.setWidget(scrollContent)

    def handle_btn_exam_save(self):
        '''
        Method which handle the creation of the student_exam object which is later send in a JSON format to the socket client.
        '''
        current_student = Student(self.txt_student_firstname.text(),self.txt_student_lastname.text(),self.txt_student_email.text(),self.txt_student_class.text())
        student_answers = []
        sorted_dict = {}
        
        
        for id in self.json["questions"]:
            for key, value in self.student_answer_dict.items():
                if str(key.get_id()) == id:
                    sorted_dict[key] = value
                    break
                     
        
        for question,widgets in sorted_dict.items():
            if question.get_type() == "qcm":
                answers = []
                for element in widgets:    
                    if element.isChecked():
                        answers.append(element.text())
                new_answer = Student_Answer(str(question.get_id()),answers)
                
            else:
                new_answer = Student_Answer(str(question.get_id()),widgets.text())
            student_answers.append(new_answer.create_json())
        student_exam = Student_Exam(self.json["nom"],current_student.create_json(),student_answers)
        json_sent = student_exam.create_json()
        self.json_returned = json_sent
        self.mainwindow.close()
        
    
    def get_json_returned(self):
        '''
        Method which returns the exam's json.
        '''
        return self.json_returned


