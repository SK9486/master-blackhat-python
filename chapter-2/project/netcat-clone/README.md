argparger used to give inputs in the cmd
thread used to do independed muti procesing
sys use to read the cmds enter in the teminals

import argparse
def main():
    parser = argparse.ArgumentParser(description="Welcome the user")
    parser.add_argument("-n","--name",help="your name",required=True)
    parser.add_argument("-g","--group",help="your grp name",default="sk_creations")
    # (name,grp) = parser.parse_args()
    args = parser.parse_args()
    print(f"Hello {args.name} from {args.group} welcomes you to our project !! ")
main()



import threading
import time

def prog1():
    for i in range(1,6):
        print("p1: ",i)
        time.sleep(1)
def prog2():
    for i in range(1,6):
        print("p2: ",i)
        time.sleep(1)

t1 = threading.Thread(target=prog1)
t2 = threading.Thread(target=prog2)
t1.start()
t2.start()
t1.join()
t2.join()


import sys
args = sys.argv
for a in args:
    if(a == "exit"):
        print("exiting .."+"\n")
        sys.exit()
    else:
        print(a)


netcat clone projecr as per now we completed local version try it in wifi