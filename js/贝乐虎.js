var rule = {
    类型: '影视', //影视|听书|漫画|小说
    title: '贝乐虎[儿]',
    host: 'https://vd.ubestkid.com',
    url: '/api/v1/bv/video#pg=fypage',
    homeUrl: '/api/v1/bv/video',
    searchable: 0,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'IOS_UA',
    },
    timeout: 5000,
    class_parse: $js.toString(() => {
        input = JSON.parse(ungzip('H4sIAAAAAAAAA4VUy27aUBD9F6+zwKRAk1+pqqpSsuiiVRfdVFUlUnCCwU1IwqNuHggFQ1owOCGNjAnwM547l10/oZeiRmTuoO5s6ZyZc87M3BefjA8f3+++erNjbKdTG8ufd6/f7hrbxu9GeSDOs6IWxGFRXN4bnzdW0Ka5qcPjKBJBBXO+OPGfwlNpHY3jI7BC7HoyuCLFNzM6HB6yMMvJu4t4VJbuIanPqIFpCYrXkJ8J3yHorXVqOLSZMHW4vLcw6oibiZy0TRoNU34Vj71eHDnga66ZkCgvtDXeFjO4v7i68kRbcDmNHha2bZXWTBYuqRluFKd5vGhyWWUSjIXSjagdsMmanOPiF1H34vBw8RFUiFdGjdgrz6duHNawSufMJKNWAitjtFlBKa78rz3ZdBRUnN1S+c8Z+f8WFCwPznzZD+g2cZ4fSa0OulPsHD8lpZNrF/aoJQd1gmaGvESLqhVHJSIoybkoOws1fhuKDWh1qQVmyjj+Js57fAPmfsg1L3cE7QIZN5MV1K8faSJnQXV/OVKqkXG1ANo/5o2hYou7KQxGVCnXTyOtEWsmuHXzDqDt4ve8jLrx5JT2e/ZfxppmaYYp+y1sePC1qbabSmOfpCs4HmI/i72Kll+GiU9UA/WosIec5O5+sK/gysL8p6OHleTeFUU6cXE4hsIq7+UfFA1HoacGAAA='));
    }),
    play_parse: true,
    lazy: $js.toString(() => {
        input = {
            parse: 0,
            url: input + '#.mp4'
        };
    }),
    推荐: $js.toString(() => {
        let pdata = {
            age: 1,
            appver: "6.1.9",
            egvip_status: 0,
            svip_status: 0,
            vps: 60,
            subcateId: 56,
            p: 1
        };
        //   let pbody = buildUrl('',pdata).split('?')[1];
        //   let html = post(input,{body:pbody});
        let html = post(input, {
            data: pdata
        });
        let json = JSON.parse(html);
        let data = json.result.items;
        let d = [];
        data.forEach(it => {
            d.push({
                vod_id: it.url + '@@' + it.title + '@@' + it.image,
                vod_name: it.title,
                vod_pic: it.image,
                vod_remarks: '👀' + it.viewcount || '',
            });
        });
        VODS = d;
    }),
    一级: $js.toString(() => {
        let pdata = {
            age: 1,
            appver: "6.1.9",
            egvip_status: 0,
            svip_status: 0,
            vps: 60,
            subcateId: MY_CATE,
            p: MY_PAGE
        };
        let html = post(input.split('#')[0], {
            data: pdata
        });
        let json = JSON.parse(html);
        let data = json.result.items;
        let d = [];
        data.forEach(it => {
            d.push({
                vod_id: it.url + '@@' + it.title + '@@' + it.image,
                vod_name: it.title,
                vod_pic: it.image,
                vod_remarks: '👀' + it.viewcount || '',
            });
        });
        VODS = d;
    }),
    二级: '*',
}