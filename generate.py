#!/bin/python
#-*-coding:utf8-*-
import sys
import os

template_path=os.path.join(os.path.dirname(__file__),'templates')

def copy_replace_file(srcfile, dstfile, replaces):
    print("generate file:"+dstfile+" ...")
    with open(srcfile, "r") as f:
        data = f.read()
        for key in replaces:
            data = data.replace(key, str(replaces[key]))
        with open(dstfile, "w") as of:
            of.write(data)

def path_fixing(path):
    if path.find('/') == 0:
        return path
    else:
        return '${PROJECT_SOURCE_DIR}/'+path

def generate(desc , path):
    rootf = os.path.join(template_path,'root.txt')
    libf = os.path.join(template_path,'lib.txt')
    exef = os.path.join(template_path,'exe.txt')
    definations = '\n'.join(map(lambda s:'ADD_DEFINITIONS(-D'+s+')',desc.DEFS))
    if len(desc.DEFS) == 0 :
        definations=''

    if len(desc.LIBS) + len(desc.EXES) == 0:
        print("not found lib or exe modules")
        sys.exit(-1)

    subdirs = ''
    if len(desc.LIBS) > 0 :
        subdirs = subdirs + '\n'.join(map(lambda l:'add_subdirectory('+l['subdir']+')', desc.LIBS))
    subdirs = subdirs + '\n';
    if len(desc.EXES) > 0 :
        subdirs = subdirs + '\n'.join(map(lambda l:'add_subdirectory('+l['subdir']+')', desc.EXES))

    copy_replace_file(rootf, path+'/CMakeLists.txt',
            {'<definations>': definations,
             '<debug_mode>': desc.DEBUG,
             '<project_name>': desc.PROJECT,
             '<add_subdirectory_area>': subdirs,
             '<project_version>': desc.VERSION})

    for lib in desc.LIBS:
        includes = '\n'.join(map(path_fixing,lib['includes']))
        subf=os.path.join(path,lib['subdir'],'CMakeLists.txt')
        copy_replace_file(libf, subf,
            {'<lib_name>': lib['name'],
             '<includes>': includes})

    for exe in desc.EXES:
        includes = '\n'.join(map(path_fixing,exe['includes']))
        subf=os.path.join(path,exe['subdir'],'CMakeLists.txt')
        linkpaths = '\n'.join(map(path_fixing,exe['linkpaths']))
        linklibs = '\n'.join(exe['linklibs'])
        copy_replace_file(exef, subf,
            {'<exe_name>': exe['name'],
             '<includes>': includes,
             '<linkpaths>': linkpaths,
             '<linklibs>': linklibs})

def main(desc_file_path):
    #import desc_file
    path=os.path.dirname(desc_file_path)
    name=os.path.basename(desc_file_path)
    sys.path.append(path)
    desc=__import__(name)
    generate(desc, path)

def usage():
    print("./generate.py <description filepath>")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
        sys.exit(-1)
    main(sys.argv[1])
