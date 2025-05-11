globalThis.getHeaders = function () {
    let tkurl = 'https://app.whjzjx.cn/v1/account/login';
    let opt = {
        headers: {
        'user-agent': 'okhttp/4.10.0',
        'user_agent': 'Mozilla/5.0 (Linux; Android 13; PEQM00 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36',
        'Host': 'app.whjzjx.cn',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '40',
        'Accept-Encoding': 'gzip'
        },
        method: 'POST',
        body: 'device=2cdbf9265f4d63b82a30735793127c962'
    };
    let tk = JSON.parse(request(tkurl,opt)).data.token;
    let kheader = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; PEQM00 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36',
    'authorization': tk,
    'Content-Type': 'application/json; charset=UTF-8'
    };
    return kheader
}

var rule = {
author: '小可乐/2410/第一版',
title: '星芽短剧',
类型: '影视',
host: 'https://app.whjzjx.cn',
hostJs: '',
headers: {'User-Agent': 'okhttp/4.10.0'},
编码: 'utf-8',
timeout: 5000,

homeUrl: '/cloud/v2/theater/home_page?theater_class_id=5&type=1&page_num=1&page_size=24',
url: '/cloud/v2/theater/home_page?theater_class_id=fyclass&type=1&fyfilter&page_num=fypage&page_size=24',
filter_url: '{{fl.class}}',
detailUrl: '',
searchUrl: '/v3/search',
searchable: 1, 
quickSearch: 1, 
filterable: 1, 

class_name: '剧场&热播剧&会员精选&新剧&星选好剧&阳光剧场',
class_url: '1&2&8&3&7&5',
filter_def: {},

play_parse: true,
lazy: `js:
if (/\\.(m3u8|mp4)/.test(input)) {
    input = { jx: 0, parse: 0, url: input }
} else {
    input = { jx: 0, parse: 1, url: input }
}`,

limit: 9,
double: false,
推荐: '*',
一级: `js:
input = input.replace(/&{2,}/g,'&');
let kjson = JSON.parse(request(input, {headers: getHeaders()}));
VODS = [];
let klists = kjson.data.list;
klists.forEach((it) => {
    VODS.push({
        vod_name: it.theater.title,
        vod_pic: it.theater.cover_url,
        vod_remarks: it.theater.total + '集' + '|' + it.theater.theme,
        vod_id: 'https://app.whjzjx.cn/v2/theater_parent/detail?theater_parent_id=' + it.theater.id
    })
})
`,
二级: `js:
let kjson = JSON.parse(request(input, {headers: getHeaders()}));
let kplist = kjson.data.theaters.map((it) => { return it.num + '$' + it.son_video_url });
VOD = {
    vod_id: input,
    vod_name: kjson.data.title,
    vod_pic: kjson.data.cover_url,
    type_name: kjson.data.desc_tags.join('|'),
    vod_remarks: kjson.data.total + '集',
    vod_year: '未知',
    vod_area: '未知',
    vod_director: '星芽短剧',
    vod_actor: kjson.data.filing,
    vod_content: kjson.data.introduction,
    vod_play_from: '👶星芽专线',
    vod_play_url: kplist.join('#')
}
`,
搜索: `js:
let kjson = JSON.parse(request(input, {headers: getHeaders(), method: 'POST', body: {'text': KEY} }));
VODS = [];
let klists = kjson.data.theater.search_data;
klists.forEach((it) => {
    VODS.push({
        vod_name: it.title,
        vod_pic: it.cover_url,
        vod_remarks: it.total + '集' + '|' + it.score_str,
        vod_id: 'https://app.whjzjx.cn/v2/theater_parent/detail?theater_parent_id=' + it.id
    })
})
`,

filter: {
"1":[
{"key":"class","name":"剧情","value":[{"n":"全部","v":"class2_ids=0"},{"n":"都市","v":"class2_ids=4"},{"n":"古装","v":"class2_ids=5"},{"n":"现代言情","v":"class2_ids=15"},{"n":"战神","v":"class2_ids=24"},{"n":"逆袭","v":"class2_ids=7"},{"n":"穿越","v":"class2_ids=17"},{"n":"历史","v":"class2_ids=40"},{"n":"赘婿","v":"class2_ids=26"},{"n":"神医","v":"class2_ids=25"},{"n":"重生","v":"class2_ids=6"},{"n":"甜宠","v":"class2_ids=33"},{"n":"古代言情","v":"class2_ids=37"},{"n":"玄幻","v":"class2_ids=35"},{"n":"萌宝","v":"class2_ids=9"},{"n":"脑洞","v":"class2_ids=32"},{"n":"亲情","v":"class2_ids=41"},{"n":"虐恋","v":"class2_ids=8"}]}
]
}
}