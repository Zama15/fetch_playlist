from sys import stdout
from traceback import format_exc

def log(msg: str):
  print(msg, file=stdout, flush=True)

def log_trace():
  print(format_exc(), file=stdout, flush=True)
