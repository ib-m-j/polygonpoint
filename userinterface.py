import PySimpleGUI as sg      
import numpy
import matplotlib as plt
import thepolygons

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

def circle(x):
    return (250+100*x[0]-2,250+ 100*x[1] -2, 250+100*x[0]+2,250+ 100*x[1]+2) 

#def drawLines(canvas, outer, inner, color = 'black'):
#    skip = 3
#    currentDir = 0
#    currentLevel = outer
#    count = 0
#    while True:
#        startPoint = currentLevel.size*numpy.array(
#            currentLevel.directions[currentDir])+numpy.array((400,400))
#        
#        if currentLevel == outer:
#            currentLevel = inner
#        else:
#            currentLevel = outer
#            
#        currentDir = (currentDir + skip) % currentLevel.nPoints
#        endPoint = currentLevel.size* numpy.array(currentLevel.directions[
#                currentDir]) + numpy.array((400,400))
#        canvas.create_line(list(startPoint) + list(endPoint), fill = color)
#        count = count + 1
#        #        if (currentLevel == 0) and (currentLevel == outer):
#        if count == 14:
#            break
#

class CanvasMap:
    def __init__(self, origin, scale):
        self.origin = origin
        self.scale = scale

    def setcanvas(self, canvas):
        self.canvas = canvas
        
    def map(self, point):
        mirrorPoint = numpy.array((point[0], -point[1]))
        return list(self.scale*mirrorPoint +self.origin)


        
drawObjects = []
currentMap = CanvasMap(numpy.array((400,400)), 4)

def redraw():
    for o in drawObjects:
        o.draw(currentMap)


        
def drawBoard(outer, inner, polygon):#cellKeys):

    sg.theme('DarkAmber')    # Keep things interesting for your users
#    cells =  [[sg.Input(
#        justification="center", enable_events=True, size=(4,2),
#        key=(i,j)) for i in range(8)
#    ] for j in range(8)]
#
    
    layout = [[sg.Text('Persistent window')],
              [sg.Exit(),sg.Button("Redo"),
               sg.Text("Outer size"), 
               sg.Slider(range = (0,1000), orientation = 'h', default_value = outer.size,
                         key = '-o-', enable_events = True),
               sg.Text("Inner size"),
               sg.Slider(range = (0,100), orientation = 'h', default_value = inner.size,
                         key = '-i-', enable_events = True)],
              [sg.Text(str(polygon.advance), key = '-updatetext-'),
                  sg.Text('Advance 1'),
               sg.Slider(range= (1,5), orientation = 'h', default_value = polygon.advance[0],
                         key = '-advance1-', enable_events = True),
               sg.Text('Advance 2'),
               sg.Slider(range= (0,5), orientation = 'h', default_value = polygon.advance[1],
                         key = '-advance2-', enable_events = True)],
               [sg.Text('Spikes'),
                sg.Slider(range= (1,20), orientation = 'h', default_value = polygon.spikes,
                          key = '-spikes-', enable_events = True),
                sg.Text('Zoom'),
                sg.Button("In", key= '-in-'), sg.Button('Out', key = '-out-'),
                sg.Slider(range= (-10,10), orientation = 'h', default_value = 0,
                          key = '-innerturn-', enable_events = True)],
              [sg.Canvas(key='mycanvas',
                         size=(800,800),background_color="white")]]     

    window = sg.Window('Window that stays open', layout, finalize=True)
    canvas = window['mycanvas'].TKCanvas
    
    currentMap.setcanvas(canvas)
    redraw()
        
#    outer.draw(canvas, numpy.array((400, 400)), 'black')    
#    inner.draw(canvas, numpy.array((400, 400)), 'black')    
#    print("window created")

    while True:   # The Event Loop
        window.Refresh()
        event, values = window.read()
        print(event, values)
        if event == '-o-':
            canvas.delete('all')
            polygon.outer.size = values[event]
            redraw()
              
            #outer.updateAndDraw(window['o'].TKScale.get(), canvas, numpy.array((400,400)))    
        if event == '-i-':
            canvas.delete('all')
            polygon.inner.size = values[event]
            redraw()
        if event == '-in-':
            canvas.delete('all')
            currentMap.scale = currentMap.scale/2
            redraw()
        if event == '-out-':
            canvas.delete('all')
            currentMap.scale = currentMap.scale*2
            redraw()
        if event == '-advance1-':
            canvas.delete('all')
            if len(polygon.advance) == 1:
                polygon.advance = [int(values[event])]
            else:
                polygon.advance = [int(values[event])] + polygon.advance[1:]
            window['-updatetext-'].update(str(polygon.advance))
            redraw()
        if event == '-advance2-':
            canvas.delete('all')
            if values[event] == 0:
                polygon.advance = [polygon.advance[0]]
            else:
                polygon.advance = [polygon.advance[0]] + [int(values[event])]
            window['-updatetext-'].update(str(polygon.advance))
            redraw()
#        if event == '-skip-':
#            canvas.delete('all')
#            polygon.skip = int(values[event])
#            redraw()
        if event == '-spikes-':
            canvas.delete('all')
            polygon.respike(int(values[event]))
            redraw()
        if event == '-innerturn-':
            canvas.delete('all')
            polygon.innerturn(int(values[event]))
            redraw()
        if event == "Redo":
            drawLines(canvas, outer, inner)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
 
    window.close()


if __name__ == '__main__':
    outerPolygon = thepolygons.PolygonPoints(5)

    
    drawBoard(outerPolygon)
