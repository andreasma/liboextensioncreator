LibreOffice Extension Creator
=============================

The LibreOffice extension creator makes it more easy to create a non-code extension for LibreOffice. It provides an input form for the data for an extension with proper license information. The GUI/form is created by PyQt. It currently holds all fields to create a sceleton of a non-code LibreOffice extension.

The PyQt program will be updated regularly with new features to add languages and the features to create complete non-code LibreOffice extensions.


Requirements
------------

If you want to run the code you should create a Python 3 (>= 3.6) virtual environment.
Then please install with pip3 the following packages:
- PyQt5
- validators

and if you want to create a binary file you should also install with pip3:
- PySide2
- PyInstaller
