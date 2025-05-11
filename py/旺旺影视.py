# -*- coding: utf-8 -*-
# by @嗷呜
import concurrent.futures
import json
import re
import sys
import time
from base64 import b64decode, b64encode
import requests
from pyquery import PyQuery as pq
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def init(self, extend=""):
        self.host = self.gethost()
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="130", "Google Chrome";v="130"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?1',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Dest': 'video',
        'Sec-Fetch-Storage-Access': 'active',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }

    config ={"1": [{"key": "cateId","name": "类型","value": [{"n": "全部","v": "1"},{"n": "动作片","v": "5"},{"n": "喜剧片","v": "6"},{"n": "爱情片","v": "7"},{"n": "科幻片","v": "8"},{"n": "恐怖片","v": "9"},{"n": "剧情片","v": "10"},{"n": "战争片","v": "11"},{"n": "惊悚片","v": "16"},{"n": "奇幻片","v": "17"}]},{"key": "area","name": "地区","value": [{"n": "全部","v": ""},{"n": "大陆","v": "大陆"},{"n": "香港","v": "香港"},{"n": "台湾","v": "台湾"},{"n": "美国","v": "美国"},{"n": "韩国","v": "韩国"},{"n": "日本","v": "日本"},{"n": "泰国","v": "泰国"},{"n": "新加坡","v": "新加坡"},{"n": "马来西亚","v": "马来西亚"},{"n": "印度","v": "印度"},{"n": "英国","v": "英国"},{"n": "法国","v": "法国"},{"n": "加拿大","v": "加拿大"},{"n": "西班牙","v": "西班牙"},{"n": "俄罗斯","v": "俄罗斯"},{"n": "其它","v": "其它"}]},{"key": "year","name": "时间","value": [{"n": "全部","v": ""},{"n": "2024","v": "2024"},{"n": "2023","v": "2023"},{"n": "2022","v": "2022"},{"n": "2021","v": "2021"},{"n": "2020","v": "2020"},{"n": "2019","v": "2019"},{"n": "2018","v": "2018"},{"n": "2017","v": "2017"},{"n": "2016","v": "2016"},{"n": "2015","v": "2015"},{"n": "2014","v": "2014"},{"n": "2013","v": "2013"},{"n": "2012","v": "2012"},{"n": "2011","v": "2011"},{"n": "2010","v": "2010"},{"n": "2009","v": "2009"},{"n": "2008","v": "2008"},{"n": "2007","v": "2007"},{"n": "2006","v": "2006"},{"n": "2005","v": "2005"},{"n": "2004","v": "2004"},{"n": "2003","v": "2003"},{"n": "2002","v": "2002"},{"n": "2001","v": "2001"},{"n": "2000","v": "2000"},{"n": "1999","v": "1999"},{"n": "1998","v": "1998"},{"n": "1997","v": "1997"},{"n": "1996","v": "1996"},{"n": "1995","v": "1995"},{"n": "1994","v": "1994"},{"n": "1993","v": "1993"},{"n": "1992","v": "1992"},{"n": "1991","v": "1991"},{"n": "1990","v": "1990"},{"n": "1989","v": "1989"},{"n": "1988","v": "1988"},{"n": "1987","v": "1987"},{"n": "1986","v": "1986"},{"n": "1985","v": "1985"},{"n": "1984","v": "1984"},{"n": "1983","v": "1983"},{"n": "1982","v": "1982"},{"n": "1981","v": "1981"},{"n": "1980","v": "1980"},{"n": "1979","v": "1979"},{"n": "1978","v": "1978"},{"n": "1977","v": "1977"},{"n": "1976","v": "1976"},{"n": "1975","v": "1975"},{"n": "1974","v": "1974"},{"n": "1973","v": "1973"},{"n": "1972","v": "1972"},{"n": "1971","v": "1971"},{"n": "1970","v": "1970"},{"n": "1969","v": "1969"},{"n": "1968","v": "1968"},{"n": "1967","v": "1967"},{"n": "1966","v": "1966"},{"n": "1965","v": "1965"},{"n": "1964","v": "1964"},{"n": "1963","v": "1963"},{"n": "1962","v": "1962"},{"n": "1961","v": "1961"},{"n": "1960","v": "1960"},{"n": "1959","v": "1959"},{"n": "1958","v": "1958"},{"n": "1957","v": "1957"},{"n": "1956","v": "1956"},{"n": "1955","v": "1955"},{"n": "1954","v": "1954"},{"n": "1953","v": "1953"},{"n": "1952","v": "1952"},{"n": "1951","v": "1951"},{"n": "1950","v": "1950"},{"n": "1949","v": "1949"},{"n": "1948","v": "1948"},{"n": "1947","v": "1947"},{"n": "1946","v": "1946"},{"n": "1945","v": "1945"},{"n": "1944","v": "1944"},{"n": "1943","v": "1943"},{"n": "1942","v": "1942"},{"n": "1941","v": "1941"},{"n": "1940","v": "1940"},{"n": "1939","v": "1939"},{"n": "1938","v": "1938"},{"n": "1937","v": "1937"},{"n": "1936","v": "1936"},{"n": "1935","v": "1935"},{"n": "1934","v": "1934"},{"n": "1933","v": "1933"},{"n": "1932","v": "1932"},{"n": "1931","v": "1931"},{"n": "1930","v": "1930"},{"n": "1929","v": "1929"},{"n": "1928","v": "1928"},{"n": "1927","v": "1927"},{"n": "1926","v": "1926"},{"n": "1925","v": "1925"},{"n": "1924","v": "1924"},{"n": "1923","v": "1923"},{"n": "1922","v": "1922"},{"n": "1921","v": "1921"},{"n": "1920","v": "1920"},{"n": "1919","v": "1919"},{"n": "1918","v": "1918"},{"n": "1917","v": "1917"},{"n": "1916","v": "1916"},{"n": "1915","v": "1915"},{"n": "1914","v": "1914"}]},{"key": "letter","name": "字母","value": [{"n": "全部","v": ""},{"n": "A","v": "A"},{"n": "B","v": "B"},{"n": "C","v": "C"},{"n": "D","v": "D"},{"n": "E","v": "E"},{"n": "F","v": "F"},{"n": "G","v": "G"},{"n": "H","v": "H"},{"n": "I","v": "I"},{"n": "J","v": "J"},{"n": "K","v": "K"},{"n": "L","v": "L"},{"n": "M","v": "M"},{"n": "N","v": "N"},{"n": "O","v": "O"},{"n": "P","v": "P"},{"n": "Q","v": "Q"},{"n": "R","v": "R"},{"n": "S","v": "S"},{"n": "T","v": "T"},{"n": "U","v": "U"},{"n": "V","v": "V"},{"n": "W","v": "W"},{"n": "X","v": "X"},{"n": "Y","v": "Y"},{"n": "Z","v": "Z"},{"n": "0-9","v": "0-9"}]},{"key": "by","name": "排序","value": [{"n": "全部","v": ""},{"n": "时间","v": "time"},{"n": "人气","v": "hits"},{"n": "评分","v": "score"}]}],"2": [{"key": "cateId","name": "类型","value": [{"n": "全部","v": "2"},{"n": "国产剧","v": "12"},{"n": "港台泰","v": "13"},{"n": "日韩剧","v": "14"},{"n": "欧美剧","v": "15"}]},{"key": "area","name": "地区","value": [{"n": "全部","v": ""},{"n": "大陆","v": "大陆"},{"n": "香港","v": "香港"},{"n": "台湾","v": "台湾"},{"n": "美国","v": "美国"},{"n": "韩国","v": "韩国"},{"n": "日本","v": "日本"},{"n": "泰国","v": "泰国"},{"n": "新加坡","v": "新加坡"},{"n": "马来西亚","v": "马来西亚"},{"n": "印度","v": "印度"},{"n": "英国","v": "英国"},{"n": "法国","v": "法国"},{"n": "加拿大","v": "加拿大"},{"n": "西班牙","v": "西班牙"},{"n": "俄罗斯","v": "俄罗斯"},{"n": "其它","v": "其它"}]},{"key": "year","name": "时间","value": [{"n": "全部","v": ""},{"n": "2024","v": "2024"},{"n": "2023","v": "2023"},{"n": "2022","v": "2022"},{"n": "2021","v": "2021"},{"n": "2020","v": "2020"},{"n": "2019","v": "2019"},{"n": "2018","v": "2018"},{"n": "2017","v": "2017"},{"n": "2016","v": "2016"},{"n": "2015","v": "2015"},{"n": "2014","v": "2014"},{"n": "2013","v": "2013"},{"n": "2012","v": "2012"},{"n": "2011","v": "2011"},{"n": "2010","v": "2010"},{"n": "2009","v": "2009"},{"n": "2008","v": "2008"},{"n": "2007","v": "2007"},{"n": "2006","v": "2006"},{"n": "2005","v": "2005"},{"n": "2004","v": "2004"},{"n": "2003","v": "2003"},{"n": "2002","v": "2002"},{"n": "2001","v": "2001"},{"n": "2000","v": "2000"},{"n": "1999","v": "1999"},{"n": "1998","v": "1998"},{"n": "1997","v": "1997"},{"n": "1996","v": "1996"},{"n": "1995","v": "1995"},{"n": "1994","v": "1994"},{"n": "1993","v": "1993"},{"n": "1992","v": "1992"},{"n": "1991","v": "1991"},{"n": "1990","v": "1990"},{"n": "1989","v": "1989"},{"n": "1988","v": "1988"},{"n": "1987","v": "1987"},{"n": "1986","v": "1986"},{"n": "1985","v": "1985"},{"n": "1984","v": "1984"},{"n": "1983","v": "1983"},{"n": "1982","v": "1982"},{"n": "1981","v": "1981"},{"n": "1980","v": "1980"},{"n": "1979","v": "1979"},{"n": "1978","v": "1978"},{"n": "1977","v": "1977"},{"n": "1976","v": "1976"},{"n": "1975","v": "1975"},{"n": "1974","v": "1974"},{"n": "1973","v": "1973"},{"n": "1972","v": "1972"},{"n": "1971","v": "1971"},{"n": "1970","v": "1970"},{"n": "1969","v": "1969"},{"n": "1968","v": "1968"},{"n": "1967","v": "1967"},{"n": "1966","v": "1966"},{"n": "1965","v": "1965"},{"n": "1964","v": "1964"},{"n": "1963","v": "1963"},{"n": "1962","v": "1962"},{"n": "1961","v": "1961"},{"n": "1960","v": "1960"}]},{"key": "letter","name": "字母","value": [{"n": "全部","v": ""},{"n": "A","v": "A"},{"n": "B","v": "B"},{"n": "C","v": "C"},{"n": "D","v": "D"},{"n": "E","v": "E"},{"n": "F","v": "F"},{"n": "G","v": "G"},{"n": "H","v": "H"},{"n": "I","v": "I"},{"n": "J","v": "J"},{"n": "K","v": "K"},{"n": "L","v": "L"},{"n": "M","v": "M"},{"n": "N","v": "N"},{"n": "O","v": "O"},{"n": "P","v": "P"},{"n": "Q","v": "Q"},{"n": "R","v": "R"},{"n": "S","v": "S"},{"n": "T","v": "T"},{"n": "U","v": "U"},{"n": "V","v": "V"},{"n": "W","v": "W"},{"n": "X","v": "X"},{"n": "Y","v": "Y"},{"n": "Z","v": "Z"},{"n": "0-9","v": "0-9"}]},{"key": "by","name": "排序","value": [{"n": "全部","v": ""},{"n": "时间","v": "time"},{"n": "人气","v": "hits"},{"n": "评分","v": "score"}]}],"3": [{"key": "area","name": "地区","value": [{"n": "全部","v": ""},{"n": "大陆","v": "大陆"},{"n": "香港","v": "香港"},{"n": "台湾","v": "台湾"},{"n": "美国","v": "美国"},{"n": "韩国","v": "韩国"},{"n": "日本","v": "日本"},{"n": "泰国","v": "泰国"},{"n": "新加坡","v": "新加坡"},{"n": "马来西亚","v": "马来西亚"},{"n": "印度","v": "印度"},{"n": "英国","v": "英国"},{"n": "法国","v": "法国"},{"n": "加拿大","v": "加拿大"},{"n": "西班牙","v": "西班牙"},{"n": "俄罗斯","v": "俄罗斯"},{"n": "其它","v": "其它"}]},{"key": "year","name": "时间","value": [{"n": "全部","v": ""},{"n": "2024","v": "2024"},{"n": "2023","v": "2023"},{"n": "2022","v": "2022"},{"n": "2021","v": "2021"},{"n": "2020","v": "2020"},{"n": "2019","v": "2019"},{"n": "2018","v": "2018"},{"n": "2017","v": "2017"},{"n": "2016","v": "2016"},{"n": "2015","v": "2015"},{"n": "2014","v": "2014"},{"n": "2013","v": "2013"},{"n": "2012","v": "2012"},{"n": "2011","v": "2011"},{"n": "2010","v": "2010"},{"n": "2009","v": "2009"},{"n": "2008","v": "2008"},{"n": "2007","v": "2007"},{"n": "2006","v": "2006"},{"n": "2005","v": "2005"},{"n": "2004","v": "2004"},{"n": "2003","v": "2003"},{"n": "2002","v": "2002"},{"n": "2001","v": "2001"},{"n": "2000","v": "2000"},{"n": "1999","v": "1999"},{"n": "1998","v": "1998"},{"n": "1997","v": "1997"},{"n": "1996","v": "1996"},{"n": "1995","v": "1995"},{"n": "1994","v": "1994"},{"n": "1993","v": "1993"},{"n": "1992","v": "1992"},{"n": "1991","v": "1991"},{"n": "1990","v": "1990"},{"n": "1989","v": "1989"},{"n": "1988","v": "1988"},{"n": "1987","v": "1987"},{"n": "1986","v": "1986"},{"n": "1985","v": "1985"},{"n": "1984","v": "1984"},{"n": "1983","v": "1983"}]},{"key": "letter","name": "字母","value": [{"n": "全部","v": ""},{"n": "A","v": "A"},{"n": "B","v": "B"},{"n": "C","v": "C"},{"n": "D","v": "D"},{"n": "E","v": "E"},{"n": "F","v": "F"},{"n": "G","v": "G"},{"n": "H","v": "H"},{"n": "I","v": "I"},{"n": "J","v": "J"},{"n": "K","v": "K"},{"n": "L","v": "L"},{"n": "M","v": "M"},{"n": "N","v": "N"},{"n": "O","v": "O"},{"n": "P","v": "P"},{"n": "Q","v": "Q"},{"n": "R","v": "R"},{"n": "S","v": "S"},{"n": "T","v": "T"},{"n": "U","v": "U"},{"n": "V","v": "V"},{"n": "W","v": "W"},{"n": "X","v": "X"},{"n": "Y","v": "Y"},{"n": "Z","v": "Z"},{"n": "0-9","v": "0-9"}]},{"key": "by","name": "排序","value": [{"n": "全部","v": ""},{"n": "时间","v": "time"},{"n": "人气","v": "hits"},{"n": "评分","v": "score"}]}],"4": [{"key": "cateId","name": "类型","value": [{"n": "全部","v": "4"},{"n": "动漫剧","v": "18"},{"n": "动漫片","v": "19"}]},{"key": "area","name": "地区","value": [{"n": "全部","v": ""},{"n": "大陆","v": "大陆"},{"n": "香港","v": "香港"},{"n": "台湾","v": "台湾"},{"n": "美国","v": "美国"},{"n": "韩国","v": "韩国"},{"n": "日本","v": "日本"},{"n": "泰国","v": "泰国"},{"n": "新加坡","v": "新加坡"},{"n": "马来西亚","v": "马来西亚"},{"n": "印度","v": "印度"},{"n": "英国","v": "英国"},{"n": "法国","v": "法国"},{"n": "加拿大","v": "加拿大"},{"n": "西班牙","v": "西班牙"},{"n": "俄罗斯","v": "俄罗斯"},{"n": "其它","v": "其它"}]},{"key": "year","name": "时间","value": [{"n": "全部","v": ""},{"n": "2024","v": "2024"},{"n": "2023","v": "2023"},{"n": "2022","v": "2022"},{"n": "2021","v": "2021"},{"n": "2020","v": "2020"},{"n": "2019","v": "2019"},{"n": "2018","v": "2018"},{"n": "2017","v": "2017"},{"n": "2016","v": "2016"},{"n": "2015","v": "2015"},{"n": "2014","v": "2014"},{"n": "2013","v": "2013"},{"n": "2012","v": "2012"},{"n": "2011","v": "2011"},{"n": "2010","v": "2010"},{"n": "2009","v": "2009"},{"n": "2008","v": "2008"},{"n": "2007","v": "2007"},{"n": "2006","v": "2006"},{"n": "2005","v": "2005"},{"n": "2004","v": "2004"},{"n": "2003","v": "2003"},{"n": "2002","v": "2002"},{"n": "2001","v": "2001"},{"n": "2000","v": "2000"},{"n": "1999","v": "1999"},{"n": "1998","v": "1998"},{"n": "1997","v": "1997"},{"n": "1996","v": "1996"},{"n": "1995","v": "1995"},{"n": "1994","v": "1994"},{"n": "1993","v": "1993"},{"n": "1992","v": "1992"},{"n": "1991","v": "1991"},{"n": "1990","v": "1990"},{"n": "1989","v": "1989"},{"n": "1988","v": "1988"},{"n": "1987","v": "1987"},{"n": "1986","v": "1986"},{"n": "1985","v": "1985"},{"n": "1984","v": "1984"},{"n": "1983","v": "1983"},{"n": "1982","v": "1982"},{"n": "1981","v": "1981"},{"n": "1980","v": "1980"},{"n": "1979","v": "1979"},{"n": "1978","v": "1978"},{"n": "1977","v": "1977"},{"n": "1976","v": "1976"},{"n": "1975","v": "1975"},{"n": "1974","v": "1974"},{"n": "1973","v": "1973"},{"n": "1972","v": "1972"},{"n": "1971","v": "1971"},{"n": "1970","v": "1970"},{"n": "1969","v": "1969"},{"n": "1968","v": "1968"},{"n": "1967","v": "1967"}]},{"key": "letter","name": "字母","value": [{"n": "全部","v": ""},{"n": "A","v": "A"},{"n": "B","v": "B"},{"n": "C","v": "C"},{"n": "D","v": "D"},{"n": "E","v": "E"},{"n": "F","v": "F"},{"n": "G","v": "G"},{"n": "H","v": "H"},{"n": "I","v": "I"},{"n": "J","v": "J"},{"n": "K","v": "K"},{"n": "L","v": "L"},{"n": "M","v": "M"},{"n": "N","v": "N"},{"n": "O","v": "O"},{"n": "P","v": "P"},{"n": "Q","v": "Q"},{"n": "R","v": "R"},{"n": "S","v": "S"},{"n": "T","v": "T"},{"n": "U","v": "U"},{"n": "V","v": "V"},{"n": "W","v": "W"},{"n": "X","v": "X"},{"n": "Y","v": "Y"},{"n": "Z","v": "Z"},{"n": "0-9","v": "0-9"}]},{"key": "by","name": "排序","value": [{"n": "全部","v": ""},{"n": "时间","v": "time"},{"n": "人气","v": "hits"},{"n": "评分","v": "score"}]}],"26": [{"key": "area","name": "地区","value": [{"n": "全部","v": ""},{"n": "大陆","v": "大陆"},{"n": "香港","v": "香港"},{"n": "台湾","v": "台湾"},{"n": "美国","v": "美国"},{"n": "韩国","v": "韩国"},{"n": "日本","v": "日本"},{"n": "泰国","v": "泰国"},{"n": "新加坡","v": "新加坡"},{"n": "马来西亚","v": "马来西亚"},{"n": "印度","v": "印度"},{"n": "英国","v": "英国"},{"n": "法国","v": "法国"},{"n": "加拿大","v": "加拿大"},{"n": "西班牙","v": "西班牙"},{"n": "俄罗斯","v": "俄罗斯"},{"n": "其它","v": "其它"}]},{"key": "year","name": "时间","value": [{"n": "全部","v": ""},{"n": "2024","v": "2024"},{"n": "2023","v": "2023"},{"n": "2022","v": "2022"},{"n": "2021","v": "2021"},{"n": "2020","v": "2020"}]},{"key": "letter","name": "字母","value": [{"n": "全部","v": ""},{"n": "A","v": "A"},{"n": "B","v": "B"},{"n": "C","v": "C"},{"n": "D","v": "D"},{"n": "E","v": "E"},{"n": "F","v": "F"},{"n": "G","v": "G"},{"n": "H","v": "H"},{"n": "I","v": "I"},{"n": "J","v": "J"},{"n": "K","v": "K"},{"n": "L","v": "L"},{"n": "M","v": "M"},{"n": "N","v": "N"},{"n": "O","v": "O"},{"n": "P","v": "P"},{"n": "Q","v": "Q"},{"n": "R","v": "R"},{"n": "S","v": "S"},{"n": "T","v": "T"},{"n": "U","v": "U"},{"n": "V","v": "V"},{"n": "W","v": "W"},{"n": "X","v": "X"},{"n": "Y","v": "Y"},{"n": "Z","v": "Z"},{"n": "0-9","v": "0-9"}]},{"key": "by","name": "排序","value": [{"n": "全部","v": ""},{"n": "时间","v": "time"},{"n": "人气","v": "hits"},{"n": "评分","v": "score"}]}]}

    def homeContent(self, filter):
        data = self.getpq()
        cdata = data('#topnav .swiper-wrapper li')
        result = {}
        classes = []
        videos = []
        for k in cdata.items():
            i = k('a').attr('href')
            if i and 'type' in i and '音乐' not in k.text():
                classes.append({
                    'type_name': k.text(),
                    'type_id': i.split('-')[-3],
                })
        for i in list(data('.globalPicList').items())[1:]:
            videos.extend(self.getlist(i('ul li')))
        result['class'] = classes
        result['filters'] = self.config
        result['list'] = videos
        return result

    def homeVideoContent(self):
        pass

    def categoryContent(self, tid, pg, filter, extend):
        data = self.getpq(
            f"/vod-list-id-{extend.get('cateId', tid)}-pg-{pg}-order--by-{extend.get('by', 'time')}-class-0-year-{extend.get('year', '')}-letter-{extend.get('letter', '')}-area-{extend.get('area', '')}-lang-.html")
        result = {}
        result['list'] = self.getlist(data('.globalPicList .resize_list li'))
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        data = self.getpq(ids[0])
        v = data('.numList ul li').eq(0)('a').attr('href')
        html = self.getpq(v)
        d = html('.detailPosterIntro script').eq(0).text()
        mac_from = re.search(r"mac_from='(.*?)'", d)
        mac_url = re.search(r"mac_url='(.*?)'", d).group(1)
        z = data('.page-bd')
        c = z('.desc_item')
        vod = {
            'vod_name': z('h1 a').text(),
            'vod_year': c.eq(3)('a').text(),
            'vod_remarks': c.eq(0)('font').text(),
            'vod_actor': c.eq(1)('a').text(),
            'vod_director': c.eq(2)('a').text(),
            'vod_content': data('.detail-con p').text().split('：')[-1],
            'vod_play_from': mac_from.group(1) if mac_from else '呜呜呜',
            'vod_play_url': mac_url
        }
        return {'list': [vod]}

    def searchContent(self, key, quick, pg="1"):
        data = pq(self.post(f"{self.host}/index.php?m=vod-search", data={'wd': key}, headers=self.headers).text)
        video = []
        for k in data('#data_list li').items():
            video.append({
                'vod_id': k('.pic a').attr('href'),
                'vod_name': k('.sTit').text(),
                'vod_pic': k('.pic img').attr('src'),
                'vod_year': k('.sStyle').text(),
                'vod_remarks': k('.sDes').eq(-1).text()
            })
        return {'list': video, 'page': pg}

    def playerContent(self, flag, id, vipFlags):
        try:
            if flag == '呜呜呜': raise Exception('未找到播放地址')
            jxdata = self.getpq(f"/player/{flag}.js").html()
            jxurl = re.search(r'http.*?url=', jxdata).group()
            data = self.fetch(f"{jxurl}{id}", headers=self.headers).text
            matches = re.findall(r'http.*?url=', data)
            if len(matches):
                url = []
                for i, x in enumerate(matches):
                    js = {'jx': x, 'id': id}
                    purl = f"{self.getProxyUrl()}&wdict={self.e64(json.dumps(js))}"
                    url.extend([f'线路{i + 1}', purl])
            else:
                url = re.search(r"url='(.*?)'", data).group(1)
            if not url: raise Exception('未找到播放地址')
            p = 0
        except:
            p, url = 1, id
        return {'parse': p, 'url': url, 'header': self.headers}

    def localProxy(self, param):
        wdict = json.loads(self.d64(param['wdict']))
        url = f"{wdict['jx']}{wdict['id']}"
        data = pq(self.fetch(url, headers=self.headers).text)
        html = data('script').eq(-1).text()
        url = re.search(r'src="(.*?)"', html).group(1)
        return [302, 'text/html', None, {'Location': url}]

    def liveContent(self, url):
        pass

    def gethost(self):
        data = pq(self.fetch('https://www.nmdvd.com', headers=self.headers).text)
        hlist = data('a[rel="nofollow"] b').text().split(' ')
        return self.host_late(hlist)

    def host_late(self, urls):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_url = {
                executor.submit(self.test_host, f"https://{url}"): f"https://{url}"
                for url in urls
            }
            results = {}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    results[url] = future.result()
                except Exception as e:
                    results[url] = float('inf')
        min_url = min(results.items(), key=lambda x: x[1])[0] if results else None
        if all(delay == float('inf') for delay in results.values()) or not min_url:
            return f"https://{urls[0]}"
        return min_url

    def test_host(self, url):
        try:
            start_time = time.monotonic()
            response = requests.head(
                url,
                timeout=1.0,
                allow_redirects=False,
                headers=self.headers
            )
            response.raise_for_status()
            return (time.monotonic() - start_time) * 1000
        except Exception as e:
            print(f"测试{url}失败: {str(e)}")
            return float('inf')

    def getpq(self, path=''):
        data = self.fetch(f"{self.host}{path}", headers=self.headers).text
        return pq(data)

    def getlist(self, data):
        videos = []
        for k in data.items():
            i = k('.sBottom')
            j = i('em').text()
            i.remove('em')
            videos.append({
                'vod_id': k('a').attr('href'),
                'vod_name': k('.sTit').text(),
                'vod_pic': k('.pic img').attr('src'),
                'vod_year': j,
                'vod_remarks': i.text(),
            })
        return videos

    def e64(self, text):
        try:
            text_bytes = text.encode('utf-8')
            encoded_bytes = b64encode(text_bytes)
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64编码错误: {str(e)}")
            return ""

    def d64(self, encoded_text):
        try:
            encoded_bytes = encoded_text.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64解码错误: {str(e)}")
            return ""
