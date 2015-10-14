#this file is a demo config
PROJECT='demo'
VERSION='0.0.1'
DEBUG = 1
DEFS =['']
LIBS = [
        {
            'name':'demolib1',
            'subdir':'lib1',
            'includes':['']
        },
        {
            'name':'demolib1',
            'subdir':'lib2',
            'includes':['']
        }
]
EXES = [
        {
            'name':'demoexe1',
            'subdir':'exe1',
            'includes':[''],
            'linkpaths':[''],
            'linklibs':['']
        }
]