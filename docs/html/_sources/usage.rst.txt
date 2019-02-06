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
