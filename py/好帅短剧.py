# -*- coding: utf-8 -*-
# by @嗷呜
import json
import sys
sys.path.append('..')
from base.spider import Spider
from pyquery import PyQuery as pq

class Spider(Spider):

    def init(self, extend=""):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def action(self, action):
        pass

    def destroy(self):
        pass

    host='https://www.nhsyy.com'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': host,
        'Pragma': 'no-cache',
        'Referer': f'{host}/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="130", "Google Chrome";v="130"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    def homeContent(self, filter):
        data = pq(self.fetch(self.host, headers=self.headers).text)
        result = {}
        classes = []
        for i in data('.drop-content-items li').items():
            j = i('a').attr('href')
            if j and 'type' in j:
                id = j.split('/')[-1].split('.')[0]
                classes.append({
                    'type_name': i('a').text(),
                    'type_id': id
                })
        hlist = self.getlist(data('.module-lines-list .module-item'))
        result['class'] = classes
        result['list'] = hlist
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        data = self.fetch(f'{self.host}/vodshwo/{tid}--------{pg}---.html', headers=self.headers).text
        vlist = self.getlist(pq(data)('.module-list .module-item'))
        return {"list": vlist, "page": pg, "pagecount": 9999, "limit": 90, "total": 999999}

    def detailContent(self, ids):
        data = pq(self.fetch(f"{self.host}{ids[0]}", headers=self.headers).text)
        udata = data('.scroll-box-y .scroll-content a')
        vdata = data('.video-info-main .video-info-item')
        vod = {
            'vod_year': vdata.eq(2)('div').text(),
            'vod_remarks': vdata.eq(3)('div').text(),
            'vod_actor': vdata.eq(1)('a').text(),
            'vod_director': vdata.eq(0)('a').text(),
            'typt_name': data('.video-info-aux a').eq(0).attr('title'),
            'vod_content': vdata.eq(4)('p').eq(-1).text(),
            'vod_play_from': '嗷呜爱看短剧',
            'vod_play_url': '#'.join([f"{i.text()}${i.attr('href')}" for i in udata.items()]),
        }
        result = {"list": [vod]}
        return result

    def searchContent(self, key, quick, pg="1"):
        dlist = self.fetch(f'{self.host}/vodsearch/{key}----------{pg}---.html', headers=self.headers).text
        ldata = pq(dlist)('.module-list .module-search-item')
        vlist = []
        for i in ldata.items():
            img = i('.module-item-pic')
            vlist.append({
                'vod_id': i('.video-serial').attr('href'),
                'vod_name': img('img').attr('alt'),
                'vod_pic': img('img').attr('data-src'),
                'vod_year': i('.tag-link a').eq(0).text(),
                'vod_remarks': i('.video-serial').text()
            })
        result = {"list": vlist, "page": pg}
        return result

    def playerContent(self, flag, id, vipFlags):
        data=self.fetch(f"{self.host}{id}", headers=self.headers).text
        jstr = pq(data)('.player-wrapper script').eq(0).text()
        try:
            jdata = json.loads(jstr.split('=', 1)[-1])
            url = jdata.get('url') or jdata.get('next_url')
            p=0
        except:
            url,p = f"{self.host}{id}",1
        return {'parse': p, 'url': url, 'header': self.headers}

    def localProxy(self, param):
        pass

    def getlist(self, data):
        vlist = []
        for i in data.items():
            img = i('.module-item-pic')
            vlist.append({
                'vod_id': img('a').attr('href'),
                'vod_name': img('img').attr('alt'),
                'vod_pic': img('img').attr('data-src'),
                'vod_remarks': i('.module-item-text').text()
            })
        return vlist
