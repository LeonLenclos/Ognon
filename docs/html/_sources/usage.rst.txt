Usage
=====

Basic usage
-----------

Run ognon with `$ python -m ognon`

Then go to http://localhost:40460/


Server API usage
----------------

POST requests can be send to the ognon server. data are sent and received in json.

Paths
^^^^^

The server will look into ognon to find a function corresponding to the path

::

    POST /path/to/function/

the two kinds of functions that must be used are `/control/controller/function/` and `/view/function/`. 

Parameters
^^^^^^^^^^

When a request is sent to the server, two parameters can be passed. They are both optional.

- `cursor` (string) : the id of the cursor to be used. (default is 'default')
- `args` (object) : the args to be passed to the function. Keys are arguments names, values are arguments values. Can be ommited if the function take no other args than the cursor. 


Example
^^^^^^^
To draw a line on the cell curently pointed by the cursor 'default'.

.. code-block:: javascript

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


OSC Server usage
----------------

Ognon run two servers at the same time. The HTTP server (that is used in the web interface to get pages and post requests) and the OSC server. The OSC server expects roughly the same types of requests than the POST handler of the HTTP server. But since the OSC protocole is simpler than HTTP, it will do less.

See -> http://opensoundcontrol.org/spec-1_0

The OSC server should be able to handle requests on **any control function that only take a cursor argument**. The request adress should be the path to the control function and a cursor id must be passed as an argument.

Paths
^^^^^
The server will look into ognon to find a control function corresponding to the path

::

    /control/<module>/<function>

Cursor id
^^^^^^^^^

For the cursor id you may want to use ``default``.

Server port
^^^^^^^^^^^

The new default port to the Ognon OSC server is ``504600`` (``5005`` in Ognon v0)

Example
^^^^^^^

To run the animation (``/step`` in Ognon v0)

:: 

	/control/navigator/run default

To go to the first frame of the animation (``/reset`` in Ognon v0)

:: 

	/control/navigator/go_to_first_frm default

To play/pause the animation

:: 

	/control/navigator/play default

