
import sys, json, os

default_fn = "settings.json"

class Configuration(dict):
    def save(self, fn=default_fn):
        fd = open(fn,"w")
        json.dump(self,fd, indent=4, sort_keys=True)
        fd.close()

    def load(self, fn=default_fn):
        fd = open(fn,"r")
        self.update(json.load(fd))
        fd.close()

conf = Configuration()
if os.environ.get("SETTINGS"):
    conf.load(os.environ.get("SETTINGS"))
elif os.path.exists(default_fn):
    conf.load()
else:
    print("Warning: configuration not found!", file=sys.stderr)
