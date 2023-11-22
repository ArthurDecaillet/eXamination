
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from ORM import *
import json



class Ui_correction_ui(object):
    def setupUi(self, correction_ui,json_received,exam):
        correction_ui.setObjectName("correction_ui")
        correction_ui.resize(791, 587)
        self.centralwidget = QtWidgets.QWidget(correction_ui)

        self.lst_exam_correction = QtWidgets.QListWidget(self.centralwidget)
        self.lst_exam_correction.setGeometry(QtCore.QRect(195, 40, 351, 461))

        self.lst_exam_correction.itemDoubleClicked.connect(self.handle_subject_Dclick)

        self.btn_correction_save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_correction_save.setGeometry(QtCore.QRect(330, 510, 75, 23))

        

        correction_ui.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(correction_ui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 791, 21))
        self.menubar.setObjectName("menubar")

        correction_ui.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(correction_ui)
        self.statusbar.setObjectName("statusbar")

        correction_ui.setStatusBar(self.statusbar)
        self.exam = exam
        self.json = json_received
        self.refresh_exam_list(json_received)

        self.retranslateUi(correction_ui)
        QtCore.QMetaObject.connectSlotsByName(correction_ui)

    def retranslateUi(self, correction_ui):
        _translate = QtCore.QCoreApplication.translate
        correction_ui.setWindowTitle(_translate("correction_ui", "MainWindow"))
        self.btn_correction_save.setText(_translate("correction_ui", "Enregistrer"))

    def refresh_exam_list(self,json_received):
        '''
        Method which refreshes the student's exam list and the graphic interface that goes with it
        '''
        

        self.lst_exam_correction.clear()
        self.json = json_received
        for exam in self.json:
            student_exam_db = get_student_exam_by_email(exam["nom"],exam["eleve"]["email"])
            if student_exam_db == None:
                new_student = Student(exam["eleve"]["prénom"],exam["eleve"]["nom"],exam["eleve"]["email"],exam["eleve"]["classe"])
                new_exam = Student_Exam(exam["nom"],new_student.create_json(),exam["reponse_eleve"])
                
                new_exam.insert_db()
                
            firstname = exam["eleve"]["prénom"]
            lastname = exam["eleve"]["nom"]
            student = f"{firstname} {lastname}"
            item = QtWidgets.QListWidgetItem(student,self.lst_exam_correction)

    def handle_subject_Dclick(self, student):
        '''
        Method which handles the double click of an exam and open the window with this exam's informations
        '''

        json_index = self.lst_exam_correction.row(student)
        exam_json = self.json[json_index]

        self.window = QtWidgets.QMainWindow()
        self.ui = Exam_correction_UI()
        self.ui.setupUi(self.window,exam_json)
        self.window.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.window.show()
        


class Exam_correction_UI(object):
    def setupUi(self, Correction_UI,json):
        Correction_UI.setObjectName("Correction_UI")
        Correction_UI.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Correction_UI)
        self.centralwidget.setObjectName("centralwidget")

        self.mainwindow = Correction_UI
        self.json = json
        self.is_correcting = True

        self.correction_scroll = QtWidgets.QScrollArea(self.centralwidget)
        self.correction_scroll.setGeometry(QtCore.QRect(30, 30, 741, 511))
        self.correction_scroll.setWidgetResizable(True)
        self.correction_scroll.setObjectName("correction_scroll")
        self.correction_scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.correction_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.correction_scroll.setWidgetResizable(True)


        
        
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.btn_correction_save=QtWidgets.QPushButton()
        
        self.btn_correction_save.setText("Enregistrer")
        
        self.btn_correction_save.clicked.connect(self.handle_btn_correction_save)
        
        self.teacher_points = {}
        self.current_document_index = 0
        
        if get_student_exam_by_email(self.json["nom"],self.json["eleve"]["email"]) == None:
            self.handle_correction_display()
        else:
            self.handle_correction_display_db()


        

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 3, 121, 20))
        self.label.setObjectName("label")

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
        self.label.setText(_translate("Correction_UI", "Correction des examens"))

    

    def handle_correction_display(self):
        '''
        Method which manages the display of the different questions from the exam clicked with the json received information. This method happens only the first time the user open the exam.
        '''
        scrollContent = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout()
        self.teacher_points = {}
        student_label = QtWidgets.QLabel()
        
        
        lastname = self.json["eleve"]["nom"]
        firstname = self.json["eleve"]["prénom"]
        email = self.json["eleve"]["email"]
        classe = self.json["eleve"]["classe"]
        student_label.setText(f"nom: {lastname}\nprénom: {firstname}\nemail:{email}\nclasse: {classe}")
        scroll_layout.addWidget(student_label)

        self.teacher_points.clear()
        counter = 0
        for questions in self.json["reponse_eleve"]:
            db_question = get_question_by_id(questions["question"])
            question = db_question[0]
            
            question_widget = QtWidgets.QWidget()
            question_layout = QtWidgets.QVBoxLayout()
            lbl_content = QtWidgets.QLabel()
            student_answer = QtWidgets.QLabel()
            
            counter += 1
            
            lbl_content.setText(f"Question n°{counter} : " + question.get_content())
            
            
            if question.get_type() == "qcm":

                points = auto_correct(2, question.get_answers(), questions["réponse"])
                student_answers = ""
                for answer in questions["réponse"]:
                    student_answers += answer + " "
                student_answer.setText("Réponse de l'élève: " + student_answers + f"\npoints obtenus: {points}")
                question_layout.addWidget(lbl_content)
                question_layout.addWidget(student_answer)
            else:
                student_answer.setText("Réponse de l'élève: " + questions["réponse"])
                teacher_point = QtWidgets.QDoubleSpinBox()
                teacher_point.setValue(questions["points"])
                teacher_point.setSingleStep(0.5)
                self.teacher_points[question] = teacher_point
                question_layout.addWidget(lbl_content)
                question_layout.addWidget(student_answer)
                question_layout.addWidget(teacher_point)
            question_widget.setLayout(question_layout)
            scroll_layout.addWidget(question_widget)
            
            scroll_layout.addWidget(self.btn_correction_save)
            scrollContent.setLayout(scroll_layout)
            self.correction_scroll.setWidget(scrollContent)
        
            
    def handle_correction_display_db(self):
        '''
        Method which manages the display of the different questions from the exam clicked with the database informations
        '''
        student_exam = get_student_exam_by_email(self.json["nom"],self.json["eleve"]["email"])
        student_exam_json = student_exam.create_json()
        scrollContent = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout()
        self.teacher_points = {}
        student_label = QtWidgets.QLabel()
        
        
        lastname = student_exam_json["eleve"]["nom"]
        firstname = student_exam_json["eleve"]["prénom"]
        email = student_exam_json["eleve"]["email"]
        classe = student_exam_json["eleve"]["classe"]
        student_label.setText(f"nom: {lastname}\nprénom: {firstname}\nemail:{email}\nclasse: {classe}")
        scroll_layout.addWidget(student_label)

        self.teacher_points.clear()
        counter = 0
        for questions in student_exam_json["reponse_eleve"]:
            db_question = get_question_by_id(questions["question"])
            question = db_question[0]
            
            question_widget = QtWidgets.QWidget()
            question_layout = QtWidgets.QVBoxLayout()
            lbl_content = QtWidgets.QLabel()
            student_answer = QtWidgets.QLabel()
            
            counter += 1
            
            lbl_content.setText(f"Question n°{counter} : " + question.get_content())
            
            
            if question.get_type() == "qcm":
                
                points = auto_correct(2, question.get_answers(), questions["réponse"])
                student_answers = ""
                for answer in questions["réponse"]:
                    student_answers += answer + " "
                student_answer.setText("Réponse de l'élève: " + student_answers + f"\npoints obtenus: {points}")
                question_layout.addWidget(lbl_content)
                question_layout.addWidget(student_answer)
            else:
                student_answer.setText("Réponse de l'élève: " + questions["réponse"])
                teacher_point = QtWidgets.QDoubleSpinBox()
                teacher_point.setValue(questions["points"])
                teacher_point.setSingleStep(0.5)
                self.teacher_points[question] = teacher_point
                question_layout.addWidget(lbl_content)
                question_layout.addWidget(student_answer)
                question_layout.addWidget(teacher_point)
            question_widget.setLayout(question_layout)
            scroll_layout.addWidget(question_widget)
            
            scroll_layout.addWidget(self.btn_correction_save)
            scrollContent.setLayout(scroll_layout)
            self.correction_scroll.setWidget(scrollContent)
        

    def handle_btn_correction_save(self):
        '''
        Method which handle the press of the save correction button and the insert/update of the different Student_exam within the database
        '''
        list_student_answer = []
        total_points = 0
        
        for question, points in self.teacher_points.items():
            for response in self.json["reponse_eleve"]:
                if response['question'] == str(question.get_id()):
                    new_student_answer = Student_Answer(question.get_id(),response["réponse"],points.value())
                    list_student_answer.append(new_student_answer.create_json())

                
            total_points+=points.value()
        for questions in self.json["reponse_eleve"]:
            db_question = get_question_by_id(questions["question"])
            question = db_question[0]
            if question.get_type() == "qcm":
                points = auto_correct(2, question.get_answers(), questions["réponse"])
                total_points+=points
                new_student_answer = Student_Answer(question.get_id(),questions["réponse"],points)
                list_student_answer.append(new_student_answer.create_json())
        if get_student_exam_by_email(self.json["nom"],self.json["eleve"]["email"]) == None:
            new_corrected_exam = Student_Exam(self.json["nom"],self.json["eleve"],list_student_answer,total_points)
            new_corrected_exam.insert_db()
        else:
            
            uncorrected_student_exam = get_student_exam_by_email(self.json["nom"],self.json["eleve"]["email"])
            uncorrected_student_exam.update_db(list_student_answer,total_points)
            
        
        self.mainwindow.close()

    

    


def correction_main(json):
    '''
        Main correction function
        @parameter json: json containing all the informations from the student's exams
    '''
    points_per_qcm = 4
    points_per_def = 4
    total_points = 0
    student_points = 0
    grade = []
    for document in json:
        for questions in document["réponse_élève"]:
            db_question = get_question_by_id(questions["question"])
            for question in db_question:
                content = question.get_content()
                student_answer = questions["réponse"]
                if question.get_type() == "qcm":
                    student_points += auto_correct(points_per_qcm,question.get_answers(),student_answer)
                    total_points += points_per_qcm
                    
                elif question.get_type() == "définition":
                    student_points += teacher_correct(question,questions["réponse"])
                    total_points += points_per_def
        grade.append(grade_calculator(total_points,student_points))
    return grade
    

def auto_correct(points,solution,student_answer):
    '''
        Function which automatically correct the question and calculate the points received
        @parameter points: number of points the questions posesses
        @parameter solution: list of all the correct answers of the question (list[string])
        @parameter student_answer: list of all the student answers to the question (list[string])
        @returns: the number of points gotten in this question by the student. 
    '''
    result = points
    point_per_answer = points/4*len(solution)
    if solution == student_answer:
        result = points
    else:
        non_common_elements = [element for element in solution if element not in student_answer]
        number_missing_answer = len(non_common_elements)
        result -= number_missing_answer*point_per_answer
        if len(student_answer) > len(solution):
            errors = len(student_answer)-len(solution)
            result -= errors*point_per_answer
    if result < 0:
        result = 0
    return result


def teacher_correct(question,answer):
    '''
        Function which asks the teacher to give an answer points according to the student's answer.
        @parameter question: Question's object
        @parameter answer: list of all the student's answer to the question (list[string])
        @returns: the number of point gotten in this question by the student.
    '''
    points = round(float(input(f"question: {question.get_content()}\n réponse: {answer}\n combien de points? ")),1)
    return points


def grade_calculator(total, points):
    '''
        Function which calculate the grade of the student according to the number of points gotten and the total of points. (calculated according to the swiss way)
        @parmater total: total of points of the exam (float)
        @parameter points: total of points gotten by the students in this exam (float)
        @returns: the grade gotten by the student (float)
    '''
    grade = round(points/total*5+1,2)
    return grade

