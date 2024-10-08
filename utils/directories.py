import os
import shutil

def makeDirectories(directories):
    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d)

def removeUnwantedContent(directories, files):
    for d in directories:
        if os.path.exists(d):
            shutil.rmtree(d)
    for f in files:
        if os.path.exists(f):
            os.remove(f)
    