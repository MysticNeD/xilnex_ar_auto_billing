To add/modify coordinates, make sure to use the same format:

if you want to add/change a specific coordinate, head to config.py and look for the name:

blank_click to confirmation_click are on sales invoice tab (the billing part)
position_1 to position_13 are the 13 transfer notes in a page (if it is not 13, check resolution or zoom in settings)

to add coordinaates, make sure you only add in config and insert into final_version.py with example below:
'
'
v
pa.click(x=COORDINATES['confirm'][0], y=COORDINATES['confirm'][1])

if you wish to add a new file, dont forget to import config "from config import COORDINATES"
0 = first position(x) , 1 = second position(y)
