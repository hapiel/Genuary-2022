import sys, os
sys.path.append(os.path.abspath("D:\9mediatech\python\genuary"))

import vsketch
from shapely import geometry, affinity

import utils 

class Day03SpaceSketch(vsketch.SketchClass):
    
    bg_line_count = vsketch.Param(100)
    bg_step = vsketch.Param(0.3)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("200mmx125mm", landscape=False)
        vsk.scale("mm")

        
        bg_lines_coords = []
        bg_lines_coords_2 = []
        bg_lines_coords_3 = []

        bg_line_count = utils.css_to_mm(vsk.height) / self.bg_step

        for y in range(int(bg_line_count/3)):
            y = vsk.map(y, 0, bg_line_count /3, 0, utils.css_to_mm(vsk.height))
            bg_lines_coords.append(((-10,y),(210,y)))
            bg_lines_coords_2.append(((-10,y + self.bg_step),(210,y + self.bg_step)))
            bg_lines_coords_3.append(((-10,y + self.bg_step * 2),(210,y + self.bg_step * 2)))
        
        bg_lines = geometry.MultiLineString(bg_lines_coords)
        bg_lines_2 = geometry.MultiLineString(bg_lines_coords_2)
        bg_lines_3 = geometry.MultiLineString(bg_lines_coords_3)

        stars = geometry.MultiPoint([(10,10), (20,20), (20,50), (160,30)])
        # vsk.geometry(stars.buffer(10))

        circle = geometry.Point(100,62.5).buffer(40 , resolution=32)
        circle2 = geometry.Point(97,59.5).buffer(35 , resolution=32)
        circle3 = geometry.Point(96,58.5).buffer(34 , resolution=32)


        rect = geometry.Polygon([(0,0), (200,0), (200,125), (0,125)])

        
        space = rect.difference(circle).difference(stars.buffer(vsk.random(3)))
        space2 = rect.difference(circle2).difference(stars.buffer(vsk.random(3)))
        space3 = rect.difference(circle3).difference(stars.buffer(vsk.random(3)))
        
        # space2 = space2.difference(stars.buffer(5))

        vsk.geometry(bg_lines.intersection(space))
        vsk.geometry(bg_lines_2.intersection(space2))
        vsk.geometry(bg_lines_3.intersection(space3))
        



    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day03SpaceSketch.display()
