import vsketch
import numpy as np
from svgpath2mpl import parse_path
from shapely import geometry
import xml.etree.ElementTree as etree


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

def svgfile_geometries(filepath):
    
    tree = etree.parse(filepath)
    root = tree.getroot()
    
    
    path_elems = root.findall('.//{http://www.w3.org/2000/svg}path')
    mpl_paths = [parse_path(elem.attrib['d']) for elem in path_elems]
    
    geometries = []
    for path in mpl_paths:
        
        coords = path.to_polygons(closed_only=False)
        
        geometries.append(geometry.LineString(coords[0]))
    
    return geometries