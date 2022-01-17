import vsketch
import math

class Day16GradientGoneWrongSketch(vsketch.SketchClass):

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")
        
        
        vsk.rotate(-0.2)
        count = 110
        ph = .5
        pw = 1.7
        for i in range(count):
            
            if i < count*0.36:
                vsk.stroke(1)
                
            elif i < count * 0.5:
                vsk.stroke(1 + i %2)
            elif i < count *0.65:
                vsk.stroke(2)
            elif i < count *0.85:
                vsk.stroke(2 + i %2)
            else: 
                vsk.stroke(3)

            if i < 2: continue

            h = vsk.map(math.pow(i, ph), 0, math.pow(count, ph), 0, count) 
            w = vsk.map(math.pow(i, pw), 0, math.pow(count, pw), 0, count) 

            vsk.rotate(0.004)
            with vsk.pushMatrix():
                vsk.rotate(math.sin(i/3.2)*0.03)
                vsk.ellipse(0,0,w, h)
                
        
        
        vsk.vpype("color -l 2 #0c9c48")
        vsk.vpype("color -l 3 #147582")
        vsk.vpype("color -l 1 #1f67bf")
        


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype(f"rotate 180 linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day16GradientGoneWrongSketch.display()
