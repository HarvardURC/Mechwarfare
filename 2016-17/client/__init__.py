
from botnet.logging import *

from subprocess import Popen, DEVNULL, PIPE, STDOUT

import atexit
import asyncio
import pygame

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
        pygame.init()
        self.surface = pygame.display.set_mode((400, 200))
        pygame.display.set_caption("BabyMech Status")
        pygame.font.init()
        self.font = pygame.font.SysFont("Consolas", 20)
        asyncio.get_event_loop().call_soon(self.__pump_events)

    def __str__(self):
        return self.__js.get_name()

    def __pump_events(self):
        pygame.event.pump()
        pygame.display.flip()
        asyncio.get_event_loop().call_later(0.1, self.__pump_events)
    
    def fatal(self, message):
        log(message)
        log("Quitting...")
        exit()

    def connected(self, protocol):
        self.protocol = protocol
        self.vidopts = 0
        # self.video() # Don't start video automatically anymore

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

    def PANP(self, nil, pos):
        text = self.font.render("Pan: {:>7}".format(pos),
                                True, (255, 255, 255), (0,0,0))
        self.surface.blit(text, (10, 10))
        
    def TILT(self, nil, pos):
        text = self.font.render("Tilt: {:>7}".format(-pos),
                                True, (255, 255, 255), (0,0,0))
        self.surface.blit(text, (210, 10))
        
    def send_VSTR(self):
        self.protocol.send_message("VSTR", VIDEO_PORT, 0,
                                   VIDOPTS[self.vidopts])
        
    def VSTR(self, port, val=None):
        pass

    def OERR(self, *data, **kwargs):
        error("\aMotor overload error!\a")
