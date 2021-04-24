import PySimpleGUI as sg      
import numpy
import matplotlib as plt
import thepolygons

def focus_next_window(event):
    event.widget.tk_focusNext().focus()
    return("break")

def circle(x):
    return (250+100*x[0]-2,250+ 100*x[1] -2, 250+100*x[0]+2,250+ 100*x[1]+2) 

def drawLines(canvas, outer, inner, color = 'black'):
    skip = 3
    currentDir = 0
    currentLevel = outer
    count = 0
    while True:
        startPoint = currentLevel.size*numpy.array(
            currentLevel.directions[currentDir])+numpy.array((400,400))
        
        if currentLevel == outer:
            currentLevel = inner
        else:
            currentLevel = outer
            
        currentDir = (currentDir + skip) % currentLevel.nPoints
        endPoint = currentLevel.size* numpy.array(currentLevel.directions[
                currentDir]) + numpy.array((400,400))
        canvas.create_line(list(startPoint) + list(endPoint), fill = color)
        count = count + 1
        #        if (currentLevel == 0) and (currentLevel == outer):
        if count == 14:
            break

def drawBoard(outer, inner):#cellKeys):

    sg.theme('DarkAmber')    # Keep things interesting for your users
#    cells =  [[sg.Input(
#        justification="center", enable_events=True, size=(4,2),
#        key=(i,j)) for i in range(8)
#    ] for j in range(8)]
#
    
    layout = [[sg.Text('Persistent window')],
              [sg.Exit(),sg.Button("Redo"),
               sg.Slider(range = (0,200), orientation = 'h', default_value = outer.size,
                         key = 'o', enable_events = True),
               sg.Slider(range = (0,200), orientation = 'h', default_value = inner.size,
                         key = 'i', enable_events = True)], 
              [sg.Canvas(key='mycanvas',size=(800,800),background_color="white")]]     

    window = sg.Window('Window that stays open', layout, finalize=True)
    canvas = window['mycanvas'].TKCanvas
    print(window['o'].TKScale.get())
    outer.draw(canvas, numpy.array((400, 400)), 'black')    
    inner.draw(canvas, numpy.array((400, 400)), 'black')    
    print("window created")

    while True:   # The Event Loop
        print("heer")
        event, values = window.read()
        print(event, values)
        if event == 'o':
            outer.updateAndDraw(window['o'].TKScale.get(), canvas, numpy.array((400,400)))    
        if event == 'i':
            inner.updateAndDraw(window['i'].TKScale.get(), canvas, numpy.array((400,400)))    
        if event == "Redo":
            drawLines(canvas, outer, inner)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
 
    window.close()


if __name__ == '__main__':
    outerPolygon = thepolygons.PolygonPoints(5)

    
    print(drawBoard(outerPolygon))
