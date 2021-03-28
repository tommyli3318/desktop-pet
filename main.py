import tkinter
import os
import random
from platform import system

class Pet:
    def __init__(self):
        self.root = tkinter.Tk() # create window
        self.delay = 200 # delay in ms
        self.pixels_from_right = 200 # change to move the pet's starting position
        self.pixels_from_bottom = 200 # change to move the pet's starting position
        self.move_speed = 6 # change how fast the pet moves in pixels

        # initialize frame arrays
        self.animation = dict(
            idle = [tkinter.PhotoImage(file=os.path.abspath('gifs/idle.gif'), format = 'gif -index %i' % i) for i in range(5)],
            idle_to_sleep = [tkinter.PhotoImage(file=os.path.abspath('gifs/idle-to-sleep.gif'), format = 'gif -index %i' % i) for i in range(8)],
            sleep = [tkinter.PhotoImage(file=os.path.abspath('gifs/sleep.gif'), format = 'gif -index %i' % i) for i in range(3)]*3,
            sleep_to_idle = [tkinter.PhotoImage(file=os.path.abspath('gifs/sleep-to-idle.gif'), format = 'gif -index %i' % i) for i in range(8)],
            walk_left = [tkinter.PhotoImage(file=os.path.abspath('gifs/walk-left.gif'), format = 'gif -index %i' % i) for i in range(8)],
            walk_right = [tkinter.PhotoImage(file=os.path.abspath('gifs/walk-right.gif'),format = 'gif -index %i' % i) for i in range(8)]
        )

        # window configuration
        self.root.overrideredirect(True) # remove UI
        if system() == 'Windows':
            self.root.wm_attributes('-transparent','black')
        else: # platform is Mac/Linux
            # https://stackoverflow.com/questions/19080499/transparent-background-in-a-tkinter-window
            self.root.wm_attributes('-transparent', True) # do this for mac, but the bg stays black
            self.root.config(bg='systemTransparent')
        
        self.root.attributes('-topmost', True) # put window on top
        self.root.bind("<Button-1>", self.onLeftClick)
        self.root.bind("<Button-2>", self.onRightClick)
        self.root.bind("<Button-3>", self.onRightClick)
        self.root.bind("<Key>", self.onKeyPress)
        self.label = tkinter.Label(self.root,bd=0,bg='black') # borderless window
        if system() != 'Windows':
            self.label.config(bg='systemTransparent')
        self.label.pack()
        
        screen_width = self.root.winfo_screenwidth() # width of the entire screen
        screen_height = self.root.winfo_screenheight() # height of the entire screen
        self.min_width = 10 # do not let the pet move beyond this point
        self.max_width = screen_width-110 # do not let the pet move beyond this point
        
        # change starting properties of the window
        self.curr_width = screen_width-self.pixels_from_right
        self.curr_height = screen_height-self.pixels_from_bottom
        self.root.geometry('%dx%d+%d+%d' % (100, 100, self.curr_width, self.curr_height))
        

    def update(self, i, curr_animation):
        # print("Curently: %s" % curr_animation)
        self.root.attributes('-topmost', True) # put window on top
        animation_arr = self.animation[curr_animation]
        frame = animation_arr[i]
        self.label.configure(image=frame)
        
        # move the pet if needed
        if curr_animation in ('walk_left', 'walk_right'):
            self.move_window(curr_animation)
        
        i += 1
        if i == len(animation_arr):
            # reached end of this animation, decide on the next animation
            next_animation = self.getNextAnimation(curr_animation)
            self.root.after(self.delay, self.update, 0, next_animation)
        else:
            self.root.after(self.delay, self.update, i, curr_animation)


    def onLeftClick(self, event):
        print("detected left click")
    
    
    def onRightClick(self, event):
        self.quit()


    def onKeyPress(self, event):
        if event.char in ('q', 'Q'):
            self.quit()
    
    
    def move_window(self, curr_animation):
        if curr_animation == 'walk_left':
            if self.curr_width > self.min_width:
                self.curr_width -= self.move_speed
            
        elif curr_animation == 'walk_right':
            if self.curr_width < self.max_width:
                self.curr_width += self.move_speed

        self.root.geometry('%dx%d+%d+%d' % (100, 100, self.curr_width, self.curr_height))
    

    def getNextAnimation(self, curr_animation):
        if curr_animation == 'idle':
            return random.choice(['idle', 'idle_to_sleep', 'walk_left', 'walk_right'])
        elif curr_animation == 'idle_to_sleep':
            return 'sleep'
        elif curr_animation == 'sleep':
            return random.choice(['sleep', 'sleep_to_idle'])
        elif curr_animation == 'sleep_to_idle':
            return 'idle'
        elif curr_animation == 'walk_left':
            return random.choice(['idle', 'walk_left', 'walk_right'])
        elif curr_animation == 'walk_right':
            return random.choice(['idle', 'walk_left', 'walk_right'])
         
    
    def run(self):
        self.root.after(self.delay, self.update, 0, 'idle') # start on idle
        self.root.mainloop()
    
    
    def quit(self):
        self.root.destroy()


if __name__ == '__main__':
    print('Initializing your desktop pet...')
    print('To quit, right click on the pet')
    pet = Pet()
    pet.run()
