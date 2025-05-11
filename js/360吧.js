globalThis.getVideos = function(link, key) {
    let html = request(link);
    let json = JSON.parse(html);
    let data = json.data;
    data = data[key];
    let videos = data.map((n) => {
        let id = n.url;
        let name = n.league_name_zh + ' ' + n.home_team_zh + ' VS ' + n.away_team_zh;
        let pic = n.cover;
        let remarks = n.nickname;
        return {
            vod_id: id,
            vod_name: name,
            vod_pic: pic,
            vod_remarks: remarks,
        };
    });
    return videos
}
var rule = {
    类型: '影视', //影视|听书|漫画|小说
    title: '360吧[球]',
    host: 'https://m.360ba.co/',
    homeUrl: '/api/web/h5_index',
    url: '/api/web/live_lists/fyclass',
    searchUrl: '/api/web/search?keyword=**',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'MOBILE_UA',
    },
    timeout: 5000,
    class_name: '全部&足球&篮球&综合',
    class_url: '1&2&3&99',
    play_parse: true,
    pagecount: {
        "1": 1,
        "2": 1,
        "3": 1,
        "99": 1,
    },
    lazy: $js.toString(() => {
        input = {
            parse: 0,
            url: input,
            header: rule.headers
        };
    }),
    预处理: $js.toString(() => {
        Object.assign(rule.headers, {
            'Referer': rule.host,
            'Origin': rule.host,
        });
    }),
    推荐: $js.toString(() => {
        VODS = getVideos(input, 'hot_matches');

    }),
    一级: $js.toString(() => {
        VODS = [];
        if (MY_PAGE <= 1) {
            VODS = getVideos(input, 'data');
        }
    }),
    二级: '*',
    搜索: $js.toString(() => {
        VODS = [];
        if (MY_PAGE <= 1) {
            VODS = getVideos(input, 'ball');
        }
    }),
}