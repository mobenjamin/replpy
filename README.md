# ReplPy

## Usage
Just run the main.py with Python 2.7. Since Tk is part of this project, it might be necessary to install that (use `pacman -S tk` if using Arch Linux). 

You can exit the program using Ctrl+C (which doesn't work after opening a turtle window). You have to press Enter after Ctrl+C) or by typing `:exit`. 

The `test.scm` file contains a few fancy lambda definitions to test the functionality. It also opens a turtle window and moves the turtle 100 forward. Load the file by typing `(load "test.scm")`.

## Build in 
The following functionality is currently implemented:

### Scheme
* `define`
* `if`
* `cond`
* `lambda`
* `car`
* `cdr`
* `cons`
* `load` (loads a file)

### Math
* `\+`
* `\-`
* `\*`
* `/`
* `<`
* `\>`
* `=`
* `dsin` (returns sin of x degree)
* `rsin` (returns sin of x radians)
* `pi`
* `e`

### Misc
* `print`

### Turtle Graphics
This opens a graphic window when calling `(tinit w h)`. `w` and `h` are the height and width of the window.
The following functions are supported:
* `texit` (close the turtle window)
* `tforward` (move the turtle x forward)
* `tback` (move the turtle x back)
* `tleft` (rotate the turtle x degree to the left)
* `tright` (rotate the turtle x degree to the right)
* `tcircle` (draw a circle with radius x)
* `tsize` (set pen size of the turtle)
* `tspiral` (draw a rainbow spiral with x steps)
