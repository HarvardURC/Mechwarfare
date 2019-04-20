import thread
import time
time.sleep(5)

class _CDC :
    def __init__(self):
        self.dev = "/dev/tty.usbmodem3671271"
        self.query = ""
    def read(self,_passarg):
        with open("/dev/tty.usbmodem3671271", "r") as readBuff:
            while True :
                ans = readBuff.readline()
                if ans:
                    print ans[:-2]
                time.sleep(0.001)
    def write(self,_passarg) :
        with open("/dev/tty.usbmodem3671271","a") as writeBuff:
            while True :
                if self.query != "":
                    writeBuff.write(self.query+"\n")
                    self.query = ""
                time.sleep(0.001)
CDC = _CDC()
thread.start_new_thread(CDC.read,(None,))
thread.start_new_thread(CDC.write,(None,))

while True:
    q = "SEND-TEST%02d"%2
    CDC.query = q+((64-len(q))*"\x00")
    time.sleep(0.1)
