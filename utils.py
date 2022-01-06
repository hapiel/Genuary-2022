import vsketch
import numpy as np

def css_to_cm(css):
    return vsketch.Vsketch.map(css, 0, 37.7952755905511811, 0, 1)

def css_to_mm(css):
    return vsketch.Vsketch.map(css, 0, 3.77952755905511811, 0, 1)

def clamp(num, _min, _max):
    return(max(_min, min(_max, num)))

def find_angle(a, b, c):
    # (x, y) for each parameter
    
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    ba = a-b
    bc = c-b

    cos_a = clamp(np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc)), -1, 1)
    return np.arccos(cos_a)