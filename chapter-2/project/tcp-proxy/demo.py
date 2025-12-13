import threading
import time

# A global flag to control the thread
run_again = True

def worker():
    global run_again
    while True:
        # print "hello" 5 times
        for _ in range(5):
            print("hello")
            time.sleep(0.5)

        # after printing, wait for main thread to give input
        print("Waiting for input (y/n)...")
        
        # GLOBAL PAUSE: thread stops until main thread updates run_again
        while run_again is None:
            time.sleep(0.1)

        # if user says 'n' → exit the thread
        if run_again == False:
            print("Thread exiting...")
            return
        
        # reset for next cycle
        run_again = None


# ---------------------------
# MAIN THREAD
# ---------------------------
run_again = None
t = threading.Thread(target=worker)
t.start()

while True:
    user = input("Continue? (y/n): ").strip().lower()

    if user == "y":
        run_again = True
    elif user == "n":
        run_again = False
        break
    else:
        print("Enter only y/n.")
