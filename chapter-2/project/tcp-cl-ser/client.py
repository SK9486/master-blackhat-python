
import socket  as sc
soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
port = 4000
ip = "localhost"
conn = soc.connect((ip,port))
(ip,pt) = soc.getsockname()
while True:
    mess = input(ip+" : ")
    if(mess == "" or mess == "exit"):
        break
    soc.send(mess.encode())
    rep = soc.recv(1078)
    print(ip+" : "+rep.decode())
soc.close()
