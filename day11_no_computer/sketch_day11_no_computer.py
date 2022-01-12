import vsketch
from shapely import geometry, affinity
import os

class Day11NoComputerSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")

        sub = vsketch.Vsketch()
        sub.vpype("text -a center 'computer' ")
        
        w = 190
        h = 120
        
        
        line_count = 100
        lines = []
        for y in range(line_count):
            y = vsk.map(y, 0, line_count, 0, h)
            
            lines.append(geometry.LineString([(0,y), (w, y)])) 
        
        
        mask = affinity.translate(geometry.Polygon([(-43,-10),(45,-10), (45,10), (-43,10)]), w/2-1, h/2)
        
        # vsk.geometry(mask)
        
        vsk.geometry(geometry.MultiLineString(lines).difference(mask))
        
        vsk.translate(w/2 -1 , h/2)
        
        vsk.sketch(sub)  

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        filename = os.path.basename(__file__)[7:-3]
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort gwrite {filename}.gcode")


if __name__ == "__main__":
    Day11NoComputerSketch.display()
