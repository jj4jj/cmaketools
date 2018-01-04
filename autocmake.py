#!/bin/python
#-*- coding:utf-8 -*-
import os
import sys
from jinja2 import Template 
cdr=os.path.dirname(__file__)
pctf=os.path.join(cdr,'project.cmake')
ptf=open(pctf).read(1024*1024)
pct = Template(ptf.decode('utf8')) 
##
uctf=os.path.join(cdr,'unit.cmake')
utf=open(uctf).read(1024*1024)
uct = Template(utf.decode('utf8')) 
def render(f,t,e,fe):
    print 'render file:%s ...'%(f,)
    open(f,'w').write(Template(Template(t.render(e)).render(fe)).render(e).encode('utf8'))

def run(wdr, config):
    prjc='/'.join((wdr,'CMakeLists.txt'))
    keys=filter(lambda xk:xk[0:2] != '__', dir(config))
    env={}
    fmte={}
    benv={}
    ########################################
    benv['cdir']='${CMAKE_CURRENT_SOURCE_DIR}'
    benv['root']='${PROJECT_SOURCE_DIR}'
    #reserve
    for k in keys:
        if k != 'env':
            env[k]=getattr(config,k)
        else:
            fmte=getattr(config,k)
            env['env']=fmte
    #########################################
    env.update(benv)
    fmte.update(benv)
    ##########################################
    render(prjc, pct, env, fmte)
    units = getattr(config,'units',[])
    for unit in units:
        env['unit']=unit
        #print str(unit.get('objs',None))
        render('/'.join((wdr, unit['subdir'], 'CMakeLists.txt')) ,uct,env, fmte)
    
if __name__ == '__main__':
    wdr='.'
    mdf='cmake_conf.py'
    if len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            wdr=os.path.dirname(sys.argv[1])
            mdf=os.path.basename(sys.argv[1])
        else:
            wdr=sys.argv[1]
    sys.path.append(wdr)
    mdc=__import__(mdf.split('.')[0])
    run(wdr, mdc)
    autogen=wdr+'/'+'autobuild.sh'
    if not os.path.exists(autogen):
        at=Template(open(os.path.join(cdr,'autobuild.sh')).read(1024*1024))
        render(autogen, at, {'autocmake_dir':cdr,"cmake_conf":os.path.join(wdr,mdf)},{})

