import vsketch
from shapely import geometry

class TestCircleSketch(vsketch.SketchClass):

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("100mmx100mm", landscape=False)
        vsk.scale("mm")

        line_coords = []
        line_count = 10

        for y in range(int(line_count)):
            y = vsk.map(y, 0, line_count -1, 0, 10)
            line_coords.append(((0,y),(11,y)))
            
        lines = geometry.MultiLineString(line_coords)

        dist = 1.11111111111111
        # dist = 1.11111111111112

        circle = geometry.Point(5,5).buffer(5 - dist)

        vsk.geometry(lines.intersection(circle))

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    TestCircleSketch.display()
