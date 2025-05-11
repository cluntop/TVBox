var rule = {
  类型:'影视',//影视|听书|漫画|小说
  title:'河马短剧[短]',
  host:'https://www.kuaikaw.cn',
  url:'/fyclass/0/fypage',
  searchUrl:'/search/fypage?searchValue=**',
  searchable:2,
  quickSearch:0,
  filterable:0,
  /*filter:'H4sIAAAAAAAAA31X204qWRD9FcLzMaGbTUPPH8w3nMyDM+PTzJxJ5prJyUlABOSm4kFRQXAUBURuigZpsX+ma/fuv5jdmtC1CzIPGrWK2qtWrbr4ORT+/rdf//59K/xN6GPocyj809Y/8sfwD5t/bH37Y/hDKPxp8xffGHYnFjSL/l/+2vz5z6X/J98Gma6X7r7Z/F8j4dCXD0ujd37IT66XRk2Lq3a4foDZObIbMcXOxxWoL5b2RNRUzOKgBMPg47GEuSGfUEOIp4xIByEY0xWzW23A8CIwG6pZTG69WpenejzZRe8QlJNtt9rCWahBYL/Mp6/Ybqj2keXM75FdJymMLLDTvDFCLoz5qZJ3Xou8agdOTI+rcVIlaMzhKMt3T5ZeJosSsG1xlXGsU+f1Ar0XUZ/i52kxLgaFYREJJ6KtFP8y4/afvd4dikTIc6+bYoQkEDEZlYjXP+H5ojMrwmQSOOqmmp3bb4rHOmZZ1Rq/u4TjBmTbMHxaesU1NQg8Tx3rCvId5GFsxHVCtIyDXEwaZL/t9mzHKmDhq8qV9ebpDA6SiJKi56YwKqE3EpJhZhJucvBsiZ0KnzYDwLpaBllsyTGCEov60iFVf5mLZAbqTVgcBs0QV3XqPliuhXUeI3AKE7BrqJRxw1eFWgZ3b+wz/IYckawmD+2yY+UCIJoKhI8O4aqP2VU1I+wF3Fhuqi8qd1LxWDNq2lKZbvUewTAJ1iLcpHHXJdZUEZWQ6GC878znbr6HGCVtVLvgRyXMGFvTsZhxMjle0jCuYM2rCJzZMQa4kj8UWtDGRMbU992LqXfU8HJlaGRxC6tR+PadexygYCy2weigf5sqyIW8s7cDgxuMM7Fif7bIUIrr6htiYfFzPGYTaiNAKeN2WpC5+x+X+ZOcN4E9GqG9tM/r93xQEruooyIErZfMissBUm98gxlqwu+LDfd/zCTZ2LdQOsYaN2hbO/M8BqFql9dtMVdKG5fNaKhIYa/lZco4XzLoCl3+goNoK8PbbbxgkGQFHNnKZoyQsSM/D6VgDLCoCo+f1XiqiMtFWCxfKotTN0l7XD/wZIfvHkgcaMUT9RZqkksxLuOtKOkkSKuPopPFBZMu+ob8RrZQzxZPBV57cntB38Y1MjfsodQyXvhqXl7tFnpn6ONkaq3bh4yMDrfRglQOymkvhwdEQicDYiBXnnxM4Vknd5aXXsBsG+Mlc7I392pTLCMVsLP4KraVA4fIsP8vaTtyRlZPxbCNtUzs+Sm+A6WdyryrrkDSjfIigPkA8e0fV7qxxseZWXCTQ5HYGsVZ4iqFH1PJEKcHfHaFweq0J+TViepKWq5TwZtTk2SpXFsFf9jaTS95hipKOkfKGRYTrGXN1zJJZr8tV7XoJvEOYQYdzWMYBtwypslhR+STK+MpwKKmdCELf7YrXZRdpRlkNhMp6yYVod956GAi85KWhZFl3TuDDuaVHM9+/esLiRAfJiaZh35tUSMxcui/dxvWOZln6QzfafHHFM5SdXFeLnjeFp28l8WH2rq1zgc3PP8V15hwXr/E//pIIWpr0KDrZqXwq+qQtJJHDvb4dpWk5LuEvnv/+g+LRDj8hg4AAA==',
  filter_url:'{{fl.cateId}}',
  filter_def:{ browse:{cateId:'browse'}},*/
  headers:{
      'User-Agent':'MOBILE_UA',
  },
  timeout:5000,
  class_parse:'.PcHeader_navBox__ZpLDU a;a&&Text;a&&href;.*/(.*)',
  cate_exclude:'',
  play_parse:true,
  lazy:$js.toString(()=>{
    input = {parse:1,url:input,js:''};
  }),
  double:true,
  推荐:'.FeaturedList_featuredBox__vtx4A;.FeaturedList_featuredItem__w9Jy0;.FeaturedList_bookName__lcwp9&&Text;.image_imageItem__IZeBT&&src;.FeaturedList_lastChapter__XbMSI&&Text;.FeaturedList_itemImg__kq6zA&&href',
  一级:'body .BrowseList_listItem__h7lD4;.BrowseList_bookName__FIG1o p&&Text;.image_imageItem__IZeBT&&src;.BrowseList_lastChapter__dkL54&&Text;.image_imageBox__Mubn5&&href',
  二级:{
    title:'h1&&Text;.DramaDetail_tagItem__L546Y&&Text',
    img:'.DramaDetail_bookCover__mvLQU&&src',
    //desc:'主要信息;年代;地区;演员;导演',
    content:'.adm-ellipsis&&Text',
    tabs:'.dramaDetail_contentBox__WImsV h3',
    lists:'.dramaDetail_catalog__M4si4:eq(#id)&&a',
    tab_text:'body&&Text',
    list_text:'body&&Text',
    list_url:'a&&href',
    list_url_prefix: '',
  },
  搜索:'body .MTagBookList_tagBookItem__C_038;.image_imageScaleBox__JFwzM img&&alt;.image_imageItem__IZeBT&&src;.MTagBookList_totalChapterNum__vjOW4&&Text;.image_imageScaleBox__JFwzM&&href',
}