# emfbadge-conway

Runs Conway's Game of Life on the 2016 EMB badge. The rules are pretty simple:

- If the cell is alive
	- If 2 to 3 surrounding cells are alive -> stay alive
	- If less than 2 or more than 3 are alive -> die

- If the cell is dead
	- If exactly 3 surrounding cells are alive -> live
	- Otherwise -> stay dead


