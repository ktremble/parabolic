'''
Some code borrowed/modified from a given simple
graphics library used for creating a canvas and drawing
simple shapes.

I wanted to see if you can graph a parabola using those functions
'''

import tkinter
from tkinter import *
import time
import re

class graphics:
    def __init__(self, w, h, title):
        ''' Initialize the graphics object.
        Creates a new tkinter Tk object,
        and a tkinter Canvas object,
        placed insize the Tk object.
        '''
        self.primary = tkinter.Tk()
        self.primary.title(title)
        self.primary.geometry('%dx%d+%d+%d' % (w+150, h, 50, 100))
        self.canvas = tkinter.Canvas(self.primary, width=w, height=h, highlightthickness=0)
        self.canvas.focus_set()
        self.canvas.pack(side=tkinter.RIGHT)
        self.mouse_x = 0
        self.mouse_y = 0
        self.images = {}
        self.frame_count = 0
        self.__handle_motion()
        self.w = w

    '''
    BEGIN PRIVATE FUNCTION(S)
    '''

    def __handle_motion(self):
        ''' Ensure mouse x and y coordinates are updated when mouse moves.
        '''
        def motion_action(event):
            self.mouse_x = event.x
            self.mouse_y = event.y
        self.canvas.bind('<Motion>', motion_action)

    '''
    END PRIVATE FUNCTION(S)
    '''

    '''
    START MY CALCULATOR FUNCTIONS
    '''
    def input_section(self):
        '''
        Creates the data input section for what will
        be calculated. Based on the formula x=X and y=a*x**2+Y,
        gets variables, a,X,Y
        '''
        self.a_val=1
        self.x_val=1
        self.y_val=1

        # section for getting (a) variable
        self.a_label = tkinter.Label(text="a (float)")
        self.a = tkinter.Entry(justify='center')
        self.a_label.pack()
        self.a.insert(0,"0.01")     # default entry box value
        self.a.pack()

        # section for getting (x) variable
        self.x_label = tkinter.Label(text="x-vertex (integer)")
        self.x = tkinter.Entry(justify='center')
        self.x_label.pack()
        self.x.insert(0,"0")        # default entry box value
        self.x.pack()

        # section for getting (y) variable
        self.y_label = tkinter.Label(text="y-vertex (integer)")
        self.y = tkinter.Entry(justify='center')
        self.y_label.pack()
        self.y.insert(0,"0")        # default entry box value
        self.y.pack()

        # section for getting direction (choice) variable, radio buttons
        self.choice = IntVar()
        self.r1 = Radiobutton(text="left-right", variable=self.choice, value=1)
        self.r2 = Radiobutton(text="up-down", variable=self.choice, value=0)
        self.r1.pack()
        self.r2.pack()

        # Button to click to draw parabola
        self.enter = tkinter.Button(text="Graph Parabola", command=self.get_result)
        self.enter.pack()

        # in case of value error
        self.error = tkinter.Label(text="")
        self.error.pack()

    def get_result(self):
        '''
        Event handler for when "graph parabola" is clicked.
        Gets the values from the data entry points and calls
        the function to draw the parabola on the canvas.
        '''
        gui = self
        width = self.w

        #get values from input
        a_val = self.a.get()
        x_val = self.x.get()
        y_val = self.y.get()
        val = self.choice.get()

        swap = False
        if val==1:
            swap = True         # False = Vertical parabola, True = horizontal

        # check for valid values. Draw graph if valid. Give error msg if invalid
        try :
            x = int(x_val)      # X vertex
            y = int(y_val)      # Y Vertex
            a = float(a_val)    # up or down
        except :
            self.error.config(text = "\nAll values must\nbe numeric.", foreground="red")
            return
        else:
            self.error.config(text = "")
            gui.clear()
            gui.rectangle(0,0,width+10,width+10,'white')
            gui.draw_grid()

        # draw parabola
        self.parabolic(-a,x,y,swap)


    def parabolic(self,a,X,Y,swap):
        '''
        Based on vertex formula for parabolas. Draws a parabola
        on the canvas witht the given variables. Parabola is drawn
        Based on the origin of the grid.
        a: the a constant in the parabola function
        X: the location of the X vertex of the parabola
        Y: the location of the Y vertex of the parabola
        swap: if True the X and Y values are swapped when calculating
                rotates the parabola sideways
        '''
        gui = self
        width = self.w
        #Formula for parabolas:
        # y = x**2
        # y = a(x-X)**2+Y

        X = X+width//2      #X and Y should start at the center of canvas
        Y = -Y+width//2

        # Gets a list of all x_coords and calculates y using those values
        # Creates a list of x-y coordinate tuples
        if swap:
            x_coords = range(-width, width+1)
            coords = [(x+Y, a*(x)**2+X) for x in x_coords]
        else:
            x_coords = range(-width, width+1,1)
            coords = [(x+X, a*(x)**2+Y) for x in x_coords]

        # Draws a circle at each coordinate tuple
        for circle in coords:
            x2 = circle[0]
            y2 = circle[1]
            color = 'red'
            if swap:
                gui.ellipse(y2,x2,3,3,color)
            else:
                gui.ellipse(x2,y2,3,3,color)

        # Draw line of symmetry and mark vertex
        if swap:
            gui.line(0,Y,width,Y,'purple',2)
        else:
            gui.line(X,0,X,width,'purple',2)
        gui.ellipse(X,Y,10,10,'purple')
        gui.text(X+5,Y,"({},{})".format(X-width//2,-(Y-width//2)),'purple',12)



    def draw_grid(self):
        '''
        Draws the graph grid with the center being the origin and
        tick marks every 10 steps. Every 50 steps are marked with
        a number for easy reading.
        '''
        gui = self
        width = self.w
        scale = 50

        # draw X and Y axis
        gui.line(0,width//2,width,width//2,'blue',2)
        gui.line(width//2,0,width//2,width,'blue',2)

        # draw tick marks
        for mark in range(0,width+1):
            # uniform number width
            num_x = '{:4d}'.format(mark-width//2)
            num_y = '{:4d}'.format(width//2-mark)

            # If a tick mark is at step 50 make it a little wider than the others
            widen = 5
            if mark%scale==0:
                widen += 4

            #Draw a tick mark every 10 steps on x and y axis
            if mark%10==0:
                gui.line(mark, width//2-widen, mark, width//2+widen, 'blue', 2)
                gui.line(width//2-widen, mark, width//2+widen, mark, 'blue', 2)

            # Draw the number for the step 50 ticks, 0 drawn slightly off to the side
            offset = mark - 13
            if mark-width//2 == 0:
                    gui.text(offset, width//2+3, "0", 'blue', 8)
            elif mark%scale==0:
                gui.text(offset, width//2+widen, num_x, 'blue', 8)
                gui.text(width//2-32,offset+5, num_y, 'blue', 8)

    '''
    END CALCULATOR FUNCTIONS
    '''

    def resize(self, width, height):
        self.primary.geometry(str(width) + 'x' + str(height))

    def text(self, x, y, content, fill='black', size=17):
        ''' Draw text on the canvas.
        Must always specify the text, x, y position.
        Can optionally specify the fill color and size.
        '''
        text = self.canvas.create_text(x, y, text=content, fill=fill, font=('Arial', size), anchor='nw')
        self.canvas.move(text, 0, 0)

    def get_color_string(self, red, green, blue):
        ''' accepts three ints that should represent and RGB color.
        Returns a hex string'''
        hex_string = hex(red)[2:].rjust(2, '0') + \
                     hex(green)[2:].rjust(2, '0') + \
                     hex(blue)[2:].rjust(2, '0')
        return '#' + hex_string

    def triangle(self, x1, y1, x2, y2, x3, y3, fill='black'):
        ''' Draw a triangle.
        The three corners of the triangle are specified with the parameter coordinates.
        '''
        r = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=fill)
        self.canvas.move(r, 0, 0)

    def line(self, x1, y1, x2, y2, fill='black', width=3):
        ''' Draw a line.
        The two ends of the line are specified with the parameter coordinates.
        '''
        r = self.canvas.create_line(x1, y1, x2, y2, fill=fill, width=width)
        self.canvas.move(r, 0, 0)

    def ellipse(self, x, y, w, h, fill='black'):
        ''' Draw an ellipse on the canvas.
        Specify x, y (center of ellipse) and width / height.
        '''
        r = self.canvas.create_oval(x-(w/2), y-(h/2), x+(w/2), y+(h/2), fill=fill, outline='')
        self.canvas.move(r, 0, 0)

    def rectangle(self, x, y, w, h, fill='black'):
        ''' Draw a rectangle on the canvas.
        Specify x, y (top-left corner) and width / height.
        '''
        r = self.canvas.create_rectangle(x, y, x+w, h+y, fill=fill, outline='')
        self.canvas.move(r, 0, 0)

    def update(self):
        ''' Does an idle task update and regular update.
        '''
        self.primary.update_idletasks()
        self.primary.update()

    def frame_space(self, frame_rate):
        ''' Sleeps for a time that corresponds to the provided frame rate.
        '''
        sleep_ms = 1.0 / float(frame_rate)
        time.sleep(sleep_ms)

    def update_frame(self, frame_rate):
        ''' Updates and sleeps.
        This should be called at the end of each iteration of a users draw loop.
        '''
        self.update()
        self.frame_space(frame_rate)
        self.frame_count += 1

    def clear(self):
        ''' Clears the canvas.
        '''
        self.canvas.delete('all')


def main():
    width = 500
    scale = 50

    # create canvas
    gui = graphics(width,width,"Parabolic Funtime")
    gui.rectangle(0,0,width+10,width+10,'white')

    # grid
    gui.draw_grid()
    gui.input_section()
    gui.parabolic(-.01,0,0,False)       # draws default parabola

main()


