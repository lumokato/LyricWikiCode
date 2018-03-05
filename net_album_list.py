import os
import sys
import urllib
import re
import time
import types
import urllib.request


# 去除文件名显示错误
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "__", title)
    return new_title


# 读取指定路径的文件
def getdoclist(docpath):
    docdata = open(docpath)
    doclist = docdata.read().splitlines()
    return doclist


# 获取网页信息
def getHtml(url):
    hds = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.138 Safari/537.36',
           'Referer': 'http://music.163.com/'}
    request = urllib.request.Request(url, headers=hds)
    page = urllib.request.urlopen(request)
    html = page.read()
    return html


def savedoc(filepath, content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()


def appenddoc(filepath, content):
    f = open(filepath, 'a')
    f.write(content)
    f.close()


def getRegex(regex, data):
    dat = re.compile(regex)
    ret = re.findall(dat, data)
    return ret


def getCited(sen):
    reg = r'"([^\"]+)\"'
    kw = re.compile(reg)
    kword = re.findall(kw, sen)
    if kword:
        return kword
    # 根据社团id获取专辑列表


def getAlbumList(id_Group):
    url_Group = 'http://music.163.com/api/artist/albums/' + str(id_Group) + '?id=' + str(
        id_Group) + '&offset=0&total=true&limit=1000'
    page_Group = getHtml(url_Group)
    # 反向寻找专辑id
    reg0 = r'"buSsi"(.+?)"eman"'
    abmdata = getRegex(reg0, page_Group.decode()[::-1])
    abmlist = []
    for abms in abmdata:
        abms = abms[::-1]
        abmnm = getRegex('"(.+?)","id', abms)[0]
        abmid = getRegex('"id":(\d+),', abms)[0]
        abmlist.append([abmnm, abmid])
    return abmlist


# 根据专辑id获取歌词页面
def getTrackList(id_Album, savetxt):
    url_Album = 'http://music.163.com/api/album/' + str(id_Album) + '?ext=true&id=' + str(
        id_Album) + '&offset=0&total=true&limit=1000'
    page_album = getHtml(url_Album)
    page_rev = page_album.decode()[::-1]
    reg1 = r'"R_SO_4_(\d+)"'
    songid_total = getRegex(reg1, page_album.decode())
    # writelinez = []
    for songid in songid_total:
        song_name = getRegex(songid[::-1] + r':"di","(.+?)"', page_rev)[0][::-1]


def songpage(sid, sname, savetxt):
    writelinez = ['\n\n################################\n\n', sname,
                  '\n\n#####################################\n\n']
    url_Track = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(sid) + '&lv=-1&kv=-1&tv=-1'
    page_song = getHtml(url_Track)
    if len(page_song) > 150:
        try:
            print(sname)
            writelinez.extend(lrctotxt(page_song.decode()))
            with open(savetxt, 'a', encoding='utf-8') as file:
                for writex in writelinez:
                    file.write('%s' % (writex))
        except (KeyError, IndexError):
            appenddoc('rubbish', str(sid) + '\n')


# 根据歌词页面转化为wiki格式
def lrctotxt(songpage):
    writeline = ['__LYRICS__\n\n{{歌词信息|\n']
    lrc = getRegex(r'"lrc":{(.*?}),"', songpage)[0]
    tlrc = getRegex(r'"tlyric":{(.*?}),"', songpage)[0]
    # 在有翻译时
    if tlrc != '"version":0,"lyric":null}':
        if tlrc[-4:] != '\\n"}':
            tlrc = tlrc[:-2] + '\\n"}'
        tran_user = ''
        tran_det = getRegex(r'"transUser":{.+?}', songpage)
        if tran_det:
            tran_user = getRegex(r'"nickname":"(.+?)"', tran_det[0])[0]
        writeline.append('| 语言 = 日文\n| 翻译 = 中文\n| 译者 = ' + tran_user + '\n}}\n\nlyrics=\n\n')
        timeline = {}
        linex = getRegex(r'(\[\d.*?)\\n', lrc)
        tlinex = getRegex(r'(\[\d.*?)\\n', tlrc)
        # 如果有时间轴
        if linex:
            for lines in linex:
                linen = lines
                timenx = getRegex(r'\[(\d.+?)\]', lines)
                sen = getRegex(r'(.*?)\]\d', linen[::-1])[0][::-1]
                if not sen:
                    sen = ''
                for timen in timenx:
                    timeline[timen] = [sen, '']
            for tlines in tlinex:
                ttimenx = getRegex(r'\[(\d.+?)\]', tlines)
                tsen = getRegex(r'(.*?)\]\d', tlines[::-1])[0][::-1]
                for ttimen in ttimenx:
                    if ttimen in timeline.keys():
                        senj = timeline[ttimen][0]
                        timeline[ttimen] = [senj, tsen]
                    else:
                        timeline[ttimen] = ''
            for tls in sorted(timeline.keys()):
                if timeline[tls] == '':
                    writeline.append('sep=' + tls + '\n\n')
                else:
                    if type(timeline[tls][0]) == list:
                        appenddoc('rubbish', filesave + '\n')
                        break
                    else:
                        if timeline[tls][0].strip() == '':
                            writeline.append('sep=' + tls + '\n\n')
                        else:
                            writeline.append('time=' + tls + '\n')
                            writeline.append('ja=' + timeline[tls][0] + '\n')
                            writeline.append('zh=' + timeline[tls][1] + '\n\n')
                            # 如果无时间轴
        else:
            wordline = getRegex(r'"lyric":"(.*?)"}', lrc)[0]
            tranline = getRegex(r'"lyric":"(.*?)"}', tlrc)[0]
            wordn = getRegex(r'(.*?)\\n', wordline)
            trann = getRegex(r'(.*?)\\n', tranline)
            if len(wordn) != len(trann):
                print('0')
            else:
                for i in range(len(wordn)):
                    if wordn[i].strip() == '':
                        writeline.append('sep=\n\n')
                    else:
                        writeline.append('time=\n')
                        writeline.append('ja=' + wordn[i] + '\n')
                        writeline.append('zh=' + trann[i] + '\n\n')
    else:
        writeline.append('| 语言 = 日文\n| 翻译 =\n| 译者 =\n}}\n\nlyrics=\n\n')
        linex = getRegex(r'(\[\d.*?)\\n', lrc)
        if linex:
            timeline = {}
            for lines in linex:
                linen = lines
                timenx = getRegex(r'\[(.*?)\]', lines)
                sen = getRegex(r'(.*?)\]', linen[::-1])[0][::-1]
                for timen in timenx:
                    timeline[timen.lstrip()] = sen
            for tls in sorted(timeline.keys()):
                if timeline[tls].strip() == '':
                    writeline.append('sep=' + tls + '\n\n')
                else:
                    writeline.append('time=' + tls + '\n')
                    writeline.append('ja=' + timeline[tls] + '\n')
                    writeline.append('zh=\n\n')
        else:
            wordline = getRegex(r'"lyric":"(.*?)"}', lrc)[0]
            wordn = getRegex(r'(.*?)\\n', wordline)
            wordnx = []
            for wordx in wordn:
                wordnx.append(wordx)
            for i in range(len(wordnx)):
                if not wordnx[i].strip():
                    writeline.append('sep=\n\n')
                else:
                    writeline.append('time=\n')
                    writeline.append('ja=' + wordnx[i] + '\n')
                    writeline.append('zh=\n\n')
    return writeline


# 进行文本输出
def saveAll(groupnum):
    group = open('GroupId', 'rb').readlines()[groupnum]
    groupname = getCited(group.decode())[0]
    writelinex = [groupname, '\n**************************\n\n']
    with open(groupname, 'w', encoding='utf-8') as file:
        for writex in writelinex:
            file.write('%s' % (writex))
    print(groupname)
    groupid = getCited(group.decode())[1]
    albumlist = getAlbumList(groupid)
    for albums in albumlist:
        albumname = albums[0]
        albumid = albums[1]
        writelinea = ['\n\n\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n\n\n', albumname,
                      '\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n']
        with open(groupname, 'a', encoding='utf-8') as file:
            for writex in writelinea:
                file.write('%s' % (writex))
        getTrackList(albumid, groupname)


# print(getAlbumList(19783)[1][0])
saveAll(72)
# getTrackList(82840,"test")