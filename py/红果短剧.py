# -*- coding: utf-8 -*-
# by @嗷呜
import re
import sys
from pyquery import PyQuery as pq
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):

    def init(self, extend=""):
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    host='https://www.hongguodj.cc'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': host,
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="134", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    def homeContent(self, filter):
        result = {}
        classes = []
        vlist = []
        data = pq(self.fetch(self.host, headers=self.headers).text)
        for i in list(data('.slip li').items())[1:]:
            classes.append({
                'type_name': i.text(),
                'type_id': re.findall(r'\d+', i('a').attr('href'))[0]
            })
        for i in data('.wrap .rows').items():
            vlist.extend(self.getlist(i('li')))
        result['class'] = classes
        result['list'] = vlist
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        data=pq(self.fetch(f'{self.host}/type/{tid}-{pg}.html', headers=self.headers).text)
        result = {}
        result['list'] = self.getlist(data('.list ul li'))
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        data=pq(self.fetch(f'{self.host}{ids[0]}', headers=self.headers).text)
        v=data('.info')
        p=v('p')
        vod = {
            'vod_name': v('h1').text(),
            'type_name': p.eq(2).text(),
            'vod_year': p.eq(3).text(),
            'vod_area': p.eq(4).text(),
            'vod_remarks': v('em').text(),
            'vod_actor': p.eq(0).text(),
            'vod_director': p.eq(1).text(),
            'vod_content': data('#desc .text').text(),
            'vod_play_from': '',
            'vod_play_url': ''
        }
        names = [i.text()  for i in data('.title.slip a').items()]
        plist=[]
        for i in data('.play-list ul').items():
            plist.append('#'.join([f'{j("a").text()}${j("a").attr("href")}' for j in i('li').items()]))
        vod['vod_play_from'] = '$$$'.join(names)
        vod['vod_play_url'] = '$$$'.join(plist)
        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        data=pq(self.fetch(f'{self.host}/search/{key}----------{pg}---.html', headers=self.headers).text)
        return {'list': self.getlist(data('.show.rows li')),'page':pg}

    def playerContent(self, flag, id, vipFlags):
        p=0
        uid=f'{self.host}{id}'
        data=pq(self.fetch(uid, headers=self.headers).text)
        url=data('.video.ratio').attr('data-play')
        if not url:
            url = uid
            p = 1
        return  {'parse': p, 'url': url, 'header': self.headers}

    def localProxy(self, param):
        pass

    def getlist(self,data):
        vlist = []
        for j in data.items():
            vlist.append({
                'vod_id': j('a').attr('href'),
                'vod_name': j('img').attr('alt'),
                'vod_pic': self.host + j('img').attr('data-src'),
                'vod_year': j('.bg').text(),
                'vod_remarks': j('p').text()
            })
        return vlist


