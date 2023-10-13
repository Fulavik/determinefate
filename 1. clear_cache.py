import os, sys 
findonly = False 
rootdir = os.getcwd() 

found = removed = 0

for (thisDirLevel, subsHere, filesHere) in os.walk(rootdir):

    for filename in filesHere:

        if filename.endswith('.pyc'):

            fullname = os.path.join(thisDirLevel, filename) 

            print('=>', fullname) 
            
            if not findonly:
                os.remove(fullname) 
                removed += 1
