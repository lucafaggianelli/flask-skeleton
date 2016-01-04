#!/usr/bin/env python
import sys
import os
from {[ name ]} import app

PORT = 5000
HOST = '127.0.0.1'

DIRS = (
)

if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
        HOST = '0.0.0.0'
    except:
        print 'Invalid port number', sys.argv[1]

for d in DIRS:
    try:
        os.makedirs(d, 0755)
        print 'Created folder:', d
    except OSError:
        pass

app.run(host=HOST,port=PORT,debug=True)
