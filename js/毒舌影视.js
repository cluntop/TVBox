var rule = {
    author: '乐哥250316',
    title: '毒舌影视',
    类型: '影视',
    //首页网址
    host: 'https://www.nanyangcn.net/',
    hostJs: ``,
    headers: {
        'User-Agent': 'Mozilla/5.0',
    },
    编码: 'utf-8',
    timeout: 5000,
    homeUrl: '/',
    //分类页
    url: '/fyclass/index-fypage.html',
    //筛选页
    filter_url: '',
    detailUrl: '',
    searchUrl: '/search/**-fypage.html',
    searchable: 1,
    quickSearch: 1,
    filterable: 1,
    limit: 10,
    double: false,
    class_name: '电影&电视剧&动漫&综艺',
    //静态分类值
    class_url: 'dianying&dianshiju&dongman&zongyi',
    推荐: '*',
    //数组、标题、图片、副标题、链接，分类页找参数
    一级: '.col-sm-3:has(h5);.video-pic.loading&&title;.video-pic.loading&&data-original;.text-bg-r&&Text;a&&href',
    //搜索页找参数  数组标题图片副标题链接
    搜索: '.details-info-min;*;*;.hidden-sm&&Text;*',
    二级: `js:
 let html = request(input);
VOD = {};
 VOD.vod_id = input;
        //定位详情页标题
        VOD.vod_name = pdfh(html, "h1&&Text:gt(em)");
        //定位详情页图片链接
        VOD.vod_pic = pd(html, ".video-pic&&style");
        //定位详情页类型
        VOD.type_name = pdfh(html, ".info&&li:eq(2)&&Text").replace("类型：", "");
        //状态备注
        VOD.vod_remarks = pdfh(html, ".info&&li:eq(2)&&Text").replace("提醒：", "");
        //年份
        VOD.vod_year = pdfh(html, ".info&&li:eq(9)&&Text").replace("年份：", "");
        //地区
        VOD.vod_area = pdfh(html, ".info&&li:eq(6)&&Text").replace("国家/地区：", "");
        //导演
        VOD.vod_director = pdfh(html, ".info&&li:eq(5)&&Text").replace("导演：", "");
        //演员
        VOD.vod_actor = pdfh(html, ".info&&li:eq(3)&&Text").replace("主演：", "");
        //简介
        VOD.vod_content = ("✨乐哥为您介绍剧情👉请不要相信视频中的广告，以免上当受骗！" + pdfh(html, "body&&.collapse:eq(1)&&Text"));
        //线路
       let r_ktabs = pdfa(html,'.nav-tabs&&.gico');
 let ktabs = r_ktabs.map(it => ("✨乐哥推荐✨" +pdfh(it, 'a&&Text')));
 VOD.vod_play_from = ktabs.join('$$$');
 let klists = [];
 //播放
let r_plists = pdfa(html, 'body&&.clearfix.fade');
 r_plists.forEach((rp) => {
     let klist = pdfa(rp, 'li').reverse().map((it) => {
     return pdfh(it, 'a&&Text') + '$' + pd(it, 'a&&href', input);
     });
    klist = klist.join('#');
     klists.push(klist);
});
 VOD.vod_play_url = klists.join('$$$')
 `,
    //是否启用辅助嗅探: 1,0
    sniffer: 0,
    // 辅助嗅探规则
    isVideo: 'http((?!http).){26,}\\.(m3u8|mp4|flv|avi|mkv|wmv|mpg|mpeg|mov|ts|3gp|rm|rmvb|asf|m4a|mp3|wma)',
    play_parse: true,
    //播放地址通用解析
    lazy: `js:
let kcode = JSON.parse(request(input).match(/var player_.*?=(.*?)</)[1]);
let kurl = kcode.url;
if (kcode.encrypt == '1') {
url = unescape(url)
} else if (kcode.encrypt == '2') {
url = unescape(base64Decode(url))
};
if (/\\.(m3u8|mp4)/.test(kurl)) {
input = { jx: 0, parse: 0, url: kurl }
} else {
input = { jx: 0, parse: 1, url: input }
}`,
    filter: {}
}