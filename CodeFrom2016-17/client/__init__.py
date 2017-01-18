
from botnet.logging import *

from subprocess import Popen

VIDEO_PORT = 6000
CMDLINE = "netcat -l -p {port} | mplayer -fps 60 -cache 1024 -cache-min 1 -"

class Client:
    def fatal(self, message):
        log(message)
        log("Quitting...")
        exit()

    def connected(self, protocol):
        self.protocol = protocol
        self.video()

    def video(self, toggle=False):
        if hasattr(self, "proc"):
            self.proc.kill()
            self.proc.wait(1)
        self.proc = Popen(cmdline.format(VIDEO_PORT), shell=True)
        self.protocol.send_message("VSTR", VIDEO_PORT, 0)
        
