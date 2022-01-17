import vsketch
import math


class Day173ColorsSketch(vsketch.SketchClass):

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")
        vsk.penWidth("0.9mm")
        
        vsk.noStroke()
        s = 9

        cols = 12
        rows = 7
        
        spacing = 15
        padding = 2
        
        for x in range(cols):
            rx = vsk.map(x, 0, cols - 1, 0, 1)
            rx = math.sin(x * ( math.pi / (cols -1)))
            
            for y in range(rows):
                
                rot = vsk.map(x, 0, cols - 1, 0 , math.pi/(cols ) * ((cols ) + y*1.5 ))
                
                rx = abs(math.sin(rot))
                ry = vsk.map(y, 0, rows -1 , 0, 1)
                
                # left, middle right, top, bottom
                lt = (0,s * ry  * (rx))
                lb = (0, lt[1] + s *(1-ry))
                rt = (s, s * ry   * (1-rx))
                rb = (s, rt[1] + s* (1-ry))
                mt = (s * (1-rx), 0)
                mm = (s * rx, s * (ry / 2) * (rx) + s/2 * ry )
                mm = (s * rx, lt[1] + rt[1])
                mb = (s * rx, mm[1] + s*(1-ry))
                
                with vsk.pushMatrix():
                    vsk.translate(x * spacing, y * spacing)
                    # left
                    vsk.fill(1)
                    vsk.quad(*lt, *mm, *mb, *lb)
                    # right
                    vsk.translate(padding,0)
                    vsk.fill(2)
                    vsk.quad(*mm, *rt, *rb, *mb)
                    # top
                    vsk.fill(3)
                    vsk.translate(-padding/2, -padding)
                    vsk.quad(*lt, *mt, *rt, *mm)
                
        vsk.vpype("color -l 2 #FFFF00")
        vsk.vpype("color -l 1 #289c60")
        vsk.vpype("color -l 3 #ba4307")

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort gwrite top.gcode")


if __name__ == "__main__":
    Day173ColorsSketch.display()
