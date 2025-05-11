# -*- coding: utf-8 -*-
# by @嗷呜
import colorsys
import random
import re
import sys
from base64 import b64decode, b64encode
from email.utils import unquote
from Crypto.Hash import MD5
sys.path.append("..")
import json
import time
from pyquery import PyQuery as pq
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

    def action(self, action):
        pass

    def destroy(self):
        pass

    host='https://www.aowu.tv'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="134", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': f'{host}/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'priority': 'u=0, i',
    }

    def homeContent(self, filter):
        data=self.getpq(self.fetch(self.host,headers=self.headers).text)
        result = {}
        classes = []
        ldata=data('.wrap.border-box.public-r .public-list-box')
        cd={"新番":"32","番剧":"20","剧场":"33"}
        for k,r in cd.items():
            classes.append({
                'type_name': k,
                'type_id': r,
            })
        videos=[]
        for i in ldata.items():
            j = i('.public-list-exp')
            k=i('.public-list-button')
            videos.append({
                'vod_id': j.attr('href').split('/')[-1].split('-')[0],
                'vod_name': k('.time-title').text(),
                'vod_pic': j('img').attr('data-src'),
                'vod_year': f"·{j('.public-list-prb').text()}",
                'vod_remarks': k('.public-list-subtitle').text(),
            })
        result['class'] = classes
        result['list']=videos
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        body = {'type':tid,'class':'','area':'','lang':'','version':'','state':'','letter':'','page':pg}
        data = self.post(f"{self.host}/index.php/api/vod", headers=self.headers, data=self.getbody(body)).json()
        result = {}
        result['list'] = data['list']
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        data = self.getpq(self.fetch(f"{self.host}/play/{ids[0]}-1-1.html", headers=self.headers).text)
        v=data('.player-info-text .this-text')
        vod = {
            'type_name': v.eq(-1)('a').text(),
            'vod_year': v.eq(1)('a').text(),
            'vod_remarks': v.eq(0).text(),
            'vod_actor': v.eq(2)('a').text(),
            'vod_content': data('.player-content').text()
        }
        ns=data('.swiper-wrapper .vod-playerUrl')
        ps=data('.player-list-box .anthology-list-box ul')
        play,names=[],[]
        for i in range(len(ns)):
            n=ns.eq(i)('a')
            n('span').remove()
            names.append(re.sub(r"[\ue679\xa0]", "", n.text()))
            play.append('#'.join([f"{v.text()}${v('a').attr('href')}" for v in ps.eq(i)('li').items()]))
        vod["vod_play_from"] = "$$$".join(names)
        vod["vod_play_url"] = "$$$".join(play)
        result = {"list": [vod]}
        return result

    def searchContent(self, key, quick, pg="1"):
        data = self.fetch(f"{self.host}/index.php/ajax/suggest?mid=1&wd={key}&limit=9999&timestamp={int(time.time()*1000)}", headers=self.headers).json()
        videos=[]
        for i in data['list']:
            videos.append({
                'vod_id': i['id'],
                'vod_name': i['name'],
                'vod_pic': i['pic']
            })
        return {'list':videos,'page':pg}

    def playerContent(self, flag, id, vipFlags):
        p,url1= 1,''
        yurl=f"{self.host}{id}"
        data = self.getpq(self.fetch(yurl, headers=self.headers).text)
        dmhtm=data('.ds-log-set')
        dmdata={'vod_id':dmhtm.attr('data-id'),'vod_ep':dmhtm.attr('data-nid')}
        try:
            jstr = data('.player-top.box.radius script').eq(0).text()
            jsdata = json.loads(jstr.split('=',1)[-1])
            url1= jsdata['url']
            data = self.fetch(f"{self.host}/player/?url={unquote(self.d64(jsdata['url']))}", headers=self.headers).text
            data=self.p_qjs(self.getjstr(data))
            url=data['qualities'] if len(data['qualities']) else data['url']
            p = 0
            if not url:raise Exception("未找到播放地址")
        except Exception as e:
            self.log(e)
            url = yurl
            if re.search(r'\.m3u8|\.mp4',url1):url=url1
        dmurl = f"{self.getProxyUrl()}&data={self.e64(json.dumps(dmdata))}&type=dm.xml"
        return {"parse": p, "url": url, "header": {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'},'danmaku':dmurl}

    def localProxy(self, param):
        try:
            data = json.loads(self.d64(param['data']))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'origin': self.host,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            params = {'vod_id': data['vod_id'], 'vod_ep': data['vod_ep']}
            res = self.post(f"https://app.wuyaoy.cn/danmu/api.php/getDanmu", headers=headers, data=params).json()
            danmustr = f'<?xml version="1.0" encoding="UTF-8"?>\n<i>\n\t<chatserver>chat.aowudm.com</chatserver>\n\t<chatid>88888888</chatid>\n\t<mission>0</mission>\n\t<maxlimit>99999</maxlimit>\n\t<state>0</state>\n\t<real_name>0</real_name>\n\t<source>k-v</source>\n'
            my_list = ['1', '4', '5', '6']
            for i in sorted(res['data'], key=lambda x: x['time']):
                dms = [str(i.get('time',1)), random.choice(my_list), '25', self.get_color(), '0']
                dmtxt = re.sub(r'[<>&\u0000\b]', '', self.cleanText(i.get('text', '')))
                tempdata = f'\t<d p="{",".join(dms)}">{dmtxt}</d>\n'
                danmustr += tempdata
            danmustr += '</i>'
            return [200,'text/xml',danmustr]
        except Exception as e:
            print(f"获取弹幕失败：{str(e)}")
            return ""

    def getbody(self, params):
        t=int(time.time())
        h = MD5.new()
        h.update(f"DS{t}DCC147D11943AF75".encode('utf-8'))
        key=h.hexdigest()
        params.update({'time':t,'key':key})
        return params

    def getpq(self, data):
        data=self.cleanText(data)
        try:
            return pq(data)
        except Exception as e:
            print(f"{str(e)}")
            return pq(data.encode('utf-8'))

    def get_color(self):
        h = random.random()
        s = random.uniform(0.7, 1.0)
        v = random.uniform(0.8, 1.0)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        decimal_color = (r << 16) + (g << 8) + b
        return str(decimal_color)

    def getjstr(self, data):
        pattern = r'new\s+Artplayer\s*\((\{[\s\S]*?\})\);'
        match = re.search(pattern, data)
        config_str = match.group(1) if match else '{}'

        replacements = [
            (r'contextmenu\s*:\s*\[[\s\S]*?\{[\s\S]*?\}[\s\S]*?\],', 'contextmenu: [],'),
            (r'customType\s*:\s*\{[\s\S]*?\},', 'customType: {},'),
            (r'plugins\s*:\s*\[\s*artplayerPluginDanmuku\(\{[\s\S]*?lockTime:\s*\d+,?\s*\}\)\,?\s*\]', 'plugins: []')
        ]
        for pattern, replacement in replacements:
            config_str = re.sub(pattern, replacement, config_str)
        return config_str

    def p_qjs(self, config_str):
        try:
            from com.whl.quickjs.wrapper import QuickJSContext
            ctx = QuickJSContext.create()
            js_code = f"""
            function extractVideoInfo() {{
                try {{
                    const config = {config_str};
                    const result = {{
                        url: "",
                        qualities: []
                    }};
                    if (config.url) {{
                        result.url = config.url;
                    }}
                    if (config.quality && Array.isArray(config.quality)) {{
                        config.quality.forEach(function(q) {{
                            if (q && q.url) {{
                                result.qualities.push(q.html || "嗷呜");
                                result.qualities.push(q.url);
                            }}
                        }});
                    }}

                    return JSON.stringify(result);
                }} catch (e) {{
                    return JSON.stringify({{
                        error: "解析错误: " + e.message,
                        url: "",
                        qualities: []
                    }});
                }}
            }}
            extractVideoInfo();
            """
            result_json = ctx.evaluate(js_code)
            ctx.destroy()
            return json.loads(result_json)

        except Exception as e:
            self.log(f"执行失败: {e}")
            return {
                "error": str(e),
                "url": "",
                "qualities": []
            }

    def e64(self, text):
        try:
            text_bytes = text.encode('utf-8')
            encoded_bytes = b64encode(text_bytes)
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            return ""

    def d64(self,encoded_text):
        try:
            encoded_bytes = encoded_text.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            return ""


