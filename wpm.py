import curses
from curses import wrapper
import time
import random 

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr(1,0,"Welcome to the Word Per Minute Game! ", curses.color_pair(3))
    stdscr.addstr(2,0,"Press any key to begin! ", curses.color_pair(2))
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm,cpm):
    stdscr.addstr(target, curses.color_pair(3))
    stdscr.addstr(2,0,f"WPM: {wpm}")
    stdscr.addstr(2,8,f"Character Per minute: {cpm}")
    #printing the loaded text and our wpm

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
            #if the text matches, green color else it's displayed in red.
        stdscr.addstr(0, i, char , color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines() 
        return random.choice(lines).strip()

def wpm_test(stdscr):
    target_text= load_text()
    current_text = []
    wpm = 0
    cpm = 0
    start_time= time.time()
    stdscr.nodelay(True)
    # loading text from file, making a current text file for typing, wpm variable for calculating it, starting the timer
    # making the screen have no delay.
    i = 0
    while True:
        time_elapsed = max(time.time() - start_time , 1)
        wpm = round((len(current_text) /(time_elapsed / 60)) / 5)
        cpm = round(len(current_text) /(time_elapsed / 60))
        #calculating wpm and cpm
        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm, cpm)
        #displaying the text
        stdscr.refresh()
        if "".join(current_text) == target_text: #making it a string from a list, checking if both of the text matches
            color = curses.color_pair(2)
            rwpm = round(i/(time_elapsed/60)/5)
            rcpm = round(i/(time_elapsed/60))
            stdscr.addstr(3, 0,f"Raw WPM: {rwpm}",color)
            stdscr.addstr(3, 13,f"Character Per minute: {rcpm}",color)
            if wpm <= 20:
                stdscr.addstr(4,0 ,"You're a Sloth.")
            elif wpm <= 40:
                stdscr.addstr(4,0 ,"You're a T-Rex.")
            elif wpm < 60:
                stdscr.addstr(4, 0, "You're very close to become a Cheetah.")
            else:
                stdscr.addstr(4,0, "You're a Cheetah.")
            stdscr.nodelay(False)
            break
        try:
            key = stdscr.getkey()
            i+=1
            # making the screen no delay means it's constantly running, so we're handling an exception here.
            # if using the getkey() gives an error, we are going to skip over the loop
        except:
            continue

        if ord(key) == 27:
            stdscr.nodelay(False)
            #if ESC is pressed, we break out of the program.
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
                #typing backslash erases the last letter from current text
        elif len(current_text) < len(target_text):
            current_text.append(key)
    
def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
       # time_elapsed, i= 
        stdscr.addstr(5,0, "You completed the text! Press any key to continue.")
        key2 = stdscr.getkey()
        #pressing anything except ESC will make us play the game once again.
        if ord(key2) == 27:
            break
    

wrapper(main)