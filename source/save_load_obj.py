import pickle
import os
script_dir = os.path.dirname(__file__)

def save_obj(obj, name):
    with open(os.path.join(script_dir, 'obj/'+ name + '.pkl'), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(os.path.join(script_dir, 'obj/'+ name + '.pkl'), 'rb') as f:
        return pickle.load(f)