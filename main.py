import tkinter
import os
import random

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
        self.label = tkinter.Label(self.root,bd=0,bg='black') # borderless window
        self.root.overrideredirect(True) # remove UI
        self.root.wm_attributes('-transparentcolor','black')
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
        print("Curently: %s" % curr_animation)
        animation_arr = self.animation[curr_animation]
        frame = animation_arr[i]
        self.label.configure(image=frame)
        
        # move the pet if needed
        if curr_animation in ('walk_left', 'walk_right'):
            self.move_window(curr_animation)
        
        i += 1
        if i == len(animation_arr):
            # reached end of this animation, decide on the next animation
            next_animation = self.get_next_animation(curr_animation)
            self.root.after(self.delay, self.update, 0, next_animation)
        else:
            self.root.after(self.delay, self.update, i, curr_animation)


    def move_window(self, curr_animation):
        if curr_animation == 'walk_left':
            if self.curr_width > self.min_width:
                self.curr_width -= self.move_speed
            
        elif curr_animation == 'walk_right':
            if self.curr_width < self.max_width:
                self.curr_width += self.move_speed

        self.root.geometry('%dx%d+%d+%d' % (100, 100, self.curr_width, self.curr_height))
    

    def get_next_animation(self, curr_animation):
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

if __name__ == '__main__':
    pet = Pet()
    pet.run()