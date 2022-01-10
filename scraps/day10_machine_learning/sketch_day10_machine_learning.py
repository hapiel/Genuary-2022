import vsketch

import sys, os
sys.path.append(os.path.join(os.path.abspath(__file__), "../../"))
import utils 

from svgpath2mpl import parse_path
from shapely import geometry
import xml.etree.ElementTree as etree
import svgutils
import vpype

# def svgfile_geometries(filepath):
    
#     svg = svgutils.transform.fromfile(filepath)
#     originalSVG = svgutils.compose.SVG(filepath)
    
#     originalSVG.scale(0.3)
#     originalSVG.rotate(90)
    
#     figure= svgutils.compose.Figure(50,100, originalSVG)

    
#     tree = etree.parse(filepath)
#     tree = etree.ElementTree(etree.fromstring(figure.tostr()))
#     root = tree.getroot()
    
    
#     path_elems = root.findall('.//{http://www.w3.org/2000/svg}path')
#     mpl_paths = [parse_path(elem.attrib['d']) for elem in path_elems]
    
#     geometries = []
#     for path in mpl_paths:
        
#         coords = path.to_polygons(closed_only=False)
        
#         geometries.append(geometry.LineString(coords[0]))
    
#     return geometries

def svgfile_geometries(filepath):
    
    tree = etree.parse(filepath)
    root = tree.getroot()
    
    
    path_elems = root.findall('.//{http://www.w3.org/2000/svg}path')
    mpl_paths = [parse_path(elem.attrib['d']) for elem in path_elems]
    
    geometries = []
    for path in mpl_paths:
        
        path._interpolation_steps=5
        
        coords = path.to_polygons(closed_only=False)
        
        geometries.append(geometry.LineString(coords[0]))
    
    return geometries

class Day10MachineLearningSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        
        
        svg_file = "D:/9mediatech/python/genuary/day10_machine_learning/single_curve.svg"
        # for geo in svgfile_geometries(svg_file):
        #     vsk.geometry(geo)
        
        sub = vsketch.Vsketch()
        sub.vpype(f"read -q 0.1mm {svg_file}")
        
        doc = vpype.read_multilayer_svg(svg_file, quantization=0.1)  # unit: px
        lid = 1
        for path in doc.layers[lid]:
            poly = geometry.LineString([(p.real, p.imag) for p in path])
        
            vsk.geometry(poly)
        vsk.sketch(sub)  # draw the subsketch in vsk, applying any transforms you may have
        
        vsk.scale("mm")
        
        vsk.square(10,0,10)
        
    


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day10MachineLearningSketch.display()
