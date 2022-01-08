import vsketch
from shapely import geometry
import math

class Day08SingleCurveSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)
    
    detail = vsketch.Param(10)
    
    step1 = vsketch.Param(0.1)
    
    point_count = vsketch.Param(1000)
    
    min_val = vsketch.Param(3.28, decimals= 3)
    max_val = vsketch.Param(3.33, decimals= 3)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")

        vsk.scale(0.08)
        
        def curve_boy(val1, val2):
        
            points = []
            for i in range(self.point_count):
                x = math.sin(i / self.detail) * (10 + i * self.step1)
                y = math.cos(i / self.detail) * (10 + i * self.step1)
                
                x += math.sin(i / val1) * (10 + i * self.step1)
                y += math.cos(i / val2) * (10 + i * self.step1)
                

                points.append((x,y))

            vsk.geometry(geometry.LineString(points))
        
        
        for x in range(5):
            for y in range(3):
                
                if (y + 1) % 2 == 0:
                    x = 4 -x
                
                val1 = min(vsk.map(x +(y * 5 ), 0, 7, self.min_val, self.max_val), self.max_val)
                val2 = max(vsk.map(x + (y * 5), 7, 15, self.min_val, self.max_val), self.min_val)
                
            
                with vsk.pushMatrix():
                    vsk.translate(x*450, y * 450)
                    curve_boy(val1, val2)



    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort gwrite last.gcode")


if __name__ == "__main__":
    Day08SingleCurveSketch.display()
