# kaminskov
<img width="128" height="128" alt="kaminskov" src="https://github.com/user-attachments/assets/e1229569-9b7d-496e-9894-6900a8154c36" />

Text editor in which one can code in the terminal I made as an alternative to micro (https://github.com/zyedidia/micro). I made it because I wanted to edit `.html` files in it, but the Javascript code incorporated into the `.html` file itself was not treated as seperate by the current release of micro. It is compatible with the current release of PyPy for Python 3 which can be used for faster loading speeds. It is supposed to be easier than something like Vim, but it might be initially less intuitive than micro. 
- <kbd>CTRL</kbd> + <kbd>K</kbd>: Defining a starting point for the selection.
- <kbd>CTRL</kbd> + <kbd>L</kbd>: Cancelling the selection.
- <kbd>CTRL</kbd> + <kbd>C</kbd>: Copying the selection (from the starting point to where the cursor is at) and  the selection.
- <kbd>CTRL</kbd> + <kbd>S</kbd>: Saving a file or not (by leaving it empty).
- <kbd>CTRL</kbd> + <kbd>Q</kbd>: Saving or not (by leaving it empty) and quiting.
- <kbd>CTRL</kbd> + <kbd>F</kbd>: Finding a piece of text before or after the current position.
- <kbd>CTRL</kbd> + <kbd>R</kbd>: Replacing all instances of a piece of text with another piece of text.

This is the structure of the code:
- One for procesing the file. The examples can be used for understanding how it works.
- Two functions: one for moving the cursor one place to the left, one for shifting it one place to the right. They both should return a boolean and modify the array specified in the arguments, because arrays are "No Copy" values in Python.
- Two functions: one for determing if the position is at the first spot and one for comparing it with the last spot of the text.
- One for dealing with popups.
- One for finding and replacing all instances of something with something else.  
- One for finding an instance of something with regards to the current position of the cursor.
- One for determining, if *just* after the position, something appears.
- One for joining the strings that result from joining arrays of strings, since it is an array
- Main loop
  - State of the cursor -> special state or a vector. In the case it is a vector, then one is to indicate in what an array of the variable made to work as efficient for the data storage done, then the other is used to indicate in what element of that array which is a string with either length 0 or 1.
  - The data structure used is an array of arrays of strings, that should theorically either be empty or just have one character.
  - Depending on the key being pressed, it does something different.
  - It create a syntax highlighting map based on the `regex` array.
    - The `regex` array is composed of [regex which determines the segments of text to which the style (language) applies to, style itself] arrays.
      - Inside the style array is a bunch of arrays that can include keywords or patterns followed by the color number.
  - It adds the cursor. If `special`, then at the very start and if not, before creating the higlight map, it actually finds where that would be on the string.
