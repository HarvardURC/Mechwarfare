from .settings import conf
import sys, time, os
import traceback as tb

DEFAULT_CONFIG = {
    "errors": 2,
    "warnings": 2,
    "debug": 2,
    "logging": 1,
    "folder": "."
}

settings = conf.get("logging",DEFAULT_CONFIG)

if conf.get("daemon") or settings.get("client"):
    DESCRIPTORS = [open(os.devnull, "w"),
                   open(os.path.join(settings.get("folder", "."),
                                     "output.log"), "a"),
                   open(os.path.join(settings.get("folder", "."),
                                     "errors.log"), "a")]
else:
    DESCRIPTORS = [open(os.devnull, "w"), sys.stdout, sys.stderr]

def _log(level, *args):
    fd = DESCRIPTORS[settings[level]]
    ts = time.strftime("[%m/%d/%y %H:%M:%S]")
    out = " ".join([ts] + [str(i) for i in args])
    out = out.replace("\n","\n" + ts + " ")
    fd.write(out + "\n")
    fd.flush()

def log(*args):
    _log("logging", *args)

def debug(*args):
    _log("debug", "Debug:", *args)

def warn(*args):
    _log("warnings", "Warning:", *args)

def error(*args):
    _log("errors", *args)

def last_exception():
    error(tb.format_exc())

__all__ = ["log", "debug", "warn", "error", "last_exception"]
