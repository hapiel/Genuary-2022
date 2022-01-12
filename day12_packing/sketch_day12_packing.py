
import vsketch
import sys, os
sys.path.append(os.path.join(os.path.abspath(__file__), "../../"))
import utils 
import math

from shapely import geometry, affinity

class Circle:
    
    def __init__(self, vsk,  other, xy=None, rand=1) -> None:
        
        self.o = other
        
        if xy == None:
            self.x = vsk.random(self.o.widthmm)
            self.y = vsk.random(self.o.heightmm)
        else:
            self.x = xy[0]
            self.y = xy[1]
        
        self.step_size = 1 + vsk.random(rand)
        self.r = self.o.radius_min + vsk.random(rand)
        self.r_max = vsk.random(self.o.radius_max/2, self.o.radius_max)
        
        
        
    def grow(self, circles):
        
        

        while self.r < self.r_max and not self.colliding(circles, self.step_size):
            
            self.r += self.step_size
        
    def draw_circle(self, vsk):
        vsk.circle(self.x, self.y, radius=self.r)
        
    def add_circle(self):
        return geometry.Point(self.x, self.y).buffer(self.r)
    
    def add_square(self):
        r = self.r * self.o.square_size
        square = geometry.Polygon([(-r/2, -r/2), (r/2, -r/2), (r/2,r/2), (-r/2, r/2)])
        square = affinity.translate(square, self.x, self.y)
        square = affinity.rotate(square, self.o.rotstart + math.pow(self.x*0.02, 3))
        return square
    
    def draw_square(self, vsk):
        with vsk.pushMatrix():
            vsk.translate(self.x , self.y )
            if self.o.square_rotate: vsk.rotate(self.o.rotstart + math.pow(self.x*0.02, 3), degrees=True)
            r = self.r * self.o.square_size
            vsk.square(- r/2, - r/2, r)
    
    def colliding(self, circles, step_size=0):
        
        for circle in circles:
                
                # skip self
                if circle == self:
                    continue
                
                # find nearby circle
                if math.dist((circle.x, circle.y), (self.x, self.y)) < circle.r + self.r + step_size: 
                    return True
                
                # past x boundary
                if self.x - self.r < 0 or self.x + self.r > self.o.widthmm:
                    return True
                
                # past y boundary
                if self.y - self.r < 0 or self.y + self.r > self.o.heightmm:
                    return True
        
        return False

class Day12PackingSketch(vsketch.SketchClass):
    
    border = vsketch.Param(10)
    radius_min = vsketch.Param(1.0)
    radius_max = vsketch.Param(20)
    
    count = vsketch.Param(200)
    
    circles = vsketch.Param(False)
    squares = vsketch.Param(True)
    square_rotate = vsketch.Param(True)
    
    square_size = vsketch.Param(1.2, decimals=2)
    
    grow_treshold = vsketch.Param(0.2)
    
    force_fill = vsketch.Param(False)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")
        
        self.rotstart = vsk.random(260)
        
        self.widthmm = utils.css_to_mm(vsk.width) - self.border * 2
        self.heightmm = utils.css_to_mm(vsk.height) - self.border * 2
        
        circles = []
        for i in range(self.count):
            circle = Circle(vsk, self)
            if circle.colliding(circles):
                continue
            
            if vsk.random(1) < self.grow_treshold:
                circle.grow(circles)
            circles.append(circle)
        
        for circle in circles:
            circle.grow(circles)
        
        if self.force_fill:
            for x in range(100):
                x = vsk.map(x, 0, 100, 0, self.widthmm)
                for y in range(50):
                    y = vsk.map(y, 0, 50, 0, self.heightmm)
                    
                    circle = Circle(vsk, self, (x + vsk.random(1), y + vsk.random(1)), 0.5)
                    if circle.colliding(circles):
                        continue
                    circle.grow(circles)
                    circles.append(circle)
        
        geometries = []
        for circle in circles:
            if self.circles:
                circle.draw_circle(vsk)
            if self.squares:
                circle.draw_square(vsk)
            geometries.append(circle.add_square())
        
        
        line_count = 35
        lines = []
        extension = 2
        for y in range(line_count):
            y = y*y
            y = vsk.map(y,  line_count*line_count, 0, -extension, self.heightmm + extension)
            
            lines.append(geometry.LineString([(-extension,y), (self.widthmm + extension, y)]))
        
        
        vsk.geometry(geometry.MultiLineString(lines).difference(geometry.MultiPolygon(geometries).buffer(0)))


            



    def finalize(self, vsk: vsketch.Vsketch) -> None:
        filename = os.path.basename(__file__)[7:-3]
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort gwrite {filename}.gcode")


if __name__ == "__main__":
    Day12PackingSketch.display()
