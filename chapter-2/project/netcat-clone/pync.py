import socket as sc
import threading
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="wallie-talkie program for secret communication")
    parser.add_argument("-l","--listen",help="enter True if you want to listen to the connection",action="store_true")
    parser.add_argument("-t","--target",help="enter the ip addres of the target",default="0.0.0.0")
    parser.add_argument("-p","--port",help="Enter the port of the taget",required=True,type=int)
    parser.add_argument("-m","--message",help="Enter the meaage you want to send",default="hello computer !!")
    args = parser.parse_args()
    print(args)
    if args.listen:
        print("---------- server mode selected  ----------")
        server_loop(args.target,args.port)
    else :
        if not args.target:
            print("######### client mode required target #########")
            sys.exit(1) #no target is sprecifed then get out of the program 
        client_sender(args.target,args.port,args.message)

def client_sender(ip,port,mess):
    soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM) #to accect ip add in the formate of ip and alow the the flow of data as steam 
    soc.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1) #to re-usage same address and port after killing the running to avoid os error sayng its already in use
    try:
        conn = soc.connect((ip,port))
        soc.send(mess.encode())
        while True:
            res = soc.recv(4096) # maintain the bit as 4096 because its common to use that 
            if not res:
                print("---------- connection was closed by the server  ----------")
                break
            print(f"{ip} : "+res.decode())
            new_mess = input("Enter : ")
            if(new_mess == ""):
                print("---------- connection was closed by the you  ----------")
                break
            soc.send(new_mess.encode())
    except Exception as e:
        print(f"######### error ocuured while connecting : {e} #########")
    finally:
        soc.close()

def server_loop(ip,port):
    try:
        soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
        soc.bind((ip,port))
        soc.listen()
        print(f"listening for incoming coneections on {ip}:{port}............")
        while True:
            (cl_soc,cl_add)=soc.accept()
            (cl_ip,cl_prt) = cl_add
            print(f"********** Got an connection from {cl_ip} **********")
            th = threading.Thread(target=handle_clients,args=(cl_soc,cl_ip))
            th.start()
    except Exception as e:
        print(f"######### error ocuured while connecting : {e} #########")
    finally:
        soc.close()
        cl_soc.close()

def handle_clients(cl_soc,cl_ip):
    while True:
        res = cl_soc.recv(4096)
        if not res:
             print("---------- connection was closed by the client  ----------")
             break
        print_lock = threading.Lock()
        with print_lock:
            print(f"{cl_ip}: "+res.decode())
            # to handle mutiple clients one should print at an time 
        new_mess = input("Enter : ")
        if(new_mess == ""):
            return
        cl_soc.send(new_mess.encode())
        
main()