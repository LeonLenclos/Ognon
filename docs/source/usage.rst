Usage
=====

Basic usage
-----------

Run ognon with 

::

 $ python -m ognon

Then go to http://localhost:40460/ with a modern browser.

What's going on ?
-----------------

Ognon prints out some informations :

::

 +------------+
 | Ognon v1.x |
 +------------+
 Working on file:///home/user/ognons/
 Serving on http://localhost:40460
 Serving on osc://localhost:50460

We got :

- The Ognon version
- The location on your computer where ognon saves and exports files
- The adress where the http server is serving
- The adress where the osc server is serving

If you visit the http adress (e.g. with firefox), you will find the *web interface*. This is where you can edit and manage your projects.

**You can now read the web interface guide** -> :ref:`ognonWebInterface`. 


Advanced command line options
------------------------------

- ``$ python -m ognon --help`` or ``-h`` : get the help
- ``$ python -m ognon --test`` or ``-t``  : run the tests (pytest)
- ``$ python -m ognon --browse`` or ``-b``  : open a web browser at the server adress
- ``$ python -m ognon --no-osc`` : do not start the osc server
- ``$ python -m ognon --ip-adress 1.2.3.4`` : set the server ip adress (default is localhost)
- ``$ python -m ognon --projects-dir /path/to/projects/directory/`` : set a different projects directory.

HTTP Server API
---------------

POST requests can be sent to the ognon server. data are sent and received in JSON.

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
			coords:[0,0,50,50]
		}
	}


OSC Server API
--------------

Ognon run two servers at the same time. The HTTP server (that is used in the web interface to get pages and to post requests) and the OSC server. The OSC server expects roughly the same types of requests than the POST handler of the HTTP server. But since the OSC protocole is simpler than HTTP, it will do less.

The Ognon OSC server should be able to handle requests on any *control function*. The request adress should be the path to the *control function* and a cursor id must be passed as a first argument.

.. warning:: Untested : Some requests may not be supported by the osc server. Because of the types of parameters.

.. seealso:: OSC specification on the official website : http://opensoundcontrol.org/spec-1_0

Paths
^^^^^

The server will look into ognon to find a control function corresponding to the path : :samp:`/control/{module}/{function}`.

For a complete list of *control functions* see :class:`ognon.control`.

For your OSC client you would probably want to use the *navigator* functions. They allow to navigate in the animation : :samp:`/control/navigator/{function}` (see :class:`ognon.control.navigator`)

Cursor id
^^^^^^^^^

The cursor id can be any string. But you may want to use ``default``. 

Server port
^^^^^^^^^^^

The port to the Ognon OSC server is ``50460``

Example
^^^^^^^

- To run the animation (``/step`` in Ognon v0) :
    :samp:`/control/navigator/run {cursor-id}`
- To play/pause the animation :
    :samp:`/control/navigator/play {cursor-id}`
- To go to the first frame of the animation (``/reset`` in Ognon v0) :
    :samp:`/control/navigator/go_to_first_frm {cursor-id}`
- To go to the nth frame of the animation :
    :samp:`/control/navigator/go_to_frm {cursor-id} {n}`
- To select an animation  :
    :samp:`control/animsmanager/select_anim {cursor-id} {name-of-the-animation}`

Control Ognon with OSC and Puredata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: static/pd/simple-ognon-osc-client.png
   :align: center
   
   *simple-ognon-osc-client.pd* 

:download:`download simple-ognon-osc-client.pd <static/pd/simple-ognon-osc-client.pd>`

.. seealso:: The good tutorial to use OSC with puredata :  http://write.flossmanuals.net/pure-data/osc/
