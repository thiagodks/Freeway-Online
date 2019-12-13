#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create a lumnosity mask for the current layer 

# (c) Ofnuts 2019
#
#   History:
#
#   v0.0: 2019-11-14: Initial version
#   v0.1: 2019-11-14: Fix DDD curve (thanks Blighty)
#   v1.0: 2019-11-16: Add custom masks
#   v1.1: 2019-11-18: Add general "Initial luminosity" mask
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANDABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import sys,os,os.path,traceback,codecs,re
from gimpfu import *

debug='OFN_DEBUG' in os.environ
  
def trace(s):
    if debug:
        print (s)

channelPrefix='#Luminosity:' 

curves=[
    ('Raw luminosity',          'Starting point for your custom masks via "quickmask"',[0.00,0.00,1.00,1.00]),
    ('Patdavid/Lights/L',       'From Patdavid\'s tutorial',[0.00,0.00,1.00,1.00]),
    ('Patdavid/Lights/LL',      'From Patdavid\'s tutorial',[0.00,0.00,0.50,0.00,1.00,1.00]),
    ('Patdavid/Lights/LLL',     'From Patdavid\'s tutorial',[0.00,0.00,0.67,0.00,1.00,1.00]),
    ('Patdavid/Darks/D',        'From Patdavid\'s tutorial',[0.00,1.00,1.00,0.00]),
    ('Patdavid/Darks/DD',       'From Patdavid\'s tutorial',[0.00,1.00,0.50,0.00,1.00,0.00]),
    ('Patdavid/Darks/DDD',      'From Patdavid\'s tutorial',[0.00,1.00,0.33,0.00,1.00,0.00]),
    ('Patdavid/MidTones/M',     'From Patdavid\'s tutorial',[0.00,0.00,0.50,0.50,1.00,0.00]),
    ('Patdavid/MidTones/MM',    'From Patdavid\'s tutorial',[0.00,0.00,0.50,1.00,1.00,0.00]),
    ('Patdavid/MidTones/MMM',   'From Patdavid\'s tutorial',[0.00,0.00,0.33,1.00,0.67,1.00,1.00,0.00]),
    ]

def createMask(image,layer,name,curve):
    # Only work on layers or groups, exclude channels
    if not isinstance(layer,gimp.Layer):
        raise Exception('The active item is not a layer or a layer group')
    
    # Remove prevoiusly created luminosity channel(s) (normally only one)
    for c in image.channels:
        if c.name.startswith(channelPrefix):
            image.remove_channel(c)
    # Create channel
    lumChannel=gimp.Channel(image,channelPrefix+name,image.width,image.height,1.0,gimpcolor.RGB(255.,255.,255.))
    lumChannel.visible=False
    image.insert_channel(lumChannel,position=0)
    # Copy layer (copy/paste does auto desaturation with luminosity) 
    pdb.gimp_selection_none(image)
    pdb.gimp_edit_copy(layer)
    pdb.gimp_floating_sel_anchor(pdb.gimp_edit_paste(lumChannel,True))
    # Apply curves and set selection
    pdb.gimp_drawable_curves_spline(lumChannel,HISTOGRAM_VALUE,len(curve),curve)
    pdb.gimp_image_select_item(image,CHANNEL_OP_REPLACE,lumChannel)
    # Set source layer as active drawable again
    image.active_layer=layer

def protected(function):
    '''
    Create protected version of function
    '''
    def p(*parms):
        image=parms[0]
        pdb.gimp_image_undo_group_start(image)
        try:
            function(*parms)
        except Exception as e:
            traceback.print_exc()
            #print e.args[0]
            pdb.gimp_message(e.args[0])
        pdb.gimp_image_undo_group_end(image)
    return p

def menuFromName(name):
    split=name.split('/')
    if len(split)==1:
        return '',name
    else:
        return '/'+'/'.join(split[:-1]),split[-1]


### Registration
whoiam='\n'+os.path.abspath(sys.argv[0])
author='Ofnuts'
copyrightYear='2019'
desc='Create a luminosity mask for the current layer'
menuRoot=['<Image>/Select/Luminosity','<Image>/Test'][debug]

def createMaskPlugin(name,desc,curve):
    '''
    Create the function called as the plugin
    '''
    
    def maskPlugin(image,layer):
        createMask(image,layer,name,curve)
        
    menuLoc,menuEntry=menuFromName(name)
    atomSuffix=re.sub('[/ \']','-',name).lower()
    trace('Creating plugin for %r, atomSuffix: %r' % (name,atomSuffix))
    register(
        'ofn-luminosity-mask-%s' % atomSuffix,
        'Luminosity mask: %s %s' % (desc, whoiam),
        'Luminosity mask: %s' % desc,
        author,author,copyrightYear,menuEntry,"*",
        [(PF_IMAGE, "image", "Input image", None),(PF_DRAWABLE,'drawable','Input drawable',None),],[],
        protected(maskPlugin),
        menu=menuRoot+menuLoc,
    )

def readIniFile(iniFilePath):
    trace('Reading %s' % iniFilePath)
    curves=[]
    try:
        with codecs.open(iniFilePath, 'r', encoding='utf-8') as iniFile:
            for i,line in enumerate(iniFile,1):
                line=line.strip()
                if not line:
                    continue
                if line.startswith('#'):
                    continue
                curveData=line.split(';',2)
                if len(curveData)!=3:
                    trace('Line %d does not contain at least 3 elements' % i)
                    continue
                curveName=curveData[0].strip()
                curveDesc=curveData[1].strip()
                try:
                    curvePoints=[float(x) for x in curveData[2].split()]
                except ValueError as ve:
                    print('Line %d: %s' % (i,ve))
                    continue
                if len(curvePoints)<4:
                    print('Line %d: Curve definition should have be least 4 values' % i)                    
                    continue
                if len(curvePoints)%2:
                    print('Line %d: Curve definition should have an even number of values' % i)
                    continue
                curves.append((curveName,curveDesc,curvePoints))
    except Exception as e:
        print(e)
        traceback.print_exc()
    return curves
        
mydir,myfile=os.path.split(sys.argv[0])
iniFileName=os.path.splitext(myfile)[0]+'.ini'
dirs=[os.path.join(gimp.directory,'tool-presets'),os.path.join(gimp.directory),mydir]

for d in dirs:
    iniFilePath=os.path.join(d,iniFileName)
    trace('Checking %s' % iniFilePath)
    if os.path.isfile(iniFilePath):
        break
else:
    iniFilePath=None

if iniFilePath:
    curves=readIniFile(iniFilePath)

for name,desc,curve in curves:
    createMaskPlugin(name,desc,curve)

main()