#!/usr/bin/env python3

"""
Client 
"""
import socket, requests


def create_request(request_type, file_name, host):
    return """%s /%s HTTP/1.1\r\nHost:%s\r\n\r\n""" %(request_type, file_name, host)
    

# def init():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((host, PORT))
#         # print(create_request(request_type, file_name, host))
#         s.sendall(create_request(request_type, file_name, host).encode())
#         data = s.recv(1024)
#     print('Received', repr(data))


def do_get(s, file_name, host):
    s.sendall(create_request("GET", file_name, host).encode())

def do_post(s, file_name, host):
    req_head = create_request("POST", file_name, host).encode()
    f = open(file_name, 'rb')
    req_data = f.read()
    f.close()
    req_head += req_data
    s.sendfile(file_name)


if __name__ == "__main__":
    host = '127.0.0.1'    # Server addr
    port = 4000           # Server port
    #request_type = "GET"
    file_name = 'public/index.html'

    request_type ="POST"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        ###########################
        if request_type =="GET":
            do_get(s, file_name, host)

        elif request_type =="POST":
            do_post(s, file_name, host)
        else:
            print("INVALID Request Type")
        # print(create_request(request_type, file_name, host))
        #s.sendall(create_request(request_type, file_name, host).encode())
        data = s.recv(1024)
        print('Received', repr(data))
    
    
