import socket as sc
def client():
    proxy_ip = input("Enter proxy ip address : ")
    proxy_port = int(input("Enter port no :"))
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
    ser_ip = input("Enter ip address : ")
    ser_port = int(input("Enter port no :"))
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
    proxy_ip = input("Enter proxy ip address : ")
    proxy_port = int(input("Enter port no :"))
    ser_ip = input("Enter ip address : ")
    ser_port = int(input("Enter port no :"))
    try :
        # proxy ==> server for clients
        p_soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        p_soc.bind((proxy_ip,proxy_port))
        p_soc.listen()
        print(f"proxy listening for client request at {proxy_ip}::{proxy_port}")
        (cl_soc,cl_add) = p_soc.accept()
        (cl_ip,cl_port) = cl_add
        print(f"proxy got an client request from {cl_ip}::{cl_port}")
        # proxy ==> act as an client to the server
        s_soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        s_soc.connect((ser_ip,ser_port))
        print(f"proxy connected to the server at {ser_ip}::{ser_port}")
        while 1 :
            serv_res = s_soc.recv(4096)
            if not serv_res:
                print("server stopped the connection")
                # cl_soc.shutdown(sc.SHUT_WR)
                break
            print("Server responded : ",serv_res.decode(),"forwading to the client...")
            cl_soc.send(serv_res)
        while 1:
            cl_res = cl_soc.recv(4096)
            if not cl_res:
                print("client stooped the connection")
                # cl_soc.shutdown(sc.SHUT_WR)
                break
            print("Client responded : ",cl_res.decode(),"forwading to the server...")
    except Exception as e:
        print("error ocuur (proxy side) : ",e)
    finally:
        s_soc.close()
        cl_soc.close()
        p_soc.close()

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

main()