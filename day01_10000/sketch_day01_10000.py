import sys, os
sys.path.append(os.path.abspath("D:\9mediatech\python\genuary"))

import vsketch
import utils 

total_lines = 0

# test stuff:
def grid(self, vsk, width, height):
        for x in range(self.x_count):
            x = vsk.map(x, 0, self.x_count, 0, width -self.margin)

            for y in range(self.y_count):
                y = vsk.map(y, 0, self.y_count, 0, height -self.margin)

                vsk.line( x, y, x + self.line_length, y)


class Grass:
    "a single grass blade"

    def __init__(self, vsk, params, spacing, height, x) -> None:

        self.p = params
        self.height = height
        self.spacing = spacing
        

        # bezier curve points: anchor top, control, control, anchor bottom
        x_noise = ( vsk.noise( x /self.p["noise_scale"]) *self.p["noise_max"]) -self.p["noise_max"] /2
        x_random = vsk.random(self.p["random_x_max"]) - self.p["random_x_max"]/2
        
        y_noise = vsk.noise(0, x/20)*30
        self.length_deduction = y_noise

        self.x1 = x + x_noise + x_random
        self.y1 = y_noise
        self.x2 = x
        self.y2 = height / 4 + y_noise * 0.75
        self.x3 = x
        self.y3 = height / 2 + y_noise * 0.5
        self.x4 = x
        self.y4 = height

    def draw(self, vsk):
        
        line_count = int(self.height / self.spacing)

        for line in range(line_count):
            global total_lines
            if total_lines == 10000: break
            pos = vsk.map(line, 0, line_count, 1, 0)
            x = vsk.bezierPoint(self.x1, self.x2, self.x3, self.x4, pos)
            y = vsk.map(line, line_count,0,  self.length_deduction, self.height )

            if line > line_count/2.5:

                len = vsk.map(line, line_count/2.5, line_count, self.p["line_length"], self.p["line_length"]/3.5) 
            else:
                len = self.p["line_length"]
            # y = vsk.bezierPoint(self.y1, self.y2, self.y3, self.y4, pos)
            vsk.line( x, y, x + len, y)

            
            total_lines += 1


    def draw_curve(self, vsk):
        vsk.bezier(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.x4, self.y4)

        vsk.circle(self.x2, self.y2, 1)
        vsk.circle(self.x3, self.y3, 2)
        


class Day0110000Sketch(vsketch.SketchClass):
    # Sketch parameters:

    y_count = vsketch.Param(130)
    x_count = vsketch.Param(77)
    line_length = vsketch.Param(1.8)
    margin = vsketch.Param(5.0)
    x_margin = vsketch.Param(30)

    noise_scale = vsketch.Param(20)
    noise_max = vsketch.Param(40)
    random_x_max = vsketch.Param(20)
    spacing = vsketch.Param(0.8)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        global total_lines
        total_lines = 0

        params = {
            "y_count": self.y_count,
            "x_count": self.x_count,
            "line_length": self.line_length,
            "margin": self.margin,
            "noise_scale" : self.noise_scale,
            "noise_max" : self.noise_max,
            "random_x_max" : self.random_x_max,
            "x_margin" : self.x_margin,
            }
        
        vsk.size("200mmx125mm", landscape=False)
        vsk.scale("mm")
        width = utils.css_to_mm(vsk.width)
        height = utils.css_to_mm(vsk.height)
        # grid(self, vsk, width, height)

        for x in range(self.x_count):
            x = vsk.map(x, 0, self.x_count, 0, width -self.x_margin)
            blade = Grass(vsk, params, self.spacing, height - self.margin , x)
            # blade.draw_curve(vsk)
            blade.draw(vsk)

        print(total_lines)

        #single
        # blade = Grass(vsk, params, 1, height - self.margin , 1)
        # blade.draw_curve(vsk)
        # blade.draw(vsk)



    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort gwrite last.gcode")


if __name__ == "__main__":
    Day0110000Sketch.display()
