#!/usr/bin/env python3

import socket, time, os, threading
     

class MyServer(object):
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.public_dir = 'public'
        self.host = host
        self.port = port
    
    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(5)
        while True:
            (client, address) = self.s.accept()
            client.settimeout(50)
            print('Connected by client ', address)
            threading.Thread(target=self._handle_client, args=(client, address)).start()
    
    def _handle_client(self, client, address):
        try:
            # self.s.bind((self.host, self.port))
            # self.s.listen()
            # self.conn, self.addr = self.s.accept()
            # print('Connected by client ', self.addr)
            #while True:
            data = client.recv(1024)
            if not data:
                print("NO DATAAA")
                client.close()
                #break
            self._handle_data(data, client)
            client.close()
        except Exception as e:
            print("ERROR!!", e)
 
    def _generate_headers(self, response_code):
        """ Generate HTTP response headers """
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Connection: close\n\n'
        return header

    # def _send_data(self, data_response):
    #     self.conn.send(data_response)
    #     return
    #     #self.conn.close()

    def _handle_data(self, data, client):
        parsed_req = data.decode().split()
        # print(parsed_req)
        file_requested =  parsed_req[1].split('?')[0]
        file_requested = os.path.join(self.public_dir, file_requested.split('/')[1])
        print("file_requested: ", file_requested)
        if parsed_req[0] == "GET":
            print("GET Request received from client for %s" %(parsed_req[1]))
            try:
                #print("file--", file)
                f = open(file_requested, 'rb')
                if parsed_req[0] == "GET":
                    response_data = f.read()
                f.close()
                response_header = self._generate_headers(200)
                response = response_header.encode()
                response += response_data
            except:
                print("File not found !")
                response_header = self._generate_headers(404)
                response = response_header.encode()
        
        elif(parsed_req[0] == "POST"):
            print("POST Request received from client for %s" %(parsed_req[1]))
            try:
                print("file--", parsed_req)
                f = open(file_requested, 'w')
                f.write("")
                f.close()
                response_header = self._generate_headers(200)
                response = response_header.encode()
            except:
                print("File not written !")
                response_header = self._generate_headers(404)
                response = response_header.encode()
        else:
            print("Wrong Request")
            response_header = self._generate_headers(404)

        print(response)
        # response = response_header.encode()
        # if parsed_req[0] == "GET":
        #     response += response_data
        #self._send_data(response)
        client.send(response)
        client.close()
        return
    
   


if __name__ == "__main__":
    HOST = '127.0.0.1'  
    PORT = 4000
    ms = MyServer(HOST, PORT)
    ms.start()

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by client ', addr)
#         while True:
#             data = conn.recv(1024)
#             print(data)
#             if not data:
#                 break
#             conn.sendall(data)
