#-*- coding:utf-8 -*-
__author__ = 'JasonTan'

import re
import sys
import os
import string

OUTDIR = 'output'
SOURCEDIR = 'source'
INPUTDIR = 'input'



def replaceTag(indir, outdir):
    """
     将原始文档中的timex3 标签替换
    """
    files = os.listdir(indir)
    for name in files:
        oldfile = open(indir + os.sep + name, 'r')
        olddata = oldfile.read()
        oldfile.close()

        olddata = olddata.replace('type=', 'TYPE=')
        olddata = olddata.replace('value=', 'VAL=')

        if not os.path.isdir(outdir):
            os.mkdir(outdir)
        out = open(outdir + os.sep + name, 'w')
        out.write(olddata)
        out.close()



#返回原始文档中TEXT前所有标签内容 和TEXT之间的内容
def getcommmon(content, filename):
    #读原始语料文档
    oldfile = open(SOURCEDIR + os.sep + filename, 'r')
    olddata = oldfile.read()
    newdata = content

    textpa = re.compile(r'<TEXT>(.*?)</TEXT>',re.DOTALL)
    textold = textpa.findall(olddata)[0].strip()
    textnew = textpa.findall(newdata)[0].strip()

    eventpa = re.compile(r'(<EVENT.*?>(.*?)</EVENT>)')
    timex3pa = re.compile(r'(<TIMEX3.*?>(.*?)</TIMEX3>)')
    event = eventpa.findall(textnew)
    timex3 = timex3pa.findall(textnew)

    # print(event)
    # print(timex3)
    textold = textold.replace('\n','</s>\n')
    # print(textold)
    #替换event标签
    start = 0
    oldstr = textold.split()
    # print(oldstr)
    for word in event:
        index = start
        while index < len(oldstr):
            if oldstr[index].find(word[1]) != -1:
                ss = oldstr[index].index(word[1]);
                tmp = oldstr[index][:ss]
                tmp = tmp + word[0]
                tmp = tmp + oldstr[index][ss+len(word[1]):]
                oldstr[index] = tmp
                # oldstr[index] = word[0]
                break
            index = index + 1
        start = index + 1

    textold = ' '.join(oldstr)
    # print(textold)
    #替换时间标签
    results = ''
    for timex in timex3:
        # print(timex)
        #修改TIMEX3 属性标签
        timestr = timex[0].replace('TYPE', 'type')
        timestr = timestr.replace('VAL', 'value')
        timestr = timestr.replace('MOD', 'mod')
        timestr = timestr.replace('ALT_value','value')
        tmppa = re.compile(r'anchorTimeID=".*?"')
        timestr = re.sub(tmppa, '', timestr)
        tmppa = re.compile(r'valueFromFunction=".*?"')
        timestr = re.sub(tmppa, '', timestr)
        tmppa = re.compile(r'beginPoint=".*?"')
        timestr = re.sub(tmppa, '', timestr)
        tmppa = re.compile(r'endPoint=".*?"')
        timestr = re.sub(tmppa, '', timestr)
        tmppa = re.compile(r'PERIODICITY=".*?"')
        timestr = re.sub(tmppa, '', timestr)

        #替换旧文档中的标签，遍历整个旧文档
        p = re.compile(timex[1].strip())
        tmp = p.sub(timestr, textold, 1)
        index = tmp.index(timex[1].strip()) + len(timex[1].strip()) + len('</TIMEX3>')
        results = results + tmp[0:index]
        textold  = tmp[index:]
        #print(results)
        #print(textold)
    results = results + textold
    oldfile.close()
    results = results.replace('</s>','\n')
    #TEXT前的标签 和TEXT间内容相加
    results = olddata[:olddata.index('<TEXT>')]+"\n<TEXT>\n" + results
    return results

#清理标签
def pureFile(filename):
    with open(INPUTDIR+os.sep + filename,'r') as file:
        data = file.read()

    lex = re.compile(r'<\s*lex.*?>')
    lex1 = re.compile(r'</lex>')
    NG = re.compile(r'<NG>')
    NG1 = re.compile(r'</NG>')
    VG = re.compile(r'<VG>')
    VG1 = re.compile(r'</VG>')
    s = re.compile(r'<s>')
    s1 = re.compile(r'</s>')
    #替换掉上面这些标签
    res = lex.sub('',data)
    res = lex1.sub('',res)
    res = NG.sub('',res)
    res = NG1.sub('',res)
    res = VG.sub('',res)
    res = VG1.sub('',res)
    res = s.sub('',res)
    res = s1.sub('',res)
    #找到下面所有的标签列表，以备后用
    makeinstance = re.compile(r'<MAKEINSTANCE.*?></MAKEINSTANCE>')
    tlink = re.compile(r'<TLINK.*?></TLINK>')
    slink = re.compile(r'<SLINK.*?></SLINK>')
    instances = makeinstance.findall(res)
    tlinks = tlink.findall(res)
    slinks = slink.findall(res)
    #将上面三种标签去掉
    res = makeinstance.sub('',res)
    res = tlink.sub('',res)
    res = slink.sub('',res)

    textpa = re.compile(r'<TEXT>.*?</TEXT>',re.DOTALL)
    textcontent = textpa.findall(res)[0]
    result =  getcommmon(textcontent, filename)
    result = result + "\n</TEXT>\n\n"
    #print(result)

    for ins in instances:
        result  = result + ins + "\n"
    result = result + "\n\n"
    for ins in tlinks:
        result  = result + ins + "\n"

    result = result + '</TimeML>'

    print('writing file '+filename)
    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)
    out = open(OUTDIR + "/"+filename[:filename.rfind('.')], 'w')
    out.write(result)
    out.close()


if __name__ == "__main__":
    for i in range(len(sys.argv)):
        print("第%d个参数是：%s" % (i,sys.argv[i]))
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print("parameters wrong!\n Usage: 1. python pureFile inputDIR OUTDIR SOURCEDIR")
        print("2. replace timetag: python pureFile inputDIR OUTDIR")
        sys.exit(0)
    INPUTDIR = sys.argv[1]
    OUTDIR = sys.argv[2]
    if len(sys.argv) == 3:
        replaceTag(INPUTDIR, OUTDIR)
    else:
        SOURCEDIR = sys.argv[3]
        if os.path.isdir(INPUTDIR):
            listfile = os.listdir(INPUTDIR)
            for name in listfile:
                pureFile(name)