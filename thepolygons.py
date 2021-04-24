import math
import userinterface
import numpy

def ovalCoords(p, size = 1):
    px = p[0]
    py = p[1]
    return (px-size, py-size, px+size, py+size)


class Polygon:
    def __init__(self, outer, inner, skip = 1):
        self. outer = outer
        self.inner = inner
        self.skip = skip
        self.allPointKeys = [(x,1) for x in range(outer.nPoints)]+\
                            [(x,2) for x in range(inner.nPoints)]
        self.allPointsKeysSorted = sorted(self.allPointKeys)
        print(self.allPointsKeysSorted)
        
        
    def draw(self, canvasMap):
        self.outer.draw(canvasMap)
        if self.skip % 2 == 1:
            self.inner.draw(canvasMap)
        currentKeyIndex = 0

        def getLevel(index):
            if self.allPointsKeysSorted[index][0] == 1:
                res = (outer, index % 2)
            else:
                res = (inner, index // 2)
            return res
        
        (level, ind) = getLevel(currentKeyIndex)
        p1 = level.size*numpy.array(level.directions[ind])

        
        while (True):
            currentKeyIndex = (currentKeyIndex + self.skip) % len(self.allPointsKeysSorted)
            print(currentKeyIndex)
            (level, ind) = getLevel(currentKeyIndex)
            p2 = level.size*numpy.array(level.directions[ind])
            print(p1, canvasMap.map(p1),p2, canvasMap.map(p2))
            canvasMap.canvas.create_line(canvasMap.map(p1) + canvasMap.map(p2))
            if currentKeyIndex == 0:
                break
            p1 = p2
            
                          
            
class PolygonPoints:
    def __init__(self, nPoints, size, startAngle = 0  ):
        self.nPoints = nPoints
        self.size = size
        self.directions = [
            (math.cos(2*math.pi*x/nPoints), math.sin(2*math.pi*x/nPoints)) \
            for x in range(nPoints)]

    def draw(self, canvasMap, color = 'black'):
        for p in self.directions:
            oC = ovalCoords(self.size*numpy.array(p))
            p1 = numpy.array(oC[:2])
            p2 = numpy.array(oC[2:4])
            canvasMap.canvas.create_oval(canvasMap.map(p1)+canvasMap.map(p2), outline=color)

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

    outer = PolygonPoints(7, 100)
    inner  = PolygonPoints(7, 50)
    #five.draw()
    userinterface.drawObjects.extend([Polygon(outer, inner, 1)])
    userinterface.drawBoard(outer, inner)
