from pymongo import *
from bson import ObjectId
from json import *

#the ip address of the database must be equivalent to the one below

CONNECTION_LINK = "mongodb://admin:password@10.205.201.100:27017/"
DB_NAME = "dbExamination"
COLLECTION_NAME_Q = "Question"
COLLECTION_NAME_E = "Examen"
COLLECTION_NAME_SUBJECT = "Subject"
COLLECTION_NAME_STUDENT_EXAM ="Examen_eleve"

question_collection = ''
examen_collection = ''

def connect():
    '''
        This function allows the programm to connect to the mongo database which is running inside a docker vm
    '''
    global question_collection,examen_collection,subject_collection,student_exam_collection
    client = MongoClient(CONNECTION_LINK)
    mydb = client[DB_NAME]
    question_collection = mydb[COLLECTION_NAME_Q]
    examen_collection = mydb[COLLECTION_NAME_E]
    subject_collection = mydb[COLLECTION_NAME_SUBJECT]
    student_exam_collection = mydb[COLLECTION_NAME_STUDENT_EXAM]

connect()

class Subject():
    '''
        Class representing the Matiere collection within the database.
    '''

    def __init__(self,name,questions_id=[]):
        '''
            Class Subject's constructor
        '''
        self.__name = name
        '''
            private attribute representing the name of the subject
        '''
        
        self.__questions_id = questions_id
        '''
            private attribute representing all the questions' id present in that specific subject
        '''


    def get_name (self):
        '''
            Getter method for the name attribute
            @returns self.__name => private name attribute 
        '''
        return self.__name
    
    def get_questions_id(self):
        '''
            Getter method for the questions' id attribute
            @returns self.__questions_id => private questions_id attribute 
        '''
        return self.__questions_id
    
    def insert_db(self):
        '''
            Method which allows the user to insert a subject inside the database. For this method to work, it needs a variable named
            subject_collection containing the connection string to the database.
        '''
        
        subject_collection.insert_one(self.create_json())

    def delete_db(self):
        '''
            Method which allows the user to delete a subject inside the database. For this method to work, it needs a variable named
            subject_collection containing the connection string to the database.
        '''
        subject_collection.delete_one({"nom": self.__name})
    
    def update_db(self,new_name,new_questions):
        '''
            Method which updates the subject informations within the database.
            @parameter new_name: represent the new name of the subject (string)
            @parameter new_questions: represent the new questions' id of the subject (list[string])
        '''
        id = self.find_subject_db()
        self.update_all(new_name,new_questions)
        json = self.create_json()
        subject_collection.update_one({"_id":id},{"$set":json})
    
    def update_db_with_id(self,id,new_name,new_questions):
        '''
            Method which updates the subject's informations within the database
            @parameter id: id of the subject within the database
            @parameter new_name: represent the new name of the subject (string)
            @parameter new_questions: represent the new questions' id of the subject (list[string])
        '''
        self.update_all(new_name,new_questions)
        json = self.create_json()
        subject_collection.update_one({"_id":id},{"$set":json})

    def update_all(self,new_name,new_questions_id):
        '''
            Method which updates all the informations within the subject's object.
            @parameter new_name: this parameter represent the new name of the subject
            @parameter new_questions_id: this parameter represent the new questions' id of the subject
        '''
        self.__name = new_name
        self.__questions_id = new_questions_id
    
    def create_json(self):
        '''
            Method which build the subject's json using the available datas
            @returns: returns the json of all the datas
        '''
        json_inserting = {"nom": self.__name, "questions":self.__questions_id}
        return json_inserting
    
    def find_subject_db(self):
        '''
            Method which serach through the database all the subject with the same name and returns the id of the first one.
            @returns: returns the first subject's id.
        '''
        subjects=list(subject_collection.find({"nom":self.__name}))
        subject = subjects[0]
        subject_id = subject["_id"]
        return subject_id

    def add_question(self,question_id):
        '''
            Method which handles the adding of a new question to this subject object and by modifying the database.
        '''
        subject_collection.update_one({"nom":self.__name},{"$push":{"questions":question_id}})
        self.__questions_id.append(question_id)



class Question:
    '''
        Class representing the question document from the database. This class is a class
        used for inheritance.
    '''
    
    def __init__ (self,type, content, subject,question_id = ""):
        '''
            Class question's constructor.
        '''
        self.__content = content
        '''
            private attribute representing the content of the question
        '''
        self.__subject = subject
        '''
            private attribute representing the subject of the question
        '''
        self.__type = type
        '''
            private attribute representing the type of the question
        '''
        
        self.__question_id = question_id
        '''
            private attribute representing the id of the question (if given)
        '''
        

    
    def get_type(self):
        '''
            Getter method for the type attribute
            @returns self.__type => private type attribute
        '''
        return self.__type

    def get_subject(self):
        '''
            Getter method for the subject attribute
            @returns self.__subject => private subject attribute
        '''
        return self.__subject
    
    def get_content(self):
        '''
            Getter method for the content attribute
            @returns self.__content => private content attribute
        '''
        return self.__content
    
    def get_id(self):
        '''
            Getter method for the id attribute
            @returns self.__id => private id attribute
        '''
        return self.__question_id
    
    def __set_id(self,new_id):
        '''
            Setter method for the __id attribute
        '''
        self.__question_id = new_id

    def set_content(self,new_content):
        '''
            Setter method for the __content attribute
        '''
        self.__content = new_content

    def set_type(self,new_type):
        '''
            Setter method for the __type attribute
        '''
        self.__type = new_type

    def set_subject(self,new_subject):
        '''
            Setter method for the __subject attribute
        '''
        self.__subject = new_subject

    def update_data(self,new_content="",new_type="",new_subject=""):
        '''
            Method which updates all the different data at once.
        '''
        if new_content != "":
            self.__content = new_content
        if new_type != "":
            self.__type = new_type
        if new_subject != "":
            self.__subject = new_subject
   
    def db_insert(self,json_inserting):
        '''
            Method which allows the user to insert a question inside the database. For this method to work, it needs a variable named
            questionCollection containing the connection string to the database.
        '''
        
        question_collection.insert_one(json_inserting)

    def db_delete(self):
        '''
            Method which allows the user to delete a question inside the database. For this method to work, it needs a variable named
            questionCollection containing the connection string to the database.
        '''
        
        question_collection.delete_one({"contenu": self.__content})

    def db_update(self,json_incerting):
        '''
            Method which allows the user to update a question inside the database. For this method to work, it needs a variable named
            questionCollection containing the connection string to the database.
            if the object doesn't have an id, the programm will search through the database to find the document based on its content and then it will update the document.
            @returns status_msg (string) => message containging the status of the update action.
        '''
        status_msg = ""
        if self.__question_id == "":
            # checks if the id is empty
            search_document = question_collection.find_one({"contenu": self.__content})

            if search_document:
                # checks if the query isn't empty
                self.__question_id = search_document["_id"]
                status_msg = "l'opération a été éffectuée avec succès."
            else:
                status_msg = "Aucune question correspondante trouvée dans la base de données. Veuillez insérer votre question avant de procéder à une mise à jour."

        
        question_collection.update_one({"_id":self.__question_id},{"$set": json_incerting})
        return status_msg
        

            
class QCM(Question):
    '''
        Class name QCM which inherits from the Question class. This class represents a specific type of question, the Multiple choice questions.
    '''
    def __init__(self,type, content,subject,options,answers,question_id=""):
        '''
            QCM class' constructor.
        '''
        super().__init__(type, content,subject,question_id)
        self.__options = options
        '''
            private attribute representing the answer's options of the question
        '''
        self.__answers = answers
        '''
            private attribute representing the correct answer of the question
        '''

    def get_options(self):
        '''
            Getter method for the options attribute
            @returns self.__options (list)=> private options attribute
        '''
        return self.__options
    
    def get_answers(self):
        '''
            Getter method for the answers attribute
            @returns self.__answers => private answers attribute
        '''
        return self.__answers
    
    def create_json(self):
        '''
            Method which creates the json file of the current object
            @returns: returns a json type file containing the object's informations
        '''
        json_inserting = {"type": self.get_type(), "contenu": self.get_content(), "branche": self.get_subject(), "option": self.__options, "solution": self.__answers}
        return json_inserting


    def update_data(self,new_content="",new_type="",new_subject="", new_options ="", new_answers =""):
        '''
            Method that updates all the question infomations at one.
        '''
        if new_content != "":
            self.set_content(new_content)
        if new_type != "":
            self.set_type(new_type)
        if new_subject != "":
            self.set_subject(new_subject)
        if new_options != "":
            self.__options = new_options
        if new_answers != "":
            self.__answers = new_answers

    def db_update(self):
        '''
            Method which allows the user to insert a question inside the database. For this method to work, it needs a variable named
            questionCollection containing the connection string to the database.
            if the object doesn't have an id, the programm will search through the database to find the document based on its content and then it will update the document
            @returns status_msg (string) => message containging the status of the update action.
        '''

        super().db_update(self.create_json())
    
    def db_insert(self):
        '''
            Method which allows the user to insert a question inside the database. For this method to work, it needs a variable named
            questionCollection containing the connection string to the database.
        '''
        super().db_insert(self.create_json())
       
    

class DEF(Question):
    '''
        Class name DEF which inherits from the Question class. This class represents a specific type of question, the definition question.
    '''
    def __init__ (self, type, content,subject,question_id=""):
        '''
            DEF's constructor method
        '''
        super().__init__(type, content,subject,question_id)
        
    def update_data(self,new_content="",new_type="",new_subject=""):
        '''
            Method that updates all the question infomations at one.
        '''
        if new_content != "":
            self.set_content(new_content)
        if new_type != "":
            self.set_type(new_type)
        if new_subject != "":
            self.set_subject(new_subject)
    
    def create_json(self):
        '''
            Method which creates the json file of the current object
            @returns: returns a json type file containing the object's informations
        '''
        json_inserting = {"type": self.get_type(), "contenu": self.get_content(), "branche": self.get_subject()}
        return json_inserting
    
    def db_insert(self):
        '''
            Method which allows the user to insert a question inside the database. For this method to work, it needs a variable named
            questionCollection containing the connection string to the database.
        '''
        super().db_insert(self.create_json())

    def db_update(self):
        '''
            Method which allows the user to insert a question inside the database. For this method to work, it needs a variable named
            questionCollection containing the connection string to the database.
            if the object doesn't have an id, the programm will search through the database to find the document based on its content and then it will update the document
            @returns status_msg (string) => message containging the status of the update action.
        '''
        super().db_update(self.create_json())
        


class Exam():
    '''
        Class named Exam, it represents the examen document within the database.
    '''
    def __init__ (self,name: str,teacher: object,questions:list,date: str):
        '''
            Class Exam's constructor.
        '''
        self.__name = name
        '''
            private attribute representing the name of the exam
        '''
        self.__teacher = teacher
        '''
            private attribute representing the teacher (object) giving the exam
        '''
        self.__questions = questions
        '''
            private attribute representing a list of IDs (string) from the questions document
        '''

        self.__date = date
        '''
            private attribute representing the date when the exam took place
        '''
        

    def get_name(self):
        '''
            Getter method for the name attribute
            @returns self.__name => private name attribute
        '''
        return self.__name
    
    def get_teacher(self):
        '''
            Getter method for the teacher attribute which is a Teacher object (possibility to use the getter of that class)
            @returns self.__teacher => private teacher attribute
        '''
        return self.__teacher
    
    def get_questions(self):
        '''
            Getter method for the questions attribute which is only the question's id as a string
            @returns self.__questions => private questions attribute
        '''
        return self.__questions
    
    def get_date(self):
        '''
            Getter method for the date attribute
            @returns self.__date => private date attribute
        '''
        return self.__date
    
    def set_questions(self,questions):
        '''
            Setter method for the __questions attribute
        '''
        self.__questions = questions
    
    def question_formating(self,questions_list):
        '''
            Function that determine the type of a question and then start the appropriate fromating frunction for it
        '''
        formated_question_list = []
        counter = 0
        for question in questions_list:
            if question["type"] == "qcm":
                formated_question_list.append(self.qcm_formating(question,counter))
                counter += 1
                
            elif question["type"] == "définition":
                formated_question_list.append(self.def_formating(question,counter))
                counter += 1

        return formated_question_list
    

    def qcm_formating(self,question, question_no):
        '''
        Method which takes a JSON and a question number and format this into an object corresponding to an object
        @parameter question (JSON) => JSON containing a question with its informations
        @parameter question_no (int) => parameter corresponding to the question number
        @returns number (QCM object) => returns a QCM object which contains all the necessary information for the question
        '''
        number = question_no 
        number = QCM(question["type"],question["contenu"] ,question["branche"],question["option"],question["solution"], question["_id"])
        return number
    
    def def_formating(self,question, question_no):
        '''
        Method which takes a JSON and a question number and format this into an object corresponding to an object
        @parameter question (JSON) => JSON containing a question with its informations
        @parameter question_no (int) => parameter corresponding to the question number
        @returns number (DEF object) => returns a DEF object which contains all the necessary information for the question
        '''
        number = question_no 
        number = DEF(question["type"],question["contenu"], question["branche"], question["_id"])
        return number

    
    def get_random_question(self, number_question):
        '''
            Method that allows the user to get random questions from the database and formating into QCM of DEF objects. Then it changes
            the question attribute of the Exam class to the list of questions formed with the different methods.
            @parameter number_question (int) => number representing the amount of random questions that the user wants.
        '''
        random_questions = list(question_collection.aggregate([{ "$sample": { "size": number_question }}]))
        list_random_question = self.question_formating(random_questions)
        self.set_questions(list_random_question)


    def db_insert(self):
        '''
            Method which allows the user to create an Examen document within the database. For this method to work, it requires a variable named examenCollection with the connection
            string to the right collection within the database.
        '''
        json_inserting = self.get_json()
        examen_collection.insert_one(json_inserting)
    
    def get_json(self):
        '''
            Method which allows the user to create the json corresponding to the exam datas.
            @returns: returns the json file containing all the datas
        '''
        json = {"nom": self.__name, "professeur": {"nom": self.__teacher.get_lastname(), "prenom": self.__teacher.get_firstname(),"email": self.__teacher.get_email()},"questions":self.__questions, "date": self.__date}
        return json
    


class Student_Exam():
    '''
        Class name Student_Exam, it represents the Examen_eleve document wihtin the database
    '''
    def __init__(self,name,student: object,student_answers: list, points = 0 ):
        '''
            Student_exam class' constructor.
        '''
        self.__name = name
        '''
            private attribute representing the name of the exam the student has completed.
        '''
        self.__student = student
        '''
            private attribute representing the student with his infos that has completed this exam.
        '''
        self.__student_answers = student_answers
        '''
            private attrbute representing all the student's answers with their respective questions.
        '''
        self.__points = points
        '''
            private attribute representing the student's points gotten in the exam (attribute generally set after the correction)
        '''

    def get_name(self):
        '''
            Getter method for the name attribute
            @returns self.__name => private name attribute
        '''
        return self.__name
    def get_student(self):
        '''
            Getter method for the student attribute which a Student object (possibility to use the getter methods of this class)
            @returns self.__student => private student attribute
        '''
        return self.__student
    def get_student_answers(self):
        '''
            Getter method for the student_answers attribute which is a list of a document
            @returns self.__student_answers => private student_answers attribute
        '''
        return self.__student_answers
    
    def get_points(self):
        '''
            Getter method for the points attribute which is a float of the total points gotten in the exam
            @returns self.__points => private points attribute
        '''
        return self.__points
    
    def set_points(self, points):
        '''
            Setter method fot the points attribute.
            @parameter points => points gotten by the student in his exam (float)
        '''
        self.__points = points
    
    def set_student_answer(self,new_student_answers):
        '''
        Setter for the student_answer private attribute
        @new_student_answers (String) => new student answer 
        '''
        self.__student_answers = new_student_answers

    def create_json(self):
        '''
            Method which build the subject's json using the available datas
            @returns: returns the json of all the datas
        '''
        json_inserting = {"nom": self.__name, "eleve":self.__student,"reponse_eleve":self.__student_answers,"points":self.__points}
        
        return json_inserting
    
    def insert_db(self):
        '''
            Method which allows the user to insert a subject inside the database. For this method to work, it needs a variable named
            subject_collection containing the connection string to the database.
        '''
        
        student_exam_collection.insert_one(self.create_json())

    def update_db(self,new_student_answer,new_points):
        '''
            Method which updates the subject informations within the database.
            @parameter new_name: represent the new name of the subject (string)
            @parameter new_questions: represent the new questions' id of the subject (list[string])
        '''
        id = self.find_student_exam_db()
        self.set_student_answer(new_student_answer)
        student_exam_collection.update_one({"_id":id},{"$set":{"reponse_eleve":new_student_answer,"points":new_points}})
    
    def find_student_exam_db(self):
        '''
            Method which serach through the database all the subject with the same name and returns the id of the first one.
            @returns: returns the first subject's id.
        '''
        student_exams=list(student_exam_collection.find({"$and":[{"nom":self.__name},{"eleve.email":self.__student["email"]}]}))
        student_exam = student_exams[0]
        student_exam_id = student_exam["_id"]
        return student_exam_id



class Student_Answer():
    '''
        Class name Student_Answer, it represents the reponse_eleve document within the database.
    '''
    def __init__(self,question: str,student_answer,points=0):
        '''
            Student_Answer's constructor
        '''
        self.__question = question
        '''
            private attribute representing the question within the exam and that goes with the student answer (id)
        '''
        self.__student_answer = student_answer
        '''
            private attribute representing the student's answer to the corresponding question
        '''
        self.__points = points
        '''
            private attribute representing the student's point gotten in this question (0 by default)
        '''

    def get_question(self):
        '''
            Getter method for the question attribute
            @returns self.__question => private question attribute
        '''
        return self.__question
    
    def get_student_answer(self):
        '''
            Getter method for the student_answer attribute
            @returns self.__student_answer => private student_answer attribute
        '''
        return self.__student_answer
    
    def get_points(self):
        '''
            Getter method for the points attribute
            @returns self.__points => private points attribute
        '''
        return self.__points
    
    def create_json(self):
        '''
            Method which create the Student_answer json with the database format
            @return: json_returned -> json file with all the informations
        '''
        json_returned = {"question":self.__question,"réponse":self.__student_answer,"points":self.__points}
        return json_returned
    
    

    
class Teacher():
    '''
        Class named Teacher, it represents the Professeur document within the Examen document
    '''
    def __init__ (self,firstname,lastname,email):
        '''
            Class Teacher's constructor.
        '''
        self.__firstname = firstname
        '''
            private attribute representing the firstname of the teacher
        '''
        self.__lastname = lastname
        '''
            private attribute representing the lastname of the teacher
        '''
        self.__email = email
        '''
            private attribute representing the email of the teacher
        '''
    
    def get_firstname(self):
        '''
            Getter method for the firstname attribute
            @returns self.__firstname => private firstname attribute
        '''
        return self.__firstname
    
    def get_lastname(self):
        '''
            Getter method for the lastname attribute
            @returns self.__lastname => private lastname attribute
        '''
        return self.__lastname
    
    def get_email(self):
        '''
            Getter method for the email attribute
            @returns self.__email => private email attribute
        '''
        return self.__email
    

class Student():
    '''
        Class named Student, representing the Eleve document within the database.
    '''
    def __init__(self,firstname,lastname,email,classe):
        '''
            Student class' constructor.
        '''
        self.__firstname = firstname
        '''
            private attribute representing the firstname of the student.
        '''
        self.__lastname = lastname
        '''
            private attribute representing the lastname of the student.
        '''
        self.__email = email
        '''
            private attribute representing the email of the student.
        '''
        self.__classe = classe
        '''
            private attribute representing the class the student is in.
        '''
    
    def get_firstname(self):
        '''
            Getter method for the firstname attribute
            @returns self.__firstname => private firstname attribute
        '''
        return self.__firstname
    
    def get_lastname(self):
        '''
            Getter method for the lastname attribute
            @returns self.__lastname => private lastname attribute
        '''
        return self.__lastname
    
    def get_email(self):
        '''
            Getter method for the email attribute
            @returns self.__email => private email attribute
        '''
        return self.__email
    
    def get_classe(self):
        '''
            Getter method for the classe attribute
            @returns self.__classe => private classe attribute
        '''
        return self.__classe
    
    def create_json(self):
        '''
            Method which create a json with all the student information with the database format
            @return: json_returned -> json file with all the information needed
        '''
        json_returned = {"prénom":self.__firstname,"nom":self.__lastname,"email":self.__email,"classe":self.__classe}
        return json_returned


def question_formating(questions_list):
    '''
        Function that determine the type of a question and then start the appropriate fromating frunction for it
    '''
    formated_question_list = []
    counter = 0
    
    for question in questions_list:
        if question["type"] == "qcm":
            
            formated_question_list.append(qcm_formating(question,counter))
            counter += 1
                
        elif question["type"] == "définition":
            formated_question_list.append(def_formating(question,counter))
            counter += 1

    return formated_question_list
    

def qcm_formating(question, question_no):
    '''
        Method which takes a JSON and a question number and format this into an object corresponding to an object
        @parameter question (JSON) => JSON containing a question with its informations
        @parameter question_no (int) => parameter corresponding to the question number
        @returns number (QCM object) => returns a QCM object which contains all the necessary information for the question
    '''
    number = question_no 
    number = QCM(question["type"],question["contenu"] ,question["branche"],question["option"],question["solution"], question["_id"])
    return number
    
def def_formating(question, question_no):
    '''
        Method which takes a JSON and a question number and format this into an object corresponding to an object
        @parameter question (JSON) => JSON containing a question with its informations
        @parameter question_no (int) => parameter corresponding to the question number
        @returns number (DEF object) => returns a DEF object which contains all the necessary information for the question
    '''
    number = question_no 
    number = DEF(question["type"],question["contenu"], question["branche"], question["_id"])
    return number

    
def random_question(number_question,subject,type):
    '''
        Method that allows the user to get random questions from the database and formating into QCM of DEF objects. Then it changes
        the question attribute of the Exam class to the list of questions formed with the different methods.
        @parameter number_question (int) => number representing the amount of random questions that the user wants.
    '''
    random_questions = list(question_collection.aggregate([{"$match":{"type":type, "branche":subject}},{ "$sample": { "size": number_question }}]))
    list_random_question = question_formating(random_questions)
    return list_random_question

def get_all_question():
    '''
        Function which gets all the questions present whitin the database.
        @returns: returns all the question's object
    '''
    all_question = list(question_collection.find({}))
    list_all_question = question_formating(all_question)
    return list_all_question

def get_questions_by_subject(subject_name):
    '''
        Function which get all the question of a sepcified subject passed down through parameters.
        @parameter subject_name (string) => name of the subject 
        @returns: returns the list of all the question's object.
    '''
    subject = list(subject_collection.find({"nom":subject_name}))
    for element in subject:
        
        subject_object = Subject(element["nom"],element["questions"])
        
        list_all_question = subject_object.get_questions_id()
        list_question_mongo = []
        list_question_object = []
        for question_id in list_all_question:
            list_question_mongo.append(question_collection.find({"_id":question_id}))

        for question in list_question_mongo:
            list_question_object.append(question_formating(question))

    return list_question_object

def get_all_subject():
    '''
        Function which gets all the subjects present within the database.
        @returns: returns the liste of all the subject's object.
    '''
    all_subject = list(subject_collection.find({}))
    list_all_subject = []
    for element in all_subject:
        subject_element = Subject(element["nom"],element["questions"])
        list_all_subject.append(subject_element)

    return list_all_subject

def get_question_by_content(content):
    '''
        Function which get a question's id using the content of the question.
        @parameter content (string) => content of the question 
        @returns: returns the id of the question
    '''
    id = ""
    questions = list(question_collection.find({"contenu":content}))

    for question in questions:
        id = question["_id"]
    return id

def get_question_by_id(id):
    '''
        Function which gets a question using its id.
        @parameter id (string) => id of the question 
        @returns list_question => list of questions found
    '''
    questions = list(question_collection.find({"_id":ObjectId(id)}))
    list_question = question_formating(questions)
    return list_question


def get_subject_by_name(name):
    '''
        Function which gets a subject using its name.
        @parameter name (string) => name of the subject 
        @returns the subject's object
    '''
    subjects = list(subject_collection.find({"nom":name}))
    new_subject = ""
    for subject in subjects:
        new_subject = Subject(subject["nom"],subject["questions"])
    return new_subject

def get_subject_id(name):
    '''
        Function which get the subjects in the database according to a name.
        @parameter name (string)=> represent the name of the subject
        @returns: returns the id of the subject
    '''
    subjects = list(subject_collection.find({"nom":name}))
    id = ""
    for subject in subjects:
        id = subject["_id"]
    return id


def get_student_exam_by_email(name,email):
    '''
    Function which serach within the database all the student exams realted to an exam name and a student's email.
    @returns => new_student_exam, a Student exam's object if it exists in the database.
    '''
    student_exams = list(student_exam_collection.find({"$and":[{"nom":name},{"eleve.email":email}]}))
    new_student_exam = ""
    if student_exams:
        for student_exam in student_exams:
            new_student_exam = Student_Exam(student_exam["nom"],student_exam["eleve"],student_exam["reponse_eleve"],student_exam["points"])
        return new_student_exam
    else:
        return None


def get_student_exam_by_exam(name):
    '''
    Function which search within the database, all the student exams related to the name of an exam.
    @return => student_exam_list, list of all the student_exam's object present in the database.
    '''
    student_exams = list(student_exam_collection.find({"nom":name}))
    student_exam_list = []
    if student_exams:
        for exam in student_exams:
            new_student_exam = Student_Exam(exam["nom"],exam["eleve"],exam["reponse_eleve"],exam["points"])
            student_exam_list.append(new_student_exam.create_json())
    else:
        student_exam_list = None
    return student_exam_list

def get_student_exam_by_student_name(lastname, firstname):
    '''
    Function which search within the database for student exams which have the same student information.
    @return => new_student_exam, student_exam's object corresponding
    '''
    student_exam = list(student_exam_collection.find({"$and":[{"eleve.nom":lastname},{"eleve.prénom":firstname}]}))
    new_student_exam = ""
    if student_exam:
        for student_exam in student_exam:
            new_student_exam = Student_Exam(student_exam["nom"],student_exam["eleve"],student_exam["reponse_eleve"],student_exam["points"])
        return new_student_exam
    else:
        return None
    

def get_all_exams():
    '''
    Function which search within the database all the exams.
    @return => exam_list, list of all the exams (json format) present in the database.
    '''
    exams_db = list(examen_collection.find())
    exam_list = []
    if exams_db:
        for exam in exams_db:
            new_teacher = Teacher(exam["professeur"]["prenom"],exam["professeur"]["nom"],exam["professeur"]["email"])
            new_exam = Exam(exam["nom"].strip(),new_teacher,exam["questions"],exam["date"])
            exam_list.append(new_exam.get_json())
    else:
        exam_list = None
    return exam_list

