import os
import sys
import urllib
import re
import time
import types
import urllib.request

#去除文件名显示错误
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "__", title)
    return new_title

#读取指定路径的文件
def getdoclist(docpath):
    docdata = open(docpath)
    doclist = docdata.read( ).splitlines( )
    return doclist

#获取网页信息
def getHtml(url):
    
    hds = {'Cookie' : 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.138 Safari/537.36',
           'Referer' : 'http://music.163.com/' }  
    request = urllib.request.Request(url,headers=hds)
    page = urllib.request.urlopen(request)
    html = page.read()
    return html

def savedoc(filepath,content):
    f = open(filepath,'w')
    f.write(content)
    f.close()

def appenddoc(filepath,content):
    f = open(filepath,'a')
    f.write(content)
    f.close()

def getRegex(regex,data):
    dat = re.compile(regex)
    ret = re.findall(dat,data)
    return ret

def getCited(sen):
    reg = r'"([^\"]+)\"'
    kw = re.compile(reg)
    kword = re.findall(kw,sen)
    if kword:
        return kword

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value/1000)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def groupId():
    id_list = [["Dandelion Trio","11465"], ["Yonder Voice","13535"], ["IRON ATTACK!","14353"], ["まらしぃ","14786"], ["ゆよゆっぺ","15916"], ["坂上なち","16208"], ["ししまいブラザーズ","17730"], ["ALiCE'S EMOTiON","18461"], ["Alstroemeria Records","18468"], ["Sound Online","18473"], ["アールグレイ","18495"], ["A-One","18498"], ["Amateras Records","18529"], ["Alice Music","18537"], ["Aftergrow","18594"], ["Arte Refact","18619"], ["AGENT 0","18631"], ["Applice","18666"], ["AdamKadmon","18685"], ["CROW'SCLAW","18956"], ["C-CLAYS","18959"], ["COOL&CREATE","18972"], ["C.H.S","19011"], ["CYTOKINE","19016"], ["DDBY","19184"], ["Diverse System","19185"], ["DiGiTAL WiNG","19233"], ["EastNewSound","19312"], ["ふぉれすとぴれお","19453"], ["FELT","19460"], ["Foreground Eclipse","19464"], ["ファクトリー ノイズ&AG","19531"], ["Golden City Factory","19612"], ["GET IN THE RING","19621"], ["はちみつれもん","19774"], ["Halozy","19780"], ["Innocent Key","19914"], ["IOSYS","19917"], ["iemitsu","19920"], ["efs","19930"], ["君の美術館","20147"], ["K2 SOUND","20158"], ["回路","20172"], ["こなぐすり","20175"], ["街角麻婆豆","20183"], ["Liz Triangle","20365"], ["Lunatico","20382"], ["Lapis moss","20395"], ["monochrome-coat","20565"], ["MISTY RAIN","20584"], ["Melodic Taste","20598"], ["minimum electric design","20623"], ["MN-logic24","20710"], ["NiZi RiNGO","20823"], ["NJK Record","20863"], ["ORANGE★JAM","20960"], ["QUINTET","21120"], ["QLOCKS","21121"], ["六弦アリス","21171"], ["魂音泉","21200"], ["领域ZERO","21218"], ["Riverside","21245"], ["RegaSound","21256"], ["Silver Forest","21354"], ["ShibayanRecords","21546"], ["Studio “Syrup Comfiture”","21560"], ["SOUND HOLIC","21580"], ["Sound CYCLONE","21599"], ["Sun Flower Field","21641"], ["サリー","21676"], ["Sound Refil","21812"], ["TAMUSIC","21967"], ["凋叶棕","21981"], ["TaNaBaTa","22011"], ["TUMENECO","22033"], ["虎の穴","22082"], ["T.Piacere","22173"], ["Unlucky Morpheus","22203"], ["UNDEAD CORPORATION","22209"], ["XL project","22387"], ["Yellow-Zebra","22436"], ["ZYTOKINE","22501"], ["556ミリメートル","22534"], ["38BEETS","22544"], ["Like a rabbit","95779"], ["岸田教団＆THE明星ロケッツ","159577"], ["SYNC.ART'S","161241"], ["＜echo＞PROJECT","190991"], ["クロネコラウンジ","713039"], ["SPACELECTRO","930015"], ["ESQUARIA","930018"], ["流派未月亭","1050749"], ["Swing Of the Dead","1188016"], ["Frozen Starfall","11974138"], ["東方事変","11975012"], ["Melonbooks Records","12048156"], ["CielArc","12261241"], ["404 Not Founds","12274135"], ["THE OTHER FLOWER","12451165"], ["秋叶文化祭","22035"], ["森罗万象","19795"], ["上海THONLY组委会","12007100"], ["少女フラクタル","1044250"], ["石鹸屋","21535"], ["天然ジェミニ","22039"], ["豚乙女","19794"], ["文鸟Online","20601"], ["舞風","20554"], ["暁Records","18637"], ["幽閉サテライト","22435"], ["舞音KAGURA","12561350"], ["四面楚歌","12354017"], ["Crazy Beats","12024141"], ["Eurobeat Union","1150334"], ["Pizuya's Cell","1078354"], ["発热巫女~ず","19783"], ["歌恋人","1097137"], ["少年ヴィヴィッド","21790"], ["少女全自動","21662"], ["Crest","18905"], ["少女理論観測所","12132610"], ["死際サテライト","711084"], ["フーリンキャットマーク","12408143"], ["紺碧studio","12624053"]]
    return id_list
#根据社团id获取专辑列表
def getAlbumList(id_Group):
    url_Group = 'http://music.163.com/api/artist/albums/'+ str(id_Group) +'?id=' + str(id_Group) + '&offset=0&total=true&limit=1000'
    page_Group = getHtml(url_Group)
    #反向寻找专辑id
    reg0 = r'"buSsi"(.+?)"eman"'
    abmdata = getRegex(reg0,page_Group.decode()[::-1])
    abmlist = []
    for abms in abmdata:
        abms = abms[::-1]
        abmnm = getRegex('"(.+?)","id',abms)[0]
        abmid = getRegex(r'"id":(\d+),',abms)[0]
        abmlist.append([abmnm,abmid])
    return abmlist

#根据专辑id获取歌词页面
def getTrackList(id_Album, group_name, album_name):
    url_Album = 'http://music.163.com/api/album/' + str(id_Album) + '?ext=true&id=' + str(id_Album) + '&offset=0&total=true&limit=1000'
    page_album = getHtml(url_Album)
    page_rev = page_album.decode()[::-1]
    reg1 = r'"R_SO_4_(\d+)"'
    songid_total = getRegex(reg1,page_album.decode())
    #writelinez = []
    for songid in songid_total:
        song_name = getRegex(songid[::-1] + r':"di","(.+?)"',page_rev)[0][::-1]
        url_Track = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(songid) + '&lv=-1&kv=-1&tv=-1'
        page_song =  getHtml(url_Track)
        if len(page_song) > 150:
            try:
                print(song_name)
                user_info = lrctotxt(page_song.decode(), group_name, album_name, song_name)
                with open('user_info','a',encoding='utf-8') as file:
                    file.write(user_info)
            except (KeyError,IndexError):
                appenddoc('rubbish',str(songid)+'\n')

#根据歌词页面转化为用户详细信息
def lrctotxt(songpage, group_name, album_name, track_name):
    tlrc = getRegex(r'"tlyric":{(.*?}),"',songpage)[0]
    lyric_user = ''
    lyric_time = ''
    tran_user = ''
    tran_time = ''
    lyric_det = getRegex(r'"lyricUser":{.+?}',songpage)
    if lyric_det:
        lyric_user = getRegex(r'"nickname":"(.+?)"',lyric_det[0])[0]
        lyric_time_str = getRegex(r'"uptime":(.+?)}',lyric_det[0])[0]
        lyric_time = timestamp_datetime(int(lyric_time_str))
    #在有翻译时
    if tlrc != '"version":0,"lyric":null}':
        tran_det = getRegex(r'"transUser":{.+?}',songpage)
        if tran_det:
            tran_user = getRegex(r'"nickname":"(.+?)"',tran_det[0])[0]
            tran_time_str = getRegex(r'"uptime":(.+?)}',tran_det[0])[0]
            tran_time = timestamp_datetime(int(tran_time_str))
    writeline = '"%s","%s","%s","%s","%s","%s","%s"\n'%(group_name, album_name, track_name, tran_user, tran_time, lyric_user, lyric_time)
    return writeline

#进行文本输出
def saveAll(groupnum):
    iferror = 0
    group = groupId()[groupnum]
    groupname = group[0]
    print(groupname)
    groupid = group[1]
    albumlist = getAlbumList(groupid)
    for albums in albumlist:
        albumname = albums[0]
        albumid = albums[1]
        if albumid == groupid:
            iferror = 1
            break
        getTrackList(albumid, groupname, albumname)
    return iferror

#getTrackList(82840,"test")
#print(getAlbumList(19783)[1][0])
if __name__ == '__main__':
    startnum = 1
    endnum = 124
    while startnum < endnum:
        errorcode = saveAll(startnum - 1)
        if not errorcode:
            startnum += 1

