import socket as sc
import threading
from datetime import datetime

def client():
    # proxy_ip = input("Enter proxy ip address : ")
    proxy_ip = "127.0.0.1"
    # proxy_port = int(input("Enter port no :"))
    proxy_port = 8000
    try:
        soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        soc.connect((proxy_ip,proxy_port))
        print(f"client connected to the server : {proxy_ip}::{proxy_port}")
        while 1:
            res = soc.recv(4096)
            if not res:
                print("connection was closed by server")
                break
            print("Server :"+res.decode())
            mess = input("Enter : ")
            if mess == "" or mess == "exit":
                print("connection was closed by client")
                soc.shutdown(sc.SHUT_WR)
                break
            soc.send(mess.encode())
    except Exception as e:
        print("Error occured (clint side ) : ",e)
    finally:
        soc.close()

def server():
    ser_ip = "127.0.0.1"
    # ser_ip = input("Enter ip address : ")
    ser_port = 9000
    # ser_port = int(input("Enter port no :"))
    try :
        soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        soc.bind((ser_ip,ser_port))
        soc.listen()
        print("server listing for connections ....")
        (cl_sock,cl_add) = soc.accept()
        (cl_ip,cl_port) = cl_add
        print(f"Got connection request from {cl_ip}::{cl_port}")
        cl_sock.send("wlcome to the server ".encode())
        while 1 :
            resp = cl_sock.recv(4096)
            if not resp:
                print("client closed the connection")
                break    
            print(f"Client : {resp.decode()}")
            mess = input("Enter : ")
            if mess == "" or mess == "exit":
                print("server closed the connection")
                cl_sock.shutdown(sc.SHUT_WR)
                break
            cl_sock.send(mess.encode())
    except Exception as e:
        print(f"Error occur (server side) : {e}")
    finally:
        cl_sock.close()
        soc.close()
    
def proxy():
    # proxy_ip = input("Enter proxy ip address : ")
    proxy_ip = "127.0.0.1"
    # proxy_port = int(input("Enter port no :"))
    proxy_port = 8000
    # ser_ip = input("Enter ip address : ")
    ser_ip = "127.0.0.1"
    # ser_port = int(input("Enter port no :"))
    ser_port = 9000
    
    # printing those messages
    mode = None
    pattern = None

    # proxy input getting from user
    print('''
What do you want to capture?
    1. Client requests only
    2. Server responses only
    3. Keyword-based (e.g., "password")
    4. Capture everything
          ''')
    while 1:
        ch = int(input("Enter your choice : "))
        if(ch ==1):
            print("Client requests capture mode selected")
            write_logs("Client requests capture mode selected")
            mode = "CL"
            break
        elif(ch ==2):
            print("Server response capture mode selected")
            write_logs("Server response capture mode selected"+"\n"+"MODE : SR")
            mode = "SR"
            break
        elif (ch==4):
            print("all requests and response capture mode selected")
            write_logs("all requests and response capture mode selected"+"\n"+"MODE : ALL")
            mode = "ALL"
            break
        elif(ch == 3):
            print("capture based on keyword mode selected")
            mode = "KEY"
            pattern = input("Enter the pattern to capture (username,password...) : ")
            write_logs("capture based on keyword mode selected","\n"+"MODE : KEY"+"\n"+"PATTERN : "+pattern)
            break
        else:
            print("INVALID INPUT TRY AGAIN ...")
    try :
        # proxy ==> server for clients
        p_soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        p_soc.bind((proxy_ip,proxy_port))
        p_soc.listen()
        print(f"proxy listening for client request at {proxy_ip}::{proxy_port}")
        (cl_soc,cl_add) = p_soc.accept()
        (cl_ip,cl_port) = cl_add
        # proxy ==> act as an client to the server
        s_soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        s_soc.connect((ser_ip,ser_port))
        print(f"proxy connected to the server at {ser_ip}::{ser_port}")
        write_logs(f"proxy connected to the server at {ser_ip}::{ser_port}")
        cl_prox_th = threading.Thread(target=cl_prox,args=(cl_soc,s_soc,mode,pattern))
        sr_prox_th = threading.Thread(target=sr_prox,args=(cl_soc,s_soc,mode,pattern))
        cl_prox_th.start()
        sr_prox_th.start()
        cl_prox_th.join()
        sr_prox_th.join() 
    except Exception as e:
        print("error ocuur (proxy side) : ",e)
    finally:
        s_soc.close()
        cl_soc.close()
        p_soc.close()
        
def cl_prox(cl_soc,s_soc,mode,patt):
    # proxy ==> server for clients
    forward_type = None
    while 1:
        cl_res = cl_soc.recv(4096)
        if not cl_res:
            print("client stooped the connection")
            write_logs("client stooped the connection")
            # cl_soc.shutdown(sc.SHUT_WR)
            break
        cl_mess = cl_res.decode()
        if mode == "CL" or mode == "ALL":
            print(f"Client responded : ({cl_mess}) forwading to the server...")
            write_logs("MODE : CL TO SR"+"\n"+"MESSAGE : "+cl_mess)
        elif mode == "KEY":
            if patt in cl_mess:
                print(f"{patt} capture in the client responce")
                print(f"Client responce : {cl_mess}")
                write_logs("MODE : CL TO SR"+"\n"+"KEY : "+patt+"\n"+"MESSAGE : "+cl_mess)
        s_soc.sendall(cl_res)
        

def sr_prox(cl_soc,s_soc,mode,patt):
    while 1 :
        serv_res = s_soc.recv(4096)
        if not serv_res:
            print("server stopped the connection")
            write_logs("server stopped the connection")
            # cl_soc.shutdown(sc.SHUT_WR)
            break
        serv_mess = serv_res.decode()
        if mode == "SR" or mode == "ALL":
            print(f"Server responded : ({serv_mess}) forwading to the client...")
            write_logs("MODE : SR TO CL"+"\n"+"MESSAGE : "+serv_mess)
        elif mode == "KEY":
            if patt in serv_mess:
                print(f"{patt} capture in the server responce")
                print(f"Server responce : {serv_mess}")
                write_logs("MODE : CL TO SR"+"\n"+"KEY : "+patt+"\n"+"MESSAGE : "+serv_mess)
        cl_soc.sendall(serv_res)
    
def write_logs(mess):
    with open("proxy.log","a") as log_file:
        curr_time = datetime.now().strftime("%H:%M:%S")
        log_file.write(curr_time+"\n")
        log_file.write(mess+"\n")
        log_file.write("\n")
    
def read_log():
    with open("proxy.log","r") as log_file:
        print(log_file.read())

        
def main():
    print("-------------------")
    print("TCP PROXY SERVER")
    print("-------------------")
    print("1 . server")
    print("2 . client ")
    print("3 . proxy")
    ch = int(input("Enter your choise : "))
    if(ch == 1):
        print("-------------------")
        print("SERVER")
        print("-------------------")
        server()
    elif (ch == 2):
        print("-------------------")
        print("CLIENT")
        print("-------------------")
        client()
    elif (ch == 3):
        print("-------------------")
        print("PROXY")
        print("-------------------")
        proxy()
    else:
        print("invalid choice ...")
    read_log()

main()

# capture = None
#         if mode == "KEY":
#             capture = "CAPTURE BASED ON KEY"
#         elif mode == "CL":
#             capture = "CAPTURE CLIENTS REQUESTS ONLY MODE"
#         elif mode == "SR":
#             capture = "CAPTURE SERVER RESPONSE ONLY MODE"
#         else :
#             capture = "CAPTURE ALL MODE"