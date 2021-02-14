# Pd-Analyzer

Pd-Analyzer is a command-line utility that reads a Pure Data file (a "patch") and produces output in CSV format listing the messages sent and received by the patch, the Pure Data objects used in the patch, the libraries required by the patch (provided there's a "declare -lib" for each library), and any arrays defined in the patch. 

The output can be loaded into a spreadsheet program and linked into a MS Word-compatible document.

Although the internal details of the Pure Data file format are not officially documented and may change in future releases, I based it on some documentation available on the Pure Data web site:

https://puredata.info/docs/developer/PdFileFormat

It requires Python v3.x to run (although it could be easily converted to v2.x if you're still using v2.x). It uses only standard libraries (sys, os, getopt), so no additional libraries need to be installed in Python.

Typical usage:

> python Pd-Analyzer.py -i MyPatch.pd > MyPatch.csv

## Authors

David Kettle

# How to contribute

Feel free to suggest features or report bugs by opening an issue. If you'd like to make modifications to the code yourself, you can download or clone the code, but please understand that if you modify the code, I'm unable to provide support for your modified version. I'm the sole developer and only have time to support my own releases.
