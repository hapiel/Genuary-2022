import vsketch
import ndjson
from shapely import geometry, affinity
import os

with open("penis-simplified.ndjson") as file:
    data = ndjson.load(file)

class Penis:
    
    def __init__(self, vsk,  other) -> None:
        
        self.o = other
        
        self.vsk = vsk
        
        self.x = vsk.random(self.o.widthmm)
        self.y = vsk.random(self.o.heightmm)
        
        
        self.step_size = 0.3
        self.r = self.o.radius_min 
        self.r_max = vsk.random(self.o.radius_max/2, self.o.radius_max)
        

        penis = data[int(vsk.random(25000))]
        lines = []
        for stroke in penis["drawing"]:
            line = []
            for pos, _ in enumerate(stroke[0]):
                line.append((stroke[0][pos]/100, stroke[1][pos]/100))
            if len(line) > 1:
                lines.append(line)

        
        self.shape = affinity.translate(geometry.MultiLineString(lines), self.x, self.y )
        
        
    def grow(self, penisses):
        
        while self.r < self.r_max and not self.colliding(penisses, self.step_size):
            
            self.shape = affinity.scale(self.shape, 1 + self.step_size, 1 + self.step_size)
            self.r += self.step_size
        
    
    def add_penis(self):

        return self.shape
    
    
    def colliding(self, penisses, step_size=0):
        
        for penis in penisses:
                
                # skip self
                if penis == self:
                    continue
                
                # find nearby circle
                if penis.shape.intersects(affinity.scale(self.shape, 1 + step_size, 1 + step_size)):
                    return True
                

        
        return False

class Day14SomethingYoudNeverMakeSketch(vsketch.SketchClass):
    

    widthmm = vsketch.Param(170)
    heightmm = vsketch.Param(100)
    
    hor = vsketch.Param(10)
    ver = vsketch.Param(8)
    
    radius_min = vsketch.Param(0.5)
    radius_max = vsketch.Param(3.1)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)

        vsk.scale("mm")
        
        
        penisses = []
        for i in range(250):
            
            
            penis = Penis(vsk, self)

            if penis.colliding(penisses):
                continue
            penis.grow(penisses)
            penisses.append(penis)

            vsk.geometry(penis.add_penis())
        


        

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        filename = os.path.basename(__file__)[7:-3]
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort gwrite {filename}.gcode")


if __name__ == "__main__":
    Day14SomethingYoudNeverMakeSketch.display()
