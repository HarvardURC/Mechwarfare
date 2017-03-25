
from botnet.logging import *

from subprocess import Popen, DEVNULL, PIPE, STDOUT

import atexit
import asyncio

VIDEO_PORT = 6868
CMD1 = ("netcat",)
CMD2 = ("mplayer", "-fps", "60", "-cache", "1024", "-cache-min", "1", "-")
GST = ("gst-launch-1.0", "udpsrc", "port={}", "!",
       "application/x-rtp,payload=96", "!", "rtph264depay", "!", "avdec_h264",
       "!", "autovideosink", "sync=false")

VIDOPTS = [
    {"width": 1920, "height": 1080},
    {"width": 1280, "height": 720}
]

class Client:
    def __init__(self, addr):
        self.server = addr
    
    def fatal(self, message):
        log(message)
        log("Quitting...")
        exit()

    def connected(self, protocol):
        self.protocol = protocol
        self.vidopts = 0
        self.video()

    def video(self, toggle=False):
        if hasattr(self, "proc1"):
            self.proc1.kill()
            self.proc1.wait(1)
        if toggle:
            self.vidopts += 1
            if self.vidopts >= len(VIDOPTS):
                self.vidopts = 0
        cmdline = list(GST)
        cmdline[2] = cmdline[2].format(VIDEO_PORT)
        self.proc1 = Popen(cmdline, stderr=STDOUT,
                           stdout=get_log_fd("gstreamer"))
        atexit.register(self.proc1.kill)
        asyncio.get_event_loop().call_later(3, self.send_VSTR)

    def send_VSTR(self):
        self.protocol.send_message("VSTR", VIDEO_PORT, 0,
                                   VIDOPTS[self.vidopts])
        
    def VSTR(self, port, val=None):
        pass
