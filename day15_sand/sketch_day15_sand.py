import vsketch
import vpype
from shapely import geometry, affinity
import numpy as np
import os

class Day15SandSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)
    
    w = vsketch.Param(0.8)
    h = vsketch.Param(0.8)
    
    col = vsketch.Param(80)
    row = vsketch.Param(40)
    
    size = vsketch.Param(1.0)
    
    trim_low = vsketch.Param(200)
    trim_high = vsketch.Param(700)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx125mm", landscape=False)

        files = {
            "s": "s.svg",
            "a": "a.svg",
            "n": "n.svg",
            "d": "d.svg",
        }
        
        shapes = []
        
        for letter in files:
            doc = vpype.read_multilayer_svg(files[letter], quantization=0.1)  # unit: px
            lid = 1
            for path in doc.layers[lid]:
                shape = geometry.LineString([(p.real, p.imag) for p in path])
                shape = affinity.scale(shape, self.size, self.size)
                if letter == "s":
                    shape = affinity.translate(shape, 1.1,0)
                if letter == "d":
                    shape = affinity.translate(shape, -0.2,-1.9)
                if letter == "a":
                    shape = affinity.translate(shape, -0.2,0)
                
                shapes.append(shape)
        
        perlin = vsk.noise(np.linspace(0, 2, self.col), np.linspace(0, 15, self.row))
        

        for c in range(self.col):
            x = vsk.map(c, 0, self.col, 0, vsk.width * self.w)
            for r in range(self.row):
                y = vsk.map(r, 0, self.row, 0, vsk.height * self.h)
                with vsk.pushMatrix():
                    
                    _x = x + perlin[c, r] * 180
                    _y = y + perlin[c, r] * 12
                    
                    if _x < self.trim_low or _x > self.trim_high: continue

                    vsk.translate(_x, _y)
                    vsk.geometry(shapes[(c + r) % 4])
                


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        filename = os.path.basename(__file__)[7:-3]
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort gwrite {filename}.gcode")


if __name__ == "__main__":
    Day15SandSketch.display()
