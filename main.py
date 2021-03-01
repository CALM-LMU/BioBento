def script_method(fn, _rcb=None):
    return fn
def script(obj, optimize=True, _frames_up=0, _rcb=None):
    return obj    
import torch.jit
torch.jit.script_method = script_method 
torch.jit.script = script

import os
os.environ['PATH'] += (os.path.dirname(os.path.realpath(__file__)))

from bentoml.server import start_dev_server

path = os.getcwd()

start_dev_server(os.path.join(path, 'bento_cpu'), 5000, False, False)