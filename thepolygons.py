import math
import userinterface
import numpy

def ovalCoords(p, size = 2):
    px = p[0]
    py = p[1]
    return (px-size, py-size, px+size, py+size)

class PolygonPoints:
    def __init__(self, nPoints, size, alignment = 0  ):
        self.nPoints = nPoints
        self.size = size
        self.directions = [
            (math.cos(2*math.pi*x/nPoints), math.sin(2*math.pi*x/nPoints)) \
            for x in range(nPoints)]

    def draw(self, canvas, center, color):
        for p in self.directions:
            canvas.create_oval(ovalCoords(self.size*numpy.array(p) + center),outline=color)

    def updateAndDraw(self, newSize, canvas, center):
        self.draw(canvas, center, "white")
        self.size = newSize
        self.draw(canvas, center, "black")
        for p in self.directions:
            canvas.create_oval(ovalCoords(self.size*numpy.array(p) + center),outline="black")


        
#        for x in self.points:
#            print(x)
#

if __name__ == '__main__':

    outer = PolygonPoints(7, 400)
    inner  = PolygonPoints(7, 100)
    #five.draw()

    userinterface.drawBoard(outer, inner)
