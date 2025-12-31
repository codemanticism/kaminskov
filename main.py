import time
from sys import argv
import subprocess
import signal
import locale
import tkinter as tk
from tkinter import simpledialog
import threading
import time
import re
import curses
txt = ""
file_input = ""
locale.setlocale(locale.LC_ALL, "")
regexes = [[r"[\s\S]*", []]]
regex = []
def process(string, default):
    global regexes
    for line in string.split("\n"):
        if len(line) >= 1:
            if line[0] == '@':
                count = 0
                a = ""
                b = ""
                pieces = re.split(r"(?<!\\)\'", line[1:]) 
                for piece in pieces:
                    if count == 1:
                        a = piece
                    elif count == 3:
                        open_file = open(piece, "r")
                        read_file = open_file.read()
                        regexes.append([a, []])
                        process(read_file, len(regexes) - 1)
                        open_file.close()
                    count += 1
            elif line[0] == ':':
                t = ""
                count = 0
                pieces = re.split(r"(?<!\\)\'", line[1:])
                for piece in pieces:
                    if count == 1:
                        t = piece
                    elif count == 3:
                        regexes[default][1].append([t, int(piece)])            
                    count += 1
def before(optimizing_data_structure, position, special, yes_or_no):
    if special:
        return True
    if is_first(optimizing_data_structure, position):
        return True
    while True:
        old_position = [position[0], position[1]]
        if (position[1] - 1) >= 0:
            position[1] -= 1
        else:
            if (position[0] - 1) >= 0:
                px = [position[0],-1]
                while px[1] == -1:
                    px[0] -= 1
                    px[1] = len( optimizing_data_structure[ px[0] ] ) - 1
                if px[1] == -1:
                    return                
                position[0] = px[0]
                position[1] = px[1]
        if old_position == position:
            return special
        if optimizing_data_structure[position[0]][position[1]] != '':
            return special
    return special
def after(optimizing_data_structure, position, special, yes_or_no):
    if special:
        return False
    if is_last(optimizing_data_structure, position):
        return special
    while True:
        old_position = [position[0], position[1]]
        if (position[1] + 1) < len(optimizing_data_structure[ position[0] ]):
            #print("after-a")
            position[1] += 1
        else:
            #print("after-b")
            if (position[0] + 1) < len(optimizing_data_structure ):
                #print("after-c")
                px = [position[0],-1]
                while px[1] == -1:
                    px[0] += 1
                    px[1] = 0
                    if len( optimizing_data_structure[ px[0] ] ) == 0:
                        px[1] = -1
                if px[1] == -1:
                    return
                position[0] = px[0]
                position[1] = px[1]
        if old_position == position:
            return special
        if optimizing_data_structure[position[0]][position[1]] != '':
            return special
            #print(position == px, "?")
    return special
def is_first(optimizing_data_structure, position):
    if (len(transform_to_text(optimizing_data_structure)) == 0):
        return True
    px = [0,0]
    special = False
    while optimizing_data_structure[px[0]][px[1]] == '':
        special = after(optimizing_data_structure, px, False, False)
    return px == position
def is_last(optimizing_data_structure, position):
    if (len(transform_to_text(optimizing_data_structure)) == 0):
        return True    
    px = [ len(optimizing_data_structure) - 1 , 0 ]
    special = False
    while len(optimizing_data_structure[px[0]]) == 0:
        px[0] -= 1
    px[1] = len(optimizing_data_structure[ px[0] ]) - 1
    while optimizing_data_structure[px[0]][px[1]] == '':
        special = before(optimizing_data_structure, px, special, False)
    #print( optimizing_data_structure[1][0] )
    #print(px, position)
    #print(len(optimizing_data_structure) - 1)
    return px == position
def multi_input_popup(title, string_arrays):
    # Hidden root
    root = tk.Tk()
    root.withdraw()

    # Popup window
    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("600x600")
    entries = []

    for some_string in string_arrays:
        tk.Label(popup, text=some_string).pack(pady=5)

        text = tk.Text(popup, width=30, height=4)
        text.pack(pady=5)

        entries.append(text)
        
    validation = []
    def on_ok():
        validation.clear()
        for text in entries:
            validation.append(text.get("1.0", "end-1c"))  # keep newlines
        popup.destroy()
        root.destroy()

    def on_close():
        # Return empty list
        validation.clear()
        popup.destroy()
        root.destroy()
    popup.bind("<Control-Return>", lambda event: on_ok())
    popup.bind("<Control-Enter>",  lambda event: on_ok())
    popup.protocol("WM_DELETE_WINDOW", on_close)
    tk.Button(popup, text="OK", command = on_ok).pack(pady=10)

    popup.mainloop()
    return validation
def find_and_replace(optimizing_data_structure, match_with, replace_with):
    position = [0,0]
    special = False
    while optimizing_data_structure[position[0]][position[1]] == '':
        special = after(optimizing_data_structure, position, False)
    while True:
        px = [0,0]
        px[0] = position[0]
        px[1] = position[1]
        #print("*")
        if compare(optimizing_data_structure, px, match_with):
            index = 0
            while index < len(match_with):
                #print("?")
                if index < len(replace_with):
                    optimizing_data_structure[position[0]][position[1]] = replace_with[index]
                else:
                    optimizing_data_structure[position[0]][position[1]] = '' # lack of alignment between
                special = after(optimizing_data_structure, position, False)
                index += 1
                if (index) == len(match_with):
                    special = before(optimizing_data_structure, position, special, False)
            if (len(match_with)) < len(replace_with):
                for character in replace_with[len(match_with):]:
                    #print("!")
                    if (position[0] + 1) not in range(len(optimizing_data_structure)):
                        optimizing_data_structure.append([character])
                    else:
                        optimizing_data_structure[position[0]].insert(1 + position[1], character)
                    special = after(optimizing_data_structure, position, False,  False)
        else:
            special = after(optimizing_data_structure, position, False)
            if is_last(optimizing_data_structure, position):
                return
def find(optimizing_data_structure, match_with, order, position):
    px = [position[0], position[1]]
    times= 0
    special = False
    if order < 0:
        while True:
            px_copy = [px[0], px[1]]
            if compare(optimizing_data_structure, px_copy, match_with):
                times += 1
                if ((-1) * order) == times:
                    position[0] = px[0]
                    position[1] = px[1]
                    return
            special = before(optimizing_data_structure, px, special, False)
    elif order > 0:
        while True:
            px_copy = [px[0], px[1]]
            if compare(optimizing_data_structure, px_copy, match_with):
                times += 1
                if order == times:
                    position[0] = px[0]
                    position[1] = px[1]
                    return
            special = after(optimizing_data_structure, px, special, False)
def compare(optimizing_data_structure, position, match_with):
    index = 0
    special = False
    while index < len(match_with):
        if optimizing_data_structure[ position[0] ][ position[1] ] != match_with[index]:
            return False
        special = after(optimizing_data_structure, position, special, False)
        index += 1
    return True
def transform_to_text(array):
    list_of_things_that_will_be_displayed = []
    for key in range(len(array)):
        list_of_things_that_will_be_displayed.append( "".join( array[key] ) )
    # Iterate over all non-overlapping matches
    return "".join(list_of_things_that_will_be_displayed)
def main(stdscr):
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    global regexes
    global txt
    if len(argv) >= 2:
        if "." in argv[1]:
            seperation = argv[1].split(".")
            style_file = open(seperation[len(seperation)  - 1] + '.txt', "r") 
            style = style_file.read()
            process(style, 0)
            style_file.close()
    try:
        optimizing_data_structure = []
        read_text_file = open(argv[1], "r")
        text_contents = read_text_file.read()
        if len(text_contents) == 0:
            text_contents = " "
        for character in text_contents:
            optimizing_data_structure.append([character])    
        read_text_file.close()
    except:
        optimizing_data_structure = [[' ']] # A data structure optimized for the purpose of addition and deletion
    new_text = []
    save_as = ""
    special = False
    position = [0,0]
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.curs_set(0)      # hide cursor
    stdscr.nodelay(False)  # wait for keypress
    stdscr.addstr("Press keys (q to quit)\n")
    curses.start_color()
    curses.use_default_colors()  # optional, but recommended
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    stdscr.scrollok(True)
    able_to_be_modified = True
    position_copy = [-1,-1]
    special_copy = False
    clipboard = ""
    curses.raw()          # Ctrl+C becomes input, not SIGINT
    curses.noecho()       # optional
    stdscr.keypad(True)   # optional but recommended
    
    while True:
        keyboard_key = stdscr.get_wch()
        # Dealing with keys
        if isinstance(keyboard_key, int):
            if keyboard_key == curses.KEY_UP:
                while (optimizing_data_structure[position[0]][position[1]] != '\n') and (is_first(optimizing_data_structure , position) == False):
                    special = before(optimizing_data_structure, position, special, True)
                special = before(optimizing_data_structure, position, special, True)
                while (optimizing_data_structure[position[0]][position[1]] != '\n') and (is_first(optimizing_data_structure , position) == False):
                    special = before(optimizing_data_structure, position, special, True)
                special = after(optimizing_data_structure, position, special, True)           
            elif keyboard_key == curses.KEY_DOWN:
                #print( is_last(optimizing_data_structure , position) == False )
                while (optimizing_data_structure[position[0]][position[1]] != '\n') and (is_last(optimizing_data_structure , position) == False):
                    special = after(optimizing_data_structure, position, special, True)
                special = after(optimizing_data_structure, position, special, True)
            elif keyboard_key == curses.KEY_LEFT:
                special = before(optimizing_data_structure, position, special, True)
            elif keyboard_key == curses.KEY_RIGHT:
                special = after(optimizing_data_structure, position, special, True)
        else:
            if (keyboard_key == '\b'):
                if(position_copy[0] != -1):
                    position_start = [position_copy[0], position_copy[1]]
                    special_start = special_copy
                    while (special_start != special) or (position_start != position):
                        special_start = after(optimizing_data_structure, position_start, special_start, True)
                        if special_start == False:
                            optimizing_data_structure[position_start[0]][position_start[1]] = ''    
                    position_copy[0] = -1
                if able_to_be_modified:
                    if(special == False):
                        optimizing_data_structure[position[0]][position[1]] = '' # lack of alignment between
                    special = before(optimizing_data_structure, position, special, True)
            elif (keyboard_key == '\x0b'): # CTRL + K
                able_to_be_modified = False
                position_copy[0] = position[0]
                position_copy[1] = position[1]
                special_copy = special
            elif (keyboard_key == '\x0c'): # CTRL + L
                position_copy[0] = -1
                able_to_be_modified = True
            elif (keyboard_key == '\x03'): # CTRL + C
                if(position_copy[0] != -1):
                    position_start = [position_copy[0], position_copy[1]]
                    special_start = special_copy
                    clipboard = []
                    while (special_start != special) or (position_start != position):
                        special_start = after(optimizing_data_structure, position_start, special_start, True)
                        if special_start == False:
                            clipboard.append( optimizing_data_structure[position_start[0]][position_start[1]] )  
                    clipboard_str = "".join(clipboard)
                    subprocess.run(
                        ["xclip", "-selection", "clipboard"],
                        input=clipboard_str,
                        text=True,
                        check=True
                    )
                    position_copy[0] = -1
                    able_to_be_modified = True
            elif (keyboard_key == '\x13') or (keyboard_key == '\x11'): #CTRL + S, CTRL + Q
                if len(argv) >= 2:
                    try: 
                        write_file = open(argv[1], "w")
                        write_file.write(transform_to_text(optimizing_data_structure))
                        write_file.close()
                        if (keyboard_key == '\x11'):
                            return
                        continue
                    except:
                        0
                if save_as == "":
                    save_as_array = multi_input_popup("Save popup", ["Save as ..."])
                    if len(save_as_array) > 0:
                        save_as = save_as_array[0]
                if save_as != "":    
                    write_file = open(save_as, "w")
                    write_file.write(transform_to_text(optimizing_data_structure))
                    write_file.close()            
                if (keyboard_key == '\x11'):
                    return
            elif keyboard_key == '\x06':
                an_array = multi_input_popup("Find", ["Find", "Distance (negative number or positive number or zero to cancel)"])
                if an_array == ['','']:
                    continue
                find( optimizing_data_structure, an_array[0], int(an_array[1]), position)
            elif keyboard_key == '\x12':
                if able_to_be_modified:
                    an_array = multi_input_popup("Find and replace all popup", ["Find", "Replace with"])
                    if an_array == ['','']:
                        continue
                    find_and_replace( optimizing_data_structure, an_array[0], an_array[1])
                    last = len(optimizing_data_structure) - 1
                    position = [last ,len(optimizing_data_structure[last]) - 1]
                    special = False
            elif keyboard_key == '\n':
                if able_to_be_modified:
                    some_copy_special = special
                    some_copy_position = [ position[0], position[1] ]
                    if (optimizing_data_structure[ some_copy_position[0] ][ some_copy_position[1] ] == '\n'):
                        some_copy_special = before(optimizing_data_structure, some_copy_position, some_copy_special, False)
                    while (is_first(optimizing_data_structure, some_copy_position) == False):
                        some_copy_special = before(optimizing_data_structure, some_copy_position, some_copy_special, False)
                        if (optimizing_data_structure[ some_copy_position[0] ][ some_copy_position[1] ] == '\n'):
                            some_copy_special = after(optimizing_data_structure, some_copy_position, some_copy_special, False)
                            break
                    some_copy_special_copy = some_copy_special
                    some_copy_position_copy = [some_copy_position[0], some_copy_position[1]] 
                    clone_this = ['\n']
                    while (optimizing_data_structure[ some_copy_position_copy[0] ][ some_copy_position_copy[1] ] == '\t') or (optimizing_data_structure[ some_copy_position_copy[0] ][ some_copy_position_copy[1] ] == ' '):
                        clone_this.append( optimizing_data_structure[ some_copy_position_copy[0] ][ some_copy_position_copy[1] ] )
                        if (is_last(optimizing_data_structure, some_copy_position_copy)):
                            break
                        some_copy_special_copy = after(optimizing_data_structure, some_copy_position_copy, some_copy_special_copy, False)                
                    for character_in_clone_this in clone_this:
                        if(special):
                            optimizing_data_structure[position[0]].insert(0, character_in_clone_this)
                        else:
                            if (position[0] + 1) not in range(len(optimizing_data_structure)):
                                optimizing_data_structure.append([character_in_clone_this])
                            else:
                                optimizing_data_structure[position[0]].insert(1 + position[1], character_in_clone_this)
                        special = after(optimizing_data_structure, position, special, True)       
            else:
                if able_to_be_modified:            
                    if(special):
                        optimizing_data_structure[position[0]].insert(0, keyboard_key)
                    else:
                        if (position[0] + 1) not in range(len(optimizing_data_structure)):
                            optimizing_data_structure.append([keyboard_key])
                        else:
                            optimizing_data_structure[position[0]].insert(1 + position[1], keyboard_key)
                    special = after(optimizing_data_structure, position, special, True)
        #print(position)
        position_on_the_line = 0
        enabled = False
        if len(optimizing_data_structure[position[0]][position[1]]) == 0:
            special = before(optimizing_data_structure, position, special, False)
            if len(optimizing_data_structure[position[0]][position[1]]) == 0:
                special = True
        i = 0
        if special == False:
            ps = [0,0]
            if len(optimizing_data_structure[0]) > 0:
                while (position[0] != ps[0]) or (ps[1] != position[1]):
                    if(optimizing_data_structure[ps[0]][ps[1]] != ''):
                        i += 1
                    after(optimizing_data_structure, ps, False, False)
        file_input = transform_to_text(optimizing_data_structure)
        what_will_be_shown = []
        areas_in_which_it_applies = []
        count = len(regexes) - 1
        #print(regexes[0][0])
        while count >= 0:
            areas_in_which_it_applies.append([])
            for match in re.finditer(regexes[count][0], file_input):
                start_index = match.start()
                end_index = match.end()
                pos = [start_index, end_index]
                boolean1 = False
                boolean2 = False
                #other -> element_pos
                for area in areas_in_which_it_applies:
                    for element_pos in area:
                        if (element_pos[0] >= start_index): 
                            boolean1 = True
                        if (element_pos[1] <= end_index):
                            boolean2 = True
                if boolean1 and boolean2:
                    areas_in_which_it_applies[len(areas_in_which_it_applies) - 1].append([start_index, element_pos[0]])
                    areas[len(areas) - 1].append([])
                    pos = [element_pos[1], end_index]
                elif boolean1:
                    pos = [start_index, element_pos[0]]
                elif boolean2:
                    pos = [element_pos[1], end_index]     
                areas_in_which_it_applies[len(areas_in_which_it_applies) - 1].append(pos)
                # Get the matched string
                matched_string = match.group()
                # Get the span as a tuple
                span_tuple = match.span()
            count -= 1
        #print(areas_in_which_it_applies)
        # areas_in_which_it_applies[ ]
        areas = []
        f = [0,0,0]
        number = len(areas_in_which_it_applies) - 1
        while number >= 0:
            areas.append([])
            for some_range in areas_in_which_it_applies[number]:
                areas[f[0]].append([])
                for regex in regexes[number][1]:
                    areas[f[0]][f[1]].append([])
                    # print(regex[0], file_input[some_range[0]:some_range[1]])
                    for match in re.finditer(regex[0], file_input[some_range[0]:some_range[1]]):
                        start_index = match.start()
                        end_index = match.end()
                        areas[f[0]][f[1]][f[2]].append([some_range[0] +  start_index, some_range[0] + end_index, regex[1]])
                    f[2] += 1
                f[1] += 1
            number -= 1
            f[0] += 1
        stdscr.erase()
        stdscr.move(0, 0) 
        cursor = 0
        for character_id in range(len(file_input)):
            no_color = True
            for super_super_area_integer in range( len(areas ) ):
                for super_area_integer in range(len(areas[super_super_area_integer])):
                    for area_integer in range(len(areas[super_super_area_integer][super_area_integer])):
                        for sub_area_integer in range(len(areas[super_super_area_integer][super_area_integer][area_integer])):
                            three_values = areas[super_super_area_integer][super_area_integer][area_integer][sub_area_integer]
                            upper_bound = three_values[1]
                            lower_bound = three_values[0]
                            color = three_values[2]
                            if (character_id <= upper_bound) and (character_id >= lower_bound):
                                if no_color:
                                    no_color = False
                                    what_will_be_shown.append( [color + 2, file_input[character_id]] )
            if no_color:
                what_will_be_shown.append( [2, file_input[character_id]] )
        #print(what_will_be_shown)
        if special:
            stdscr.addstr("█" )
        j = 0
        for color_id, text in what_will_be_shown:
            stdscr.addstr(text, curses.color_pair(color_id))
            if special == False:
                if i == j:
                    stdscr.addstr("█")
            j += 1
        stdscr.refresh()
curses.wrapper(main)
