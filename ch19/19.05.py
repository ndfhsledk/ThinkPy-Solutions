# A vector graphics editor is a program that allows users to draw and edit
# shapes on the screen and generate output files in vector graphics formats
# like Postscript and SVG1 .
# Write a simple vector graphics editor using Tkinter. At a minimum, it should
# allow users to draw lines, circles and rectangles, and it should use 
# Canvas.dump to generate a Postscript description of the contents of the 
# Canvas. As a challenge, you could allow users to select and resize items 
# on the Canvas.

# Current Status: Incomplete
from tkinter import *
from tkinter.messagebox import showinfo
from swampy.Gui import *

class Draggable(Item):
    def __init__(self, item):
        self.canvas = item.canvas
        self.tag = item.tag
        self.bind('<Button-1>', self.select)
        self.bind('<B1-Motion>', self.drag)
        self.bind('<Release-1>', self.drop)

    def select(self, event):
        self.dragX = event.x
        self.dragY = event.y

        self.fill = self.cget('fill')
        self.config(fill='yellow')

    def drag(self, event):
        dx, dy = event.x - self.dragX, event.y - self.dragY
        self.dragX, self.dragY = event.x, event.y
        self.move(dx, dy)

    def drop(self, event):
        self.config(fill= self.fill)


class Scalable(Item):
    def __init__(self, item):
        self.canvas = item.canvas
        self.tag = item.tag
        self.bind('<Button-2>', self.select)
        self.bind('<B2-Motion>', self.drag)
        self.bind('<Release-2>', self.drop)

    def select(self, event):
        self.dragX = event.x
        self.dragY = event.y

        self.fill = self.cget('fill')
        self.config(fill='red')

    def drag(self, event):
        dx, dy = event.x - self.dragX, event.y - self.dragY
        self.dragX, self.dragY = event.x, event.y
        rx, ry = 0, 0
        coords = self.coords()
        x1, y1 = tuple(coords[0])
        x2, y2 = tuple(coords[1])
        x0 = x2 - x1
        y0 = y2 - y1
        if not x0 == 0:
            rx = (x0 + dx) / x0
        if not y0 == 0:
            ry = (y0 + dy) / y0
        ra = (abs(rx) + abs(ry))/2
        ca.scale(self.tag, 200, 200, ra, ra)

    def drop(self, event):
        self.config(fill= self.fill)

       


g = Gui()
g.title('graphic editor')

def create_line():
    line = ca.line([[-10, -10], [10, 10]], fill = 'black')
    Draggable(line)
    Scalable(line)

def create_circle():
    circle = ca.circle([0,0],50)
    Draggable(circle)
    Scalable(circle)

def create_rect():
    rect = ca.rectangle([[-20, 20],[20, -20]])
    Draggable(rect)
    Scalable(rect)

def save():
    ca_content = ca.postscript()
    try:
        fin = open('graphic_output','w')
        fin.write(ca_content)
        fin.close()
        showinfo('success', 'save sucessfully')
    except Exception as e:
        print(e)
        showinfo('error', e)
    
    

g.row()
line_bu = g.bu('line', create_line)
circle_bu = g.bu('circle', create_circle)
rect_bu = g.bu('rect', create_rect)
save_bu = g.bu('save', save)
g.endrow()
ca = g.ca(width=400, height=400, bg='white')
