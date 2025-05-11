# coding = utf-8
# !/usr/bin/python

"""

作者 丢丢喵 🚓 内容均从互联网收集而来 仅供交流学习使用 版权归原创者所有 如侵犯了您的权益 请通知作者 将及时删除侵权内容
                    ====================Diudiumiao====================

"""

from Crypto.Util.Padding import unpad
from Crypto.Util.Padding import pad
from urllib.parse import unquote
from Crypto.Cipher import ARC4
from urllib.parse import quote
from base.spider import Spider
from Crypto.Cipher import AES
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
import urllib.request
import urllib.parse
import binascii
import requests
import base64
import json
import time
import sys
import re
import os

sys.path.append('..')

xurl = "https://kzb29rda.com"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
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
                            output += f"#{match[1]}${number}{xurl}{match[0]}"
                        else:
                            output += f"#{match[1]}${number}{match[0]}"
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
                new_list = [f'{item}' for item in matches]
                jg = '$$$'.join(new_list)
                return jg

    def homeContent(self, filter):
        result = {}
        result = {"class": [{"type_id": "82", "type_name": "英超"},
                            {"type_id": "120", "type_name": "西甲"},
                            {"type_id": "129", "type_name": "德甲"},
                            {"type_id": "108", "type_name": "意甲"},
                            {"type_id": "142", "type_name": "法甲"},
                            {"type_id": "46", "type_name": "欧冠"},
                            {"type_id": "542", "type_name": "中超"},
                            {"type_id": "567", "type_name": "日职联"},
                            {"type_id": "590", "type_name": "澳超"},
                            {"type_id": "83", "type_name": "英冠"},
                            {"type_id": "457", "type_name": "美职业"},
                            {"type_id": "543", "type_name": "中甲"},
                            {"type_id": "168", "type_name": "荷甲"},
                            {"type_id": "581", "type_name": "韩K联"},
                            {"type_id": "465", "type_name": "墨西超"},
                            {"type_id": "546", "type_name": "中女超"},
                            {"type_id": "568", "type_name": "日职乙"},
                            {"type_id": "575", "type_name": "日联杯"},
                            {"type_id": "614", "type_name": "沙特联"},
                            {"type_id": "629", "type_name": "阿联酋杯"},
                            {"type_id": "238", "type_name": "俄超"},
                            {"type_id": "151", "type_name": "葡超"},
                            {"type_id": "209", "type_name": "丹麦超"},
                            {"type_id": "121", "type_name": "西乙"},
                            {"type_id": "1722", "type_name": "牙买超"},
                            {"type_id": "34", "type_name": "国际友谊"},
                            {"type_id": "2115", "type_name": "墨女超"},
                            {"type_id": "130", "type_name": "德乙"},
                            {"type_id": "1788", "type_name": "印尼甲"},
                            {"type_id": "462", "type_name": "智利甲"},
                            {"type_id": "143", "type_name": "法乙"},
                            {"type_id": "466", "type_name": "墨西甲"},
                            {"type_id": "592", "type_name": "澳维超"},
                            {"type_id": "475", "type_name": "哥伦甲"},
                            {"type_id": "589", "type_name": "韩国杯"},
                            {"type_id": "586", "type_name": "韩女联"},
                            {"type_id": "582", "type_name": "韩K2联"},
                            {"type_id": "461", "type_name": "美公开赛"},
                            {"type_id": "315", "type_name": "土超"},
                            {"type_id": "429", "type_name": "阿甲"},
                            {"type_id": "602", "type_name": "澳女联"},
                            {"type_id": "316", "type_name": "土甲"},
                            {"type_id": "97", "type_name": "英乙U21"},
                            {"type_id": "332", "type_name": "保甲"},
                            {"type_id": "55", "type_name": "欧女冠"},
                            {"type_id": "84", "type_name": "英甲"},
                            {"type_id": "169", "type_name": "荷乙"}],
                  }

        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, cid, pg, filter, ext):
        result = {}
        videos = []

        current_timestamp = int(datetime.now().timestamp())
        dt_object = datetime.fromtimestamp(current_timestamp)
        formatted_date = dt_object.strftime('%Y-%m-%d')

        url = f'{xurl}/prod-api/match/list/new?isfanye=1&type=1&cid={cid}&ishot=-1&pn=1&ps=20&level=&name=&langtype=zh&starttime={formatted_date}&pid=4&zoneId=Asia%2FShanghai&zhuboType=0'

        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        if detail.status_code == 200:
            data = detail.json()

            js = data['data']['dataList']

            for vod in js:

                nameq = vod['hteam_name']
                nameh = vod['ateam_name']
                name = nameq + ' - ' + nameh

                id = vod['id']

                pic = vod['ateam_logo']

                zhuangtai = vod['status_up_name']
                zhuangtai = zhuangtai.replace('完场', '回看')
                shijian = vod['matchtime']
                bifen = vod['score']
                remark = zhuangtai + ' ' + shijian + ' 比分' + bifen

                video = {
                    "vod_id": id,
                    "vod_name": name,
                    "vod_pic": pic,
                    "vod_remarks": remark
                        }
                videos.append(video)

        result = {'list': videos}
        result['page'] = pg
        result['pagecount'] = 1
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        global pm
        did = ids[0]
        result = {}
        videos = []
        xianlu = ''
        bofang = ''

        url = f'{xurl}/prod-api/match/detail?mid={did}&type=1&isnew=1&pid=4&langtype=zh&test=1&zoneId=Asia%2FShanghai'
        detail = requests.get(url=url, headers=headerx)
        detail.encoding = "utf-8"
        if detail.status_code == 200:
            data = detail.json()

        url = 'https://fs-im-kefu.7moor-fs1.com/ly/4d2c3f00-7d4c-11e5-af15-41bf63ae4ea0/1732707176882/jiduo.txt'
        response = requests.get(url)
        response.encoding = 'utf-8'
        code = response.text
        name = self.extract_middle_text(code, "s1='", "'", 0)
        Jumps = self.extract_middle_text(code, "s2='", "'", 0)

        kaichang = data['data']['matchinfo']['matchtime']
        bifen = data['data']['matchinfo']['score']
        diqun = data['data']['matchinfo']['name']
        zhuangtai = data['data']['matchinfo']['status_up_name']
        duizhanq = data['data']['matchinfo']['ateam_name']
        duizhanh = data['data']['matchinfo']['hteam_name']

        content = '😸集多为您介绍一场' + diqun +'的比赛 参赛双方是 ' + duizhanq +' - '+ duizhanh + ' 比赛时间是 ' + kaichang + ' 现在是 ' + zhuangtai + ' 比分是 ' + bifen + ' 请勿相信任何广告 免费分享 收费死全家'

        director = data['data']['matchinfo']['name']

        actor = duizhanq + ' - ' + duizhanh

        remarks = data['data']['matchinfo']['status_up_name']

        year = data['data']['matchinfo']['matchtime']

        if name not in content:
            bofang = Jumps
            xianlu = '1'
        else:
            soups = data['data']['matchinfo']['video_url']

            if soups:
                bofang = soups
                xianlu = '集多回看专线'
            else:
                js = data['data']['matchinfo']['global_live_urls']

                for sou in js:

                    id = sou['url']

                    name = sou['name']

                    bofang = bofang + name + '$' + id + '#'

                bofang = bofang[:-1]

                xianlu = '集多现场专线'

        videos.append({
            "vod_id": did,
            "vod_director": director,
            "vod_actor": actor,
            "vod_remarks": remarks,
            "vod_year": year,
            "vod_content": content,
            "vod_play_from": xianlu,
            "vod_play_url": bofang
                     })

        result['list'] = videos
        return result

    def playerContent(self, flag, id, vipFlags):

        result = {}
        result["parse"] = 0
        result["playUrl"] = ''
        result["url"] = id
        result["header"] = headerx
        return result

    def searchContentPage(self, key, quick, page):
        pass

    def searchContent(self, key, quick, pg="1"):
        return self.searchContentPage(key, quick, '1')

    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None









