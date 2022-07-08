Usage
=====

.. _installation:

Installation
------------

Installing ``skillsnetwork`` will depend on your local lab environment:

JupyterLab
++++++++++

Using the ``pip`` CLI:

.. code-block:: console

   $ pip install skillsnetwork

JupyterLite
+++++++++++

Using the ``piplite`` library:

.. code-block:: python

   import piplite
   await piplite.install(["skillsnetwork"])

Reading Files From URL
----------------------

Use the :func:`skillsnetwork.read` function to read files from URL to ``bytes``:

.. code-block:: python

   import skillsnetwork
   raw_content = await skillsnetwork.read("https://www.example.com/my/file.json")

This confirms the file was successfully read to string:

.. code-block:: python
   
   import json
   content = json.loads(raw_content)

.. note::

   To convert from ``bytes`` to ``str`` use :meth:`bytes.decode`.

Downloading Files From URL
--------------------------

Use the :func:`skillsnetwork.download` function to download files:

.. code-block:: python

   import skillsnetwork
   await skillsnetwork.download("https://www.example.com/my/file.json")

By default, the saved path will be printed:

.. code-block:: console

   ./file.json

This confirms the file is saved in your lab environment:

.. code-block:: python
   
   import json
   with open("file.json") as f:
       content = json.load(f)

Preparing and Extracting Large Datasets
---------------------------------------

Use the :func:`skillsnetwork.prepare` to manage large compressed datasets or datafiles:

.. code-block:: python

   import skillsnetwork
   await skillsnetwork.prepare("https://www.example.com/my/images.zip")

By default, the saved path will be printed:

.. code-block:: console

   .

This confirms the dataset was extracted to your current working directory in your lab environment:

.. code-block:: python
   
   from pathlib import Path
   for path in Path(".").rglob("*"):
       print(path)

.. code-block:: console

   ./image0.jpg
   ./image1.jpg
   ./image2.jpg
   ./image3.jpg
   ./image4.jpg
   ...