from icalendar import Calendar
from collections import defaultdict
from datetime import date, timedelta
import datetime
import re
import urllib.parse
import json

# =====================================================================
# 1. 常數與字典映射區 (Dictionaries & Mappings)
# =====================================================================
summary_map = {
    # Advent
    "Advent 1": "First Sunday", "Advent 2": "Second Sunday",
    "Advent 3": "Third Sunday", "Advent 4": "Fourth Sunday",
    # Christmas
    "Christmas Day": "Christmas Day", "Christmas 1": "First Sunday",
    "Christmas 2": "Second Sunday", "Christmas 3": "Third Sunday", "Christmas 4": "Fourth Sunday",
    # Epiphany
    "Epiphany": "Epiphany", "Epiphany 1": "First Sunday", "Epiphany 2": "Second Sunday",
    "Epiphany 3": "Third Sunday", "Epiphany 4": "Fourth Sunday", "Epiphany 5": "Fifth Sunday",
    "Epiphany 6": "Sixth Sunday", "Epiphany 7": "Seventh Sunday", "Epiphany Last": "Last Sunday",
    "Baptism of Our Lord": "First Sunday", "Transfiguration": "Last Sunday",
    # Lent
    "Lent 1": "First Sunday", "Lent 2": "Second Sunday", "Lent 3": "Third Sunday",
    "Lent 4": "Fourth Sunday", "Lent 5": "Fifth Sunday", "Ash Wednesday": "Ash Wednesday",
    "Palm Sunday": "Palm Sunday", "Good Friday": "Good Friday", "Maundy Thursday": "Maundy Thursday", "Holy Saturday": "Holy Saturday",
    # Easter
    "Easter Sunday": "Easter Sunday", "Easter 2": "Second Sunday", "Easter 3": "Third Sunday",
    "Easter 4": "Fourth Sunday", "Easter 5": "Fifth Sunday", "Ascension": "Ascension",
    # Pentecost
    "Pentecost Sunday": "Pentecost Sunday",
    # Ordinary / Proper / Trinity
    "Ordinary 1": "First Sunday", "Ordinary 2": "Second Sunday", "Ordinary 3": "Third Sunday",
    "Ordinary 4": "Fourth Sunday", "Ordinary 5": "Fifth Sunday", "Ordinary 6": "Sixth Sunday",
    "Ordinary 7": "Seventh Sunday", "Ordinary 8": "Eighth Sunday", "Ordinary 9": "Ninth Sunday",
    "Ordinary 10": "Tenth Sunday", "Ordinary 11": "Eleventh Sunday", "Ordinary 12": "Twelfth Sunday",
    "Ordinary 13": "Thirteenth Sunday", "Ordinary 14": "Fourteenth Sunday", "Ordinary 15": "Fifteenth Sunday",
    "Ordinary 16": "Sixteenth Sunday", "Ordinary 17": "Seventeenth Sunday", "Ordinary 18": "Eighteenth Sunday",
    "Ordinary 19": "Nineteenth Sunday", "Ordinary 20": "Twentieth Sunday",
    "Proper 1": "First Sunday", "Proper 2": "Second Sunday", "Proper 3": "Third Sunday",
    "Proper 4": "Fourth Sunday", "Proper 5": "Fifth Sunday", "Proper 6": "Sixth Sunday",
    "Proper 7": "Seventh Sunday", "Proper 8": "Eighth Sunday", "Proper 9": "Ninth Sunday",
    "Proper 10": "Tenth Sunday", "Proper 11": "Eleventh Sunday", "Proper 12": "Twelfth Sunday",
    "Proper 13": "Thirteenth Sunday", "Proper 14": "Fourteenth Sunday", "Proper 15": "Fifteenth Sunday",
    "Proper 16": "Sixteenth Sunday", "Proper 17": "Seventeenth Sunday", "Proper 18": "Eighteenth Sunday",
    "Proper 19": "Nineteenth Sunday", "Proper 20": "Twentieth Sunday",
    "Trinity Sunday": "Trinity Sunday", "Christ the King": "Christ the King"
}

season_map = {
    "Resurrection of the Lord": "復活節", "Epiphany of the Lord": "主顯日", "Baptism of the Lord": "耶穌受洗主日",
    "Ascension of the Lord": "基督升天日", "Nativity of the Lord": "聖誕節", "Liturgy of the Palms": "棕枝主日",
    "Liturgy of the Passion": "受難主日", "Reign of Christ": "基督君王主日", "Holy Name of Jesus": "耶穌聖名日",
    "Visitation of Mary to Elizabeth": "馬利亞探望伊利沙伯", "Holy Cross": "聖十字架日", "New Year's Day": "新年",
    "Canadian Thanksgiving Day": "加拿大感恩節", "Easter Evening": "復活節黃昏", "Monday of Holy Week": "聖週一",
    "Tuesday of Holy Week": "聖週二", "Wednesday of Holy Week": "聖週三", "of the Lord": "", "of the": "",
    "Last Sunday of End Time-Christ  King": "末期最後一主日-基督君王主日", "Christmas Eve": "平安夜",  
    "Nativity of Our Lord": "主降生日", "Reformation Day": "宗教改革日", "Reformation": "宗教改革日",
    "Christ the King": "基督君王主日", "Christ King": "基督君王主日", "Christ  King": "基督君王主日",
    "Christ the King Sunday": "基督君王主日", "All Saints": "古聖紀念日", "All Saints Day": "古聖紀念日",
    "All Saints' Day": "古聖紀念日", "All Saints'": "古聖紀念日", "Ash Wednesday": "聖灰日",
    "Palm Sunday": "棕枝主日", "Maundy Thursday": "主立聖餐日", "Holy Thursday": "主立聖餐日",
    "Good Friday": "受難日", "Holy Saturday": "聖週六", "Easter Vigil": "復活前夕守夜",
    "Easter Sunday": "復活節", "Easter Day": "復活節", "Pentecost Sunday": "聖靈降臨主日",  
    "Day of Pentecost": "聖靈降臨主日", "Holy Trinity": "三一主日", "Trinity Sunday": "三一主日",
    "Trinity": "三一主日", "Presentation of the Lord": "主奉獻日", "Presentation of Our Lord": "主奉獻日",
    "Annunciation": "天使報喜日", "Visitation": "探望日", "Nativity of John the Baptist": "施洗約翰誕辰",
    "Conversion of St. Paul": "聖保羅歸主日", "St. Michael and All Angels": "聖米迦勒與眾天使日",
    "Transfiguration Sunday": "登山變像主日", "Transfiguration of Our Lord": "登山變像主日",  
    "Transfiguration": "登山變像主日", "The Baptism of Our Lord": "耶穌受洗主日",  
    "Baptism of Our Lord": "耶穌受洗主日", "Epiphany of Our Lord": "主顯日",  
    "Ascension": "基督升天日", "Ascension of Our Lord": "基督升天日", "Ascension of our Lord": "基督升天日",
    "Christmas Day": "聖誕節", "Chistmas Day": "聖誕節", "Last Judgment": "末日審判主日",
    "Last Sunday in the Church Year": "教會年最後一主日", "Last Sunday of the Church Year": "教會年最後一主日",
    "Last Sunday of End Time": "末期最後一主日", "Resurrection of our Lord": "耶穌基督復活了！",
    "Martin Luther's birthday": "馬丁路德誕辰", "None": "", "Saints Triumphant": "聖徒得勝日",
    "Sunday of the Passion": "受難主日", "Thanksgiving Day": "感恩節", "Thanksgiving": "感恩節",
    "Easter Sunday - Dawn": "復活節早晨", "Easter Dawn": "復活節早晨",
    "Advent": "將臨期", "Christmas": "聖誕期", "the Epiphany": "顯現期", "Epiphany": "顯現期",  
    "Ephphany": "顯現期", "Lent": "預苦期", "Holy Week": "聖週", "Easter": "復活期",  
    "the Pentecost": "聖靈降臨期", "Pentecost": "聖靈降臨期", "Ordinary Time": "常年期", "End Time": "末期"
}

season_meaning_map = {
    "Advent": "將臨期—預備慶祝基督的降生，預備等候基督的再臨。",
    "Christmas": "聖誕期—慶賀基督降生，展望與基督永恆同在。",
    "Epiphany": "顯現期-慶賀基督顯明身份，開展其在世的工作。",
    "Ephphany": "顯現期-慶賀基督顯明身份，開展其在世的工作。",
    "Lent": "預苦期-藉憂傷與悔罪預備等候為我們受苦受死的基督。",
    "Holy Week": "聖週-藉憂傷與悔罪預備等候為我們受苦受死的基督。",
    "Easter": "復活期-慶賀復活的基督已為我們勝過罪與死亡。",
    "Pentecost": "聖靈降臨期-慶賀主應許的聖靈降臨。",
    "Ordinary Time": "常年期-聖靈降臨後常年期，在聖靈光照中持續學習聖道。",
    "End Time": "聖靈降臨期-慶賀主應許的聖靈降臨。"
}

ordinal_map = {
    "First": "第一", "Second": "第二", "Third": "第三", "Fourth": "第四", "Fifth": "第五",
    "Sixth": "第六", "Seventh": "第七", "Eighth": "第八", "Ninth": "第九", "Tenth": "第十",
    "Eleventh": "第十一", "Twelfth": "第十二", "Twelth": "第十二", "Thirteenth": "第十三",
    "Fourteenth": "第十四", "Fourtheenth": "第十四", "Fifteenth": "第十五", "Sixteenth": "第十六",
    "Seventeenth": "第十七", "Eighteenth": "第十八", "Nineteenth": "第十九", "Twentieth": "第二十",
    "Twent-first": "第二十一", "Twenty-first": "第二十一", "Twenty-second": "第二十二", 
    "Twenty-third": "第二十三", "Twenty-fourth": "第二十四", "Twenty-fifth": "第二十五", 
    "Twenty-sixth": "第二十六", "Twenty-seventh": "第二十七", "Twenty-eighth": "第二十八", 
    "Twenty-ninth": "第二十九", "Thirtieth": "第三十"
}

ordinal_map_2 = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7,
    "eighth": 8, "ninth": 9, "tenth": 10, "eleventh": 11, "twelfth": 12, "thirteenth": 13,
    "fourteenth": 14, "fifteenth": 15, "sixteenth": 16, "seventeenth": 17, "eighteenth": 18,
    "nineteenth": 19, "twentieth": 20, "twenty-first": 21, "twenty-second": 22, "twenty-third": 23,
    "twenty-fourth": 24, "twenty-fifth": 25,
}

arabic_to_zh = {
    "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九", "10": "十",
    "11": "十一", "12": "十二", "13": "十三", "14": "十四", "15": "十五", "16": "十六", "17": "十七", "18": "十八", "19": "十九", "20": "二十",
    "21": "二十一", "22": "二十二", "23": "二十三", "24": "二十四", "25": "二十五", "26": "二十六", "27": "二十七", "28": "二十八", "29": "二十九", "30": "三十",
    "31": "三十一", "32": "三十二", "33": "三十三", "34": "三十四"
}

book_map = {
    "Genesis": "創世記","Exodus": "出埃及記","Leviticus": "利未記","Numbers": "民數記",
    "Deuteronomy": "申命記","Joshua": "約書亞記","Judges": "士師記","Ruth": "路得記",
    "1 Samuel": "撒母耳記上","2 Samuel": "撒母耳記下","1 Kings": "列王紀上","2 Kings": "列王紀下",
    "1 Chronicles": "歷代志上","2 Chronicles": "歷代志下","Ezra": "以斯拉記","Nehemiah": "尼希米記",
    "Esther": "以斯帖記","Job": "約伯記","Psalm": "詩篇","Proverbs": "箴言",
    "Ecclesiastes": "傳道書","Song of Solomon": "雅歌","Isaiah": "以賽亞書","Jeremiah": "耶利米書",
    "Lamentations": "耶利米哀歌","Ezekiel": "以西結書","Daniel": "但以理書","Hosea": "何西阿書",
    "Joel": "約珥書","Amos": "阿摩司書","Obadiah": "俄巴底亞書","Jonah": "約拿書",
    "Micah": "彌迦書","Nahum": "那鴻書","Habakkuk": "哈巴谷書","Zephaniah": "西番雅書",
    "Haggai": "哈該書","Zechariah": "撒迦利亞書","Malachi": "瑪拉基書",
    "Matthew": "馬太福音","Mark": "馬可福音","Luke": "路加福音","John": "約翰福音",
    "Acts": "使徒行傳","Romans": "羅馬書","1 Corinthians": "哥林多前書","2 Corinthians": "哥林多後書",
    "Galatians": "加拉太書","Ephesians": "以弗所書","Philippians": "腓立比書","Colossians": "歌羅西書",
    "1 Thessalonians": "帖撒羅尼迦前書","2 Thessalonians": "帖撒羅尼迦後書","1 Timothy": "提摩太前書",
    "2 Timothy": "提摩太後書","Titus": "提多書","Philemon": "腓利門書","Hebrews": "希伯來書",
    "James": "雅各書","1 Peter": "彼得前書","2 Peter": "彼得後書","1 John": "約翰一書",
    "2 John": "約翰二書","3 John": "約翰三書","Jude": "猶大書","Revelation": "啟示錄",
    "Tobit": "多比傳", "Judith": "猶滴傳", "Additions to Esther": "以斯帖補篇",
    "Wisdom of Solomon": "所羅門智訓", "Wisdom of ben Sirach": "便西拉智訓",
    "Sirach": "便西拉智訓", "Ecclesiasticus": "便西拉智訓", "Baruch": "巴錄書",
    "Letter of Jeremiah": "耶利米書信", "Songs of the Three Young Men": "三青年之歌",
    "Susanna": "蘇撒拿傳", "Bel and the Dragon": "彼勒與大龍", "1 Maccabees": "馬加比一書",
    "2 Maccabees": "馬加比二書", "3 Ezra": "以斯拉三書", "1 Esdrae": "以斯拉三書",
    "Esdrae I": "以斯拉三書", "4 Ezra": "以斯拉四書", "2 Esdrae": "以斯拉四書",
    "Prayer of Manasseh": "瑪拿西禱詞"
}

phrase_map = {
    "Last Sunday of End Time-Christ  King": "末期最後一主日-基督君王日",
    "Last Sunday of End Time-Christ King": "末期最後一主日-基督君王日",
    "Lessons and Psalm": "經課與詩篇", "Supplemental Lectionary": "補充經課",
    "Hymn of the Day": "今日詩歌", "Hymn of  Day": "今日詩歌",
    "FIRST READING": "第一部分讀經", "SECOND READING": "第二部分讀經",
    "GOSPEL": "福音經課", "PSALM": "詩篇", "Reading": "讀經課", "Sunday": "主日"
}

color_map = {
    "Red": "紅色","Green": "綠色","Blue": "藍色","Yellow": "黃色","Purple": "紫色",
    "Orange": "橙色","Black": "黑色","White": "白色","Gray": "灰色","Brown": "棕色","Pink": "粉紅色"
}

wdb_book_map = {
    "創世記": "gen", "出埃及記": "exo", "利未記": "lev", "民數記": "num", "申命記": "deu",
    "約書亞記": "jos", "士師記": "jdg", "路得記": "rut", "撒母耳記上": "1sa", "撒母耳記下": "2sa",
    "列王紀上": "1ki", "列王紀下": "2ki", "歷代志上": "1ch", "歷代志下": "2ch", "以斯拉記": "ezr",
    "尼希米記": "neh", "以斯帖記": "est", "約伯記": "job", "詩篇": "psa", "箴言": "pro",
    "傳道書": "ecc", "雅歌": "sng", "以賽亞書": "isa", "耶利米書": "jer", "耶利米哀歌": "lam",
    "以西結書": "ezk", "但以理書": "dan", "何西阿書": "hos", "約珥書": "jol", "阿摩司書": "amo",
    "俄巴底亞書": "oba", "約拿書": "jon", "彌迦書": "mic", "那鴻書": "nam", "哈巴谷書": "hab",
    "西番雅書": "zep", "哈該書": "hag", "撒迦利亞書": "zec", "瑪拉基書": "mal",
    "馬太福音": "mat", "馬可福音": "mrk", "路加福音": "luk", "約翰福音": "jhn", "使徒行傳": "act",
    "羅馬書": "rom", "哥林多前書": "1co", "哥林多後書": "2co", "加拉太書": "gal", "以弗所書": "eph",
    "腓立比書": "php", "歌羅西書": "col", "帖撒羅尼迦前書": "1th", "帖撒羅尼迦後書": "2th",
    "提摩太前書": "1ti", "提摩太後書": "2ti", "提多書": "tit", "腓利門書": "phm", "希伯來書": "heb",
    "雅各書": "jas", "彼得前書": "1pe", "彼得後書": "2pe", "約翰一書": "1jn", "約翰二書": "2jn",
    "約翰三書": "3jn", "猶大書": "jud", "啟示錄": "rev"
}

# 現代詩歌對照表 (精簡呈現，保留原有邏輯)
hymn_map = {
    # Advent
    ("Advent", "First Sunday"): ["約書亞樂團：《打開眾城門》", "讚美之泉：《我們等候愛慕耶穌》", "小羊詩歌：《抬頭仰望》"],
    ("Advent", "Second Sunday"): ["約書亞樂團：《祢是我盼望》", "讚美之泉：《有一件事》", "小羊詩歌：《我要等候耶和華》"],
    ("Advent", "Third Sunday"): ["約書亞樂團：《祢的呼喚》", "讚美之泉：《聽見這世代的呼喚》", "小羊詩歌：《新郎的呼喚》"],
    ("Advent", "Fourth Sunday"): ["約書亞樂團：《相信擁抱》", "讚美之泉：《深深地敬拜》", "小羊詩歌：《新婦的祈禱》"],
    ("Advent", None): ["約書亞樂團：《抓住永恆》", "讚美之泉：《恢復敬拜》", "小羊詩歌：《奇妙的預備》"],
    # Christmas
    ("Christmas", "Christmas Eve"): ["約書亞樂團：《台北的聖誕節》", "讚美之泉：《我們歡慶聖誕》", "小羊詩歌：《彌賽亞》"],
    ("Christmas", "Christmas Day"): ["約書亞樂團：《榮美的救主》", "讚美之泉：《是耶穌的名》", "小羊詩歌：《祂的兒子》"],
    ("Christmas", "First Sunday"): ["約書亞樂團：《這是真愛》", "讚美之泉：《最大的福分》", "小羊詩歌：《耶穌,萬名之上的名》"],
    ("Christmas", "Second Sunday"): ["約書亞樂團：《找到我》", "讚美之泉：《I Will Sing Hallelujah [我要唱哈利路亞]》", "小羊詩歌：《你們要讚美耶和華》"],
    ("Christmas", "Third Sunday"): ["約書亞樂團：《天父祢都看顧》", "讚美之泉：《天父祢愛我》", "小羊詩歌：《耶穌基督是主》"],
    ("Christmas", "Fourth Sunday"): ["約書亞樂團：《大過一切的愛》", "讚美之泉：《是祢，耶穌》", "小羊詩歌：《榮耀都歸神羔羊》"],
    ("Christmas", None): ["約書亞樂團：《就這樣沉浸在祢愛中》", "讚美之泉：《大山可以挪開》", "小羊詩歌：《祢是配》"],
    # Epiphany
    ("Epiphany", "Epiphany"): ["約書亞樂團：《我神真偉大》", "讚美之泉：《榮耀至高神》", "小羊詩歌：《萬民同來敬拜》"],
    ("Epiphany", "First Sunday"): ["約書亞樂團：《榮美輝煌》", "讚美之泉：《榮耀榮耀榮耀》", "小羊詩歌：《願祢的國降臨》"],
    ("Epiphany", "Second Sunday"): ["約書亞樂團：《主祢是我們的太陽》", "讚美之泉：《Holy, Holy [聖潔榮耀主]》", "小羊詩歌：《我是祢所造》"],
    ("Epiphany", "Third Sunday"): ["約書亞樂團：《在呼召我之處》", "讚美之泉：《我的耶穌》", "小羊詩歌：《哦主,祢名何其美》"],
    ("Epiphany", "Fourth Sunday"): ["約書亞樂團：《讓祂的喜樂充滿你》", "讚美之泉：《愛使我們勇敢》", "小羊詩歌：《我的幫助從何而來＋願神興起》"],
    ("Epiphany", "Fifth Sunday"): ["約書亞樂團：《如祢》", "讚美之泉：《偉大的神》", "小羊詩歌：《哈利路!主我神作王了》"],
    ("Epiphany", "Sixth Sunday"): ["約書亞樂團：《通往祢的路》", "讚美之泉：《聖潔和榮耀》", "小羊詩歌：《永遠稱頌祢》"],
    ("Epiphany", "Seventh Sunday"): ["約書亞樂團：《敬畏的心》", "讚美之泉：《為榮耀的創造》", "小羊詩歌：《我願意》"],
    ("Epiphany", "Eighth Sunday"): ["約書亞樂團：《我安然居住》", "讚美之泉：《不停讚美祢》", "小羊詩歌：《倚靠祢》"],
    ("Epiphany", "Ninth Sunday"): ["約書亞樂團：《祂是你的幫助》", "讚美之泉：《披上讚美衣》", "小羊詩歌：《Faith Over Fear》"],
    ("Epiphany", "Tenth Sunday"): ["約書亞樂團：《主你永遠與我同在》", "讚美之泉：《向我的神獻上感謝》", "小羊詩歌：《我知道祢愛我》"],
    ("Epiphany", "Last Sunday"): ["約書亞樂團：《恢復榮耀》", "讚美之泉：《在祢沒有難成的事》", "小羊詩歌：《弟兄和睦同居》"],
    ("Epiphany", "Transfiguration"): ["約書亞樂團：《榮美輝煌》", "讚美之泉：《我是承載神榮耀的器皿》", "小羊詩歌：《弟兄和睦同居》"],
    ("Epiphany", None): ["約書亞樂團：《雙膝跪下觸摸天堂》", "讚美之泉：《大聲敬拜》", "小羊詩歌：《永遠稱謝祢(台)》"],
    # Lent
    ("Lent", "First Sunday"): ["約書亞樂團：《恩典之洋（即使我仍會軟弱）》", "讚美之泉：《煉淨過的生命》", "小羊詩歌：《一粒麥子》"],
    ("Lent", "Second Sunday"): ["約書亞樂團：《憐憫的愛》", "讚美之泉：《十架的大能》", "小羊詩歌：《曠野之歌》"],
    ("Lent", "Third Sunday"): ["約書亞樂團：《我要愛慕你》", "讚美之泉：《我的生命獻給祢》", "小羊詩歌：《我向祢回轉》"],
    ("Lent", "Fourth Sunday"): ["約書亞樂團：《回家》", "讚美之泉：《那麼深的渴慕》", "小羊詩歌：《神啊,我渴慕祢》"],
    ("Lent", "Fifth Sunday"): ["約書亞樂團：《堅強的愛》", "讚美之泉：《深愛耶穌》", "小羊詩歌：《跟隨到底》"],
    ("Lent", "Ash Wednesday"): ["約書亞樂團：《餘燼》", "讚美之泉：《深不見底的愛》", "小羊詩歌：《為我造清潔的心》"],
    ("Lent", None): ["約書亞樂團：《我願降服》", "讚美之泉：《浪子的我》", "小羊詩歌：《主啊,我們自卑》"],
    # Holy Week
    ("Holy Week", "Palm Sunday"): ["約書亞樂團：《和散那》", "讚美之泉：《和散那，歡迎君王》", "小羊詩歌：《錫安大道》"],
    ("Holy Week", "Maundy Thursday"): ["約書亞樂團：《父的筵席》", "讚美之泉：《愛祢直到永遠》", "小羊詩歌：《何等深情》"],
    ("Holy Week", "Good Friday"): ["約書亞樂團：《神羔羊配得》", "讚美之泉：《我是被主重價買回的人》", "小羊詩歌：《雞叫的時候》"],
    ("Holy Week", "Holy Saturday"): ["約書亞樂團：《安靜》", "讚美之泉：《藏身之處》", "小羊詩歌：《藏身祢的懷裏》"],
    ("Holy Week", None): ["約書亞樂團：《無盡的愛》", "讚美之泉：《盡情地微笑》", "小羊詩歌：《有誰》"],
    # Easter
    ("Easter", "Easter Sunday"): ["約書亞樂團：《Happy Day》", "讚美之泉：《得勝的宣告》", "小羊詩歌：《復活.升天.大使命》"],
    ("Easter", "Second Sunday"): ["約書亞樂團：《耶穌基督》", "讚美之泉：《高舉雙手敬拜》", "小羊詩歌：《主,我相信》"],
    ("Easter", "Third Sunday"): ["約書亞樂團：《重來的力量》", "讚美之泉：《不管世界如何看我》", "小羊詩歌：《站起來》"],
    ("Easter", "Fourth Sunday"): ["約書亞樂團：《上帝能夠》", "讚美之泉：《敬拜耶穌》", "小羊詩歌：《祢與我同在》"],
    ("Easter", "Fifth Sunday"): ["約書亞樂團：《甦醒》", "讚美之泉：《我敬拜祢，耶穌》", "小羊詩歌：《有祢同行》"],
    ("Easter", "Sixth Sunday"): ["約書亞樂團：《跨越》", "讚美之泉：《我活著要稱頌祢》", "小羊詩歌：《與祢一起飛翔》"],
    ("Easter", "Seventh Sunday"): ["約書亞樂團：《基督是我滿足》", "讚美之泉：《與祢漫步》", "小羊詩歌：《誰能使我與神的愛隔絕》"],
    ("Easter", "Ascension"): ["約書亞樂團：《向列國宣告》", "讚美之泉：《爭戰得勝在於祢》", "小羊詩歌：《寶座》"],
    ("Easter", "Ascension of Our Lord"): ["約書亞樂團：《向列國宣告》", "讚美之泉：《爭戰得勝在於祢》", "小羊詩歌：《寶座》"],
    ("Easter", None): ["約書亞樂團：《榮美的救主》", "讚美之泉：《Mighty [祢愛有能力]》", "小羊詩歌：《我的靈要醒起》"],
    # Pentecost
    ("Pentecost", "Pentecost Sunday"): ["約書亞樂團：《降下你恩雨》", "讚美之泉：《有你在的地方》", "小羊詩歌：《點燃》"],
    ("Pentecost", None): ["約書亞樂團：《天國文化復興》", "讚美之泉：《Reach One More [再贏得一個靈魂]》", "小羊詩歌：《有一道河》"],
    # Ordinary Time / Special
    ("Ordinary Time", "Trinity Sunday"): ["約書亞樂團：《榮美輝煌》", "讚美之泉：《三一頌》", "小羊詩歌：《聖哉全能主》"],
    ("Ordinary Time", "Saints Triumphant"): ["約書亞樂團：《無價至寶》", "讚美之泉：《我是天父的孩子》", "小羊詩歌：《有福的人》"],
    ("Ordinary Time", "Last Judgment"): ["約書亞樂團：《直到世界盡頭》", "讚美之泉：《我們的神》", "小羊詩歌：《全能神永遠掌權》"],
    ("Ordinary Time", "Christ King"): ["約書亞樂團：《為著你的榮耀》", "讚美之泉：《耶和華作王》", "小羊詩歌：《神掌權》"],
    ("Ordinary Time", "Christ the King"): ["約書亞樂團：《為著你的榮耀》", "讚美之泉：《耶和華作王》", "小羊詩歌：《神掌權》"],
    ("Ordinary Time", "Reformation"): ["約書亞樂團：《恢復榮耀》", "讚美之泉：《我選擇喜樂》", "小羊詩歌：《耶和華我的山寨》"],
    ("Ordinary Time", "All Saints"): ["約書亞樂團：《我們獻上》", "讚美之泉：《謝謝你成為我的家》", "小羊詩歌：《眾山怎樣圍繞耶路撒冷》"],
    ("Ordinary Time", "Thanksgiving"): ["約書亞樂團：《恩典之流》", "讚美之泉：《獻上讚美祭》", "小羊詩歌：《陪我走過春夏秋冬》"],
    ("Ordinary Time", None): ["約書亞樂團：《牽手》", "讚美之泉：《不動搖的信心》", "小羊詩歌：《凡事都有神的美意》"]
}

# 補充常年期詩歌
proper_pool_joshua = ["全然為你", "與你更靠近", "竭力追求", "用信心宣告", "都指向祢", "我相信", "我獻上我心", "主你永遠與我同在", "直到世界盡頭", "安靜"]
proper_pool_sop = ["深愛耶穌", "謝謝你成為我的家", "我選擇喜樂", "與祢漫步", "那麼深的渴慕", "主啊，我們敬畏祢", "耶和華是應當稱頌的", "只願有耶穌", "好喜歡與你在一起", "不管世界如何看我", "我能給你什麼", "愛祢直到永遠", "數不盡", "我全然獻上", "我心堅定於祢", "深深地敬拜", "盡情地微笑", "頌讚歸於祢", "祢就是唯一", "獻上讚美祭"]
proper_pool_lamb = ["我心堅定於祢", "倚靠祢", "Faith Over Fear", "我知道祢愛我", "最愛的地方", "即或不然", "主的小羊", "祢是我的神", "天父的小花", "阿們", "真理的話語", "祢的居所何等可愛", "一路靠著祂", "祢歡喜的祭(台)", "詩篇二十三篇(台)", "我的最愛", "可喜悅的祭", "序曲(詩篇90篇1-2)", "主耶和華是我的幫助", "詩篇二十三篇"]

for i in range(1, 33):
    hymn_map[("Ordinary Time", f"Proper {i}")] = [
        f"約書亞樂團：《{proper_pool_joshua[i % len(proper_pool_joshua)]}》",
        f"讚美之泉：《{proper_pool_sop[i % len(proper_pool_sop)]}》",
        f"小羊詩歌：《{proper_pool_lamb[i % len(proper_pool_lamb)]}》"
    ]

# 補充五旬節詩歌
pentecost_pool_joshua = ["親愛聖靈", "求充滿這地", "聖靈請你來充滿我心", "溫柔聖靈", "點燃", "觸摸天堂"]
pentecost_pool_sop = ["不要忘記", "Stay [停留]", "披上讚美衣", "我揚聲敬拜", "曠野中唯一的力量", "當祢走進我們當中", "我在這裡", "愛祢，是我一生的呼召", "蒙恩", "讓我尋見祢", "和散那"]
pentecost_pool_lamb = ["看哪,田裡莊稼成熟了", "與我同往", "祢是我的平安", "祢是我的平安 Live", "因我所遭遇的是出於祢", "祢的恩典夠我用", "父啊,我向祢呼求", "我欲等候耶和華(台)"]

num_to_word_map = {
    1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
    6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth",
    11: "Eleventh", 12: "Twelfth", 13: "Thirteenth", 14: "Fourteenth",
    15: "Fifteenth", 16: "Sixteenth", 17: "Seventeenth", 18: "Eighteenth",
    19: "Nineteenth", 20: "Twentieth", 21: "Twenty-first", 22: "Twenty-second",
    23: "Twenty-third", 24: "Twenty-fourth", 25: "Twenty-fifth",
    26: "Twenty-sixth", 27: "Twenty-seventh", 28: "Twenty-eighth",
    29: "Twenty-ninth", 30: "Thirtieth"
}

for i in range(1, 31):
    word_key = f"{num_to_word_map[i]} Sunday"
    hymns = [
        f"約書亞樂團：《{pentecost_pool_joshua[i % len(pentecost_pool_joshua)]}》",
        f"讚美之泉：《{pentecost_pool_sop[i % len(pentecost_pool_sop)]}》",
        f"小羊詩歌：《{pentecost_pool_lamb[i % len(pentecost_pool_lamb)]}》"
    ]
    hymn_map[("Pentecost", word_key)] = hymns
    hymn_map[("Pentecost", f"Pentecost {i}")] = hymns

hymn_map[("Epiphany", "Sixth Sunday after Epiphany")] = hymn_map.get(("Epiphany", "Sixth Sunday"), [])
hymn_map[("Epiphany", "Seventh Sunday after Epiphany")] = hymn_map.get(("Epiphany", "Seventh Sunday"), [])
hymn_map[("Epiphany", "Eighth Sunday after Epiphany")] = hymn_map.get(("Epiphany", "Eighth Sunday"), [])
hymn_map[("Epiphany", "Ninth Sunday after Epiphany")] = hymn_map.get(("Epiphany", "Ninth Sunday"), [])

# RCL 補漏經文
scripture_patch = {
    "A": {
        ("Advent", "First Sunday in Advent"): ["以賽亞書 2:1-5", "詩篇 122", "羅馬書 13:11-14", "馬太福音 24:36-44"],
        ("Epiphany", "Fifth Sunday after Epiphany"): ["以賽亞書 58:1-9a, (9b-12)", "詩篇 112:1-9, (10)", "哥林多前書 2:1-12, (13-16)", "馬太福音 5:13-20"],
        ("Epiphany", "Sixth Sunday after Epiphany"): ["申命記 30:15-20", "詩篇 119:1-8", "哥林多前書 3:1-9", "馬太福音 5:21-37"],
        ("Epiphany", "Seventh Sunday after Epiphany"): ["利未記 19:1-2, 9-18", "詩篇 119:33-40", "哥林多前書 3:10-11, 16-23", "馬太福音 5:38-48"],
        ("Epiphany", "Eighth Sunday after Epiphany"): ["以賽亞書 49:8-16a", "詩篇 131", "哥林多前書 4:1-5", "馬太福音 6:24-34"],
        ("Epiphany", "Ninth Sunday after Epiphany"): ["創世記 6:9-22; 8:14-19", "詩篇 46", "羅馬書 1:16-17; 3:22b-28", "馬太福音 7:21-29"],
        ("Ordinary Time", "Trinity Sunday"): ["創世記 1:1-2:4a", "詩篇 8", "哥林多後書 13:11-13", "馬太福音 28:16-20"],
        ("Ordinary Time", "Proper 1"): ["申命記 30:15-20", "詩篇 119:1-8", "哥林多前書 3:1-9", "馬太福音 5:21-37"],
        ("Ordinary Time", "Proper 2"): ["利未記 19:1-2, 9-18", "詩篇 119:33-40", "哥林多前書 3:10-11, 16-23", "馬太福音 5:38-48"],
        ("Ordinary Time", "Proper 3"): ["以賽亞書 49:8-16a", "詩篇 131", "哥林多前書 4:1-5", "馬太福音 6:24-34"],        
        ("Ordinary Time", "Proper 4"): ["創世記 6:9-22; 8:14-19", "詩篇 46", "羅馬書 1:16-17; 3:22b-28", "馬太福音 7:21-29"],
        ("Ordinary Time", "Proper 5"): ["創世記 12:1-9", "詩篇 33:1-12", "羅馬書 4:13-25", "馬太福音 9:9-13, 18-26"],
        ("Ordinary Time", "Proper 25"): ["申命記 34:1-12", "詩篇 90:1-6, 13-17", "帖撒羅尼迦前書 2:1-8", "馬太福音 22:34-46"],
        ("Ordinary Time", "Proper 26"): ["約書亞記 3:7-17", "詩篇 107:1-7, 33-37", "帖撒羅尼迦前書 2:9-13", "馬太福音 23:1-12"],
        ("Ordinary Time", "Proper 28"): ["西番雅書 1:7, 12-18", "詩篇 90:1-8, 12", "帖撒羅尼迦前書 5:1-11", "馬太福音 25:14-30"],
        ("Ordinary Time", "Christ the King"): ["以西結書 34:11-16, 20-24", "詩篇 100", "以弗所書 1:15-23", "馬太福音 25:31-46"],
        ("Ordinary Time", "Proper 29"): ["以西結書 34:11-16, 20-24", "詩篇 100", "以弗所書 1:15-23", "馬太福音 25:31-46"],
        ("Ordinary Time", "Proper 30"): ["以西結書 34:11-16, 20-24", "詩篇 100", "以弗所書 1:15-23", "馬太福音 25:31-46"],
        ("Ordinary Time", "Proper 31"): ["以西結書 34:11-16, 20-24", "詩篇 100", "以弗所書 1:15-23", "馬太福音 25:31-46"],
        ("Christmas", "Christmas Day"): [
            "【救主聖誕日 - 崇拜 I】", "以賽亞書 9:2-7", "詩篇 96", "提多書 2:11-14", "路加福音 2:1-14", "",
            "【救主聖誕日 - 崇拜 II】", "以賽亞書 62:6-12", "詩篇 97", "提多書 3:4-7", "路加福音 2:8-20", "",
            "【救主聖誕日 - 崇拜 III】", "以賽亞書 52:7-10", "詩篇 98", "希伯來書 1:1-12", "約翰福音 1:1-14"
        ]
    },
    "B": {
        ("Epiphany", "Fifth Sunday after Epiphany"): ["以賽亞書 40:21-31", "詩篇 147:1-11, 20c", "哥林多前書 9:16-23", "馬可福音 1:29-39"],
        ("Epiphany", "Sixth Sunday after Epiphany"): ["列王紀下 5:1-14", "詩篇 30", "哥林多前書 9:24-27", "馬可福音 1:40-45"],
        ("Epiphany", "Seventh Sunday after Epiphany"): ["以賽亞書 43:18-25", "詩篇 41", "哥林多後書 1:18-22", "馬可福音 2:1-12"],
        ("Epiphany", "Eighth Sunday after Epiphany"): ["何西阿書 2:14-20", "詩篇 103:1-13, 22", "哥林多後書 3:1-6", "馬可福音 2:13-22"],
        ("Epiphany", "Ninth Sunday after Epiphany"): ["申命記 5:12-15", "詩篇 81:1-10", "哥林多後書 4:5-12", "馬可福音 2:23-3:6"],
        ("Ordinary Time", "Trinity Sunday"): ["以賽亞書 6:1-8", "詩篇 29", "羅馬書 8:12-17", "約翰福音 3:1-17"],
        ("Ordinary Time", "Proper 1"): ["列王紀下 5:1-14", "詩篇 30", "哥林多前書 9:24-27", "馬可福音 1:40-45"],
        ("Ordinary Time", "Proper 2"): ["以賽亞書 43:18-25", "詩篇 41", "哥林多後書 1:18-22", "馬可福音 2:1-12"],
        ("Ordinary Time", "Proper 3"): ["何西阿書 2:14-20", "詩篇 103:1-13, 22", "哥林多後書 3:1-6", "馬可福音 2:13-22"],
        ("Ordinary Time", "Proper 4"): ["申命記 5:12-15", "詩篇 81:1-10", "哥林多後書 4:5-12", "馬可福音 2:23-3:6"],
        ("Ordinary Time", "Proper 5"): ["撒母耳記上 8:4-11, 16-20", "詩篇 138", "哥林多後書 4:13-5:1", "馬可福音 3:20-35"],
        ("Ordinary Time", "Proper 25"): ["約伯記 42:1-6, 10-17", "詩篇 34:1-8, 19-22", "希伯來書 7:23-28", "馬可福音 10:46-52"],
        ("Ordinary Time", "Proper 26"): ["路得記 1:1-18", "詩篇 146", "希伯來書 9:11-14", "馬可福音 12:28-34"],
        ("Ordinary Time", "Proper 28"): ["但以理書 12:1-3", "詩篇 16", "希伯來書 10:11-14, 19-25", "馬可福音 13:1-8"],
        ("Ordinary Time", "Christ the King"): ["撒母耳記下 23:1-7", "詩篇 132:1-12", "啟示錄 1:4b-8", "約翰福音 18:33-37"],
        ("Ordinary Time", "Proper 29"): ["撒母耳記下 23:1-7", "詩篇 132:1-12", "啟示錄 1:4b-8", "約翰福音 18:33-37"],
        ("Ordinary Time", "Proper 30"): ["撒母耳記下 23:1-7", "詩篇 132:1-12", "啟示錄 1:4b-8", "約翰福音 18:33-37"],
        ("Ordinary Time", "Proper 31"): ["撒母耳記下 23:1-7", "詩篇 132:1-12", "啟示錄 1:4b-8", "約翰福音 18:33-37"],
        ("Christmas", "Christmas Day"): [
            "【救主聖誕日 - 崇拜 I】", "以賽亞書 9:2-7", "詩篇 96", "提多書 2:11-14", "路加福音 2:1-14", "",
            "【救主聖誕日 - 崇拜 II】", "以賽亞書 62:6-12", "詩篇 97", "提多書 3:4-7", "路加福音 2:8-20", "",
            "【救主聖誕日 - 崇拜 III】", "以賽亞書 52:7-10", "詩篇 98", "希伯來書 1:1-12", "約翰福音 1:1-14"
        ]
    },
    "C": {
        ("Epiphany", "Fifth Sunday after Epiphany"): ["以賽亞書 6:1-8, (9-13)", "詩篇 138", "哥林多前書 15:1-11", "路加福音 5:1-11"],
        ("Epiphany", "Sixth Sunday after Epiphany"): ["耶利米書 17:5-10", "詩篇 1", "哥林多前書 15:12-20", "路加福音 6:17-26"],
        ("Epiphany", "Seventh Sunday after Epiphany"): ["創世記 45:3-11, 15", "詩篇 37:1-11, 39-40", "哥林多前書 15:35-38, 42-50", "路加福音 6:27-38"],
        ("Epiphany", "Eighth Sunday after Epiphany"): ["以賽亞書 55:10-13", "詩篇 92:1-4, 12-15", "哥林多前書 15:51-58", "路加福音 6:39-49"],
        ("Epiphany", "Ninth Sunday after Epiphany"): ["列王紀上 8:22-23, 41-43", "詩篇 96:1-9", "加拉太書 1:1-12", "路加福音 7:1-10"],
        ("Ordinary Time", "Trinity Sunday"): ["箴言 8:1-4, 22-31", "詩篇 8", "羅馬書 5:1-5", "約翰福音 16:12-15"],
        ("Ordinary Time", "Proper 1"): ["耶利米書 17:5-10", "詩篇 1", "哥林多前書 15:12-20", "路加福音 6:17-26"],
        ("Ordinary Time", "Proper 2"): ["創世記 45:3-11, 15", "詩篇 37:1-11, 39-40", "哥林多前書 15:35-38, 42-50", "路加福音 6:27-38"],
        ("Ordinary Time", "Proper 3"): ["以賽亞書 55:10-13", "詩篇 92:1-4, 12-15", "哥林多前書 15:51-58", "路加福音 6:39-49"],
        ("Ordinary Time", "Proper 4"): ["列王紀上 8:22-23, 41-43", "詩篇 96:1-9", "加拉太書 1:1-12", "路加福音 7:1-10"],
        ("Ordinary Time", "Proper 5"): ["列王紀上 17:8-16", "詩篇 146", "加拉太書 1:11-24", "路加福音 7:11-17"],
        ("Ordinary Time", "Proper 25"): ["約珥書 2:23-32", "詩篇 65", "提摩太後書 4:6-8, 16-18", "路加福音 18:9-14"],
        ("Ordinary Time", "Proper 26"): ["哈巴谷書 1:1-4; 2:1-4", "詩篇 119:137-144", "帖撒羅尼迦後書 1:1-4, 11-12", "路加福音 19:1-10"],
        ("Ordinary Time", "Proper 28"): ["瑪拉基書 4:1-2a", "詩篇 98", "帖撒羅尼迦後書 3:6-13", "路加福音 21:5-19"],
        ("Ordinary Time", "Christ the King"): ["耶利米書 23:1-6", "詩篇 46", "歌羅西書 1:11-20", "路加福音 23:33-43"],
        ("Ordinary Time", "Proper 29"): ["耶利米書 23:1-6", "詩篇 46", "歌羅西書 1:11-20", "路加福音 23:33-43"],
        ("Ordinary Time", "Proper 30"): ["耶利米書 23:1-6", "詩篇 46", "歌羅西書 1:11-20", "路加福音 23:33-43"],
        ("Ordinary Time", "Proper 31"): ["耶利米書 23:1-6", "詩篇 46", "歌羅西書 1:11-20", "路加福音 23:33-43"],
        ("Christmas", "Christmas Day"): [
            "【救主聖誕日 - 崇拜 I】", "以賽亞書 9:2-7", "詩篇 96", "提多書 2:11-14", "路加福音 2:1-14", "",
            "【救主聖誕日 - 崇拜 II】", "以賽亞書 62:6-12", "詩篇 97", "提多書 3:4-7", "路加福音 2:8-20", "",
            "【救主聖誕日 - 崇拜 III】", "以賽亞書 52:7-10", "詩篇 98", "希伯來書 1:1-12", "約翰福音 1:1-14"
        ]
    }
}

classical_hymns_map = {
    ("Advent", "First Sunday"): {"All": ["Savior of the nations, come"]},
    ("Advent", "Second Sunday"): {"All": ["On Jordan's bank the Baptist's cry", "Lo! He comes with clouds descending"]},
    ("Advent", "Third Sunday"): {"All": ["Hark! A thrilling voice is sounding"]},
    ("Advent", "Fourth Sunday"): {"All": ["O come, O come, Emmanuel"]},
    ("Christmas", "Christmas Eve"): {"All": ["Lo, how a rose e'er blooming"]},
    ("Christmas", "Christmas Day"): {"All": ["We praise You, Jesus, at Your birth"]},
    ("Christmas", "First Sunday"): {"All": ["Let all together praise our God"]},
    ("Christmas", "Second Sunday"): {"All": ["Within the Father's house", "From east to west"]},
    ("Epiphany", "Epiphany"): {"All": ["O Morning Star, how fair and bright"]},
    ("Epiphany", "First Sunday"): {"All": ["To Jordan came the Christ, our Lord"]},
    ("Epiphany", "Second Sunday"): {"All": ["The only Son from heaven"]},
    ("Epiphany", "Third Sunday"): {"All": ["O Christ, our true and only light", "From God the Father, virgin-born"]},
    ("Epiphany", "Fourth Sunday"): {"All": ["Son of God, eternal Savior", "Seek where you may to find a way"]},
    ("Epiphany", "Fifth Sunday"): {"A": ["Thy strong word did cleave the darkness"], "B": ["Hail to the Lord's anointed"], "C": ["Hail to the Lord's anointed"]},
    ("Epiphany", "Sixth Sunday"): {"All": ["Songs of thankfulness and praise"]},
    ("Epiphany", "Seventh Sunday"): {"All": ["My soul, now praise your Maker", "O God, O Lord of heaven and earth"]},
    ("Epiphany", "Eighth Sunday"): {"All": ["Sing praise to God, the highest good"]},
    ("Epiphany", "Transfiguration"): {"All": ["O wondrous type! O vision fair"]},
    ("Epiphany", "Last Sunday"): {"All": ["O wondrous type! O vision fair"]},
    ("Lent", "Ash Wednesday"): {"All": ["From depths of woe I cry to Thee"]},
    ("Lent", "First Sunday"): {"All": ["A mighty fortress is our God"]},
    ("Lent", "Second Sunday"): {"All": ["Lord, Thee I love with all my heart", "When in the hour of deepest need"]},
    ("Lent", "Third Sunday"): {"All": ["May God bestow on us His grace", "Lord of our life and God of our salvation"]},
    ("Lent", "Fourth Sunday"): {"All": ["God loved the world so that He gave", "I trust, O Christ, in You alone", "Jesus, priceless treasure"]},
    ("Lent", "Fifth Sunday"): {"All": ["My song is love unknown"]},
    ("Holy Week", "Palm Sunday"): {"All": ["All glory, laud, and honor", "A Lamb goes uncomplaining forth"]},
    ("Holy Week", "Maundy Thursday"): {"All": ["O Lord, we praise Thee"]},
    ("Holy Week", "Good Friday"): {"All": ["Sing, my tongue, the glorious battle"]},
    ("Easter", "Easter Sunday"): {"All": ["Awake, my heart, with gladness", "Christ Jesus lay in death's strong bands"]},
    ("Easter", "Second Sunday"): {"All": ["O sons and daughters of the King"]},
    ("Easter", "Third Sunday"): {"All": ["With high delight let us unite", "The King of love my shepherd is"]},
    ("Easter", "Fourth Sunday"): {"All": ["The King of love my shepherd is", "With high delight let us unite"]},
    ("Easter", "Fifth Sunday"): {"All": ["At the Lamb's high feast we sing", "Dear Christians, one and all, rejoice"]},
    ("Easter", "Sixth Sunday"): {"All": ["Dear Christians, one and all, rejoice", "Our Father, who from heav'n above"]},
    ("Easter", "Seventh Sunday"): {"All": ["Christ is the world's Redeemer"]},
    ("Easter", "Ascension"): {"All": ["Up through endless ranks of angels"]},
    ("Pentecost", "Pentecost Sunday"): {"All": ["Come, Holy Ghost, God and Lord"]},
    ("Ordinary Time", "Trinity Sunday"): {"All": ["Come, Holy Ghost, Creator blest"]},
    ("Ordinary Time", "Christ the King"): {"A": ["The Head that once was crowned with thorns"], "B": ["Lo! He comes with clouds descending"], "C": ["Lord, enthroned in heav'nly splendor"]},
    ("Ordinary Time", "Reformation"): {"All": ["A mighty fortress is our God", "Salvation unto us has come"]},
    ("Ordinary Time", "All Saints"): {"All": ["For all the saints who from their labors rest"]},
    ("Ordinary Time", "Holy Cross"): {"All": ["Sing, my tongue, the glorious battle", "The royal banners forward go"]},
    ("Ordinary Time", "Proper 3"): {"A": ["All depends on our possessing"], "B": ["Sing praise to God, the highest good"], "C": ["O God, my faithful God"]},
    ("Ordinary Time", "Proper 4"): {"A": ["To God the Holy Spirit let us pray"], "B": ["O day of rest and gladness"], "C": ["In the very midst of life"]},
    ("Ordinary Time", "Proper 5"): {"A": ["Let me be Thine forever"], "B": ["Rise! To arms! With prayer employ you"], "C": ["When in the hour of deepest need"]},
    ("Ordinary Time", "Proper 6"): {"All": ["O God, O Lord of heaven and earth"], "A": ["God loved the world so that He gave"], "B": ["Creator Spirit, by whose aid"], "C": ["Today Your mercy calls us"]},
    ("Ordinary Time", "Proper 7"): {"A": ["Lord of our life and God of our salvation"], "B": ["Evening and morning"], "C": ["Rise, shine, you people"]},
    ("Ordinary Time", "Proper 8"): {"A": ["Let us ever walk with Jesus"], "B": ["In the very midst of life"], "C": ["\"Come, follow Me,\" the Savior spake"]},
    ("Ordinary Time", "Proper 9"): {"A": ["I heard the voice of Jesus say"], "B": ["O Christ, our true and only light"], "C": ["Jesus has come and brings pleasure eternal"]},
    ("Ordinary Time", "Proper 10"): {"A": ["Almighty God, Your Word is cast"], "B": ["Jesus, priceless treasure"], "C": ["Where charity and love prevail"]},
    ("Ordinary Time", "Proper 11"): {"A": ["In holy conversation"], "B": ["The Church's one foundation"], "C": ["One thing's needful; Lord, this treasure"]},
    ("Ordinary Time", "Proper 12"): {"A": ["From God can nothing move me"], "B": ["Entrust your days and burdens"], "C": ["Our Father, who from heav'n above"]},
    ("Ordinary Time", "Proper 13"): {"A": ["O living Bread from heaven"], "B": ["Guide me, O Thou great Redeemer"], "C": ["Gracious God, You send great blessings"]},
    ("Ordinary Time", "Proper 14"): {"A": ["Eternal Father, strong to save"], "B": ["Lord, enthroned in heav'nly splendor"], "C": ["O little flock, fear not the foe"]},
    ("Ordinary Time", "Proper 15"): {"A": ["In Christ there is no east or west", "When in the hour of deepest need"], "B": ["O God, my faithful God", "Lord of all hopefulness"], "C": ["Lord, keep steadfast in Your Word", "From God can nothing move me"]},
    ("Ordinary Time", "Proper 16"): {"A": ["Built on the Rock the Church shall stand"], "B": ["Lord, help us ever to retain"], "C": ["A multitude comes from the east and the west"]},
    ("Ordinary Time", "Proper 17"): {"A": ["Hail, Thou once despised Jesus"], "B": ["By grace I'm saved, grace free and boundless"], "C": ["Son of God, eternal Savior"]},
    ("Ordinary Time", "Proper 18"): {"A": ["My soul, now praise your Maker"], "B": ["Praise the Almighty, my soul, adore Him"], "C": ["How clear is our vocation, Lord"]},
    ("Ordinary Time", "Proper 19"): {"A": ["Come down, O Love divine"], "B": ["Praise the One who breaks the darkness"], "C": ["Jesus sinners doth receive"]},
    ("Ordinary Time", "Proper 20"): {"A": ["Salvation unto us has come"], "B": ["Lord of glory, You have bought us"], "C": ["Seek where you may to find a way"]},
    ("Ordinary Time", "Proper 21"): {"A": ["Lord, keep steadfast in Your Word"], "B": ["Triune God, be Thou our stay"], "C": ["Lord, Thee I love with all my heart"]},
    ("Ordinary Time", "Proper 22"): {"A": ["O love, how deep, how broad, how high"], "B": ["Our Father, by whose name"], "C": ["I know my faith is founded"]},
    ("Ordinary Time", "Proper 23"): {"A": ["A multitude comes from the east and the west"], "B": ["Thee will I love, my strength, my tower"], "C": ["Your hand, O Lord, in days of old"]},
    ("Ordinary Time", "Proper 24"): {"A": ["Holy God, we praise Thy name"], "B": ["Hope of the world, Thou Christ of great compassion"], "C": ["I trust, O Lord, Your holy name"]},
    ("Ordinary Time", "Proper 25"): {"A": ["I want to walk as a child of the light", "The Law of God is good and wise"], "B": ["From God can nothing move me"], "C": ["In God, my faithful God"]},
    ("Ordinary Time", "Proper 26"): {"A": ["Lord Jesus Christ, with us abide"], "B": ["O God of mercy, God of might"], "C": ["How firm a foundation, O saints of the Lord"]},
    ("Ordinary Time", "Proper 27"): {"A": ["Wake, awake, for night is flying"], "B": ["Lord of all hopefulness"], "C": ["From God can nothing move me"]},
    ("Ordinary Time", "Proper 28"): {"All": ["The day is surely drawing near"]},
    ("Ordinary Time", "Proper 29"): {"A": ["The Head that once was crowned with thorns"], "B": ["Lo! He comes with clouds descending"], "C": ["Lord, enthroned in heav'nly splendor"]}
}

# =====================================================================
# 2. 輔助處理與計算函式 (Helper Functions)
# =====================================================================

def get_scripture_links(line):
    def replace_match(m):
        full_text = m.group(0)
        book_zh = m.group(1)
        chapter = m.group(2)
        verses_raw = m.group(3)
        wdb_code = wdb_book_map.get(book_zh)
        if wdb_code:
            url = f"https://wdbible.com/tw/bible/{wdb_code}.{chapter}.cunpt"
            if verses_raw:
                v_match = re.search(r'\d+(?:-\d+)?', verses_raw)
                if v_match:
                    url += f"#{v_match.group(0)}"
            return f'<a href="{url}" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.color=\'#2563eb\'" onmouseout="this.style.color=\'inherit\'">{full_text}</a>'
        else:
            fallback_url = f"https://wdbible.com/search?q={urllib.parse.quote(full_text)}"
            return f'<a href="{fallback_url}" target="_blank" style="color: inherit; text-decoration: none;">{full_text}</a>'
    pattern = r"([\u4e00-\u9fa5]+)\s*(\d+)(?::([\d\-a-z, \(\)]+))?"
    return re.sub(pattern, replace_match, line)

def replace_with_map(text: str, mapping: dict) -> str:
    text = text.strip()
    for eng, zh in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
        text = re.sub(re.escape(eng), zh, text, flags=re.IGNORECASE)
    return text
    
def replace_season_num(m):
    season_name = m.group(1)
    num_str = m.group(2)
    zh_num = arabic_to_zh.get(num_str, num_str)
    return f"{season_name}第{zh_num}主日"

def translate_summary(summary: str) -> str:
    corrections = {
        r"\bTwelth\b": "Twelfth", r"\bFourtheenth\b": "Fourteenth",
        r"\bTwent[- ]?first\b": "Twenty-first", r"Easter Sunday\s*[-－–—]\s*Dawn": "Easter Dawn",
        r"\bProepr\b": "Proper"
    }
    for wrong, right in corrections.items():
        summary = re.sub(wrong, right, summary, flags=re.IGNORECASE)

    summary = re.sub(r"\b(Twenty|Thirty)[-－–—](first|second|third|fourth|fifth|sixth|seventh|eighth|ninth)\b", r"\1_NUM_HYPHEN_\2", summary, flags=re.IGNORECASE)
    parts = re.split(r"\s*[－–—-]\s*", summary)
    if len(parts) > 1:
        translated_parts = [translate_summary(p.strip().replace("_NUM_HYPHEN_", "-")) for p in parts]
        return "－".join(translated_parts)

    summary = summary.replace("_NUM_HYPHEN_", "-")
    summary = replace_with_map(summary, season_map)    
    
    match = re.search(r"\(Proper\s+(\d+)\)", summary, flags=re.IGNORECASE) 
    if match: 
        proper_num = match.group(1) 
        zh_num = arabic_to_zh.get(proper_num, proper_num)
        summary = summary.replace(match.group(0), f"(常年期第{zh_num}組經課)")    
        
    match_plain = re.search(r"Proper\s+(\d+)", summary, flags=re.IGNORECASE)
    if match_plain:
        proper_num = match_plain.group(1)
        zh_num = arabic_to_zh.get(proper_num, proper_num)
        return f"常年期第{zh_num}組經課"

    match = re.match(r"(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Twenty-first|Twenty-second|Twenty-third|Twenty-fourth|Twenty-fifth|Twenty-sixth|Twenty-seventh|Twenty-eighth|Twenty-ninth|Thirtieth)\s+Sunday\s+in\s+(.+)", summary, flags=re.IGNORECASE)
    if match:
        ordinal, season = match.groups()
        zh_ordinal = ordinal_map.get(ordinal.capitalize(), ordinal)
        season_zh = season_map.get(season.strip(), season.strip())
        return f"{season_zh}{zh_ordinal}主日"

    match = re.match(r"(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Twenty-first|Twenty-second|Twenty-third|Twenty-fourth|Twenty-fifth|Twenty-sixth|Twenty-seventh|Twenty-eighth|Twenty-ninth|Thirtieth)\s+Sunday\s+after\s+(.+)", summary, flags=re.IGNORECASE)
    if match:
        ordinal, season = match.groups()
        zh_ordinal = ordinal_map.get(ordinal.capitalize(), ordinal)
        season_zh = season_map.get(season.strip(), season.strip())
        return f"{season_zh}後{zh_ordinal}主日"

    match = re.match(r"(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Twenty-first|Twenty-second|Twenty-third|Twenty-fourth|Twenty-fifth|Twenty-sixth|Twenty-seventh|Twenty-eighth|Twenty-ninth|Thirtieth)\s+Sunday\s+of\s+(.+)", summary, flags=re.IGNORECASE)
    if match:
        ordinal, season = match.groups()
        zh_ordinal = ordinal_map.get(ordinal.capitalize(), ordinal)
        season_zh = season_map.get(season.strip(), season.strip())
        return f"{season_zh}{zh_ordinal}主日"

    match = re.match(r"Last Sunday after (.+)", summary, flags=re.IGNORECASE)
    if match:
        season = match.group(1).strip()
        season_zh = season_map.get(season, season)
        return f"{season_zh}後最後一主日"

    match = re.match(r"(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Twenty-first|Twenty-second|Twenty-third|Twenty-fourth|Twenty-fifth|Twenty-sixth|Twenty-seventh|Twenty-eighth|Twenty-ninth|Thirtieth)\s+Sunday$", summary, flags=re.IGNORECASE)
    if match:
        ordinal = match.group(1)
        zh_ordinal = ordinal_map.get(ordinal.capitalize(), ordinal)
        return f"{zh_ordinal}主日"

    summary = re.sub(r"(聖靈降臨期|將臨期|聖誕期|顯現期|預苦期|復活期|常年期)\s+(\d+)", replace_season_num, summary)
    return summary

def translate_text(text, cycle_label=None, season=None, sunday=None):
    if not text: return ""
    text = text.strip().lstrip("\ufeff")
    text = re.sub(r"1\s*Corthnians", "1 Corinthians", text, flags=re.IGNORECASE)
    text = re.sub(r"\bthe\b", "", text, flags=re.IGNORECASE)

    def fix_supplemental(match):
        block = match.group(0)
        lines = block.splitlines()
        new_lines = []
        for line in lines:
            if "Supplemental Lectionary" in line:
                new_lines.append("補充經課:")
            elif line.strip(): 
                new_lines.append(replace_with_map(line.strip(), book_map))
        return "\n".join(new_lines)

    text = re.sub(r"Supplemental Lectionary:[\s\S]*?(?=\n[A-Za-z ]+:|\nPrayer|\nColor:|\Z)", fix_supplemental, text, flags=re.IGNORECASE)
    text = re.sub(r"Prayer of the Day:[\s\S]*?(?=Color:)", "Color:", text, flags=re.IGNORECASE)

    sunday_map = {"First": "第一", "Second": "第二", "Third": "第三", "Fourth": "第四", "Fifth": "第五", "Sixth": "第六", "Seventh": "第七", "Last": "最後一"}
    for eng_num, zh_num in sunday_map.items():
        text = re.sub(rf"{eng_num}\s+Sunday\s+after\s+(\w+)", rf"\1後{zh_num}主日", text, flags=re.IGNORECASE)

    text = re.sub(r"(\d+:\d+)\s*[-－–—]\s*(\d+(:\d+)?[a-z]?)", r"\1-\2", text)
    text = re.sub(r"[－–—]", "-", text)

    special_titles = {"Transfiguration of Our Lord": "登山變像日", "The Baptism of Our Lord": "主受洗日", "Baptism of Our Lord": "主受洗日", "Epiphany of Our Lord": "主顯節", "Holy Trinity": "三一主日", "Resurrection of our Lord": "耶穌基督復活了！"}
    text = replace_with_map(text, special_titles)

    match = re.search(r"Color:\s*(\w+)", text)
    if match:
        eng_color = match.group(1)
        zh_color = color_map.get(eng_color, eng_color)
        text = re.sub(r"Color:\s*\w+", f"代表顏色: {zh_color}", text)

    text = replace_with_map(text, phrase_map)
    text = replace_with_map(text, {**season_map, **book_map, **ordinal_map})
    return text
    
def parse_summary(summary_text):
    summary_text = summary_text.strip()
    summary_text = re.sub(r'\s*\(Year [ABC]\)', '', summary_text, flags=re.IGNORECASE)
    summary_text = re.sub(r'(Proper\s+\d+)\s*\(\d+\)', r'\1', summary_text, flags=re.IGNORECASE)
    summary_text = summary_text.replace("Reign of Christ - ", "").replace("Proepr", "Proper").replace("Ephphany", "Epiphany")
    
    parts = summary_text.split()
    if parts and parts[-1] in ("A", "B", "C"):
        raw_summary = " ".join(parts[:-1])
    else:
        raw_summary = summary_text

    if "Resurrection" in raw_summary: return "Easter", "Easter Sunday", "復活節"
    if "Palms" in raw_summary or "Palm Sunday" in raw_summary: return "Holy Week", "Palm Sunday", "棕枝主日"
    if "Passion" in raw_summary: return "Holy Week", "Passion Sunday", "受難主日"    
    if "Ascension" in raw_summary: return "Easter", "Ascension", "基督升天日" 
    if "Reformation" in raw_summary: return "Ordinary Time", "Reformation", "宗教改革日"
    if "Palm Sunday" in raw_summary or "Passion" in raw_summary: return "Holy Week", "Palm Sunday", "棕枝主日"
    if "Transfiguration" in raw_summary: return "Epiphany", "Transfiguration", "登山變像主日" 
    if "Trinity" in raw_summary: return "Ordinary Time", "Trinity Sunday", "三一主日"
    if "All Saints" in raw_summary: return "Ordinary Time", "All Saints", "古聖紀念日" 
    if "Christ the King" in raw_summary or ("Last Sunday" in raw_summary and "Church Year" in raw_summary): return "Ordinary Time", "Christ the King", "基督君王主日"
    if "Ash Wednesday" in raw_summary: return "Lent", "Ash Wednesday", "聖灰日"
    if "Maundy" in raw_summary or "Holy Thursday" in raw_summary: return "Holy Week", "Maundy Thursday", "主立聖餐日" 
    if "Good Friday" in raw_summary: return "Holy Week", "Good Friday", "受難日"
    if "Easter Vigil" in raw_summary: return "Easter", "Easter Vigil", "復活前夕守夜"
    if "Baptism" in raw_summary: return "Epiphany", "First Sunday", "耶穌受洗主日" 
    if "Holy Name" in raw_summary: return "Christmas", "Holy Name", "耶穌聖名日"
    if "New Year" in raw_summary: return "Christmas", "New Year", "新年"
    if "Presentation" in raw_summary: return "Epiphany", "Presentation", "主奉獻日"
    if "Annunciation" in raw_summary: return "Lent", "Annunciation", "天使報喜日"
    if "Visitation" in raw_summary: return "Easter", "Visitation", "馬利亞探望伊利沙伯"
    if "Holy Cross" in raw_summary: return "Ordinary Time", "Holy Cross", "聖十字架日"
    if "Thanksgiving" in raw_summary: return "Ordinary Time", "Thanksgiving", "感恩節"
    if "Monday of Holy Week" in raw_summary: return "Holy Week", "Monday of Holy Week", "聖週一"
    if "Tuesday of Holy Week" in raw_summary: return "Holy Week", "Tuesday of Holy Week", "聖週二"
    if "Wednesday of Holy Week" in raw_summary: return "Holy Week", "Wednesday of Holy Week", "聖週三"
    if "Holy Saturday" in raw_summary: return "Holy Week", "Holy Saturday", "聖週六"

    match_proper = re.search(r"Proper\s+(\d+)", raw_summary, flags=re.IGNORECASE)
    normalized = f"Proper {match_proper.group(1)}" if match_proper else summary_map.get(raw_summary, raw_summary)

    if "Advent" in raw_summary: season = "Advent"
    elif "Christmas" in raw_summary: season = "Christmas"
    elif "Epiphany" in raw_summary or "Baptism" in raw_summary or "Transfiguration" in raw_summary: season = "Epiphany"
    elif "Lent" in raw_summary or raw_summary in ("Ash Wednesday", "Palm Sunday", "Good Friday", "Maundy Thursday", "Holy Saturday"): season = "Lent" if "Lent" in raw_summary else "Holy Week"
    elif "Easter" in raw_summary or raw_summary == "Ascension": season = "Easter"
    elif "Pentecost" in raw_summary: season = "Pentecost"
    elif "Ordinary" in raw_summary or "Proper" in raw_summary or "Trinity" in raw_summary or raw_summary == "Christ the King": season = "Ordinary Time"
    elif raw_summary == "Last Sunday in the Church Year": season, normalized = "Ordinary Time", "Christ the King"
    elif raw_summary == "Thanksgiving": season, normalized = "Ordinary Time", "Thanksgiving"
    else: season = None

    return season, normalized, translate_summary(normalized)

def get_advent_start(year):
    date = datetime.date(year, 11, 27)
    while date.weekday() != 6: date += datetime.timedelta(days=1)
    return date

def get_cycle_label(date):
    if isinstance(date, datetime.datetime): date = date.date()
    advent_start = get_advent_start(date.year)
    liturgical_year = date.year - 1 if date < advent_start else date.year
    return ["A", "B", "C"][(liturgical_year - 2025) % 3]
    
def get_hymn_text(summary: str, date: datetime.date = None) -> str:
    season, sunday, _ = parse_summary(summary)
    if "Proper" in sunday: season = "Ordinary Time"
        
    if season == "Easter" and any(k in summary for k in ["Resurrection", "Easter Day", "Easter Dawn", "Easter Evening", "Easter Vigil"]): sunday = "Easter Sunday"
    if season == "Christmas" and "Nativity" in summary: sunday = "Christmas Eve" if "Eve" in summary else "Christmas Day"
    if season == "Epiphany" and "Epiphany of" in summary: sunday = "Epiphany"
    if season == "Pentecost" and "Day of Pentecost" in summary: sunday = "Pentecost Sunday"

    s_lower = summary.lower()
    if "holy name" in s_lower or "new year" in s_lower: season, sunday = "Christmas", "Christmas Day"
    if "presentation" in s_lower: season, sunday = "Epiphany", "Last Sunday"
    if "annunciation" in s_lower: season, sunday = "Lent", "First Sunday"
    if "passion" in s_lower or "monday of holy week" in s_lower or "tuesday of" in s_lower or "wednesday of" in s_lower: season, sunday = "Holy Week", "Good Friday"
    if "visitation" in s_lower: season, sunday = "Easter", "Seventh Sunday"
    if "holy cross" in s_lower: season, sunday = "Ordinary Time", "Saints Triumphant"
    if "thanksgiving" in s_lower: season, sunday = "Ordinary Time", "Thanksgiving"

    hymns = hymn_map.get((season, sunday))
    if not hymns:
        sorted_items = sorted(hymn_map.items(), key=lambda x: len(x[0][1] or ""), reverse=True)
        for (map_season, map_sunday), map_hymns in sorted_items:
            if map_season == season and map_sunday:
                if map_sunday.lower() == season.lower(): continue
                if map_sunday.lower() in sunday.lower() or map_sunday.lower() in summary.lower():
                    hymns = map_hymns
                    break

    if not hymns: hymns = hymn_map.get((season, None))
    if not hymns: return ""

    linked_hymns = []
    for h in hymns:
        if "《" in h and "》" in h:
            song_name = h.split("《")[1].split("》")[0].strip()
            if "小羊詩歌" in h: search_kw = f"小羊詩歌 {song_name}"
            elif "約書亞樂團" in h: search_kw = f"約書亞樂團 {song_name}"
            elif "讚美之泉" in h: search_kw = f"讚美之泉 {song_name}"
            else: search_kw = song_name
        else:
            search_kw = h.replace("《", " ").replace("》", " ").replace("：", " ")
        yt_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_kw)}"
        linked_hymns.append(f'<a href="{yt_url}" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.color=\'#2563eb\'" onmouseout="this.style.color=\'inherit\'">{h}</a>')
    return "\n".join(linked_hymns)
    
def calculate_advent1(year: int) -> date:
    for day in range(27, 34):
        d = date(year, 11 if day <= 30 else 12, day if day <= 30 else day - 30)
        if d.weekday() == 6: return d
    raise ValueError("Advent 1 not found")

def determine_cycle(dt) -> str:
    if hasattr(dt, "date"): dt = dt.date()
    advent1 = calculate_advent1(dt.year)
    year = dt.year - 1 if dt < advent1 else dt.year
    return ["A", "B", "C"][(year - 2025) % 3]

def determine_formula(summary: str, dt: date = None) -> str:
    s = summary.lower()
    if dt and dt.weekday() == 6:
        if "reformation" in s or "all saints" in s:
             easter = calculate_easter(dt.year)
             pentecost = easter + timedelta(days=49)
             if dt > pentecost:
                 weeks = (dt - pentecost).days // 7
                 return f"(calculate_easter(year+1) + timedelta(days=49)) + timedelta(weeks={weeks})"
                 
    if "ephphany" in s: s = s.replace("ephphany", "epiphany")
    if "christmas eve" in s: return "date(year, 12, 24)"
    if "nativity of the lord" in s or ("christmas day" in s and "after" not in s): return "date(year, 12, 25)"
    
    match_num = re.search(r"christmas\s+(\d+)", s)
    if match_num: return f"date(year, 12, 26) + timedelta(days=(6 - date(year, 12, 26).weekday() + 7) % 7) + timedelta(weeks={int(match_num.group(1))-1})"
    
    if "christmas" in s:
        for word, num in ordinal_map_2.items():
            if word in s or str(num) in s:
                 return f"date(year, 12, 26) + timedelta(days=(6 - date(year, 12, 26).weekday() + 7) % 7) + timedelta(weeks={num-1})"
                 
    if "baptism" in s or ("epiphany" in s and (" 1" in s or "first" in s)): return "date(year+1, 1, 7) + timedelta(days=(6 - date(year+1, 1, 7).weekday() + 7) % 7)"
    match_num = re.search(r"epiphany\s+(\d+)", s)
    if match_num: return f"date(year+1, 1, 7) + timedelta(days=(6 - date(year+1, 1, 7).weekday() + 7) % 7) + timedelta(weeks={int(match_num.group(1))-1})"

    for word, num in ordinal_map_2.items():
        if ("epiphany" in s or "ephphany" in s) and (word in s or str(num) in s):
             return f"date(year+1, 1, 7) + timedelta(days=(6 - date(year+1, 1, 7).weekday() + 7) % 7) + timedelta(weeks={num-1})"
             
    if "transfiguration" in s or "last sunday after epiphany" in s: return "calculate_easter(year+1) - timedelta(days=49)"
    if "epiphany" in s: return "date(year+1, 1, 6)"
    if "holy name" in s or "new year" in s: return "date(year+1, 1, 1)"
    if "presentation" in s: return "date(year+1, 2, 2)"
    if "annunciation" in s: return "date(year+1, 3, 25)"
    if "visitation" in s: return "date(year+1, 5, 31)"
    if "holy cross" in s: return "date(year+1, 9, 14)"

    if "ash wednesday" in s: return "calculate_easter(year+1) - timedelta(days=46)"
    for word, num in ordinal_map_2.items():
        if "lent" in s and (word in s or str(num) in s): return f"calculate_easter(year+1) - timedelta(days={42 - (num-1)*7})"

    if "palm" in s or "passion" in s: return "calculate_easter(year+1) - timedelta(days=7)"
    if "monday of holy week" in s: return "calculate_easter(year+1) - timedelta(days=6)"
    if "tuesday of holy week" in s: return "calculate_easter(year+1) - timedelta(days=5)"
    if "wednesday of holy week" in s: return "calculate_easter(year+1) - timedelta(days=4)"
    if "maundy" in s or "holy thursday" in s: return "calculate_easter(year+1) - timedelta(days=3)"
    if "good friday" in s: return "calculate_easter(year+1) - timedelta(days=2)"
    if "holy saturday" in s or "easter vigil" in s: return "calculate_easter(year+1) - timedelta(days=1)"
        
    for word, num in ordinal_map_2.items():
        if "easter" in s and (word in s or str(num) in s): return f"calculate_easter(year+1) + timedelta(weeks={num-1})"

    if "resurrection of the lord" in s or "easter evening" in s or ("easter" in s and ("day" in s or "sunday" in s or "dawn" in s or "resurrection" in s) and "2" not in s and "3" not in s): return "calculate_easter(year+1)"

    if "ascension" in s: return "calculate_easter(year+1) + timedelta(days=39)"
    if "day of pentecost" in s or s.strip() == "pentecost": return "calculate_easter(year+1) + timedelta(days=49)"
    if "trinity" in s: return "calculate_easter(year+1) + timedelta(days=56)"
    
    if "christ the king" in s or "last sunday" in s or "reign of christ" in s: return "calculate_advent1(year+1) - timedelta(days=7)"

    match_proper = re.search(r"proper\s+(\d+)", s)
    if match_proper: return f"calculate_advent1(year+1) - timedelta(weeks={30 - int(match_proper.group(1))})"
        
    match_num = re.search(r"\b(\d+)\b", s)
    if "pentecost" in s and match_num: return f"(calculate_easter(year+1) + timedelta(days=49)) + timedelta(weeks={int(match_num.group(1))})"

    for word, num in ordinal_map_2.items():
        if "pentecost" in s and word in s: return f"(calculate_easter(year+1) + timedelta(days=49)) + timedelta(weeks={num})"
             
    if "reformation" in s: return "date(year+1, 10, 31)"
    if "all saints" in s: return "date(year+1, 11, 1)"
    if "thanksgiving" in s: return "fourth_thursday_of_november(year+1)"
    if "last judgment" in s: return "calculate_advent1(year+1) - timedelta(days=14)"
    if "saints triumphant" in s: return "calculate_advent1(year+1) - timedelta(days=21)"

    for word, num in ordinal_map_2.items():
        if "advent" in s and (word in s or str(num) in s): return f"calculate_advent1(year) + timedelta(weeks={num-1})"
    return ""

def fourth_thursday_of_november(year: int) -> date:
    d = date(year, 11, 1)
    while d.weekday() != 3: d += timedelta(days=1)
    return d + timedelta(weeks=3)

def calculate_easter(year: int) -> date:
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f, g = (b + 8) // 25, (b - (b + 8) // 25 + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def eval_formula(formula: str, year: int) -> date:
    safe_env = {"date": date, "timedelta": timedelta, "calculate_easter": calculate_easter, "calculate_advent1": calculate_advent1, "fourth_thursday_of_november": fourth_thursday_of_november, "year": year}
    try:
        return eval(formula, {"__builtins__": {}}, safe_env)
    except Exception:
        return None

def build_canonical_set_with_formula(cal):
    canonical_set = []
    seen_cycle_names = set()
    corrections = {r"\bTwelth\b": "Twelfth", r"\bFourtheenth\b": "Fourteenth", r"\bTwent[- ]?first\b": "Twenty-first", r"\bProepr\b": "Proper"}

    for component in cal.walk("VEVENT"):
        summary_text = str(component.get("summary")).strip()
        summary_text = re.sub(r'\s*\(Year\s+[ABC]\)', '', summary_text, flags=re.IGNORECASE)
        dtstart = component.get("dtstart").dt
        if hasattr(dtstart, "date"): dtstart = dtstart.date()
            
        valid_weekdays = ["Nativity", "Holy Name", "New Year", "Epiphany", "Presentation", "Annunciation", "Ash Wednesday", "Holy Week", "Maundy", "Good Friday", "Holy Saturday", "Easter Vigil", "Ascension", "Visitation", "Holy Cross", "All Saints", "Thanksgiving"]
        is_sunday = (dtstart.weekday() == 6)
        is_valid_weekday = any(kw.lower() in summary_text.lower() for kw in valid_weekdays)
        
        if not is_sunday and not is_valid_weekday: continue

        if date(2025, 11, 30) <= dtstart <= date(2028, 12, 2):
            adv1_of_year = calculate_advent1(dtstart.year)
            lit_start_year = dtstart.year if dtstart >= adv1_of_year else dtstart.year - 1
            cycle = ["A", "B", "C"][(lit_start_year - 2025) % 3]

            season_keeping_summary = summary_text
            for wrong, right in corrections.items():
                season_keeping_summary = re.sub(wrong, right, season_keeping_summary, flags=re.IGNORECASE)

            if season_keeping_summary.strip() == "Last Sunday in the Church Year": season_keeping_summary = "Christ the King"

            unique_key = (cycle, season_keeping_summary)
            if unique_key in seen_cycle_names: continue
            seen_cycle_names.add(unique_key)

            formula = determine_formula(season_keeping_summary, dtstart)
            canonical_set.append({"name": season_keeping_summary, "date": dtstart, "cycle": cycle, "formula": formula})
            
    existing_propers = {"A": set(), "B": set(), "C": set()}
    existing_epiphanies = {"A": set(), "B": set(), "C": set()}
    num_to_ordinal = {5: "Fifth", 6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth"}

    for e in canonical_set:
        name_str = e["name"]
        match = re.search(r"Proper\s+(\d+)", name_str, flags=re.IGNORECASE)
        if match: existing_propers[e["cycle"]].add(int(match.group(1)))
        for num, word in num_to_ordinal.items():
            if f"{word} Sunday after Epiphany".lower() in name_str.lower():
                existing_epiphanies[e["cycle"]].add(num)

    for c in ["A", "B", "C"]:
        for p in range(1, 30):  
            if p not in existing_propers[c]:
                canonical_set.append({"name": f"Proper {p}", "date": datetime.date(2000, 1, 1), "cycle": c, "formula": f"calculate_advent1(year+1) - timedelta(weeks={30 - p})"})                
        for ep_num in range(5, 10):
            if ep_num not in existing_epiphanies[c]:
                ep_word = num_to_ordinal[ep_num]
                canonical_set.append({"name": f"{ep_word} Sunday after Epiphany", "date": datetime.date(2000, 1, 1), "cycle": c, "formula": f"date(year+1, 1, 7) + timedelta(days=(6 - date(year+1, 1, 7).weekday() + 7) % 7) + timedelta(weeks={ep_num-1})"})
        canonical_set.append({"name": "Christ the King", "date": datetime.date(2000, 1, 1), "cycle": c, "formula": "calculate_advent1(year+1) - timedelta(days=7)"})
        
    cycle_order = {"A": 0, "B": 1, "C": 2}
    canonical_set.sort(key=lambda e: (cycle_order[e["cycle"]], e["date"]))
    return canonical_set
    
def is_generic_sunday(name):
    pattern = r"^(First|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth|Eleventh|Twelfth|Thirteenth|Fourteenth|Fifteenth|Sixteenth|Seventeenth|Eighteenth|Nineteenth|Twentieth|Twenty-|Last) Sunday|Proper"
    return re.match(pattern, name, flags=re.IGNORECASE) is not None    

def get_liturgical_color(season, sunday):
    if season == "Advent": return "🔵 藍色"
    if season == "Christmas": return "⚪ 白色"
    if season == "Epiphany":
        if sunday in ["Epiphany", "First Sunday", "Transfiguration", "Presentation"]: return "⚪ 白色"
        return "🟢 綠色" 
    if season in ["Lent", "Holy Week"]:
        if sunday in ["Palm Sunday", "Maundy Thursday"]: return "🔴 紅色"
        if sunday in ["Good Friday", "Holy Saturday"]: return "⚫ 黑色"
        if sunday == "Annunciation": return "⚪ 白色"
        return "🟣 紫色"
    if season == "Easter": return "⚪ 白色"
    if season in ["Pentecost", "Ordinary Time"]:
        if sunday in ["Pentecost Sunday", "Holy Cross"]: return "🔴 紅色"
        if sunday in ["Trinity Sunday", "Christ the King", "All Saints"]: return "⚪ 白色"
        return "🟢 綠色" 
    return ""    

# =====================================================================
# 3. 核心執行與生成區 (Execution Core)
# =====================================================================
START_YEAR = 2025
YEARS = 101
END_YEAR = START_YEAR + YEARS - 1

perfect_templates = {}
all_final_events = [] # 儲存最終事件資料以供網頁輸出

print("🔄 正在讀取 ICS 與建立經文資料庫...")
with open("weekly.ics", "rb") as f:
    cal = Calendar.from_ical(f.read())

# --- (A) 解析原有三年份 ICS ---
for component in cal.walk():
    if component.name == "VEVENT":
        start_date = component.get("dtstart").dt
        check_date = start_date.date() if hasattr(start_date, "date") else start_date

        if not (START_YEAR <= start_date.year <= END_YEAR): continue

        summary_text = str(component.get("summary"))
        is_sunday = (check_date.weekday() == 6)
        summary_lower = summary_text.lower()

        if not is_sunday and "sunday" in summary_lower: continue

        valid_weekdays = ["nativity", "holy name", "new year", "epiphany", "presentation", "annunciation", "ash wednesday", "holy week", "maundy", "good friday", "holy saturday", "easter vigil", "ascension", "visitation", "holy cross", "all saints", "thanksgiving"]
        is_valid_weekday = any(kw in summary_lower for kw in valid_weekdays)
        if not is_sunday and not is_valid_weekday: continue

        summary_text = re.sub(r'\s*\(Year\s+[ABC]\)', '', summary_text, flags=re.IGNORECASE)
        if "Nativity of the Lord" in summary_text: continue

        cycle_label = get_cycle_label(start_date)
        season, sunday, display_summary = parse_summary(summary_text)

        description = str(component.get("description", "")).replace("–", "-").replace("–", "-").replace("—", "-")
        
        new_lines = []
        for line in description.splitlines():
            line = line.strip()
            if not line: continue
            line = re.sub(r'[–—−\x96\x97\u2013\u2014]', '-', line)
            if "http" in line: continue
            if line.startswith("(") and line.endswith(")"): continue

            has_book = False
            for eng_book in book_map.keys():
                if re.search(rf'\b{re.escape(eng_book)}\b', line, flags=re.IGNORECASE) and re.search(r'\d', line):
                    has_book = True
                    break
                    
            if has_book:
                line = re.sub(r'\s+and\s+', ' 與 ', line, flags=re.IGNORECASE)
                line = re.sub(r'\s+or\s+', ' 或 ', line, flags=re.IGNORECASE)
                clean_trans = translate_text(line, cycle_label, season, sunday)
                clean_trans = re.sub(r"^(第一部分讀經|第二部分讀經|福音經課|補充經課|經課與詩篇)[\s:]*", "", clean_trans).strip()
                new_lines.append(get_scripture_links(clean_trans))

        description = "\n".join(new_lines)
        if sunday == "Thanksgiving":
            egg_text = "🦃 太18:18 我實在告訴你們，凡你們在地上所捆綁的，在天上也要捆綁；凡你們在地上所釋放的，在天上也要釋放。 🦃"
            if egg_text not in description: description = (description + "\n\n" + egg_text).strip()

        hymn_text = get_hymn_text(summary_text, start_date)
        if hymn_text: description += "\n\n今日詩歌：\n" + hymn_text

        color_str = get_liturgical_color(season, sunday)
        if color_str: description += f"\n\n代表顏色：{color_str}"

        meaning_str = season_meaning_map.get(season, "")
        if meaning_str: description += f"\n節期意義：{meaning_str}"

        perfect_templates[(cycle_label, season, sunday)] = description 
        all_final_events.append({"date": check_date, "name": summary_text, "source": "original", "description": description})        

print("✨ 正在補全 100 年份所有經課事件...")
# --- (B) 依照公式生成 100 年份 ---
canonical_set_with_formula = build_canonical_set_with_formula(cal)

for church_year in range(2028, END_YEAR+2):
    advent1 = calculate_advent1(church_year)
    next_advent1 = calculate_advent1(church_year+1)
    cycle_label = determine_cycle(advent1)
    
    daily_buffer = defaultdict(list)

    for e in canonical_set_with_formula:
        if e["cycle"] != cycle_label: continue
            
        dt = eval_formula(e["formula"], church_year)
        if dt and advent1 <= dt < next_advent1:
            if "Proper" in e["name"]:
                pentecost = calculate_easter(church_year+1) + timedelta(days=49)
                if dt <= pentecost: continue 

            if "Epiphany" in e["name"] and "after" in e["name"]:
                ash_wednesday = calculate_easter(church_year+1) - timedelta(days=46)
                if dt >= ash_wednesday: continue 

            dt_str = dt.strftime('%Y%m%d')
            season, sunday, display_summary = parse_summary(e["name"])
            
            if (cycle_label, season, sunday) in perfect_templates:
                description = perfect_templates[(cycle_label, season, sunday)]
            else:
                scripture_lines = scripture_patch.get(cycle_label, {}).get((season, sunday), [])
                processed_lines = []
                for line in scripture_lines:
                    if not line: continue
                    if re.search(r'\d', line) and not line.startswith("【"): 
                        processed_lines.append(get_scripture_links(line))
                    else:
                        processed_lines.append(line)
                        
                desc_body = "\n\n".join(processed_lines)
                hymn_text = get_hymn_text(e["name"], dt)
                description = desc_body + ("\n\n今日詩歌：\n" + hymn_text if hymn_text else "")
                
                color_str = get_liturgical_color(season, sunday)
                if color_str: description += f"\n\n代表顏色：{color_str}"
                meaning_str = season_meaning_map.get(season, "")
                if meaning_str: description += f"\n節期意義：{meaning_str}"

            daily_buffer[dt_str].append({
                "name": e["name"],
                "dt": dt,
                "final_desc": description
            })

    final_event_lookup = {} 
    generated_dates = set()
    for dt_str in sorted(daily_buffer.keys()):
        candidates = daily_buffer[dt_str]
        for selected in candidates:
            all_final_events.append({"date": selected["dt"], "name": selected["name"], "source": "generated", "description": selected["final_desc"]})
        
        generated_dates.add(dt_str)
        special_candidates = [c for c in candidates if not is_generic_sunday(c["name"])]
        best_candidate = special_candidates[0] if special_candidates else candidates[0]
        final_event_lookup[dt_str] = best_candidate["final_desc"]

    # 補漏主日
    curr_sun = advent1
    while curr_sun < next_advent1:
        if curr_sun.month == 12 and curr_sun.day == 25:
            curr_sun += timedelta(days=7)
            continue
            
        s_str = curr_sun.strftime('%Y%m%d')
        if s_str not in generated_dates: 
             prev_sun = curr_sun - timedelta(days=7)
             prev_s_str = prev_sun.strftime('%Y%m%d')
             
             if prev_s_str in final_event_lookup:
                 new_desc = final_event_lookup[prev_s_str]
                 all_final_events.append({"date": curr_sun, "name": "Auto-filled (Fixed)", "source": "generated", "description": new_desc})
                 final_event_lookup[s_str] = new_desc
                 generated_dates.add(s_str)
             
        curr_sun += timedelta(days=7)     

# --- (C) 生成 100 年專屬聖誕節 ---
for yr in range(START_YEAR, END_YEAR + 2):
    dt = datetime.date(yr, 12, 25)
    cycle_label = determine_cycle(dt) 
    season, sunday = "Christmas", "Christmas Day"
    
    scripture_lines = scripture_patch.get(cycle_label, {}).get((season, sunday), [])
    processed_lines = []
    for line in scripture_lines:
        if not line: continue
        if re.search(r'\d', line) and not line.startswith("【"):
            processed_lines.append(get_scripture_links(line))
        else:
            processed_lines.append(line)
            
    desc_body = "\n\n".join(processed_lines)
    hymn_text = get_hymn_text(sunday, dt)
    description = desc_body + ("\n\n今日詩歌：\n" + hymn_text if hymn_text else "")
    
    color_str = get_liturgical_color(season, sunday)
    if color_str: description += f"\n\n代表顏色：{color_str}"
    meaning_str = season_meaning_map.get(season, "")
    if meaning_str: description += f"\n節期意義：{meaning_str}"
        
    all_final_events.append({
        "date": dt, 
        "name": "Christmas Day", 
        "source": "generated", 
        "description": description
    })

# =====================================================================
# 4. JSON 網頁資料輸出區 (Web JSON Generation)
# =====================================================================
print("🌐 準備輸出網頁專用 rcl_data.json ...")
web_data = defaultdict(list)

for ev in all_final_events:
    date_obj = ev["date"]
    if hasattr(date_obj, "date"): date_obj = date_obj.date()
        
    date_str = date_obj.strftime("%Y-%m-%d")
    raw_name = ev["name"]
    desc = ev.get("description", "")
    
    current_year = determine_cycle(date_obj)
    season, sunday, _ = parse_summary(raw_name)
    
    # 智慧路由判斷
    if sunday and "Proper" in sunday: season = "Ordinary Time"
    if season == "Easter" and any(k in raw_name for k in ["Resurrection", "Easter Day", "Easter Dawn", "Easter Evening", "Easter Vigil"]): sunday = "Easter Sunday"
    if season == "Christmas" and "Nativity" in raw_name: sunday = "Christmas Eve" if "Eve" in raw_name else "Christmas Day"
    if season == "Epiphany" and "Epiphany of" in raw_name: sunday = "Epiphany"
    if season == "Pentecost" and "Day of Pentecost" in raw_name: sunday = "Pentecost Sunday"
        
    s_lower = raw_name.lower()
    if "holy name" in s_lower or "new year" in s_lower: season, sunday = "Christmas", "Christmas Day"
    if "presentation" in s_lower: season, sunday = "Epiphany", "Last Sunday"
    if "annunciation" in s_lower: season, sunday = "Lent", "First Sunday"
    if "passion" in s_lower or "monday of holy week" in s_lower or "tuesday of" in s_lower or "wednesday of" in s_lower: season, sunday = "Holy Week", "Good Friday"
    if "visitation" in s_lower: season, sunday = "Easter", "Seventh Sunday"
    if "holy cross" in s_lower: season, sunday = "Ordinary Time", "Holy Cross"
    if "thanksgiving" in s_lower: season, sunday = "Ordinary Time", "Thanksgiving"

    # 切割詩歌與經文
    parts = desc.split("今日詩歌：")
    scriptures_raw = parts[0].strip()
    
    modern_hymns = []
    color = ""
    meaning = ""
    
    if len(parts) > 1:
        bottom_part = parts[1]
        if "代表顏色：" in bottom_part:
            c_split = bottom_part.split("代表顏色：")
            color = c_split[1].split("\n")[0].strip()
            bottom_part = c_split[0]
            
        for line in bottom_part.split("\n"):
            line = line.strip()
            if line and "節期意義：" not in line and "代表顏色：" not in line:
                modern_hymns.append(line)
                
    if "節期意義：" in desc:
        m_split = desc.split("節期意義：")
        meaning = m_split[1].split("\n")[0].strip()

    # 比對古典詩歌
    raw_c_hymns = []
    year_dict = classical_hymns_map.get((season, sunday))
    
    if not year_dict:
        sorted_items = sorted(classical_hymns_map.items(), key=lambda x: len(x[0][1] or ""), reverse=True)
        for (map_season, map_sunday), map_dict in sorted_items:
            if map_season == season and map_sunday:
                if map_sunday.lower() == (season or "").lower(): continue
                if map_sunday.lower() in (sunday or "").lower() or map_sunday.lower() in raw_name.lower():
                    year_dict = map_dict
                    break

    if year_dict:
        if current_year in year_dict:
            raw_c_hymns = year_dict[current_year]
        elif "All" in year_dict:
            raw_c_hymns = year_dict["All"]
            
    c_hymns = []
    for h in raw_c_hymns:
        search_kw = f"{h} 詩歌"
        yt_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_kw)}"
        c_hymns.append(f'<a href="{yt_url}" target="_blank" style="color: inherit; text-decoration: none;" onmouseover="this.style.color=\'#2563eb\'" onmouseout="this.style.color=\'inherit\'">{h}</a>')

    clean_scriptures = [
        s for s in scriptures_raw.split("\n") 
        if s.strip() and not s.startswith("節期意義：") and not s.startswith("代表顏色：")
    ]
    display_title = translate_summary(raw_name) if "Auto-filled" not in raw_name else "補進來的主日"

    event_item = {
        "title": display_title,
        "scriptures": clean_scriptures,
        "classical_hymns": c_hymns,
        "modern_hymns": modern_hymns,
        "color": color,
        "meaning": meaning
    }
    
    web_data[date_str].append(event_item)

# 輸出最終的 JSON
with open("rcl_data.json", "w", encoding="utf-8") as f:
    json.dump(web_data, f, ensure_ascii=False, indent=2)

print("cl_data.json 已成功產出！")