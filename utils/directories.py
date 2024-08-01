import os
import shutil

def makeDirectories(directories):
    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d)

def removeUnwantedContent(directories, files):
    for d in directories:
        shutil.rmtree(d)
    for f in files:
        os.remove(f)
    