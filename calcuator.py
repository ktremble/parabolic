import tkinter
from tkinter import *
import time

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
        #self.canvas.focus_set()
        self.canvas.pack(side=tkinter.RIGHT)
        self.mouse_x = 0
        self.mouse_y = 0
        self.images = {}
        self.frame_count = 0
        self.__handle_motion()

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

    def input_section(self):
        self.a_val=1
        self.x_val=1
        self.y_val = 1

        self.a_label = tkinter.Label(text="a (float)")
        self.a = tkinter.Entry(justify='center')
        self.a_label.pack()
        self.a.insert(0,"0.1")
        self.a.pack()

        self.x_label = tkinter.Label(text="x-vertex (integer)")
        self.x = tkinter.Entry(justify='center')
        self.x_label.pack()
        self.x.insert(0,"0")
        self.x.pack()

        self.y_label = tkinter.Label(text="y-vertex (integer)")
        self.y = tkinter.Entry(justify='center')
        self.y_label.pack()
        self.y.insert(0,"0")
        self.y.pack()

        self.choice = IntVar()
        self.r1 = Radiobutton(text="left-right", variable=self.choice, value=1)
        self.r2 = Radiobutton(text="up-down", variable=self.choice, value=0)
        self.r1.pack()
        self.r2.pack()

        self.enter = tkinter.Button(text="Graph Parabola", command=self.get_result)
        self.enter.pack()




    def get_result(self):
        gui.clear()
        gui.rectangle(0,0,width+10,width+10,'white')
        gui.draw_grid()

        a_val = self.a.get()
        x_val = self.x.get()
        y_val = self.y.get()
        choice = self.choice.get()

        #print(a_val, x_val, y_val, choice)
        if choice==1:
            choice = True
        else:
            choice = False


        x = int(x_val)           # X vertex
        y = int(y_val)           # Y Vertex
        a = float(a_val)       # up or down
        swap = choice     # False = Vertical parabola, True = horizontal

        # draw parabola
        self.parabolic(-a,x,y,swap)



    def parabolic(self,a,X,Y,swap):
        # y = x**2
        # y = a(x-X)**2+Y

        X = X+width//2
        Y = -Y+width//2

        if swap:
            x_coords = range(-width, width+1)
            coords = [(x+Y,a*(x)**2+X) for x in x_coords]
        else:
            x_coords = range(-width, width+1,1)
            coords = [(x+X,a*(x)**2+Y) for x in x_coords]

        for circle in coords:
            x2 = circle[0]
            y2 = circle[1]
            color = 'red'
            if swap:
                gui.ellipse(y2,x2,3,3,color)
            else:
                gui.ellipse(x2,y2,3,3,color)

        # line of symmetry
        if swap:
            gui.line(0,Y,width,Y,'purple',2)
        else:
            gui.line(X,0,X,width,'purple',2)
        gui.ellipse(X,Y,10,10,'purple')
        boo = Y-width//2
        gui.text(X+5,Y,"({},{})".format(X-width//2,-boo),'purple',12)



    def draw_grid(self):
        #grid
        gui.line(0,width//2,width,width//2,'blue',2)
        gui.line(width//2,0,width//2,width,'blue',2)
        for mark in range(0,width+1):
            num_x = '{:4d}'.format(mark-width//2)
            num_y = '{:4d}'.format(width//2-mark)

            widen = 5
            if mark%scale==0:
                widen += 4
            if mark%10==0:
                gui.line(mark, width//2-widen, mark, width//2+widen, 'blue', 2)
                gui.line(width//2-widen, mark, width//2+widen, mark, 'blue', 2)
            offset = mark - 13
            if mark-width//2 == 0:
                    gui.text(offset, width//2+3, "0", 'blue', 8)
            elif mark%scale==0:
                gui.text(offset, width//2+widen, num_x, 'blue', 8)
                gui.text(width//2-32,offset+5, num_y, 'blue', 8)


    def resize(self, width, height):
        self.primary.geometry(str(width) + 'x' + str(height))

    def text(self, x, y, content, fill='black', size=17):
        ''' Draw text on the canvas.
        Must always specify the text, x, y position.
        Can optionally specify the fill color and size.
        '''
        text = self.canvas.create_text(x, y, text=content, fill=fill, font=('Arial', size), anchor='nw')
        self.canvas.move(text, 0, 0)

    def set_left_click_action(self, callee):
        ''' Call the callee function whenever the left click happens.
        callee should take two parameters, the mouse x and mouse y coordinates.
        '''
        def left_click_action(event):
            callee(self, event.x, event.y)
        ''' <Button-1> is the left-most mouse button '''
        self.canvas.bind('<Button-1>', left_click_action)

    def set_right_click_action(self, callee):
        ''' Call the callee function whenever the right click happens.
        callee should take two parameters, the mouse x and mouse y coordinates.
        '''
        def right_click_action(event):
            callee(self, event.x, event.y)
        ''' <Button-2> or <Button-3> is the right-most mouse button.
        Both are set just in case '''
        self.canvas.bind('<Button-2>', right_click_action)
        self.canvas.bind('<Button-3>', right_click_action)

    def set_keyboard_action(self, callee):
        ''' Call the callee function whenever a keyboard key is pressed.
        callee should take one parameter, a char representing the key.
        '''
        def keyboard_action(event):
            callee(self, event.char)
        self.canvas.bind('<KeyPress>', keyboard_action)

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

    def image(self, x, y, up_scale, down_scale, file_name):
        ''' Draw an image on the canvas.
        Specify x, y (top-left corner) and width / height.
        '''
        if file_name not in self.images:
            self.images[file_name] = tkinter.PhotoImage(file=file_name)
        self.images[file_name] = self.images[file_name].zoom(up_scale, up_scale)
        self.images[file_name] = self.images[file_name].subsample(down_scale, down_scale)
        i = self.canvas.create_image(x, y, anchor='nw', image=self.images[file_name])
        self.canvas.move(i, 0, 0)
        return self.images[file_name]

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

width = 500
scale = 50

gui = graphics(width,width,"Parabolic Funtime")
gui.rectangle(0,0,width+10,width+10,'white')
# grid
gui.draw_grid()
gui.input_section()
gui.parabolic(-.01,0,0,False)



