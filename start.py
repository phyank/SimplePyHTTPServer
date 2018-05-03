from server import *

def setup():

    svr = LPServer("", 18080)
    svr.serve_forever()

setup()