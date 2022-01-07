import vsketch
from shapely import geometry, affinity
import random

# inspired by Sol Lewitt Wall Drawing # 370 

class Day07SolLewittSketch(vsketch.SketchClass):
    
    line_count = vsketch.Param(17)
    scale = vsketch.Param(1.5)
    distance = vsketch.Param(2)

    cols = vsketch.Param(10)
    rows = vsketch.Param(5)

    pen_dist = vsketch.Param(0.8)
    strokes = vsketch.Param(2)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")
        vsk.scale( self.scale)

        vsk.penWidth(f"{self.pen_dist}mm")
        vsk.strokeWeight(self.strokes)
    


        line_coords = []
        self.line_count 

        for y in range(int(self.line_count)):
            y = vsk.map(y, 0, self.line_count -1, 0, 10)
            line_coords.append(((0,y),(10,y)))
            
        lines = geometry.MultiLineString(line_coords)
        
        dist = vsk.map(self.distance, 0, self.line_count -1, 0, 10) - 0.0001

        shapes = (
            geometry.Point(5,5).buffer(5 - dist),                                                               # circle
            geometry.Polygon([(dist,dist), (10 - dist ,dist), (10 - dist ,10 - dist ), (dist,10 - dist )]),     # square
            geometry.Polygon([(5, dist), (10 - dist, 10 - dist), (dist, 10 - dist)]),                           # triangle
            geometry.Polygon([(5, dist), (10-dist, 5), (5, 10-dist), (dist, 5)]) ,                              # diamond
            geometry.Polygon([(dist,dist), (10 - dist ,10 - dist ), (dist,10 - dist )]),                        # straight triangle
            geometry.Polygon([(dist*2, dist), (10 - dist*2, dist), (10 - dist*2, dist*2), (10 - dist, dist*2),  # cross
                (10 - dist, 10 - dist*2), (10-dist*2, 10-dist*2), (10 - dist*2, 10-dist), (dist*2, 10-dist), 
                (dist*2, 10-dist*2), (dist, 10-dist*2), (dist, dist*2), (dist*2, dist*2)]),                     
            geometry.Polygon([(dist*2, dist), (5, dist*3), (10 -dist * 2, dist), (10-dist, dist*2),             # diagonal cross
                (10- dist*3, 5),(10-dist, 10-dist*2), (10-dist*2, 10-dist), (5, 10-dist*3), (dist*2, 10-dist),  
                (dist, 10-dist*2), (dist*3 , 5), (dist, dist*2)]),
            geometry.Polygon([(dist*2, dist), (10-dist*2, dist), (10-dist, 10-dist), (dist, 10-dist)]),         # trapezoid
            geometry.Polygon([(dist*2, dist), (10-dist, dist), (10-dist*2, 10-dist),(dist, 10-dist)]),          # skewed
            geometry.Polygon([(dist*2, dist), (10-dist*2, dist), (10-dist*2, 10-dist), (dist*2, 10-dist)])      # rectangle
        )

        for y in range(self.rows):
            for x in range(self.cols):

                with vsk.pushMatrix():
                    vsk.translate(x*10,y * 10)

                    line_bg = affinity.rotate(lines, 90 * (x + y % 2))
                    line_shape = affinity.rotate(lines, 90 * (x + y + 1 % 2))
                    shape = random.choice(shapes)

                    line_bg = line_bg.difference(shape)
                    line_shape = line_shape.intersection(shape)

                    vsk.geometry(line_bg)
                    vsk.geometry(line_shape)



    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort gwrite last.gcode")


if __name__ == "__main__":
    Day07SolLewittSketch.display()
