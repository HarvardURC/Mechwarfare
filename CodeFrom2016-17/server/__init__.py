

class Bot:
    def add_client(self, c):
        pass

    def remove_client(self, c):
        pass

    def BUTN(self, id, val):
        fd = open("/sys/class/gpio/gpio{}/value".format(id+14), "w")
        print(id, val, fd.name)
        fd.write(str(int(val))+"\n")
