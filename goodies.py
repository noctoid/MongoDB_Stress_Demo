#!/usr/local/bin/python3
import time, datetime

def printWithTimestamp(*arg):
    o = "["+datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')+"] "
    for s in [str(i) for i in arg]:
        o += s
    print(o)

def prettyPrintDict(d, indent=0):
   for key, value in d.items():
      print('---' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('---' * (indent+1) + str(value))

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) finished in %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed


if __name__ == "__main__":
    # Some tests
    printWithTimestamp("Hello, world","!")
    d = {}
    for i in range(5):
        d[i] = dict(zip((1,2,3),(4,5,6)))
    prettyPrintDict(d)
