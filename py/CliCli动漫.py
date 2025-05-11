# -*- coding: utf-8 -*-
# by @嗷呜
import base64
import json
import sys
import time
from base64 import b64decode, b64encode
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad, pad
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def init(self, extend=""):
        self.did=self.getdid()
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    host='http://60.204.242.79:8091'

    def homeContent(self, filter):
        res = self.fetch(f'{self.host}/app/channel?top-level=true', headers=self.getheaders()).text
        data = self.getdata(res)
        result = {}
        classes = []
        filters = {}
        sortsn = ['最新','最热','高分']
        for k in data['data']:
            classes.append({
                'type_name': k['name'],
                'type_id': k['id']
            })
            filters[k['id']] = []
            k['sorts']=['addtime','hits','gold']
            for key,value in k.items():
                if type(value) == list:
                    filters[k['id']].append({
                        'name': key,
                        'key': key,
                        'value': [{'v': x,'n': x if key !='sorts' else sortsn[i]} for i,x in enumerate(value) if x]
                    })
        result['class'] = classes
        result['filters'] = filters
        return result

    def homeVideoContent(self):
        res=self.fetch(f'{self.host}/app/banners/0',headers=self.getheaders()).text
        data=self.getdata(res)
        videos=[]
        for i in data['data']:
            videos.append({
                'vod_id': i['vid'],
                'vod_name': i['vname'],
                'vod_pic': i['img'],
                'vod_remarks': i['continu']
            })
        return {'list':videos}

    def categoryContent(self, tid, pg, filter, extend):
        params={'channel':tid,'type':extend.get('types',''),'area':extend.get('areas',''),'year':extend.get('years',''),'sort':extend.get('sorts','addtime'),'limit':'30','page':pg}
        data=self.fetch(f'{self.host}/app/video/list',params=params,headers=self.getheaders()).text
        data=self.getdata(data)
        videos=[]
        for i in data['data']['items']:
            videos.append({
                'vod_id': i.get('id'),
                'vod_name': i.get('name'),
                'vod_pic': i.get('pic'),
                'vod_year': i.get('year'),
                'vod_remarks': i.get('continu')
            })
        result = {}
        result['list'] = videos
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        return result

    def detailContent(self, ids):
        data=self.fetch(f'{self.host}/app/video/detail?id={ids[0]}',headers=self.getheaders()).text
        data=self.getdata(data)
        v=data['data']
        vod = {
            'type_name': v.get('type'),
            'vod_year': v.get('year'),
            'vod_area': v.get('area'),
            'vod_remarks': v.get('continu'),
            'vod_actor': v.get('actor'),
            'vod_director': v.get('director'),
            'vod_content': v.get('content'),
            'vod_play_from': '',
            'vod_play_url': ''
        }
        parts,names = [],[]
        for i in v['parts']:
            names.append(i['play_zh'])
            p=[]
            for j,x in enumerate(i['part']):
                params={'id':ids[0],'play':i['play'],'part':x}
                p.append(f'{x}${self.e64(json.dumps(params))}')
            parts.append('#'.join(p))
        vod['vod_play_from'] = '$$$'.join(names)
        vod['vod_play_url'] = '$$$'.join(parts)
        return {'list':[vod]}

    def searchContent(self, key, quick, pg="1"):
        params={'key':key,'limit':'25','page':pg}
        data=self.fetch(f'{self.host}/app/video/search',params=params,headers=self.getheaders()).text
        data=self.getdata(data)
        videos = []
        for i in data['data']['items']:
            videos.append({
                'vod_id': i.get('id'),
                'vod_name': i.get('name'),
                'vod_pic': i.get('pic'),
                'vod_year': i.get('year'),
                'vod_remarks': i.get('continu')
            })
        return {'list':videos,'page':pg}

    def playerContent(self, flag, id, vipFlags):
        params= json.loads(self.d64(id))
        data=self.fetch(f'{self.host}/app/video/play',params=params,headers=self.getheaders()).text
        data=self.getdata(data)
        urls=[]
        for i in data['data']:
            if i.get('url'):urls.extend([i['resolution'],i['url']])
        return  {'parse': 0, 'url': urls, 'header': {'User-Agent': 'Dart/3.6 (dart:io)'}}

    def liveContent(self, url):
        pass

    def localProxy(self, param):
        pass

    def getheaders(self):
        t=str(int(time.time() * 1000))
        stinf=f"3.0.0.2-{t}-Android-1.0.4.5-{self.did}"
        authentication=self.aes_encrypt(self.e64(stinf))
        headers = {
            'User-Agent': 'Dart/3.6 (dart:io)',
            'x-version': '2020-09-17',
            'appid': '4150439554430614',
            'ts': t,
            'authentication': authentication,
            'content-type': 'application/json; charset=utf-8',
        }
        return headers

    def aes_encrypt(self, text):
        key = b'ziISjqkXPsGUMRNGyWigxDGtJbfTdcGv'
        iv = b'WonrnVkxeIxDcFbv'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(text.encode("utf-8"), AES.block_size))
        ct = b64encode(ct_bytes).decode("utf-8")
        return ct

    def aes_decrypt(self, key,text):
        iv=key[::-1].encode("utf-8")
        key=key.encode("utf-8")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(b64decode(text)), AES.block_size)
        return json.loads(pt.decode("utf-8"))

    def rsa_decrypt(self, encrypted_data):
        try:
            private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
            MIIEpAIBAAKCAQEA5xpfniKIMYdjTytUBu5rsLbMtcCRW9B9DB78QEdf4wW5jO8r
            Mw7j+/mYk3ghi0xrxpjtHm1R2KgNT1b0akJCExTH7gBVcjVywpmXdNXbcuCGfVCK
            S6vYfMypmj5lNBgalCHe5AVc0ghhP3FG5j8Q5B7q00+tk4nT9nFsTmTeNcAKSH9h
            aM6a0fbiJ3eXbxEr2o8raAjck10act35t/MIUOkcrQjHx5E9Yvqgs3qbq4yDakaG
            4qfMAV4DAkkmdZ8N3fdEQ+rFJ67Spd4zzowj81+YO9wMUP2hNgfXmLOGLS5Lyi+x
            vrwwWZXAIRUkhdQEAYQlhGs8wV9P4bJnTzplewIDAQABAoIBAEnRzNUwZpybiIdT
            acXFBrUtzvoHhubzE955T04g/mn//CMeiogGq6BjO+9vIhfi01Jequ9bMBeqpoW/
            WtdOTtjVfH9zr9eJZxzt/skdPrnVKmCBB4vgWoiSv2I7qAwZ3vOOVioz5FBayOWB
            A4qsfnK/xXa2LtW/4usHk/b+lVRJZhHl3eKio2CnVBrgRb2DTx1GAwpvaRXp0oHm
            LXDEtngxN4/rh2irPKgaG/lgrCBISKUHtwtgytcpltsHMASMXIKAjZjNgCA98fA3
            te96U58wGHzQBQ5XtwTf0PiFEfJ7yOhgNRgCtiwsjGOhJFJFiiXYKzTef1GnVxPa
            wuPc0TECgYEA+KCts3ArkWLqWbi4bVDpekP71geEnQIklSAk3RRZ0eiC1pmmkuTh
            +q/4jOfoQHGuYCc8GvJqxQ8Y+aspPptbsAeRMSVovjQUvpRMqD0SWT8o3W2xGfqd
            0W4p14CIF7oXjMqQVeY468AYzxUdNsaulrp9Wnpa5njzE5D5WGDu0IcCgYEA7fSq
            kvz1oXjlljlskBwJ8gDB8j53PhuqV6Ori71G/qIGpYuOVjHSfPD/04a9T3M9olpk
            vlLOLn7GS7xa4pjugmp0EDdxBIJJtTHbbi4NL4ZoYg+vHkiemkjGLis4x5qRKjg6
            jNUEhnpksm68IUMSyO2toasfR0nVUmkb+ylKhG0CgYEAqNDZAJSyUHZcb21YdIlS
            7rzIe2wBZGZ3FnaL8T0HO9rnM/WCQA1/Tys61doFPfSylQEu85EUZBc7OxM33xW3
            7M9Gi5s+Ap/0Ue76GeXV1plnEuqPLPeZPwHREU1pmsq1gNhtppW6ooB9l+ZbPr0r
            AJdB1DRuEj2ftvJiC9tNbHMCgYEAvHaliply6hrYq6x7gX/TmKpk8bnrs3Mx7Qui
            WKDm09H8Na1cZIQ9U9uEo0H6OizpyeaSF/N5fXXHFEDwMrwxW3V4y0c96fZO7oW4
            Z4FtzBBGKDSH3BJkG4o7/GEbLWwMQUYbiWNFnETf8DqoIif/fshQVtUzhsDBhe3d
            zYUckdkCgYAJlTYhJz0qXcO8a5KsQ20/hEGRtOcq+mfPOdGYBOv6LB2ThuDKunbY
            WsmAvqSo1qoJONnhQVMSpzKWEjCYV6hcifV9aeFofD4kNmG1gWC18QIYfrihLyOU
            E4GDW7QN8HO2YiQpopGP/muKsIlCmxKP6DasgCCO36xs87Wi8gu1DA==
            -----END RSA PRIVATE KEY-----'''
            private_key = RSA.import_key(private_key_string)
            cipher = PKCS1_v1_5.new(private_key)
            encrypted_bytes = base64.b64decode(encrypted_data)
            decrypted_bytes = cipher.decrypt(encrypted_bytes, None)
            return decrypted_bytes.decode('utf-8')
        except:
            return ""

    def getdata(self, data):
        ds=data.split('.')
        key=self.rsa_decrypt(ds[0])
        result=self.aes_decrypt(key,ds[1])
        return result

    def getdid(self):
        did=self.getCache('did')
        if not did:
            t = str(int(time.time()))
            did = self.md5(t)
            self.setCache('did', did)
        return did

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

    def md5(self, text):
        h = MD5.new()
        h.update(text.encode('utf-8'))
        return h.hexdigest()

