import os
import sys
import urllib
import re
import types

def getRegex(regex,data):
    dat = re.compile(regex)
    ret = re.findall(dat,data)
    return ret

def color(note0,linedata,dics):
    #linechange = linedata
    note1 = note0 + linedata[linedata.find(note0)+1]
    linechange = linedata.replace(note1,'{{color:'+dics[note1]+'|',1).replace('\n','}}\n')
    for notex in dics.keys():
        linechange = linechange.replace(notex,'}}{{color:'+dics[notex]+'|')
    return linechange


def note(_note,diclist,formertxt,savetxt):
    formerline = []
    saveline = []
    with open(formertxt, 'r', encoding='utf-8') as file:
        for _line in file:
            formerline.append(_line)
    for lines in formerline:
        if _note in lines:
            saveline.append(color(_note,lines,diclist))
        else:
            saveline.append(lines)
    with open(savetxt, 'w', encoding='utf-8') as file:
        for saves in saveline:
            file.write('%s' % (saves))

note('·',{'·1':'#EE0000','·2':'#1E90FF','·3':'#7A378B'},'sf','sfx')
