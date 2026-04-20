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

AddonID = 'plugin.video.toya'
Addon = xbmcaddon.Addon(AddonID)

_available = None
_checked = {}

makeSort=Addon.getSetting("makeSort")
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


baseurl1='https://nowa-go.toya.net.pl'
baseurl='https://go.toya.net.pl'
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


CHANNEL_MAP = {
     "More Discovery": "TLC",
     "TV4 HD": "TV4",
     "TVN HD": "TVN",
     "13.TV HD": "13 Ulica",
     "Discovery Channel HD ": "Discovery Channel",
}

if addon.getSetting('movie_view') == 'true':
    xbmcplugin.setContent(addon_handle, 'movies')
else:
    xbmcplugin.setContent(addon_handle, 'episodes')

def toggle_view():
    current = addon.getSetting('movie_view')

    if current == 'true':
        addon.setSetting('movie_view', 'false')
        xbmcgui.Dialog().notification('ToyaGO', 'Widok LISTA', xbmcgui.NOTIFICATION_INFO)
    else:
        addon.setSetting('movie_view', 'true')
        xbmcgui.Dialog().notification('ToyaGO', 'Widok MOVIES (Netflix)', xbmcgui.NOTIFICATION_INFO)

    xbmc.executebuiltin('Container.Refresh()')


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
    from urllib.parse import parse_qsl
    import sys

    params_local = dict(parse_qsl(sys.argv[2][1:]))
    history = params_local.get('history', '')

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

def ISAplayer(protocol, stream_url, DRM=False, licKey=None, cert=None, drm_config={}):

    mimeType = {'hls': 'application/x-mpegurl', 'mpd': 'application/xml+dash'}

    import inputstreamhelper

    PROTOCOL = protocol

    if DRM:
        DRM = 'com.widevine.alpha'
        is_helper = inputstreamhelper.Helper(PROTOCOL, drm=DRM)
    else:
        is_helper = inputstreamhelper.Helper(PROTOCOL)

    if is_helper.check_inputstream():

        headers = f'User-Agent={UA}&Referer={baseurl}&Origin={baseurl}'

        play_item = xbmcgui.ListItem(path=stream_url)
        play_item.setMimeType(mimeType[protocol])
        play_item.setContentLookup(False)

        play_item.setProperty('inputstream', is_helper.inputstream_addon)
        play_item.setProperty('IsPlayable', 'true')

        # 🔥 KLUCZOWE
        play_item.setProperty('inputstream.adaptive.manifest_type', protocol)
        play_item.setProperty('inputstream.adaptive.stream_headers', headers)
        play_item.setProperty('inputstream.adaptive.manifest_headers', headers)

        if DRM:
            play_item.setProperty('inputstream.adaptive.license_type', DRM)
            play_item.setProperty('inputstream.adaptive.license_key', licKey)
            play_item.setProperty('inputstream.adaptive.license_flags', 'persistent_storage')

            # Kodi 21+
            play_item.setProperty('inputstream.adaptive.drm', json.dumps(drm_config))

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

    sources = [
        ['TV', 'tvList', tv_icon,'157 kanałów poza domem w PL/UE wraz z przewodnikiem tv - EPG'],
        ['CatchUp TV', 'catchup', catch_up,'Oglądanie programu do 7 dni wstecz na wybranych kanałach - Catch‑up TV'],
        ['FreeVOD', 'freeVOD', VOD_icon,'VOD, Free VOD, seriale - tysiące filmów i seriali, hity, nowości oraz klasyczne pozycje'],
        ['TV Toya na życzenie', 'toyaOD', vod_na,'Umożliwia oglądanie archiwalnych materiałów, programów publicystycznych, informacyjnych oraz sportowych.Nadanych przez TV TOYA'],
        ['Radio', 'radio', radio_icon,'Blisko 600 stacji radiowych'],
        ['Kamery', 'cams', camera_icon,'Około 200 kamer poglądowych tematycznie: plaże, góry, jeziora, miasta'],
        ['Karaoke','KARAcateg',Karaoke_icon,'Karaoke zbiór piosenek z tekstem'],
        ['USTAWIENIA','settings_menu',settings_icon,'Ustawienia dodatku'],
    ]


    for s in sources:

        mode = s[1]

        if mode == 'noop':
            url = 'noop://'
            isF = False
        else:
            url = build_url({'mode': mode})
            isF = False if mode in ['login_menu', 'toggle_view'] else True

        setArt = {
            'thumb': s[2],
            'poster': s[2],
            'banner': s[2],
            'icon': s[2],
            'fanart': fanart
        }

        iL = {'title': s[0], 'plot': s[3], 'mediatype': 'movie'}
        addItemList(url, s[0], setArt, 'video', iL, isF=isF)

    xbmcplugin.endOfDirectory(addon_handle)

def settings_menu():

    if addon.getSetting('logged') != 'true':
        login_label = 'Zaloguj'
        login_mode = 'login'
    else:
        login_label = 'Wyloguj'
        login_mode = 'logout'

    items = [
        [login_label, login_mode, settings_icon],
        ['Ustawienia dodatku', 'addon_settings', settings_icon],
        ['Zmień widok (Netflix mode)', 'toggle_view', settings_icon],
    ]

    for title, mode, icon in items:

        url = build_url({'mode': mode})

        setArt = {
            'thumb': icon,
            'poster': icon,
            'banner': icon,
            'icon': icon,
            'fanart': fanart
        }

        addItemList(url, title, setArt, isF=False)

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
##            xbmc.log('@@@Błąd logowania (1): '+str(resp), level=xbmc.LOGINFO)
            xbmcgui.Dialog().notification('ToyaGO', 'Błąd logowania - szczegóły w logu', xbmcgui.NOTIFICATION_INFO)
            return
        h=heaGen()
        h['User-Profile-Id']='1'

        url=apiUrl+'profiles'
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
##            xbmc.log('@@@Błąd logowania (2): profile '+str(resp), level=xbmc.LOGINFO)
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
##        xbmc.log('@@@Odświeżono token', level=xbmc.LOGINFO)
        addon.setSetting('token',resp['token'])
        addon.setSetting('refreshToken',resp['refreshToken'])

    else:
##        xbmc.log('@@@Błąd refreshtoken: '+str(resp), level=xbmc.LOGINFO)
##        xbmc.log('@@@wylogowanie', level=xbmc.LOGINFO)
        logout()
##        xbmc.log('@@@Próba zalogowania', level=xbmc.LOGINFO)
        login()
def KARAcateg():
    data = [
        ('Dla dzieci', '13761','  Karaoke zbiór piosenek z tekstem '),
        ('Biesiada', '13711','  Super na imprezę i spotkanie z przyjaciółmi! Śpiewaj, baw się i sprawdź swoje możliwości wokalne!'),
        ('Polskie', '13751','  Piosenki warte zaśpiewania'),
        ('Zagraniczne', '13752','  Śpiewaj do najlepszych podkładów instrumentalnych! '),
    ]

    for title, rid,gt in data:
        setArt = {
            'icon': Karaoke_icon,
            'fanart': fanart
        }

        url = build_url({
            'mode': 'KARA_items',
            'rid': rid
        })

        iL = {'title': title, 'plot':title+gt, 'mediatype': 'movie'}
        addItemList(url,title, setArt, 'video', iL)

    xbmcplugin.endOfDirectory(addon_handle)

def KARA_items(rid):
    ######### 'https://beta-api-atv.toya.net.pl/'
    url =apiUrl + 'vod/items'
    data = {
        "count": 100,
        "rowId": rid,
        "start": 0
    }

    h = heaGen()
    h['Accept'] = '*/*'
    h['Connection'] = 'keep-alive'
    h['Sec-Fetch-Site'] = 'same-site'
    h['Referer'] = 'https://go.toya.net.pl/vod'
    h['Origin'] = "https://go.toya.net.pl"


    resp = req('post', url, h, data)

    if not resp:
        xbmcplugin.endOfDirectory(addon_handle)
        return

    for r in resp:
##        xbmc.log("KARA FULL ITEM: " + str(r), xbmc.LOGINFO)
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

def req(t, u, h, d={}):
    session = requests.Session()
    def get_req(t, u, h, d):
        if t == 'get':
            return session.get(u, headers=h)
        elif t == 'post':
            return session.post(u, headers=h, json=d)
        elif t == 'put':
            return session.put(u, headers=h, json=d)


    resp = get_req(t, u, h, d)

    print(resp.status_code)

    if resp.status_code in [403, 401] and addon.getSetting('logged') == 'true':
##        xbmc.log('@@@Błąd autoryzacji', level=xbmc.LOGINFO)

        refreshLogin()

        if addon.getSetting('logged') == 'true':

            # 🔴 KLUCZ: budujemy HEADERS OD NOWA
            new_headers = heaGen()

            resp = get_req(t, u, new_headers, d)

        else:
##            xbmc.log('@@@Nieudane przelogowanie', level=xbmc.LOGINFO)
            return None

    elif str(resp.status_code).startswith('4'):
        return None

    if not resp.text or resp.text.strip() == "":
##        xbmc.log("EMPTY RESPONSE - RAW", xbmc.LOGINFO)
        return None

    try:
        return resp.json()
    except Exception:
##        xbmc.log("NOT JSON - RETURN RAW", xbmc.LOGINFO)
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

def epg_channel(cid, epg_data):

    epg = 'Brak danych EPG'
    poster = None
    current_name = None

    epg_chan = [p['programs'] for p in epg_data if p['channelId'] == cid]

    if len(epg_chan) > 0:
        progs = epg_chan[0]
        epg = ''

        now = int(time.time())

        for i, p in enumerate(progs):
            if (i < len(progs)-1 and progs[i+1]['s'] > now) or i == len(progs)-1:
                current_name = p['n']
                desc = p['d']
                poster = p.get('p')  # <- PLAKAT
                ts = datetime.datetime.fromtimestamp(p['s']).strftime('%H:%M')
                epg+='[COLOR yellow]%s[/COLOR][COLOR blue] %s[/COLOR][COLOR cyan] - %s[/COLOR]\n'%(ts,current_name,desc)

                break

    return epg, poster, current_name

def getEpgForChan(cid, channel_name=''):    #### godzinowe

    url = apiUrl + 'epg'
    now = int(time.time())
    t = int(time.time() - 12*60*60)

    data = [{
        "channelId": cid,
        "count": 100,
        "start": t
    }]

    h = heaGen()
    h['Content-Type'] = 'application/json; charset=UTF-8'
    resp = req('post', url, h, data)

    if resp and len(resp) == 1:

        progs = resp[0]['programs']

        start_index = 0

        # 🔴 znajdź aktualny program
        for i in range(len(progs)):
            if i < len(progs) - 1:
                if progs[i]['s'] <= now < progs[i+1]['s']:
                    start_index = i
                    break
            else:
                start_index = i

        # 🔥 od aktualnego do końca
        for i in range(start_index, len(progs)):

            p = progs[i]

            name = p['n']
            desc = p.get('sd', '')
            img = p.get('p', '')
            plot1 = p['d']
            plot =f"[COLOR cyan]{plot1}[/COLOR]"

            ts = datetime.datetime.fromtimestamp(p['s']).strftime('%H:%M')

            label = f"[COLOR yellow] {ts}[/COLOR][COLOR=turquoise]   *    {channel_name}   - PROGRAM -    *[/COLOR]\n[COLOR blue] {name}- [/COLOR]{desc}"

            setArt = {
                'thumb': img,
                'poster': img,
                'banner': img,
                'icon': img,
                'fanart': fanart
            }

            iL = {
                'title': name,
                'plot': desc
            }
            ###################   url ='Action(Back)'
            url = 'plugin://plugin.video.toya/?mode=tvList'

            iL={'title': name,'sorttitle': name,'plot': plot}
            setArt={'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart':fanart}
            addItemList(url, label, setArt, 'video', iL, isF=True)
    else:
        li = xbmcgui.ListItem("Brak danych EPG")
        xbmcplugin.addDirectoryItem(addon_handle, "", li, False)

    xbmcplugin.endOfDirectory(addon_handle)

def channelsGen():
    channels=[]
    url=apiUrl+'channels'
    h=heaGen()
    resp=req('get',url,h)
    if resp!=None:
        if 'channels' in resp:
            channels=resp['channels']
##    xbmc.log(str(channels[0]), xbmc.LOGINFO)
    return channels

def tvList():

    chanFltr=addon.getSetting('chanFltr')
    cf=chanFltr if chanFltr!='' else 'wszystkie'
    #filtr
    title='[COLOR=cyan]Kategoria:[/COLOR] %s \nLista stacji TV wybranej kategorii'%(cf)
    img='DefaultGenre.png'

    setArt={'thumb': img, 'poster': img, 'banner': img, 'icon': img, 'fanart':fanart}
    url = build_url({'mode':'setChanFltr'})
    addItemList(url, title, setArt, isF=False)

    channels=channelsGen()
    if makeSort =="true":
        channels.sort(key=lambda x: x.get('name','').lower())
    else:
        pass

    epg=EPG_data()

    idx = 1  # ✅ licznik tylko dla WYŚWIETLANYCH kanałów

    for c in channels:
        if c['isAvailable'] and c['service']==1 and cf in c['list']:

            name=c['name']
            cid=c['id']
            img=c['icon']

            plot=epg_channel(cid,epg)
            plot, poster, current_name = epg_channel(cid, epg)

            channel_name = c['name']

            # ✅ NUMERACJA
            name_num = f"[COLOR green]{idx}.[/COLOR] {name}"

            if current_name:
                name1 = f"{name_num}\n[COLOR blue]{current_name}[/COLOR]"
            else:
                name1 = name_num

            contMenu = True

            cmItems=[(
                '[B]Program Godzinowy TV[/B]',
                'Container.Update(plugin://plugin.video.toya/?mode=epg&cid=%s&channel_name=%s)' % (
                    cid,
                    quote_plus(channel_name)
                )
            )]

            iL={
                'title':name,
                'sorttitle': f"{idx:03d}",  # opcjonalnie (możesz usunąć)
                'plot': plot
            }

            setArt={
                'thumb': poster,
                'poster': poster,
                'banner': poster,
                'icon': poster,
                'fanart':poster
            }

            url = build_url({'mode':'playTV','cid':cid})
            addItemList(url, name1, setArt, 'video', iL, False, 'true', contMenu, cmItems)

            idx += 1  # ✅ zwiększamy tylko dla tych co przeszły filtr


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

def accept_age(vid):

    url = apiUrl + 'vod/ageVerification'

    data = {
        "productId": vid,
        "accept": True
    }

    resp = req('post', url, heaGen(), data)

##    xbmc.log("### AGE ACCEPT RESP: " + str(resp), xbmc.LOGINFO)

    return resp

def resolve_stream(resp, productType):

    streams = []

    # 🔴 1. główny stream
    if 'uri' in resp:
        streams.append(resp['uri'])

    # 🔴 2. fallback (jeśli API kiedyś zwróci alternatywy)
    if 'alternativeUris' in resp:
        streams += resp['alternativeUris']

    # 🔴 SORT: MPD najpierw, potem HLS
    def sort_key(u):
        if '.mpd' in u:
            return 0
        if '.m3u8' in u:
            return 1
        return 2

    streams = sorted(streams, key=sort_key)

    return streams

def playContent(productId=None, productType=None, cid=None):

##    xbmc.log("### UNIFIED PLAYER START", xbmc.LOGINFO)

    # 🔴 TRYB TV (po cid)
    if cid:
##        xbmc.log("### MODE: TV", xbmc.LOGINFO)

        channels = channelsGen()
        data = [c for c in channels if c['id'] == cid]

        if not data:
##            xbmc.log("### TV FAIL: brak kanału", xbmc.LOGINFO)
            return

        data = data[0]
        stream_url = data['uri']

        if '.mpd' in stream_url:
            protocol = 'mpd'
        else:
            protocol = 'hls'

        drm = False
        licKey = None
        drm_config = {}

        if data.get('drm'):
            drm = True

            lic_url = data['licenseProxyUri']
            pre = data['preAuthTokenUri']

            url2 = f"{pre}?cid={data['drmId']}&type=TIVI"
            resp2 = req('get', url2, heaGen())

            if not resp2:
                xbmc.log("### TV DRM FAIL", xbmc.LOGINFO)
                return

            lic_hea = heaGen()
            lic_hea[resp2['headerName']] = resp2['headerValue']
            lic_hea['content-type'] = 'application/octet-stream'

            licKey = f"{lic_url}|{urlencode(lic_hea)}|R{{SSM}}|"

            drm_config = {
                "com.widevine.alpha": {
                    "license": {
                        "server_url": lic_url,
                        "req_headers": urlencode(lic_hea),
                    }
                }
            }

        ISAplayer(protocol, stream_url, drm, licKey, None, drm_config)
        return

    # 🔴 TRYB VOD / KARAOKE
##    xbmc.log("### MODE: VOD/KARAOKE", xbmc.LOGINFO)

    if not productId or not productType:
        xbmc.log("### FAIL: brak productId", xbmc.LOGINFO)
        return

    pid = f"{productType}:{productId}"

    # 🔴 POBRANIE playbackUrl (z retry)
    resp = getPlaybackData(pid, productType)

##    xbmc.log("### playbackUrl RESP: " + str(resp), xbmc.LOGINFO)

    if not resp:
        xbmc.log("### FAIL: brak odpowiedzi playback", xbmc.LOGINFO)
        return

    # 🔴 TU dopiero używamy resolve_stream
    streams = resolve_stream(resp, productType)

    if not streams:
##        xbmc.log("### FAIL: brak streamów", xbmc.LOGINFO)
        return

    for attempt, stream_url in enumerate(streams):

        xbmc.log(f"### TRY STREAM {attempt+1}: {stream_url}", xbmc.LOGINFO)

        if '.mpd' in stream_url:
            protocol = 'mpd'
        elif '.m3u8' in stream_url:
            protocol = 'hls'
        else:
            continue

        drm = False
        licKey = None
        drm_config = {}

        if 'drmInfo' in resp:
            drm = True
            drmInfo = resp['drmInfo']

            lic_url = drmInfo['licenseProxyUri']
            pre = drmInfo['preAuthTokenUri']

            url2 = f"{pre}?cid={drmInfo['drmId']}&type={productType}"
            resp2 = req('get', url2, heaGen())

            if not resp2:
##                xbmc.log("### DRM FAIL → next stream", xbmc.LOGINFO)
                continue

            lic_hea = heaGen()
            lic_hea[resp2['headerName']] = resp2['headerValue']
            lic_hea['content-type'] = 'application/octet-stream'

            licKey = f"{lic_url}|{urlencode(lic_hea)}|R{{SSM}}|"

            drm_config = {
                "com.widevine.alpha": {
                    "license": {
                        "server_url": lic_url,
                        "req_headers": urlencode(lic_hea),
                    }
                }
            }

        try:
            ISAplayer(protocol, stream_url, drm, licKey, None, drm_config)
            return
        except Exception as e:
##            xbmc.log(f"### PLAYER FAIL: {str(e)}", xbmc.LOGINFO)
            continue

##    xbmc.log("### ALL STREAMS FAILED", xbmc.LOGINFO)
    xbmcgui.Dialog().notification('ToyaGO', 'Nie udało się odtworzyć', xbmcgui.NOTIFICATION_INFO)

def isChannelAvailableOnce(name):
    global _available

    if not name:
        return False

    key = name.split(' > ')[0].lower()

    # cache wyników
    if key in _checked:
        return _checked[key]

    #  jedno pobranie kanałów
    if _available is None:
        _available = set()
        for c in channelsGen():
            if c.get('isAvailable') and c.get('service') == 1:
                _available.add(c.get('name', '').lower())

    # szybkie sprawdzenie (bez pętli)
    status = any(key in ch for ch in _available)

    _checked[key] = status
    return status
def getPlaybackData(pid, productType):

    url = apiUrl + 'playbackUrl'
    data = {
        "productId": pid,
        "productType": productType
    }

    for i in range(2):  # 🔴 2 próby
        resp = req('post', url, heaGen(), data)
##        resp = getPlaybackData(pid, productType)


        if resp and isinstance(resp, dict) and 'uri' in resp:
            return resp

        xbmc.log(f"### playback retry {i+1}", xbmc.LOGINFO)

    return None
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
    history = params.get('history', '')
    title = r['title']
    rid = r['productId']

    # 🔹 IKONA + TYP
    img = logo_toya
    typ = "Pakiet"

    is_check_needed = False  # klucz

    if "25:" in rid:
        img = camera_icon
        typ = "Kamery"
    elif "37:" in rid:
        img = vod_na
        typ = "VOD"
        is_check_needed = True

    elif "22:" in rid:
        img = freeVOD_icon
        typ = "Darmowe VOD"
        is_check_needed = True
    elif "CUTV:" in rid:
        img = Catch_up_icon
        typ = "Catch-up TV"
        is_check_needed = True

    # OPIS + STATUS
    if is_check_needed:
        title = CHANNEL_MAP.get(title,title)

        status = isChannelAvailableOnce(title)


        if status == True:
            status_text = f"[COLOR green]Kanał {title} jest dostępny[/COLOR]"
        else:
            status_text = f"[COLOR red]Kanał {title} niedostępny[/COLOR]"
        if " > " in history:
            status = isChannelAvailableOnce(history)
            if status == True:
                status_text = f"[COLOR green]Pozycja {title} może będzie dostępna[/COLOR]"
            else:
                status_text = f"[COLOR red]Pozycja {title} niedostępna[/COLOR]"

        plot = (
            f"[B]{title}[/B]\n"
            f"[COLOR cyan]Typ:[/COLOR] {typ}\n"
            f"[COLOR yellow]Status: [/COLOR] {status_text}\n\n"
            f"[I]Rodzaj TV {history}[/I]"
        )
        title_display = f"{title}"
    else:
        # dla kamer i radia — czysto
        plot = f"[B]{title}[/B]\n[COLOR cyan]Typ:[/COLOR] {typ}"
        title_display = title

    #  ART
    setArt = {
        'thumb': img,
        'poster': img,
        'banner': img,
        'icon': img,
        'fanart': fanart
    }

    iL = {
        'title': title,
        'plot': plot
    }

    url = build_url({
        'mode': 'itemsList',
        'rid': rid,
        'history': title  # KLUCZOWE
    })

    addItemList(url, title_display, setArt, 'video', iL)


def itemsList(rid, isFolder=True):
    params = dict(parse_qsl(sys.argv[2][1:]))
    history = params.get('history', '')

    url = apiUrl + 'vod/items'
    data = {
        "count": 100,
        "rowId": rid,
        "start": 0
    }
    h = heaGen()
    resp = req('post', url, h, data)

    if resp != None:
        for r in resp:
            addItem(r, history)  # ✅ przekazanie history

    if resp[0]['productType'] in ['vod', 'cutv']:
        xbmcplugin.setContent(addon_handle, 'videos')
    if isFolder:
        xbmcplugin.endOfDirectory(addon_handle)


def addItem(i, history):  # ✅ przyjmujemy history jako parametr

    title_raw = i['title'].replace('\n', ' - ')
    pid = i['productId']
    img = i['imageUrl']

    title1 = f"[COLOR lightskyblue]{title_raw}[/COLOR]"


    if history:
        new_history = f"[COLOR coral]TV kanał \ Seria:\n{history}[/COLOR]"+"\n"+title1 ## w free vod
    else:
        new_history = title1

    title = title_raw

    setArt = {
        'thumb': img,
        'poster': img,
        'banner': img,
        'icon': img,
        'fanart': fanart
    }

    # =========================
    # CAT (LISTA)
    # =========================
    if i['productType'] == 'cat':

        url = build_url({
            'mode': 'rowsList',
            'rid': pid,
##            'history': i['title']
            'history': f"{history} > {i['title']}" if history else i['title']
        })

        iL = {
            'title': title1,
            'plot': new_history,
            'mediatype': 'movie'
        }

        addItemList(url, title1, setArt, 'video', iL)

    # =========================
    # VOD / CUTV
    # =========================
    elif i['productType'] in ['vod', 'cutv']:

        url = build_url({
            'mode': 'playVod',
            'vid': pid,
            'type': i['productType'],
            'history': f"{history} > {i['title']}" if history else i['title']
        })

        rating = float(i.get('rating', 7.5))
        duration = i.get('duration', 0)

        plot = (
            f"[COLOR coral]{new_history}[/COLOR]\n\n"
            f"[COLOR gold]Ocena {round(rating,1)}/10[/COLOR]\n"
##            f"[B]{status_text}[/B]"
        )

        fan = i.get('backgroundUrl') or img

        setArt = {
            'thumb': img,
            'poster': img,
            'banner': img,
            'icon': img,
            'fanart': fan
        }

        iL = {
            'title': title_raw,
            'plot': plot,
            'rating': rating,
            'mediatype': 'movie',
            'duration': int(duration) if duration else 0
        }

        addItemList(url, title_raw, setArt, 'video', iL, False, 'true')

    # =========================
    # WEB
    # =========================
    elif i['productType'] == 'web' and i.get('customPlayer') in ['radio', 'camera']:

        Mode = 'playRadio' if i['customPlayer'] == 'radio' else 'playCamera'

        url = build_url({
            'mode': Mode,
            'link': i['externalUri'],
            'history': f"{history} > {i['title']}" if history else i['title']
        })

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


    if mode=='playTV':
        playContent(cid=params.get('cid'))

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
        playContent(
            productId=params.get('vid'),
            productType=params.get('type')
        )

    if mode=='BUILD_M3U':
        generate_m3u()

    if mode=='KARAcateg':
       KARAcateg()

    if mode=='KARA_items':
        rid = params.get('rid')
        KARA_items(rid)

    if mode == 'playKaraoke':
        playContent(
            productId=params.get('vid'),
            productType=params.get('type')
        )

    if mode == 'login':
        login()
        xbmc.executebuiltin('Container.Refresh()')

    if mode == 'logout':
        logout()
        xbmc.executebuiltin('Container.Refresh()')

    if mode == 'settings_menu':
        settings_menu()

    if mode == 'addon_settings':
        addon.openSettings()

    if mode == 'toggle_view':
        toggle_view()

    if mode == 'epg':
        xbmc.log("### MODE EPG ENTERED", xbmc.LOGINFO)

        cid = params.get('cid')
        channel_name = params.get('channel_name', '')

        xbmc.log(f"### CID={cid} NAME={channel_name}", xbmc.LOGINFO)

        getEpgForChan(cid, channel_name)