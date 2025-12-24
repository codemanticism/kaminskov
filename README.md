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
