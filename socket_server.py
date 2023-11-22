import socket
from student import *
import json


HOST = socket.gethostbyname(socket.gethostname())

PORT = 1234

def new_client(conn, addr):
    '''
    Function which receives the exam from the client and then opens a window which allow the user to answer the questions.
    @return => student_exam: json file which represent all the student answers to this exam's questions
    '''
    print(f"new client {addr}")
    exam = conn.recv(1024)
    student_exam = ""
    if exam.decode() == "":
        print("no data received")
    else:
        if __name__ == "__main__":
            import sys
            app = QtWidgets.QApplication(sys.argv)
            Correction_UI = QtWidgets.QMainWindow()
            ui = Student_UI()
            ui.setupUi(Correction_UI,json.loads(exam.decode()))
            Correction_UI.show()
            app.exec_()
            student_exam=ui.get_json_returned()
    return student_exam
            


def get_connections():
    '''
    Function which initialize the listining of the server, it also sends back the student_exam to the client.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()

            exam_to_send = json.dumps(new_client(conn,addr))
            
            conn.sendall(exam_to_send.encode())
            print("datas sent succesfully")
        s.close()

get_connections()

