# AI-assignment3


####To run this in the current working directory you have the following options'
&nbsp;&nbsp;&nbsp;python main.py 'path-to/your-file.txt' 'Heuristic Number 1 - 7'
<br />
<br />
This is the default run setting. It runs AStar with the provided board and uses the specified heuristic
<br />
<br />
<br />
&nbsp;&nbsp;&nbsp;python main.py 'Heuristic Number 1 - 7'
<br />
<br />
This is an additional run setting that is helpful for getting a sense of a heuristic preformance for a wide range of data. Running this generates a random map of size 650 x 650 and uses the specified heuristic to run AStar
<br />
<br />
<br />
&nbsp;&nbsp;&nbsp;python main.py
<br />
<br />
This is a catch-all run setting, that prevents an error from running with no program arguments. It runs a 20 x 20 board with Heuristic 0