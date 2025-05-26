"""

作者 啦啦啦 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================kaiyuebinguan====================

"""

import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider
import sys
import json
import base64
import urllib.parse

sys.path.append('..')

xurl = "https://qkys.me"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
          }

pm = ''

class Spider(Spider):
    global xurl
    global headerx

    def getName(self):
        return "首页"

    def init(self, extend):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def extract_middle_text(self, text, start_str, end_str, pl, start_index1: str = '', end_index2: str = ''):
        if pl == 3:
            plx = []
            while True:
                start_index = text.find(start_str)
                if start_index == -1:
                    break
                end_index = text.find(end_str, start_index + len(start_str))
                if end_index == -1:
                    break
                middle_text = text[start_index + len(start_str):end_index]
                plx.append(middle_text)
                text = text.replace(start_str + middle_text + end_str, '')
            if len(plx) > 0:
                purl = ''
                for i in range(len(plx)):
                    matches = re.findall(start_index1, plx[i])
                    output = ""
                    for match in matches:
                        match3 = re.search(r'(?:^|[^0-9])(\d+)(?:[^0-9]|$)', match[1])
                        if match3:
                            number = match3.group(1)
                        else:
                            number = 0
                        if 'http' not in match[0]:
                            output += f"#{'📽️冉神👉' + match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{'📽️冉神👉' + match[1]}${number}{match[0]}"
                    output = output[1:]
                    purl = purl + output + "$$$"
                purl = purl[:-3]
                return purl
            else:
                return ""
        else:
            start_index = text.find(start_str)
            if start_index == -1:
                return ""
            end_index = text.find(end_str, start_index + len(start_str))
            if end_index == -1:
                return ""

        if pl == 0:
            middle_text = text[start_index + len(start_str):end_index]
            return middle_text.replace("\\", "")

        if pl == 1:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                jg = ' '.join(matches)
                return jg

        if pl == 2:
            middle_text = text[start_index + len(start_str):end_index]
            matches = re.findall(start_index1, middle_text)
            if matches:
                new_list = [f'✨冉神👉{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "1", "type_name": "冉神电影🎃"},
                            {"type_id": "2", "type_name": "冉神剧集🎃"},
                            {"type_id": "4", "type_name": "冉神动漫🎃"},
                            {"type_id": "5", "type_name": "冉神纪录片🎃"},
                            {"type_id": "3", "type_name": "冉神综艺🎃"}],

                  "list": [],
                  "filters": {"1": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}],
                              "2": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}],
                              "5": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}],
                              "3": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}],
                              "4": [{"key": "年代",
                                     "name": "年代",
                                     "value": [{"n": "全部", "v": ""},
                                               {"n": "2025", "v": "2025"},
                                               {"n": "2024", "v": "2024"},
                                               {"n": "2023", "v": "2023"},
                                               {"n": "2022", "v": "2022"},
                                               {"n": "2021", "v": "2021"},
                                               {"n": "2020", "v": "2020"},
                                               {"n": "2019", "v": "2019"},
                                               {"n": "2018", "v": "2018"}]}]}}

        return result

    def homeVideoContent(self):
        videos = []
        try:
            detail = requests.get(url=xurl, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('div', class_="module-items module-poster-items-base")

            for soup in soups:
                vods = soup.find_all('a', class_="module-poster-item module-item")

                for vod in vods:

                    name = vod['title']

                    id = vod['href']

                    pic = vod.find('img')['data-original']
                    if 'http' not in pic:
                        pic = xurl + pic

                    remarks = vod.find('div', class_='module-item-note')
                    if remarks:
                        remark = remarks.text.strip()
                    else:
                        remark = ""

                    video = {
                        "vod_id": id,
                        "vod_name": '冉神📽️' + name,
                        "vod_pic": pic,
                        "vod_remarks": '冉神▶️' + remark
                             }
                    videos.append(video)

            result = {'list': videos}
            return result
        except:
            pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []
        if pg:
            page = int(pg)
        else:
            page = 1

        if '年代' in ext.keys():
            NdType = ext['年代']
        else:
            NdType = ''

        if page == '1':
            url = f'{xurl}/vodshow/{cid}-----------2025.html'

        else:
            url = f'{xurl}/vodshow/{cid}--------{str(page)}---{NdType}.html'

        try:
            detail = requests.get(url=url, headers=headerx)
            detail.encoding = "utf-8"
            res = detail.text
            doc = BeautifulSoup(res, "lxml")

            soups = doc.find_all('div', class_="module")

            for soup in soups:
                vods = soup.find_all('a', class_="module-poster-item module-item")

                for vod in vods:

                    name = vod['title']

                    id = vod['href']

                    pic = vod.find('img')['data-original']

                    if 'http' not in pic:
                        pic = xurl + pic

                    remarks = vod.find('div', class_='module-item-note')
                    if remarks:
                        remark = remarks.text.strip()
                    else:
                        remark = ""

                    video = {
                        "vod_id": id,
                        "vod_name": '冉神📽️' + name,
                        "vod_pic": pic,
                        "vod_remarks": '冉神▶️' + remark
                             }
                    videos.append(video)

        except:
            pass
        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 99
        result['limit'] = 90
        result['total'] = 99
        return result

    def detailContent(self, ids):
        global pm
        did = ids[0]
        result = {}
        videos = []
        playurl = ''
        if 'http' not in did:
            did = xurl + did
        res1 = requests.get(url=did, headers=headerx)
        res1.encoding = "utf-8"
        res = res1.text

        xianlu = self.extract_middle_text(res, '<div class="module-tab-items-box hisSwiper', '<div class="shortcuts-mobile-overlay">', 2, 'data-dropdown-value="(.*?)">')

        bofang = self.extract_middle_text(res, '<div class="module-play-list-content', '</div>', 3,'href="(.*?)" title="(.*?)">')

        videos.append({
            "vod_id": did,
            "vod_actor": '😸冉神 😸冉神',
            "vod_director": '😸冉神',
            "vod_content": '😸请不要相信任何广告！！！祝您观影愉快！',
            "vod_play_from": xianlu,
            "vod_play_url": bofang
        })
        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):
        parts = id.split("http")
        xiutan = 0
        if xiutan == 0:
            if len(parts) > 1:
                before_https, after_https = parts[0], 'http' + parts[1]
            res = requests.get(url=after_https, headers=headerx)
            res = res.text

            url = self.extract_middle_text(res, '"},"url":"', '","', 0).replace('\\', '')

            result = {}
            result["parse"] = xiutan
            result["playUrl"] = ''
            result["url"] = url
            result["header"] = headerx
            return result

    def searchContentPage(self, key, quick, page):
        result = {}
        videos = []
        if not page:
            page = '1'
        if page == '1':
            url = f'{xurl}/vodsearch/-------------.html?wd={key}'
        else:
            url = f'{xurl}/vodsearch/{key}----------{str(page)}---.html'

        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        res = detail.text
        doc = BeautifulSoup(res, "lxml")

        soups = doc.find_all('div', class_="module-items module-card-items")

        for soup in soups:
            vods = soup.find_all('div', class_="module-card-item module-item")

            for vod in vods:

                name = vod.find('img')['alt']

                id = vod.find('a')['href']

                pic = vod.find('img')['data-original']
                if 'http' not in pic:
                    pic = xurl + pic

                remarks = vod.find('div', class_='module-item-note')
                remark = remarks.text.strip()
           
            video = {
                "vod_id": id,
                "vod_name": '冉神📽️' + name,
                "vod_pic": pic,
                "vod_remarks": '冉神▶️' + remark
                    }
            videos.append(video)
      

        result['list'] = videos
        result['page'] = page
        result['pagecount'] = 60
        result['limit'] = 30
        result['total'] = 999999
        return result

    def searchContent(self, key, quick):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None