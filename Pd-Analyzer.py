# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 2021

Based on unofficial documentation
See: https://puredata.info/docs/developer/PdFileFormat

@author: David Kettle
"""

import sys, os, getopt

messages = set(())
objects = set(())
arrays = set(())
libraries = set(())

def getOpts ():
    
    args = "i:h"
    longargs = [
        "input=",
        "help"]
    parms = {
        'input' : None
    }
    
    def usage ():
    
        opts = \
            "\t[-h | --help] (display help and exit)\n" + \
            "\t-i | --input <filename>\n"
            
        (path,file) = os.path.split(sys.argv[0])
        sys.stderr.write("Usage: " + file + "\n" + opts)
        
    try:
        opts, args = getopt.getopt(sys.argv[1:],args,longargs)
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit()
        
    for opt, arg in opts:
        if opt in ("-i","--input"):
            parms['input'] = arg
        elif opt in ("-h","--help"):
            usage()
            sys.exit()
    
    # Check for required parameters:
    if (parms['input']):
        return parms
    else:
        sys.stderr.write("Missing required parameter!\n")
        usage()
        sys.exit()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def process_obj (tokens):

    if tokens[4] == "bng":
        if tokens[9] != "empty":
            messages.add((tokens[9].replace('\\',''),'s'))
        if tokens[10] != "empty":
            messages.add((tokens[10].replace('\\',''),'r'))
    elif tokens[4] == "cnv":
        if tokens[8] != "empty":
            messages.add((tokens[8].replace('\\',''),'s'))
        if tokens[9] != "empty":
            messages.add((tokens[9].replace('\\',''),'r'))
    elif tokens[4] == "tgl":
        if tokens[7] != "empty":
            messages.add((tokens[7].replace('\\',''),'s'))
        if tokens[8] != "empty":
            messages.add((tokens[8].replace('\\',''),'r'))
    elif tokens[4] == "nbx":
        if tokens[11] != "empty":
            messages.add((tokens[11].replace('\\',''),'s'))
        if tokens[12] != "empty":
            messages.add((tokens[12].replace('\\',''),'r'))
    elif tokens[4] == "vsl":
        if tokens[11] != "empty":
            messages.add((tokens[11].replace('\\',''),'s'))
        if tokens[12] != "empty":
            messages.add((tokens[12].replace('\\',''),'r'))
    elif tokens[4] == "hsl":
        if tokens[11] != "empty":
            messages.add((tokens[11].replace('\\',''),'s'))
        if tokens[12] != "empty":
            messages.add((tokens[12].replace('\\',''),'r'))
    elif tokens[4] == "vradio":
        if tokens[9] != "empty":
            messages.add((tokens[9].replace('\\',''),'s'))
        if tokens[10] != "empty":
            messages.add((tokens[10].replace('\\',''),'r'))
    elif tokens[4] == "hradio":
        if tokens[9] != "empty":
            messages.add((tokens[9].replace('\\',''),'s'))
        if tokens[10] != "empty":
            messages.add((tokens[10].replace('\\',''),'r'))
    elif tokens[4] == "vu":
        if tokens[7] != "empty":
            messages.add((tokens[7].replace('\\',''),'r'))
    elif tokens[4] == "send" or tokens[4] == "s":
        messages.add((tokens[5].replace('\\',''),'s'))
    elif tokens[4] == "receive" or tokens[4] == "r":
        messages.add((tokens[5].replace('\\',''),'r'))
    else:       # must be abstraction
        if tokens[4] != "declare":
            objects.add(tokens[4])

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def process_element (tokens):

#    print(tokens)
    
    if tokens[1] == "array":
        arrays.add(tokens[2].replace('\\',''))
        return
    elif tokens[1] == "canvass":
        return
    elif tokens[1] == "connect":
        return
    elif tokens[1] == "coords":
        return
    elif tokens[1] == "declare":
        if tokens[2] == "-lib":
            libraries.add(tokens[3])
        return
    elif tokens[1] == "floatatom":
        if tokens[9] != "-":
            messages.add((tokens[9].replace('\\',''),'r'))
        if tokens[10] != "-":
            messages.add((tokens[10].replace('\\',''),'s'))
        return
    elif tokens[1] == "msg":
        msgs = tokens[4:6]
#        print("msgs: "+str(msgs))
        msgs = str(''.join(msgs))
#        print("msgs: "+str(msgs))
        msgs = msgs.split("\;")
        for msg in msgs:
            if msg != "":
#                print("msg: "+msg)
                messages.add((msg.replace('\\',''),'s'))
        return
    elif tokens[1] == "obj":
        process_obj(tokens)
        return
    elif tokens[1] == "restore":
        return
    elif tokens[1] == "symbolatom":
        if tokens[9] != "-":
            messages.add((tokens[9].replace('\\',''),'r'))
        if tokens[10] != "-":
            messages.add((tokens[10].replace('\\',''),'s'))
        return
    elif tokens[1] == "text":
        return
    else:
        sys.stderr.write("Invalid element type: " + tokens[1] + "\n")
        return
    
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def process_window (tokens):
    
    # Nothing to see here
    
    return

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def process_array (tokens):
    
    # Nothing to see here
    
    return

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
def process_line (line):
    
    tokens = line.split()
    
    if tokens[0] == "#X":       # element
        process_element(tokens)
    elif tokens[0] == "#N":     # new window (sub-patch)
        process_window(tokens)
    elif tokens[0] == "#A":     # array
        process_array(tokens)
    else:
        sys.stderr.write("Invalid chunk type: " + tokens[0] + "\n")

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def set2list (x):
    
    y = []
    for member in x:
        y.append(member)
    return y

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":

    lines = []
    
    parms = getOpts()
    if (not(parms)):
        sys.exit()
    (path, name) = os.path.split(parms['input'])
    
    # Read input file:
    
    ifile = open(parms['input'],"r")
    next = ''
    for line in ifile.readlines():
        if len(next) == 0:
            next = line.rstrip()
        else:
            next = next + ' ' + line.rstrip()
        if next[-1] == ';':
            lines.append(next[:-1])
            next = ''
    if len(next) > 0:   # every line must end with ';'
        sys.stderr.write("File incomplete!\n")
    ifile.close()
    
    # Process lines:
    
    for line in lines:
        process_line(line)
        
    # Write to output:
    
    for msg in set2list(messages):
        print(name+", message, "+msg[0]+", "+msg[1])
    for obj in set2list(objects):
        print(name+", object, "+obj)
    for arr in set2list(arrays):
        print(name+", array, "+arr)
    for lib in set2list(libraries):
        print(name+", library, "+lib)
