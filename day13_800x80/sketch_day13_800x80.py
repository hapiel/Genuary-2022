import vsketch
from shapely import geometry, affinity
import math

class Day13800x80Sketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("205mmx130mm", landscape=False)
        vsk.scale("mm")

        tex_w = 160
        tex_h = 100
        spacing = 18
        
        rect = geometry.Polygon([(0,0), (8,0), (8,80), (0,80)])
        
        rects = []
        
        for j in range(4):
            # sine lines
            lines = []
            line_count = 300
            pos = -10
            for i in range(line_count):
                line = geometry.LineString([(-50,pos,), (tex_w ,pos)])
                lines.append(line)
                pos += ((math.sin(i/3.3)) + 2) * 0.5
            
            sine_lines = geometry.MultiLineString(lines)
            
            # vsk.geometry(rect)
            # vsk.geometry(affinity.rotate(sine_lines, 5).intersection(rect))
            rects.append(affinity.translate(affinity.rotate(sine_lines, vsk.random(-30, 30)).intersection(rect), j*2 * spacing))
            rects.append(affinity.translate(rect, j*2 * spacing ))
            
            # plus signs texture
            
            plus_count = 800
            plusses = []
            for i in range(plus_count):
                x = vsk.random(-4, tex_w -4)
                y = vsk.random(-4, tex_h -4)
                len = 1
                hor = geometry.LineString([(x - len, y), (x + len, y)])
                ver = geometry.LineString([(x, y -len), (x, y + len)])
                plusses.append(hor)
                plusses.append(ver)
                
            plus_tex = geometry.MultiLineString(plusses)
            
            # vsk.geometry(rect)
            rect_plus_text = plus_tex.intersection(rect)
            
            # vsk.geometry(rect_plus_text)
            
            rects.append(affinity.translate(rect_plus_text, j*2 * spacing + spacing))
            rects.append(affinity.translate(rect, j*2 * spacing + spacing))
            # vsk.geometry(plus_tex)
            
            
        
        
        for i, shape in enumerate(rects):
            vsk.stroke(1 + i % 2)
            vsk.geometry(shape)
        

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("rotate 180 linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    Day13800x80Sketch.display()
