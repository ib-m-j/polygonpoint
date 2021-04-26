import math
import userinterface
import numpy
import itertools

def ovalCoords(p, size = 5):
    px = p[0]
    py = p[1]
    return (px-size, py-size, px+size, py+size)


def weave(L1, L2):
    component = [L1[0], L2[0]]
    if len(L1) == 1:
        return component
    rest = weave(L1[1:], L2[1:])
    return component + rest

    
class Polygon:
    def __init__(self, outer, inner, advance = [3]):
        self.outer = outer
        self.inner = inner
        self.advance = advance
        #        print(outer.size)
        #        print(outer.directions)
        #        print(outer.nPoints)
        self.updateAllPoints()
        
    def updateAllPoints(self):
        outerList = [self.outer.size*numpy.array(
            self.outer.directions[i]) for i in range(self.outer.nPoints)]
        innerList = [self.inner.size*numpy.array(
            self.inner.directions[i]) for i in range(self.inner.nPoints)]
        self.spikes = outer.nPoints
        self.allPoints =  weave(outerList, innerList)
        
    def respike(self, new):
        self.outer = PolygonPoints(int(new), self.outer.size, self.outer.offSet)
        self.inner = PolygonPoints(int(new), self.inner.size, self.inner.offSet)
        self.updateAllPoints()
        

    def innerturn(self, value):
        self.inner = PolygonPoints(self.inner.nPoints, self.inner.size,
                                          (math.pi/(5*self.inner.nPoints))*value)
        self.updateAllPoints()
        
    def draw(self, canvasMap):
        self.updateAllPoints()
        self.outer.draw(canvasMap)
        self.inner.draw(canvasMap)
        currentKey = 0
        p1 = self.allPoints[currentKey]
        advances = itertools.cycle(self.advance)
        while (True):
            currentKey = (currentKey + next(advances)) % len(self.allPoints)
            p2 = self.allPoints[currentKey]
            canvasMap.canvas.create_line(canvasMap.map(p1) + canvasMap.map(p2))
            if currentKey == 0:
                break
            p1 = p2
            
                          
            
class PolygonPoints:
    def __init__(self, nPoints, size, offSet ):
        self.nPoints = nPoints
        self.size = size

        #        if offSet:
        #            startAngle = math.pi/nPoints
        #        else:
        #            startAngle = 0
        #
        startAngle = offSet
        self.directions = [
            (math.cos(2*math.pi*x/nPoints+startAngle), math.sin(2*math.pi*x/nPoints+startAngle)) \
            for x in range(nPoints)]

        print(self.directions)
        self.offSet = offSet

    def draw(self, canvasMap, color = 'black'):
        for p in self.directions:
            pointMapped = canvasMap.map(self.size*numpy.array(p))
            oC = ovalCoords(pointMapped)
            p1 = numpy.array(oC[:2])
            p2 = numpy.array(oC[2:4])
            canvasMap.canvas.create_oval(oC, outline=color)

    def updateAndDraw(self, newSize, canvas, center):
        self.draw(canvas, center, "white")
        self.size = newSize
        self.draw(canvas, center, "black")
        for p in self.directions:
            canvas.create_oval(
                ovalCoords(self.size*numpy.array(p) + center),outline="black")


        
#        for x in self.points:
#            print(x)
#

if __name__ == '__main__':

    outer = PolygonPoints(7, 100, 0)
    inner  = PolygonPoints(7, 50, math.pi/7)
    #five.draw()
    polygon = Polygon(outer, inner, [5,3])
    userinterface.drawObjects.extend([polygon])
    userinterface.drawBoard(outer, inner, polygon)
