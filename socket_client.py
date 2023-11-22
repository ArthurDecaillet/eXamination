import socket
import json
import threading
from correction import *



student_answers = []
old_list = []

HOST = socket.gethostbyname(socket.gethostname())

PORT = 1234


    

def connection(srv_address,srv_port,json_to_send,ui):
    '''
    Function which allows the connection to a particular server and sends it a json right away, containing the created exam.
    It also refreshes the page containing the student's exam.
    '''
    global old_list
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((srv_address, srv_port))
            s.settimeout(None)
            json_str = json.dumps(json_to_send)
            s.sendall(json_str.encode())
            do_continue = True
            
            while do_continue:
                data = s.recv(1024)
                if data != b'' and data != b'""' and data.decode() != "" and data.decode() != '""':
                    do_continue = False
                    
                    decoded_data = data.decode()
                    new_exam = json.loads(decoded_data)
                    student_answers.append(new_exam)
        
        has_changed = False
        if old_list != student_answers:
            
            old_list= student_answers.copy()
            has_changed = True
        if has_changed:
            
            ui.refresh_exam_list(old_list)
    except BaseException as e:
        print(f"can't connect {e}")
        


def connection_client(json_to_send,ui):
    '''
    Function which loops trhough all the servers of the room and start a thread on the connection function
    '''
    servers = []
    for i in range(15):
        servers.append((f"10.205.201."+str(200+i),1234))
    for server_address, server_port in servers:
            t = threading.Thread(target=connection, args=(server_address,server_port,json_to_send,ui))
            t.start()
            

