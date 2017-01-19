
import pygame, asyncio, struct

from botnet.logging import *

def def_list(n):
    return list([0 for i in range(n)])

class KeyStick:
    def get_name(self):
        return "KeyStick shim"

    def get_button(self, i):
        keys = pygame.key.get_pressed()
        try:
            return keys[getattr(pygame, "K_{}".format(i))]
        except KeyError:
            warn("Invalid KeyStick key accessed")
            return False
    
class Joystick:
    def __init__(self, protocol, jid=0):
        pygame.init()
        pygame.display.iconify()
        self._protocol = protocol
        if pygame.joystick.get_count():
            self.__js = pygame.joystick.Joystick(jid)
            self.__js.init()
            self.axes = def_list(self.__js.get_numaxes())
            self.buttons = def_list(self.__js.get_numbuttons())
        else:
            warn("No joysticks found, falling back to keyboard shim.")
            self.axes = tuple()
            self.buttons = def_list(10)
            self.__js = KeyStick()
        asyncio.get_event_loop().call_soon(self.__pump_events)

    def __str__(self):
        return self.__js.get_name()

    def __pump_events(self):
        pygame.event.pump()
        self.check_axes()
        self.check_buttons()
        asyncio.get_event_loop().call_later(0.1, self.__pump_events)

    def _norm_axis(self, val):
        return round(val * 20) / 20

    def check_axes(self):
        for i, val in enumerate(self.axes):
            new = self._norm_axis(self.__js.get_axis(i))
            if new != val:
                self.axes[i] = new
                self._protocol.send_message("AXIS", i, new)
                
    def check_buttons(self):
        for i, val in enumerate(self.buttons):
            new = self.__js.get_button(i)
            if new != val:
                self.buttons[i] = new
                if i == 8:
                    if new:
                        self._protocol.receiver.video(True)
                elif i == 9:
                    if new:
                        self._protocol.receiver.fatal("START pressed.")
                else:
                    self._protocol.send_message("BUTN", i, new)
                
