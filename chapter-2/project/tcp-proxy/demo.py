from datetime import datetime
def write_logs(mess):
    with open("proxy.log","a") as log_file:
        log_file.write(mess+"\n")
    
def open_log():
    with open("proxy.log","r") as log_file:
        print(log_file.read())
        
def main():
    mess = input("Enter the mess : ")
    write_logs(mess)
    open_log() 
    curr_time = datetime.now().strftime("%H:%M:%S")
    print(curr_time)
    
main()
# [TIME]
# [ALERT]
# [CLIENT → SERVER]
# Matched pattern: password
# Payload: password=1234