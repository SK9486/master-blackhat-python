import socket as sc
soc = sc.socket(sc.AF_INET,sc.SOCK_STREAM)
port = 4000
ip = "0.0.0.0"
soc.bind((ip,port))
(ip,pt) = soc.getsockname()
print("waiting for connections ......")
soc.listen()
(cl_soc,cl_ip) = soc.accept()
(cl_name,cl_port) = cl_ip
print("Got one connection from : "+cl_name)
while True:
    rec = cl_soc.recv(1078)
    print(cl_name+" : "+rec.decode())
    mess = input(ip+": ")
    if(mess=='' or mess == "exit"):
        break
    cl_soc.send(mess.encode())
soc.close()
