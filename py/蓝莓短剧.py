# -*- coding: utf-8 -*-
import requests
import json
import time
import sys
import urllib.parse

sys.path.append('../../')
try:
    from base.spider import Spider
except ImportError:
    # 定义一个基础接口类，用于本地测试
    class Spider:
        def init(self, extend=""):
            pass

class Spider(Spider):
    def __init__(self):
        self.siteUrl = "https://app.whjzjx.cn"
        # 分类ID映射
        self.cateManual = {
            "古装": "5",
            "穿越": "17",
            "逆袭": "7",
            "重生": "6"
        }
        # 请求头
        self.headers = {
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "okhttp/4.10.0",
            "user_agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36",
            "Host": "app.whjzjx.cn",
            "Accept-Encoding": "gzip"
        }
        # token缓存
        self.token = None
        self.tokenExpireTime = 0
        
    def getName(self):
        # 返回爬虫名称
        return "蓝莓短剧"
    
    def init(self, extend=""):
        return
    
    def isVideoFormat(self, url):
        # 检查是否为视频格式
        video_formats = ['.mp4', '.m3u8', '.ts']
        for format in video_formats:
            if format in url.lower():
                return True
        return False
    
    def manualVideoCheck(self):
        # 不需要手动检查
        return False
    
    def getToken(self):
        """获取API访问Token"""
        # 如果token有效期内，直接返回
        current_time = time.time()
        if self.token and current_time < self.tokenExpireTime:
            return self.token
            
        # 否则重新获取
        try:
            tkurl = 'https://app.whjzjx.cn/v1/account/login'
            body = "device=20caaae96b3443174bf4ebdbdcc253776"
            
            response = requests.post(
                tkurl,
                headers=self.headers,
                data=body
            )
            
            if response.status_code == 200:
                json_data = response.json()
                # 修复：服务器返回的是"ok"而不是0
                if json_data.get('code') == 0 or json_data.get('code') == "ok" or json_data.get('status') == 0:
                    self.token = json_data['data']['token']
                    # 设置token过期时间为1小时
                    self.tokenExpireTime = current_time + 3600
                    return self.token
            
            print(f"获取token失败: {response.text}")
            return None
        except Exception as e:
            print(f"获取token异常: {str(e)}")
            return None
    
    def fetchWithToken(self, url, method="GET", body=None):
        """带token的网络请求"""
        token = self.getToken()
        if not token:
            print("无法获取token")
            return None
            
        headers = self.headers.copy()
        headers["authorization"] = token
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            else:  # POST
                response = requests.post(url, headers=headers, data=body, timeout=10)
                
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"请求失败: {url}, 错误: {str(e)}")
            return None
    
    def homeContent(self, filter):
        """获取首页分类及筛选"""
        result = {}
        classes = []
        
        # 添加分类
        for k in self.cateManual:
            classes.append({
                'type_id': self.cateManual[k],
                'type_name': k
            })
        
        result['class'] = classes
        
        # 获取首页推荐视频
        try:
            result['list'] = self.homeVideoContent()['list']
        except:
            result['list'] = []
            
        return result
    
    def homeVideoContent(self):
        """获取首页推荐视频内容"""
        # 使用第一个分类的内容作为首页推荐
        first_cate = list(self.cateManual.values())[0]
        result = self.categoryContent(first_cate, 1, False, None)
        # 不打印错误信息，除非列表为空
        if not result.get('list'):
            print("未获取到首页推荐视频")
        return result
    
    def categoryContent(self, tid, pg, filter, extend):
        """获取分类内容"""
        result = {}
        videos = []
        
        try:
            # 构建请求URL：分类页
            url = f"{self.siteUrl}/v1/theater/home_page?theater_class_id={tid}&page_num={int(pg)-1}&page_size=24"
            
            response = self.fetchWithToken(url)
            if not response:
                return result
                
            json_data = response.json()
            
            # 服务器正常响应状态检查，返回"ok"或status=0认为是成功
            if not(json_data.get('code') == 0 or json_data.get('code') == "ok" or json_data.get('status') == 0):
                print(f"获取分类数据失败: {json_data}")
                return result
            
            # 不再打印json_data，而是处理正常返回的数据
            # 解析视频列表
            data_list = json_data.get('data', {}).get('list', [])
            for item in data_list:
                theater = item.get('theater', {})
                if not theater:
                    continue
                    
                video_id = theater.get('id')
                title = theater.get('title')
                cover = theater.get('cover_url')
                total = theater.get('total', '')
                play_amount = theater.get('play_amount_str', '')
                
                videos.append({
                    "vod_id": video_id,
                    "vod_name": title,
                    "vod_pic": cover,
                    "vod_remarks": f"{total}集",
                    "vod_content": f"播放量:{play_amount}"
                })
            
            # 构建返回结果
            result = {
                'list': videos,
                'page': pg,
                'pagecount': 9999,  # 假设有很多页
                'limit': 24,
                'total': 999999  # 设置一个较大数值
            }
        except Exception as e:
            print(f"获取分类内容异常: {str(e)}")
            
        return result
    
    def detailContent(self, ids):
        """获取详情页内容"""
        video_id = ids[0]
        result = {}
        
        try:
            # 构建详情页请求URL
            url = f"{self.siteUrl}/v2/theater_parent/detail?theater_parent_id={video_id}"
            
            response = self.fetchWithToken(url)
            if not response:
                return {}
                
            json_data = response.json()
            if not(json_data.get('code') == 0 or json_data.get('code') == "ok" or json_data.get('status') == 0):
                print(f"获取详情数据失败: {json_data}")
                return {}
                
            # 解析详情数据
            data = json_data.get('data', {})
            title = data.get('title', '')
            cover = data.get('cover_url', '')
            total = data.get('total', '')
            
            # 提取剧集列表
            theaters = data.get('theaters', [])
            episodes = []
            
            for index, theater in enumerate(theaters):
                ep_name = f"第{theater.get('num', '')}集"
                # 生成格式为 video_id_episode_index 的ID，方便playerContent提取
                ep_url = f"{video_id}_{index}"
                episodes.append(f"{ep_name}${ep_url}")
            
            # 构建VOD数据
            vod = {
                "vod_id": video_id,
                "vod_name": title,
                "vod_pic": cover,
                "vod_remarks": f"{total}集",
                "vod_content": data.get('introduction', ''),
                "vod_play_from": "蓝莓短剧",
                "vod_play_url": "#".join(episodes)
            }
            
            result = {
                'list': [vod]
            }
        except Exception as e:
            print(f"获取详情内容异常: {str(e)}")
            
        return result
    
    def searchContent(self, key, quick, pg=1):
        """搜索功能"""
        result = {}
        videos = []
        
        try:
            # 构建搜索请求
            url = f"{self.siteUrl}/v2/search"
            body = f"text={urllib.parse.quote(key)}"
            
            response = self.fetchWithToken(url, method="POST", body=body)
            if not response:
                return {}
                
            json_data = response.json()
            # 修改这里，使用与detailContent相同的条件判断
            if not(json_data.get('code') == 0 or json_data.get('code') == "ok" or json_data.get('status') == 0):
                print(f"搜索数据失败: {json_data}")
                return {}
                
            # 解析搜索结果
            search_data = json_data.get('data', {}).get('search_data', [])
            for item in search_data:
                video_id = item.get('id')
                title = item.get('title')
                cover = item.get('cover_url')
                score = item.get('score_str', '')
                total = item.get('total', '')
                
                videos.append({
                    "vod_id": video_id,
                    "vod_name": title,
                    "vod_pic": cover,
                    "vod_remarks": f"{score}|{total}集"
                })
            
            result = {
                'list': videos,
                'page': pg
            }
        except Exception as e:
            print(f"搜索内容异常: {str(e)}")
        
        print(11111111, result)
        return result
    
    def searchContentPage(self, key, quick, pg=1):
        return self.searchContent(key, quick, pg)
    
    def playerContent(self, flag, id, vipFlags):
        """获取播放内容"""
        result = {}
        
        # 检查是否已经是直接的视频URL
        if self.isVideoFormat(id):
            result["parse"] = 0
            result["url"] = id
            result["playUrl"] = ""
            result["header"] = json.dumps(self.headers)
            return result
        
        # 如果不是直接的视频URL，需要处理一下
        try:
            # 我们需要从ID中解析出剧ID和集索引
            if id.isdigit():
                # 如果是纯数字ID，说明是剧ID，我们需要获取详情并提取第一集
                video_id = id
                ep_index = 0  # 默认获取第一集
            elif '_' in id:
                # 如果ID包含下划线，格式是 video_id_episode_index
                parts = id.split('_')
                if len(parts) >= 2:
                    video_id = parts[0]  # 这是纯数字的视频ID
                    ep_index = int(parts[1])
                else:
                    video_id = id
                    ep_index = 0
            else:
                # 假设id就是视频URL
                result["parse"] = 0
                result["url"] = id
                result["playUrl"] = ""
                result["header"] = json.dumps(self.headers)
                return result
            
            # 获取详情数据，通过详情接口获取剧集列表
            # 确保只使用纯数字的视频ID作为theater_parent_id参数
            detail_url = f"{self.siteUrl}/v2/theater_parent/detail?theater_parent_id={video_id}"
            print(f"请求详情URL: {detail_url}")
            detail_response = self.fetchWithToken(detail_url)
            
            if not detail_response or detail_response.status_code != 200:
                print("获取详情数据失败")
                return result
            
            detail_json = detail_response.json()
            # 修改这里，使用与detailContent相同的条件判断
            if not(detail_json.get('code') == 0 or detail_json.get('code') == "ok" or detail_json.get('status') == 0):
                print(f"获取详情数据错误: {detail_json}")
                return result
            
            # 获取剧集列表
            theaters = detail_json.get('data', {}).get('theaters', [])
            
            if not theaters or ep_index >= len(theaters):
                print(f"未找到剧集或索引超出范围: {ep_index}")
                return result
            
            # 获取指定索引的剧集
            episode = theaters[ep_index]
            video_url = episode.get('son_video_url', '')
            
            if not video_url:
                print(f"未找到视频URL")
                return result
            
            # 添加播放所需的headers
            play_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Referer": "http://qcapp.xingya.com.cn/"
            }
            
            # 返回播放信息
            result["parse"] = 0
            result["url"] = video_url
            result["playUrl"] = ""
            result["header"] = json.dumps(play_headers)
            
        except Exception as e:
            print(f"获取播放内容异常: {str(e)}")
            import traceback
            print(traceback.format_exc())
            
        return result
    
    def localProxy(self, param):
        """本地代理处理，此处简单返回传入的参数"""
        return [200, "video/MP2T", {}, param] 