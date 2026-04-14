# -*- coding: utf-8 -*-
import os
import sys

import requests
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import re
#import base64
#import unicodedata
import json
import random
import datetime,time
from html import unescape
from urllib.parse import urlencode, quote_plus, quote, unquote, parse_qsl

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2][1:]))
addon = xbmcaddon.Addon(id='plugin.video.toya')
PATH=addon.getAddonInfo('path')
PATH_img=PATH+'/resources/img/'
img_empty=PATH_img+'empty.png'
fanart=PATH_img+'fanart.jpg'
img_addon=PATH+'icon.png'
catch_up=PATH_img +'catch_up.png'
vod_na=PATH_img +'VOD.png'


baseurl='https://nowa-go.toya.net.pl'
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0'

apiUrl='https://api-atv.toya.net.pl/'
platform='Windows'

tv_icon ='https://data-go.toya.net.pl/logo/iconxmb/tv_icon_big.png'
radio_icon='https://data-go.toya.net.pl/logo/iconxmb/internetradio_icon_big.png'
radio_icon2='https://data-go.toya.net.pl/dottv/icons/v22/radio-internetowe.jpg'
camera_icon='https://data-go.toya.net.pl/logo/iconxmb/camera_active.png'
camera_icon2='https://data-go.toya.net.pl/dottv/icons/v22/kamery.jpg'
VOD_icon='https://data-go.toya.net.pl/logo/iconxmb/Movies_VOD_focus.png'
freeVOD_icon='https://data-go.toya.net.pl/dottv/icons/v22/freevod.jpg'
settings_icon='https://data-go.toya.net.pl/logo/iconxmb/settings_icon_big.png'
koncerty_icon='https://data-go.toya.net.pl/logo/iconxmb/koncerty_focus.png'
Karaoke_icon='https://data-go.toya.net.pl/logo/iconxmb/KaraokeTv_focus.png'
Catch_up_icon='https://data-go.toya.net.pl/dottv/icons/v22/catch-up-2.jpg'
Na_życzenie_icon='https://data-go.toya.net.pl/dottv/icons/v22/tvtoya.jpg'
logo_toya='https://data-go.toya.net.pl/atv/webapp-logo.png'

def heaGen(auth=True):
    status=addon.getSetting('logged')

    accessToken=addon.getSetting('token') if status=='true' else 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIlVTRVItUFJPRklMRS1JRCI6MX0.eyJleHAiOjE3OTIxOTk1NjUsIm5iZiI6MTc1NjE5OTIwNSwiaWF0IjoxNzU2MTk5NTY1LCJpc3MiOiJ1cm46VG95YUFQSSIsImd1ZXN0IjoxfQ.Ia4ABG2Ou_8boYjLR2IkQMk8H_zPspZlbH_8CJ16C4fvnKcmdl5xy6wJRE_lWKdvBz4RZYm0-ehjGD02QSwDqfgXA2ShJBZNIESDydZfearMZ6wc-B2rNFr2L-f6JKkcI8Uq9vcY3HtVatuJrXj_0guESNPsw9NfRJdA8VHm8yuaVteSxq_-RiZG_zJreHv98-vePbudXTgv5dc87I6PlvClBVw1PljR1O78oOOLzmgCx3jooP1eTSz0pZ-zkGTH9yWa7ZbYu08Q2_qCaOqS0ruZiBB5z6Qekuo9xCdfRBb7L7ZawzxZC7KUgJdAAzEwdYzYVo18D3b9_oRpA55p-UoutJMfnY47Z1dDILvU9o2e4peOwFQbfHn86CRDXVI2VRPAoNLAUCNLnx6112aFjHfu7gdJ0LKOMbemOKmntbsoOt-U8c24c0vnzJ_AG8aX5aiHRI1FWf5d3y4Yp_I1qjaJUaiMm8YWB-knWIwT6t2bVU1Vbfeatc9Dw8eK89vlDA-X6y4rhaBwj-O1uOmhMjELajEWOWHwIjncnW6W676VwzzyYJh9ZUqJ0cs88zTpIEDgxuSNzKlBFY5BWzsvFb2mlU-6tJvuPkog4uBxB-FVCw7misPX_-Gz87bAzc2nvq54AMsmR3JH-AYgAdKUx6GzL9rIc9DMdgyuttx3Jow'
    profil=addon.getSetting('user_profile_id') if status=='true' else '1'

    h={
        'User-Agent':UA,
        'Referer':'%s/'%(baseurl),
        'Origin':baseurl,
        'Platform':platform,
    }
    if auth:
        h['Authorization']='Bearer %s'%(accessToken)
        h['User-Profile-Id']=profil
        h['Content-type']='application/json; charset=UTF-8'

    return h

def build_url(query):
    return base_url + '?' + urlencode(query)

def addItemList(url, name, setArt, medType=False, infoLab={}, isF=True, isPla='false', contMenu=False, cmItems=[]):
    li=xbmcgui.ListItem(name)
    li.setProperty("IsPlayable", isPla)
    if medType:
        kodiVer=xbmc.getInfoLabel('System.BuildVersion')
        if kodiVer.startswith('19.'):
            li.setInfo(type=medType, infoLabels=infoLab)
        else:
            types={'video':'getVideoInfoTag','music':'getMusicInfoTag'}
            if medType!=False:
                setMedType=getattr(li,types[medType])
                vi=setMedType()

                labels={
                    'year':'setYear', #int
                    'episode':'setEpisode', #int
                    'season':'setSeason', #int
                    'rating':'setRating', #float
                    'mpaa':'setMpaa',
                    'plot':'setPlot',
                    'plotoutline':'setPlotOutline',
                    'title':'setTitle',
                    'originaltitle':'setOriginalTitle',
                    'sorttitle':'setSortTitle',
                    'genre':'setGenres', #list
                    'country':'setCountries', #list
                    'director':'setDirectors', #list
                    'studio':'setStudios', #list
                    'writer':'setWriters',#list
                    'duration':'setDuration', #int (in sec)
                    'tag':'setTags', #list
                    'trailer':'setTrailer', #str (path)
                    'mediatype':'setMediaType',
                    'cast':'setCast', #list
                }

                if 'cast' in infoLab:
                    if infoLab['cast']!=None:
                        cast=[xbmc.Actor(c) for c in infoLab['cast']]
                        infoLab['cast']=cast

                for i in list(infoLab):
                    if i in list(labels):
                        setLab=getattr(vi,labels[i])
                        setLab(infoLab[i])
    li.setArt(setArt)
    if contMenu:
        li.addContextMenuItems(cmItems, replaceItems=False)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=isF)
def KARAcateg():
    data = [
        ('Dla dzieci', '13761'),
        ('Biesiada', '13711'),
        ('Polskie', '13751'),
        ('Zagraniczne', '13752'),
    ]

    for title, rid in data:
        setArt = {
            'icon': Karaoke_icon,
            'fanart': fanart
        }

        url = build_url({
            'mode': 'KARA_items',
            'rid': rid
        })

        addItemList(url, title, setArt)

    xbmcplugin.endOfDirectory(addon_handle)

def KARA_items(rid):
    url = apiUrl + 'vod/items'
    data = {
        "count": 100,
        "rowId": rid,
        "start": 0
    }

    h = heaGen()
    resp = req('post', url, h, data)

    if not resp:
        xbmcplugin.endOfDirectory(addon_handle)
        return

    for r in resp:
        xbmc.log("KARA FULL ITEM: " + str(r), xbmc.LOGINFO)
        title = r['title']
        pid = r['productId']
        img = r['imageUrl']

        if "A ja.jpg" in img:
            img = img.replace("A ja.jpg", "A_ja.jpg")

        setArt = {
            'icon': img,
            'fanart': fanart
        }

        if r['productType'] in ['vod', 'cutv', 'music', 'karaoke']:
            url = build_url({
                'mode': 'playKaraoke',
                'vid':r['id'],
                'type': r['productType']
            })

            iL = {'title': title, 'plot': title, 'mediatype': 'movie'}

            addItemList(url, title, setArt, 'video', iL, False, 'true')

    xbmcplugin.endOfDirectory(addon_handle)

def KARA_menu():
    url = apiUrl+'vod/rows'
    data = {
        "count": 100,
        "rowId": '15',
        "start": "0"
    }
    h = heaGen()
    resp = req('post', url, h, data)

    if resp:
        for r in resp:
            title = r['title']
            pid = r['productId']

            setArt = {
                'thumb': '',
                'poster': '',
                'banner': '',
                'icon': radio_icon,
                'fanart': fanart
            }

            url = build_url({'mode': 'KARA_items', 'rid': pid})
            addItemList(url, title, setArt)

    xbmcplugin.endOfDirectory(addon_handle)



def ISAplayer(protocol, stream_url, DRM=False, licKey=None, cert=None, drm_config={}):
    mimeType={'hls':'application/x-mpegurl','mpd':'application/xml+dash'}
    import inputstreamhelper
    PROTOCOL = protocol
    if DRM:
        DRM = 'com.widevine.alpha'
        is_helper = inputstreamhelper.Helper(PROTOCOL, drm=DRM)
    else:
        is_helper = inputstreamhelper.Helper(PROTOCOL)
    if is_helper.check_inputstream():
        play_item = xbmcgui.ListItem(path=stream_url)
        play_item.setMimeType(mimeType[protocol])
        play_item.setContentLookup(False)
        play_item.setProperty('inputstream', is_helper.inputstream_addon)
        play_item.setProperty('IsPlayable', 'true')
        if DRM:
            kodiVer=xbmc.getInfoLabel('System.BuildVersion')
            if int(kodiVer.split('.')[0])<22:
                play_item.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
                play_item.setProperty('inputstream.adaptive.license_type', DRM)
                play_item.setProperty('inputstream.adaptive.server_certificate', cert)
                play_item.setProperty('inputstream.adaptive.license_key', licKey)
            else:
                play_item.setProperty('inputstream.adaptive.drm', json.dumps(drm_config))

        play_item.setProperty('inputstream.adaptive.stream_headers', 'User-Agent='+UA+'&Referer='+baseurl)
        play_item.setProperty('inputstream.adaptive.manifest_headers', 'User-Agent='+UA+'&Referer='+baseurl) #K21
        xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def directPlayer(stream_url):
    play_item = xbmcgui.ListItem(path=stream_url)
    play_item.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

def getTID():
    def code_gen(x):
        base='0123456789abcdef'
        code=''
        for i in range(0,x):
            code+=base[random.randint(0,15)]
        return code
    addon.setSetting('device_id','%s-%s-%s-%s-%s'%(code_gen(8),code_gen(4),code_gen(4),code_gen(4),code_gen(12)))

def main_menu():
    sources=[
        ['TV','tvList',tv_icon],
        ['CatchUp TV','catchup',catch_up],
        ['FreeVOD','freeVOD',VOD_icon],
        ['TV Toya na życzenie','toyaOD',vod_na],
        ['Radio','radio',radio_icon],
        ['Kamery','cams',camera_icon],
##        ['Karaoke','KARAcateg',Karaoke_icon]
    ]

    if addon.getSetting('logged')!='true':
        sources.append(['[B]ZALOGUJ[/B]','login','https://data-go.toya.net.pl/logo/iconxmb/settings_icon_big.png'])
    else:
        sources.append(['[B]WYLOGUJ[/B]','logout','https://data-go.toya.net.pl/logo/iconxmb/settings_icon_big.png'])

    for s in sources:
        isF=False if s[1] in ['login','logout'] else True
        setArt={'thumb': '', 'poster': '', 'banner': '', 'icon': s[2], 'fanart':fanart}
        url = build_url({'mode':s[1]})
        addItemList(url, s[0], setArt, isF=isF)
    xbmcplugin.endOfDirectory(addon_handle)


def login():
    u=addon.getSetting('username')
    p=addon.getSetting('password')
    if p!='' and u!='':
        url=apiUrl+'login'
        data={
            'deviceId': addon.getSetting('device_id'),
            'login': u,
            'password': p
        }
        h=heaGen(False)
        h['Content-Type']='application/json; charset=UTF-8'
        resp=requests.post(url,json=data,headers=h).json()
        if 'token' in resp:
            addon.setSetting('token',resp['token'])
            addon.setSetting('refreshToken',resp['refreshToken'])

        else:
            xbmc.log('@@@Błąd logowania (1): '+str(resp), level=xbmc.LOGINFO)
            xbmcgui.Dialog().notification('ToyaGO', 'Błąd logowania - szczegóły w logu', xbmcgui.NOTIFICATION_INFO)
            return

        url=apiUrl+'profiles'
        h=heaGen()
        h['User-Profile-Id']='1'
        h['Authorization']='Bearer %s' %(addon.getSetting('token'))
        resp=requests.get(url,headers=h).json()
        if len(resp)>0:
            profNames=[p['profile_name'] for p in resp]
            profIds=[p['id'] for p in resp]
            if len(profIds)==1:
                addon.setSetting('user_profile_id',profIds[0])
            else:
                select=xbmcgui.Dialog().select('Wybierz profil:', profNames)
                if select>-1:
                    addon.setSetting('user_profile_id',profIds[select])
                else:
                    addon.setSetting('user_profile_id',profIds[0])

            addon.setSetting('logged','true')
        else:
            xbmc.log('@@@Błąd logowania (2): profile '+str(resp), level=xbmc.LOGINFO)
            xbmcgui.Dialog().notification('ToyaGO', 'Błąd logowania - szczegóły w logu', xbmcgui.NOTIFICATION_INFO)
            return

    else:
        xbmcgui.Dialog().notification('ToyaGO', 'Uzupełnij dane logowania w ustawieniach wtyczki', xbmcgui.NOTIFICATION_INFO)

def logout():
    addon.setSetting('user_profile_id','')
    addon.setSetting('token','')
    addon.setSetting('refreshToken','')
    addon.setSetting('logged','false')

def refreshLogin():
    url=apiUrl+'login'
    data={
        "deviceId": addon.getSetting('device_id'),
        "refreshToken": addon.getSetting('refreshToken')
    }
    h=heaGen(False)
    h['Content-Type']='application/json; charset=UTF-8'
    resp=requests.post(url,json=data,headers=h).json()
    if 'token' in resp:
        xbmc.log('@@@Odświeżono token', level=xbmc.LOGINFO)
        addon.setSetting('token',resp['token'])
        addon.setSetting('refreshToken',resp['refreshToken'])

    else:
        xbmc.log('@@@Błąd refreshtoken: '+str(resp), level=xbmc.LOGINFO)
        xbmc.log('@@@wylogowanie', level=xbmc.LOGINFO)
        logout()
        xbmc.log('@@@Próba zalogowania', level=xbmc.LOGINFO)
        login()

def build_karaoke_url(productId, device_id, token):
    cid = productId

    drm = req('get',
        apiUrl + f'drm/token/?cid={cid}&type=vod',
        heaGen()
    )

    manifest = f"https://cdn-14-go.toya.net.pl/vod/{cid}/manifest.mpd"
    params = f"?p={drm['token']}&pl=Windows&device_id={device_id}"

    return manifest + params


def req(t, u, h, d={}):

    def get_req(t, u, h, d):
        if t == 'get':
            return requests.get(u, headers=h)
        elif t == 'post':
            return requests.post(u, headers=h, json=d)
        elif t == 'put':
            return requests.put(u, headers=h, json=d)

    resp = get_req(t, u, h, d)
##    xbmcgui.Dialog().textviewer('info', str(resp.text))

    print(resp.status_code)

    if resp.status_code in [403, 401] and addon.getSetting('logged') == 'true':
        xbmc.log('@@@Błąd autoryzacji', level=xbmc.LOGINFO)
        refreshLogin()

        if addon.getSetting('logged') == 'true':
            h['Authorization'] = 'Bearer %s' % addon.getSetting('token')
            resp = get_req(t, u, h, d)
        else:
            xbmc.log('@@@Nieudane przelogowanie', level=xbmc.LOGINFO)
            return None

    elif str(resp.status_code).startswith('4'):
        return None

    if not resp.text or resp.text.strip() == "":
        xbmc.log("EMPTY RESPONSE - RAW", xbmc.LOGINFO)
        return resp

    try:
        return resp.json()
    except Exception:
        xbmc.log("NOT JSON - RETURN RAW", xbmc.LOGINFO)
        return resp

def EPG_data():
    url=apiUrl+'epg'
    now=int(time.time()-2.5*60*60)

    data={
        "channelIds": "all",
        "count": 10,
        "date": now
    }
    h=heaGen()
    h['Content-Type']='application/json; charset=UTF-8'
    resp=req('post',url,h,data)
    epg=[]
    if resp!=None:
        epg=resp

    return epg

def epg_channel(cid,epg_data):
    epg='Brak danych EPG'
    epg_chan=[p['programs'] for p in epg_data if p['channelId']==cid]
    if len(epg_chan)>0:
        progs=epg_chan[0]
        epg=''
        for i,p in enumerate(progs):
            now=int(time.time())
            if (i<len(progs)-1 and progs[i+1]['s']>now) or i==len(progs)-1:
                name=p['n']
                desc=p['sd']
                ts=datetime.datetime.fromtimestamp(p['s']).strftime('%H:%M')
                epg+='[B]%s[/B] %s - [I]%s[/I]\n'%(ts,name,desc)

    return epg

def getEpgForChan(cid):
    url=apiUrl+'epg'
    now=int(time.time())
    t=int(time.time()-12*60*60)

    data=[{
        "channelId": cid,
        "count": 100,
        "start": t
    }]
    h=heaGen()
    h['Content-Type']='application/json; charset=UTF-8'
    resp=req('post',url,h,data)
    epg=''
    if resp!=None:
        if len(resp)==1:
            progs=resp[0]['programs']
            for i,p in enumerate(progs):
                if (i<len(progs)-1 and progs[i+1]['s']>now) or i==len(progs)-1:
                    name=p['n']
                    desc=p['sd']
                    ts=datetime.datetime.fromtimestamp(p['s']).strftime('%H:%M')
                    epg+='[B]%s[/B] %s - [I]%s[/I]\n'%(ts,name,desc)

    if epg=='':
        epg='Brak danych EPG'
    dialog = xbmcgui.Dialog()
    dialog.textviewer('EPG', epg)

def channelsGen():
    channels=[]
    url=apiUrl+'channels'
    h=heaGen()
    resp=req('get',url,h)
    if resp!=None:
        if 'channels' in resp:
            channels=resp['channels']

    return channels

def tvList():
    chanFltr=addon.getSetting('chanFltr')
    cf=chanFltr if chanFltr!='' else 'wszystkie'
    #filtr
    title='[COLOR=cyan]Kategoria:[/COLOR] %s'%(cf)
    img='DefaultGenre.png'
    setArt={'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart':fanart}
    url = build_url({'mode':'setChanFltr'})
    addItemList(url, title, setArt, isF=False)

    channels=channelsGen()
    epg=EPG_data()
    for c in channels:
        if c['isAvailable'] and c['service']==1 and cf in c['list']:
            name=c['name']
            cid=c['id']
            img=c['icon']
            plot=epg_channel(cid,epg)

            contMenu = True
            cmItems=[('[B]EPG[/B]','RunPlugin(plugin://plugin.video.toya?mode=epg&cid='+cid+')')]

            iL={'title': name,'sorttitle': name,'plot': plot}
            setArt={'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart':fanart}
            url = build_url({'mode':'playTV','cid':cid})
            addItemList(url, name, setArt, 'video', iL, False, 'true', contMenu, cmItems)

    xbmcplugin.endOfDirectory(addon_handle)
    xbmcplugin.addSortMethod(handle=addon_handle,sortMethod=xbmcplugin.SORT_METHOD_NONE)
    xbmcplugin.addSortMethod(handle=addon_handle,sortMethod=xbmcplugin.SORT_METHOD_TITLE)

def setChanFltr():
    chanFltr=addon.getSetting('chanFltr')
    cf=chanFltr if chanFltr!='' else 'wszystkie'
    new_cf=cf

    url=apiUrl+'channels/categories'
    resp=req('get',url,heaGen())
    if resp!=None:
        categs=['wszystkie']
        categs+=[c['name'] for c in resp]

        select = xbmcgui.Dialog().contextmenu(categs)
 ######       select=xbmcgui.Dialog().select('Kategoria:', categs)
        if select>-1:
            new_cf=categs[select]
        else:
            new_cf=cf

    if new_cf!=cf:
        addon.setSetting('chanFltr',new_cf)
        xbmc.executebuiltin('Container.Refresh()')

##def playKaraoke(vid, t):
##    xbmcgui.Dialog().textviewer('info', str(vid))
##    xbmc.log("### 1 START playKaraoke vid=" + str(vid), xbmc.LOGINFO)
##
##    drm_url = apiUrl + f"drm/token/?cid={vid}&type={t}"
##    xbmc.log("### 2 DRM URL: " + drm_url, xbmc.LOGINFO)
##
##    drm = req('get', drm_url, heaGen())
##    xbmc.log("### 3 DRM RESP: " + str(drm), xbmc.LOGINFO)
##
##    if not drm:
##        xbmc.log("### FAIL: brak DRM", xbmc.LOGINFO)
##        return
##
##    manifest_url = f"https://cdn-14-go.toya.net.pl/vod/{vid}/manifest.mpd"
##
##    lic_url = "https://api-atv.toya.net.pl/drm/license"
##
##    # 🔴 pobranie preAuth (jak w TV)
##    url_prelic = apiUrl + f"drm/token/?cid={vid}&type={t}"
##    resp2 = req('get', url_prelic, heaGen())
##
##    if not resp2 or not resp2.get('headerName'):
##        xbmc.log("### FAIL: brak preAuth", xbmc.LOGINFO)
##        return
##
##    lic_hea = heaGen()
##    lic_hea[resp2['headerName']] = resp2['headerValue']
##    lic_hea['content-type'] = 'application/octet-stream'
##
##    licKey = '%s|%s|R{SSM}|' % (lic_url, urlencode(lic_hea))
##
##    drm_config = {
##        "com.widevine.alpha": {
##            "license": {
##                "server_url": lic_url,
##                "req_headers": urlencode(lic_hea),
##            }
##        }
##    }
##
##    xbmc.log("### MPD: " + manifest_url, xbmc.LOGINFO)
##    xbmc.log("### LICKEY: " + licKey, xbmc.LOGINFO)
##
##    ISAplayer('mpd', manifest_url, True, licKey, None, drm_config)


def playKaraoke(vid, t):

    xbmc.log("### START KARAOKE STEP2: " + vid, xbmc.LOGINFO)

    url = apiUrl + 'vod/items'
    data = {
        'productId': str(vid),
        'productType': t,
        'deviceId': addon.getSetting('device_id'),
        'platform': 'Windows'
    }

    resp = req('post', url, heaGen(), data)

    xbmc.log("### STEP2 RESP: " + str(resp), xbmc.LOGINFO)

    if not resp or not isinstance(resp, list):
        xbmc.log("### FAIL STEP2", xbmc.LOGINFO)
        return

    r = resp[0]

    xbmc.log("### ITEM: " + str(r), xbmc.LOGINFO)

    # 🔥 TU SZUKAMY PRAWDZIWEGO LINKU
    if 'externalUri' in r:
        link = r['externalUri']
        xbmc.log("### FOUND LINK: " + link, xbmc.LOGINFO)
        directPlayer(link)
        return

    xbmc.log("### BRAK LINKU W STEP2", xbmc.LOGINFO)
    if not resp:
        xbmc.log("### FAIL: resp None", xbmc.LOGINFO)
        return

    if isinstance(resp, dict):
        if 'uri' not in resp:
            xbmc.log("### FAIL: brak uri w dict", xbmc.LOGINFO)
            return
    else:
        xbmc.log("### RESP NIE JSON → trzeba parsować ręcznie", xbmc.LOGINFO)
        xbmc.log(str(resp.text[:500]), xbmc.LOGINFO)
        return

    stream_url = resp['uri']

    xbmc.log("### STREAM URL: " + stream_url, xbmc.LOGINFO)

    if '.mpd' in stream_url:
        protocol = 'mpd'
    elif '.m3u8' in stream_url:
        protocol = 'hls'
    else:
        xbmc.log("### FAIL: nieznany format", xbmc.LOGINFO)
        return

    # DRM (jeśli jest)
    drm = False
    licKey = None
    drm_config = {}
    cert = None

    if 'drmInfo' in resp:
        drm = True
        drmInfo = resp['drmInfo']

        lic_url = drmInfo['licenseProxyUri']
        url_prelic = drmInfo['preAuthTokenUri']

        url2 = '%s?cid=%s&type=%s' % (url_prelic, drmInfo['drmId'], t)
        resp2 = req('get', url2, heaGen())

        if not resp2:
            xbmc.log("### FAIL DRM AUTH", xbmc.LOGINFO)
            return

        lic_hea = heaGen()
        lic_hea[resp2['headerName']] = resp2['headerValue']
        lic_hea['content-type'] = 'application/octet-stream'

        licKey = '%s|%s|R{SSM}|' % (lic_url, urlencode(lic_hea))

        drm_config = {
            "com.widevine.alpha": {
                "license": {
                    "server_url": lic_url,
                    "req_headers": urlencode(lic_hea),
                }
            }
        }

    ISAplayer(protocol, stream_url, drm, licKey, cert, drm_config)

def playTV(cid):
    channels=channelsGen()
    data=[c for c in channels if c['id']==cid]
    if len(data)>0:
        data=data[0]
        stream_url=data['uri']
        if '.mpd' in stream_url:
            protocol='mpd'
        elif '.m3u8' in stream_url:
            protocol='hls'

        drm=False
        licKey=None
        drm_config={}
        cert=None

        if data['drm']:
            drm=True
            lic_url=data['licenseProxyUri']

            url_prelic=data['preAuthTokenUri']
            url='%s?cid=%s&type=%s'%(url_prelic,data['drmId'],'TIVI')
            resp=req('get',url,heaGen())
            if resp==None:
                xbmc.log('@@@Odtwarzanie - błąd autoryzacji ', level=xbmc.LOGINFO)
                xbmcgui.Dialog().notification('ToyaGO', 'Błąd autoryzacji', xbmcgui.NOTIFICATION_INFO)
                xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem())
                return

            lic_hea=heaGen()
            lic_hea[resp['headerName']]=resp['headerValue']
            lic_hea['content-type']='application/octet-stream'

            #K21
            licKey='%s|%s|R{SSM}|'%(lic_url,urlencode(lic_hea))
            #K22
            drm_config={
                "com.widevine.alpha": {
                    "license": {
                        "server_url": lic_url,
                        "req_headers": urlencode(lic_hea),

                    }
                }
            }

        ISAplayer(protocol,stream_url,drm,licKey,cert,drm_config)
    else:
        info='Brak kanału w bazie' if len(channels)>0 else 'Problem z autoryzacją'
        xbmc.log('@@@Odtwarzanie: '+info , level=xbmc.LOGINFO)
        xbmcgui.Dialog().notification('ToyaGO', info, xbmcgui.NOTIFICATION_INFO)
        xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem())


def rowsList(c):
    url=apiUrl+'vod/rows'
    data={
        "count": 100,
        "rowId": c,
        "start": "0"
    }
    h=heaGen()
    resp=req('post',url,h,data)
    if resp!=None:
        if resp[0]['title']=='\u200f\u200f\u200e \u200e' and resp[0]['productType']=='cat':
            for r in resp:
                itemsList(r['productId'],False)
        else:
            for r in resp:
                addRow(r)

    xbmcplugin.endOfDirectory(addon_handle)

def addRow(r):
    title=r['title']
    rid=r['productId']
    img=logo_toya


    setArt={'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart':fanart}
    url = build_url({'mode':'itemsList','rid':rid})
    addItemList(url, title, setArt)

def itemsList(rid,isFolder=True):
    url=apiUrl+'vod/items'
    data={
        "count": 100,
        "rowId": rid,
        "start": 0
    }
    h=heaGen()
    resp=req('post',url,h,data)
    if resp!=None:
        for r in resp:
            addItem(r)

    if resp[0]['productType'] in ['vod','cutv']:
        xbmcplugin.setContent(addon_handle, 'videos')
    if isFolder:
        xbmcplugin.endOfDirectory(addon_handle)

def addItem(i):
    title=i['title'].replace('\n',' | ')
    pid=i['productId']
    img=i['imageUrl']

    setArt={'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart':fanart}

    if i['productType']=='cat':
        url = build_url({'mode':'rowsList','rid':pid})
        addItemList(url, title, setArt)

    elif i['productType'] in ['vod','cutv']:
        url = build_url({'mode':'playVod','vid':pid,'type':i['productType']})
        iL={'title':title,'plot':title,'mediatype':'movie'}
        addItemList(url, title, setArt, 'video', iL, False, 'true')

    elif i['productType']=='web' and ('customPlayer' in i and i['customPlayer'] in ['radio','camera']):
        if i['customPlayer']=='radio':
            Mode='playRadio'
        elif i['customPlayer']=='camera':
            Mode='playCamera'

        url = build_url({'mode':Mode,'link':i['externalUri']})
        addItemList(url, title, setArt, isF=False, isPla='true')


def playRadio(link):
    link+='|User-Agent='+UA
    directPlayer(link)

def playCamera(link):
    '''
    if '.mpd' in link:
        protocol='mpd'
    elif '.m3u8' in link:
        protocol='hls'

    ISAplayer(protocol,link)
    '''
    link+='|User-Agent='+UA
    directPlayer(link)

def playVod(vid,t):
    url=apiUrl+'playbackUrl'
    data={
        'productId':vid,
        'productType':t
    }
    resp=req('post',url,heaGen(),data)
    if resp!=None:
        if 'uri' in resp:
            stream_url=resp['uri']
            if '.mpd' in stream_url:
                protocol='mpd'
            elif '.m3u8' in stream_url:
                protocol='hls'

            drm=False
            licKey=None
            drm_config={}
            cert=None

            if 'drmInfo' in resp:
                drm=True
                drmInfo=resp['drmInfo']
                lic_url=drmInfo['licenseProxyUri']

                url_prelic=drmInfo['preAuthTokenUri']
                url='%s?cid=%s&type=%s'%(url_prelic,drmInfo['drmId'],t)
                resp=req('get',url,heaGen())
                if resp==None:
                    xbmc.log('@@@Odtwarzanie - błąd autoryzacji ', level=xbmc.LOGINFO)
                    xbmcgui.Dialog().notification('ToyaGO', 'Błąd autoryzacji', xbmcgui.NOTIFICATION_INFO)
                    xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem())
                    return

                lic_hea=heaGen()
                lic_hea[resp['headerName']]=resp['headerValue']
                lic_hea['content-type']='application/octet-stream'

                #K21
                licKey='%s|%s|R{SSM}|'%(lic_url,urlencode(lic_hea))
                #K22
                drm_config={
                    "com.widevine.alpha": {
                        "license": {
                            "server_url": lic_url,
                            "req_headers": urlencode(lic_hea),

                        }
                    }
                }

            ISAplayer(protocol,stream_url,drm,licKey,cert,drm_config)
        else:
            print(resp)
            xbmcgui.Dialog().notification('ToyaGO', 'Brak źródła', xbmcgui.NOTIFICATION_INFO)
            xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem())

    else:
        xbmcgui.Dialog().notification('ToyaGO', 'Błąd odtwarzania', xbmcgui.NOTIFICATION_INFO)
        xbmcplugin.setResolvedUrl(addon_handle, False, xbmcgui.ListItem())


def generate_m3u():
    file_name = addon.getSetting('fname')
    path_m3u = addon.getSetting('path_m3u')
    if file_name == '' or path_m3u == '':
        xbmcgui.Dialog().notification('ToyaGO', 'Ustaw nazwę pliku oraz katalog docelowy.', xbmcgui.NOTIFICATION_ERROR)
        return
    xbmcgui.Dialog().notification('ToyaGO', 'Generuję liste M3U.', xbmcgui.NOTIFICATION_INFO)
    data = '#EXTM3U\n'
    channels=channelsGen()
    for c in channels:
        if c['isAvailable']:
            name=c['name']
            cid=c['id']
            img=c['icon']

            data += '#EXTINF:0 tvg-id="%s" tvg-logo="%s",%s\nplugin://plugin.video.toya/?mode=playTV&cid=%s\n' % (name,img,name,cid)

    f = xbmcvfs.File(path_m3u + file_name, 'w')
    f.write(data)
    f.close()
    xbmcgui.Dialog().notification('ToyaGO', 'Wygenerowano listę M3U.', xbmcgui.NOTIFICATION_INFO)


mode = params.get('mode', None)

if not mode:
    if addon.getSetting('device_id')=='':
        getTID()
    main_menu()
else:
    if mode=='login':
        login()
        xbmc.executebuiltin('Container.Update(plugin://plugin.video.toya/,replace)')

    if mode=='logout':
        logout()
        xbmc.executebuiltin('Container.Update(plugin://plugin.video.toya/,replace)')

    if mode=='tvList':
        tvList()

    if mode=='setChanFltr':
        setChanFltr()

    if mode=='epg':
        cid=params.get('cid')
        getEpgForChan(cid)

    if mode=='playTV':
        cid=params.get('cid')
        playTV(cid)

    if mode=='catchup':
        rowsList('CUTV')

    if mode=='radio':
        rowsList('15')

    if mode=='cams':
        rowsList('25:25')

    if mode=='toyaOD':
        rowsList('37:37')

    if mode=='freeVOD':
        rowsList('22:22')

    if mode=='rowsList':
        rid=params.get('rid')
        rowsList(rid)

    if mode=='itemsList':
        rid=params.get('rid')
        itemsList(rid)

    if mode=='playRadio':
        link=params.get('link')
        playRadio(link)

    if mode=='playCamera':
        link=params.get('link')
        playCamera(link)

    if mode=='playVod':
        vid=params.get('vid')
        type=params.get('type')
        playVod(vid,type)

    if mode=='BUILD_M3U':
        generate_m3u()

    if mode=='KARAcateg':
       KARAcateg()

    if mode=='KARA_items':
        rid = params.get('rid')
        KARA_items(rid)

    if mode == 'playKaraoke':
        vid = params.get('vid')
        t = params.get('type')
        playKaraoke(vid, t)
