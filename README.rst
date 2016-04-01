Accessing Video Files as Python Sequences
=========================================

Quite often I find myself writing scripts which need to load a few frames from a
video file, process them and save the result to disk. It's a pain to implement
video opening, seeking and decoding over and over again and complex Python
bindings are a little overkill for my needs.

Videosequence is a library which hides the complexity of simply opening a video
file in Python as a sequence of images. It exposes a video file as just that: a
Python sequence type containing `PIL <https://pillow.readthedocs.org/>`_
``Image``-s.

For example, suppose you want to dump every frame from a video stored in
``foo.mp4`` starting from frame 100:

.. code:: python

    from contextlib import closing
    from videosequence import VideoSequence

    with closing(VideoSequence("foo.mp4")) as frames:
        for idx, frame in enumerate(frames[100:]):
            frame.save("frame{:04d}.jpg".format(idx))

You can load a single frame from a sequence just as easily. Let's dump the final
frame to another JPEG:

.. code:: python

    from contextlib import closing
    from videosequence import VideoSequence

    with closing(VideoSequence("foo.mp4")) as frames:
        frames[-1].save("final-frame.jpg")

In general, the ``VideoSequence`` behaves as if it were a long list of each
frame in the video.

What VideoSequence does
-----------------------

* Frame-accurate seeking
* Single frame indexing (``vs[0]``, ``vs[-4]``, etc.)
* Querying the length of the video (``len(vs)``)
* Slicing a sequence of frames (``vs[100:]``, ``vs[-20:]``, ``vs[10:20]``,
  ``vs[::2]``, etc.)
* Frames are represented as RGB PIL ``Image`` objects.
* Can interoperate with ``numpy``. E.g. ``np.asarray(vs[0])``.

What VideoSequence does not
---------------------------

* Handle files without exactly one (and only one) video stream
* Audio

Caveats
-------

* Iterating forward one frame at a time is fast. Tricks such as iterating
  backwards or skipping *n* frames at a time work but is likely to be slow.
* The implementation is based on `GStreamer
  <https://gstreamer.freedesktop.org/>`_
  and so *de facto* only works on a modern Unix-alike such as Linux or FreeBSD.
* The `PyGObject introspection <https://wiki.gnome.org/Projects/PyGObject>`_
  libraries must be installed. (See below.)

Installing
----------

See the sections below for any OS-specific instructions. VideoSequence can be
installed from the PyPI:

.. code:: console

    $ pip install --user videosequence

It can also be installed directly from git:

.. code:: console

    $ pip install --user git+git://github.com/rjw57/videosequence

Ubuntu and Debian
`````````````````

To install the Python GObject bindings:

.. code:: console

    $ sudo apt install git1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 \
                       python-gi python3-gi

GStreamer is almost certainly already installed if you've got some modern
desktop environment. If not:

.. code:: console

    $ sudo apt install libgstreamer1.0-dev gstreamer1.0-plugins-good

Contributing
------------

Bug fixes and ports to new backends welcome. Please make sure that the tests
still pass via ``tox`` before opening a new pull request. New functionality
should come with tests, please.

Copyright and licensing
-----------------------

Videosequence is &copy; 2016 Rich Wareham. Full licence details can be found in
the `LICENCE.txt <LICENCE.txt>`_ file.
