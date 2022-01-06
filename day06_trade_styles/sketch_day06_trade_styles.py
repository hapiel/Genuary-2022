import vsketch
from shapely import geometry, affinity
import numpy as np

import sys, os
sys.path.append(os.path.join(os.path.abspath(__file__), "../../"))
import utils 

class Day06TradeStylesSketch(vsketch.SketchClass):
    
    rand_x = vsketch.Param(75)
    rand_y = vsketch.Param(55)
    points = vsketch.Param(3)

    line_step = vsketch.Param(0.5)
    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205x130mm", landscape=False)
        vsk.scale("mm")
        widthmm = utils.css_to_mm(vsk.width)

        line_coords = []
        line_count = widthmm / self.line_step

        for y in range(int(line_count)):
            y = vsk.map(y, 0, line_count , 0, widthmm)
            line_coords.append(((- widthmm/2,y - widthmm/2),(widthmm/2,y - widthmm/2)))
            
        lines = geometry.MultiLineString(line_coords)

        first_pos = (vsk.random(self.rand_x), vsk.random(self.rand_y) )
        prev_pos = first_pos

        for i in range(self.points):
            
            if i == self.points - 1:
                new_pos = first_pos
            else:
                sign = (-1, 1)[i % 2]
                new_pos = (vsk.random(self.rand_x) * sign , vsk.random(self.rand_y) * 2 - self.rand_y )

            triangle = geometry.Polygon([(0,0), new_pos, prev_pos])

            # I don't know why this angle finding works, took a lot of trial and error
            # I need to get better at trigonometry I guess :()
            angle = utils.find_angle((np.array(prev_pos) - np.array(new_pos), np.array(new_pos) - np.array(prev_pos))[prev_pos[1] < new_pos[1]], (0,0), (1,0))
            translated_lines = affinity.translate(lines, 0, vsk.random(self.line_step))
            rotated_lines = affinity.rotate(translated_lines, angle, use_radians=True)

            vsk.geometry(rotated_lines.intersection(triangle))

            prev_pos = new_pos


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort gwrite last.gcode")


if __name__ == "__main__":
    Day06TradeStylesSketch.display()
