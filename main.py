import tkinter
import os
import random

class Pet:
    def __init__(self):
        self.window = tkinter.Tk()
        self.delay = 300 # delay in ms

        # initialize frame arrays
        self.animation = dict(
            idle = [tkinter.PhotoImage(file=os.path.abspath('gifs/idle.gif'), format = 'gif -index %i' % i) for i in range(5)],
            idle_to_sleep = [tkinter.PhotoImage(file=os.path.abspath('gifs/idle-to-sleep.gif'), format = 'gif -index %i' % i) for i in range(8)],
            sleep = [tkinter.PhotoImage(file=os.path.abspath('gifs/sleep.gif'), format = 'gif -index %i' % i) for i in range(3)],
            sleep_to_idle = [tkinter.PhotoImage(file=os.path.abspath('gifs/sleep-to-idle.gif'), format = 'gif -index %i' % i) for i in range(8)],
            walk_left = [tkinter.PhotoImage(file=os.path.abspath('gifs/walk-left.gif'), format = 'gif -index %i' % i) for i in range(8)],
            walk_right = [tkinter.PhotoImage(file=os.path.abspath('gifs/walk-right.gif'),format = 'gif -index %i' % i) for i in range(8)]
        )


        # window configuration
        self.label = tkinter.Label(self.window,bd=0,bg='black') # borderless window
        self.window.overrideredirect(True) # remove UI
        self.window.wm_attributes('-transparentcolor','black')
        self.label.pack()
        

    def update(self, i, curr_animation):
        print("Curently: %s" % curr_animation)
        animation_arr = self.animation[curr_animation]
        frame = animation_arr[i]
        self.label.configure(image=frame)
        
        i += 1
        if i == len(animation_arr):
            # reached end of this animation, decide on the next animation
            next_animation = self.get_next_animation(curr_animation)
            self.window.after(self.delay, self.update, 0, next_animation)
        else:
            self.window.after(self.delay, self.update, i, curr_animation)


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
        self.window.after(self.delay, self.update, 0, 'idle') # start on idle
        self.window.mainloop()

if __name__ == '__main__':
    pet = Pet()
    pet.run()