# 获取网易云的歌词并转化为wiki格式，以所需社团的歌曲名称顺序排列

import os
import sys
import urllib
import re
import time
import types
import urllib.request


# 一些常用函数


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


# def validateTitle(title):
#     去除文件名显示错误
#     rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
#     new_title = re.sub(rstr, "__", title)
#     return new_title


# def getdoclist(docpath):
#     读取指定路径的文件
#     docdata = open(docpath)
#     doclist = docdata.read().splitlines()
#     return doclist


def getHtml(url):
    # 获取网页信息
    hds = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.138 Safari/537.36',
           'Referer': 'http://music.163.com/'}
    request = urllib.request.Request(url, headers=hds)
    page = urllib.request.urlopen(request)
    html = page.read()
    return html


def user_id_change(netease_id):
    user_id = netease_id
    id_dic = {"風花字幕社": "[[用户:云卷]]",
              "DiPLOPiA": "[[用户:DiPLOPiA]]",
              "99NeroCake": "[[用户:99NeroCake]]",
              "-绘芸-": "[[用户:月霜]]",
              "Ecauchy": "[[用户:Ecauchy]]",
              "秘封罐头里的翅融": "[[用户:鬼翅融]]"}

    if netease_id in id_dic.keys():
        user_id = id_dic[netease_id]
    return user_id


def getAlbumList(id_Group):
    # 根据社团id获取专辑列表
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


def getTrackList(id_album, name_album):
    # 根据专辑id获取歌词页面
    url_album = 'http://music.163.com/api/album/' + str(id_album) + '?ext=true&id=' + str(
        id_album) + '&offset=0&total=true&limit=1000'
    page_album = getHtml(url_album)
    page_rev = page_album.decode()[::-1]
    reg1 = r'"R_SO_4_(\d+)"'
    songid_total = getRegex(reg1, page_album.decode())
    song_list = {}
    for songid in songid_total:
        song_name = getRegex(songid[::-1] + r':"di","(.+?)"', page_rev)[0][::-1]
        song_list[songid] = song_name + "    " + name_album  # 将曲名与专辑名合并为一个变量
    return song_list


def songpage(sid, sname, savetxt):
    # 获取歌词页面
    writelinez = ['\n#####################################\n\n', sname, "    "]
    url_track = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(sid) + '&lv=-1&kv=-1&tv=-1'
    page_song = getHtml(url_track)
    if len(page_song) > 150:
        try:
            print(sname)
            writeline_all = lrctotxt(page_song.decode())
            writelinez.extend(writeline_all[0])
            if writeline_all[1]:
                writeline_re = ['\n\n#####################################\n\n', sname,
                                '\n\n#####################################\n\n']
                writeline_re.extend(writeline_all[1])
                with open(savetxt + '_re', 'a', encoding='utf-8') as file:
                    for writere in writeline_re:
                        file.write('%s' % (writere))
            writelinez.append('%' + sname)
            with open(savetxt, 'a', encoding='utf-8') as file:
                for writex in writelinez:
                    file.write('%s' % (writex))
        except (KeyError, IndexError):
            appenddoc('rubbish', str(sid) + '\n')


def lyric_define(line_ja):
    # 判断歌词是否为附加信息
    info_re = ["作曲", "作词", "原曲",
               "サークル：", "アルバム：",
               "END",
               "Album", "Circle", "Origin",
               "Vocal", "Lyric", "Arrange"]
    for keywords in info_re:
        if keywords in line_ja:
            return False
    return True


def lrctotxt(songpage):
    # 根据歌词页面转化为wiki格式
    writeline = []
    lrc_det = getRegex(r'"lyricUser":{.+?}', songpage)
    if lrc_det:
        lrc_user = getRegex(r'"nickname":"(.+?)"', lrc_det[0])[0]
        writeline.append("歌词用户：" + lrc_user)
    writeline.append('\n\n#####################################\n\n')
    writeline.append('__LYRICS__\n\n{{歌词信息|\n')
    lrc = getRegex(r'"lrc":{(.*?}),"', songpage)[0]
    tlrc = getRegex(r'"tlyric":{(.*?}),"', songpage)[0]
    writeline_l = []  # 保留的部分
    writeline_d = []  # 去除的部分
    # 在有翻译时
    if tlrc != '"version":0,"lyric":null}':
        if tlrc[-4:] != '\\n"}':
            tlrc = tlrc[:-2] + '\\n"}'
        tran_user = ''
        tran_det = getRegex(r'"transUser":{.+?}', songpage)
        if tran_det:
            tran_user = getRegex(r'"nickname":"(.+?)"', tran_det[0])[0]
        writeline.append('| 语言 = 日文\n| 翻译 = 中文\n| 译者 = ' + user_id_change(tran_user) + '\n}}\n\nlyrics=\n\n')
        timeline = {}
        linex = getRegex(r'(\[\d.*?)\\n', lrc)
        tlinex = getRegex(r'(\[\d.*?)\\n', tlrc)
        # 如果有时间轴
        if linex:
            for lines in linex:
                linen = lines
                timenx = getRegex(r'\[(\d.+?)\]', lines)
                sen = getRegex(r'(.*?)\]\d', linen[::-1])[0][::-1].strip()
                if not sen:
                    sen = ''
                for timen in timenx:
                    timeline[timen] = [sen, '']
            for tlines in tlinex:
                ttimenx = getRegex(r'\[(\d.+?)\]', tlines)
                tsen = getRegex(r'(.*?)\]\d', tlines[::-1])[0][::-1].strip()
                for ttimen in ttimenx:
                    if ttimen in timeline.keys():
                        senj = timeline[ttimen][0]
                        timeline[ttimen] = [senj, tsen]
                    else:
                        timeline[ttimen] = ['', tsen]
            for tls in sorted(timeline.keys()):
                if timeline[tls] == '':
                    writeline_l.append('sep=' + tls + '\n\n')
                else:
                    if type(timeline[tls][0]) == list:
                        appenddoc('rubbish', 'xx' + '\n')
                        break
                    else:
                        if timeline[tls][0] == '' and timeline[tls][1] == '':
                            writeline_l.append('sep=' + tls + '\n\n')
                        else:
                            if lyric_define(timeline[tls][0]):
                                writeline_l.append('time=' + tls + '\n')
                                writeline_l.append('ja=' + timeline[tls][0] + '\n')
                                writeline_l.append('zh=' + timeline[tls][1] + '\n\n')
                            else:
                                writeline_d.append('time=' + tls + '\n')
                                writeline_d.append('ja=' + timeline[tls][0] + '\n')
                                writeline_d.append('zh=' + timeline[tls][1] + '\n\n')
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
                        writeline_l.append('sep=\n\n')
                    else:
                        if lyric_define(wordn[i]):
                            writeline_l.append('time=\n')
                            writeline_l.append('ja=' + wordn[i] + '\n')
                            writeline_l.append('zh=' + trann[i] + '\n\n')
                        else:
                            writeline_d.append('time=\n')
                            writeline_d.append('ja=' + wordn[i] + '\n')
                            writeline_d.append('zh=' + trann[i] + '\n\n')
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
                    timeline[timen.lstrip()] = sen.strip()
            for tls in sorted(timeline.keys()):
                if timeline[tls] == '':
                    writeline_l.append('sep=' + tls + '\n\n')
                else:
                    if lyric_define(timeline[tls]):
                        writeline_l.append('time=' + tls + '\n')
                        writeline_l.append('ja=' + timeline[tls] + '\n')
                        writeline_l.append('zh=\n\n')
                    else:
                        writeline_d.append('time=' + tls + '\n')
                        writeline_d.append('ja=' + timeline[tls] + '\n')
                        writeline_d.append('zh=\n\n')
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
                    if lyric_define(wordnx[i]):
                        writeline_l.append('time=\n')
                        writeline_l.append('ja=' + wordnx[i] + '\n')
                        writeline_l.append('zh=\n\n')
                    else:
                        writeline_d.append('time=\n')
                        writeline_d.append('ja=' + wordnx[i] + '\n')
                        writeline_d.append('zh=\n\n')
    linenum = 0
    for line_for in range(0, writeline_l.__len__()):
        if "sep=" in writeline_l[line_for]:
            linenum += 1
        else:
            break
    writeline_lx = writeline_l[linenum:]
    for line_rev in range(0, writeline_l.__len__())[::-1]:
        if "sep=" in writeline_l[line_rev]:
            writeline_lx.pop()
        else:
            break
    writeline.extend(writeline_lx)
    return [writeline, writeline_d]


def saveAll(groupnum):
    # 进行文本输出
    group = open('GroupId', 'rb').readlines()[groupnum]
    groupname = getCited(group.decode())[0]
    writelinex = [groupname, '\n**************************\n\n']
    with open(groupname, 'w', encoding='utf-8') as file:
        for writex in writelinex:
            file.write('%s' % (writex))
    print(groupname)
    groupid = getCited(group.decode())[1]
    albumlist = getAlbumList(groupid)
    songid_total = {}
    for albums in albumlist:
        albumname = albums[0]
        albumid = albums[1]
        writelinea = [albumname, '\n']
        with open(groupname, 'a', encoding='utf-8') as file:
            for writex in writelinea:
                file.write('%s' % (writex))
        songid_total.update(getTrackList(albumid,albumname))
    for songlist in sorted(songid_total.items(), key=lambda item: item[1]):
        songpage(songlist[0], songlist[1], groupname)

# sublime: __LYRICS__[^n]+?%
# print(getAlbumList(19783)[1][0])
# getTrackList(82840,"test")
# songpage('27580735','xx','xxx')
saveAll(59)
