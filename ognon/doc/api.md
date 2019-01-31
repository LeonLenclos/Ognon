## API

The ognon client (web interface) send requests to the ognon server (python code). Client and server talks with json data via POST requests.

#### Paths

`POST /*path*/*to*/*function*/`

the two kinds of functions that must be used are `/control/*controller*/*function*/` and `/view/*function*/`. 

#### Parameters



- `cursor` optional (string) : the id of the cursor to be used.
- `args` optional (object) : the args to be passed to the function
Keys are arguments names, values are arguments values. Can be ommited if the function take no other args than the cursor. 


#### Example

To draw a line on the cell curently pointed by the cursor 'default'.

	POST /control/drawer/draw
	{
		cursor:'default',
		args:{
			x1:23,
			x2:54
			y1:23,
			y2:54
		},
	}


## Structure of the app

Ognon is made with a *model, view, controller* approach.

### Model

The model describes every data that can be write on the disk. they are nested python classes. With no method description.

#### Project

- A list of animations
- A dict of settings

#### Animation

- A list of layers

#### Layer

- A list of ellements

#### Ellements

For now there is two kinds of ellements (cell and animref).

- A dict of options

##### Cell

- A list of lines (that are lists of points (that are a X and a Y))

##### AnimRef

- The name of the animation to play



### Cursor

The cursor is one of the most importants object. It is a point of view on a project, a *tape head*. It store a reference to the project, informations about his position and his state. It provides a bunch of getters and setters to move the cursor, know where it is and access to the ellements under it.


### Control

A bunch of stateless functions. organized into modules. They all take a cursor object as first argument. They dont return any value and raise an exception when they cant be executed in the current cursor's position.

### View

Same as control but they return something

