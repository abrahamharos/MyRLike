import json
import sys
import pprint

functionDirectory = {}
constantDirectory = {}
quadruples = {}
programName = ''

def loadData(filename):
    global functionDirectory, constantDirectory, quadruples, programName

    try:
        f = open(filename,)
        data = json.load(f)

        functionDirectory = data['functionDirectory']
        constantDirectory = data['constantDirectory']
        quadruples = data['quadruples']
        programName = data['programName']
    except:
        print('An Error ocurred while opening the compiled file ' + filename)
        exit()

def mountGlobalMemory():
    print(programName)

def main(filename):
    loadData(filename)
    mountGlobalMemory()

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Please provide a valid filename as parameter\n Example: ovejota.myRLike")
        exit()

    main(sys.argv[1])