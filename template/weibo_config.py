#-*- coding: utf-8 -*-

# Related to  aybu cloud proxy, proxy server
ABUYUN_USER = "H778U07K14M4250P"
ABUYUN_PASSWD = "FE04DDEF88A0CC9B"
ABUYUN_HOST = "proxy.abuyun.com"
ABUYUN_PORT = "9010"

# Redis keys
ACTIVATED_COOKIE = 'weibo:activated:cookie'
INACTIVATED_COOKIE = 'weibo:inactivated:cookie'
MANUAL_COOKIES = 'weibo:manual:cookies'
JOBS_QUEUE = 'weibo:user:urls'  # set or list
RESULTS_QUEUE = 'weibo:follows:info'  # set or list

# database setting
OUTER_MYSQL = {
    'host': '582af38b773d1.bj.cdb.myqcloud.com',
    'port': 14811,
    'db': 'webcrawler',
    'user': 'web',
    'passwd': "Crawler20161231",
    'charset': 'utf8',
    'connect_timeout': 20,
}
QCLOUD_MYSQL = {
    'host': '10.66.110.147',
    'port': 3306,
    'db': 'webcrawler',
    'user': 'web',
    'passwd': 'Crawler20161231',
    'charset': 'utf8',
    'connect_timeout': 20,
}
LOCAL_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}
QCLOUD_REDIS = {
    'host': '10.66.173.136',
    'port': 6379,
    'password': "crs-3gcmm8la:Data@2016",
}

# Database sql
DEPRECATE_FOLLOW = """
    UPDATE weibouserfollows
    SET is_up2date='N' 
    WHERE weibo_user_url='{user}' and follow_usercard='{followid}' and is_up2date='Y'
"""

INSERT_FOLLOW_SQL = """
    INSERT INTO weibouserfollows
    (nickname, weibo_user_url, follow_nickname, follow_fans_num, follow_weibo_num, follow_focus_num, follow_type, follow_usercard, createdate, is_up2date)
    VALUES ('{nickname}', '{user}', '{follow}', '{fans}', '{blogs}', '{focus}', '{type}', '{followid}', '{date}', '{status}')
"""

# Execute result number
SUCCESSED = 1
FAILED = -1
REQUEST_ERROR = -100
PARSE_HTML_ERROR = -101
ACCESS_URL_ERROR = -102
IGNORE_RECORD = -102

# Database Error number using 2XX
DB_WRITE_FAILED = -200
DB_CANNOT_CONNECT = -201
DB_LOST_CONNECTION = -203
DB_SYNTAX_ERROR = -204
DB_LOCK_WAIT_TIMEOUT = -205
DB_FOUND_DEADLOCK = -206
DB_SEVER_GONE_AWAY = -213
DB_UNICODE_ERROR = -207
DB_UNKNOW_ERROR = -299

# Network Error number using 3XX
NETWORK_CONNECTION_ERROR = -300
NETWORK_PROXY_ERROR = -301
NETWORK_TIMEOUT = -302

# Execute result message
ERROR_MSG_DICT = {
    SUCCESSED: "Succeeded",
    FAILED: "Failed",
    REQUEST_ERROR: "Request Target Fialed",
    PARSE_HTML_ERROR: "Parsed url or html FAILED",
    ACCESS_URL_ERROR: "Send requests FAILED",
    IGNORE_RECORD: "The record would be ignored",

    # for database
    DB_WRITE_FAILED: "Write data into database FAILED",
    DB_CANNOT_CONNECT: "Can't connect to MySQL.(服务器资源紧张，导致无法连接)",
    DB_LOCK_WAIT_TIMEOUT: "Lock wait timeout exceeded, try restarting transaction and check if someone manages the table",
    DB_SEVER_GONE_AWAY: "MySQL server has gone away",
    DB_SYNTAX_ERROR: "You have an error in your SQL syntax.(SQL语句有语法错误)",
    DB_LOST_CONNECTION: "Lost connection to MySQL server during query",
    DB_FOUND_DEADLOCK: "Deadlock found when trying to get lock; try restarting transaction",
    DB_UNICODE_ERROR: "Incorrect string value.(不能写入字符串到数据库)",
    DB_UNKNOW_ERROR: "Unknown Program or Operation Errors",

    # for network
    NETWORK_CONNECTION_ERROR: "Connection Error",
    NETWORK_TIMEOUT: "Timeout",
    NETWORK_PROXY_ERROR: "(连接池满了)Max retries exceeded with url",
}

WEIBO_MANUAL_COOKIES = {
    'liekeoth27678@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://weibo.com/u/5983286206/home?topnav=1&wvr=6' -H 'Cookie: login_sid_t=0be8efaaa70ca414577057cb637a60bc; _s_tentry=-; Apache=9033722709924.56.1481496448981; SINAGLOBAL=9033722709924.56.1481496448981; ULV=1481496448986:1:1:1:9033722709924.56.1481496448981:; SSOLoginState=1481525398; un=liekeoth27678@163.com; _T_WM=feb94eee7c2b9cefce4db07f4f61d8b9; SCF=Aq5bz-SgVolAmkEY6uNNPPFAUta_GVY7hSdrs5yNtchOvf0b3OQI4ARrpxCIwu29YWtriwDRCsuCz-PS8g8EZDc.; SUB=_2A251SjynDeTxGeNH41ET-CjOyzqIHXVWPilvrDV8PUJbmtAKLWntkW8PX3aL2yFJTaRJes1lqULsf0BPfw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW9Bg.ND2DJ.Ju6Rxkffrks5JpX5o2p5NHD95Qf1Kn0eonceo5cWs4Dqcj_i--fiK.7i-z4i--fiKy8iKLWi--RiKn7i-i2i--RiKnfiK.Xi--Ri-z7iKyF; SUHB=02M_P9sQrILLOf; ALF=1513061397; wvr=6; TC-Page-G0=0cd4658437f38175b9211f1336161d7d' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' --compressed",
    'yinxiong07181@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=2e2064f913b25f65361cc03eda1851d4; ALF=1484129554; SUB=_2A251SghCDeTxGeNH41AR-S_LyzWIHXVWtKgKrDV8PUJbkNAKLXijkW1g96xHuxUizCaugmYqY6BZtpxe_A..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whj4Fjv3QnlqUjOWq6w87aT5JpX5oz75NHD95Qf1KnEeh.pS054Ws4Dqcj_i--NiKyFi-88i--fi-i2i-iFi--Xi-iWi-2pi--NiKysi-27i--Ri-zNi-2R; _s_tentry=-; Apache=7821733612324.722.1481508770593; SINAGLOBAL=7821733612324.722.1481508770593; ULV=1481508771486:1:1:1:7821733612324.722.1481508770593:; TC-Page-G0=4c4b51307dd4a2e262171871fe64f295' -H 'Connection: keep-alive' --compressed", 
    'eid24153345bei@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=73b47e16b9293bfcc97ee068854195cc; ALF=1484129703; SUB=_2A251Sgj3DeTxGeNH7FAY8y7NzTSIHXVWtKi_rDV8PUJbkNAKLUX2kW051WFaFSMepijok6dpLmDQZGCFLg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whm-xs0.G8JG1YZNLLeLo4W5JpX5oz75NHD95Qf1KME1Ke7eKqRWs4Dqcj_i--4i-2ciKnfi--RiKyWi-i2i--fiKysi-2Xi--fiK.7iKLFi--Xi-z4iKys' -H 'Connection: keep-alive' --compressed",
    'wengdang264408@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=015bb516e99d559e2136d169533c0836; ALF=1484129794; SUB=_2A251SglSDeTxGeNH7FYQ-CbNzjuIHXVWtJcarDV8PUJbkNAKLW7ckW0FP6CdSxLieLE46WsXwF414l5kzg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5IzaXvgNY-WrKi_397p8Ju5JpX5oz75NHD95Qf1KMXeKnReK-NWs4Dqcj_i--fiKnRi-8Fi--Ri-zfiKysi--Ri-isiKLFi--NiK.EiKn0i--Ni-iWi-zp' -H 'Connection: keep-alive' --compressed",
    'tengmi27162@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=5b007ffc990f49dcce8149193ea11a04; ALF=1484129917; SUB=_2A251SgktDeTxGeNH41cU9S7NyzyIHXVWtJdlrDV8PUJbkNAKLXnZkW03iyatWYb5O_vqfmdB6Iuzp_gSjQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5EZIHqfblZDmkr_ACTAEC_5JpX5oz75NHD95Qf1KnfSK-7eK57Ws4Dqcj_i--fi-88i-8Wi--Ri-8si-i8i--fiKysiKnEi--fi-zpiKnfi--4i-2fi-88; TC-Page-G0=2b304d86df6cbca200a4b69b18c732c4; _s_tentry=-; Apache=5746471704135.472.1481509141735; SINAGLOBAL=5746471704135.472.1481509141735; ULV=1481509141828:1:1:1:5746471704135.472.1481509141735:' -H 'Connection: keep-alive' --compressed",
    'q0306469pinchigu@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: TC-Page-G0=2b304d86df6cbca200a4b69b18c732c4; login_sid_t=57b60a112b0217aab59f75fa7ef54ee6; _T_WM=921aeb2273197bbe72f5654477129e7c; ALF=1484130029; SUB=_2A251Sgm9DeRxGeNH41YV8S7OyTSIHXVWtJf1rDV8PUJbkNAKLVmgkW1DKSsu51PPIBesHVzTqfvgfD-eug..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhYnQ_u4Ss67ApHGPRNokrr5JpX5oz75NHD95Qf1KnXSh27eozRWs4Dqcj_i--fi-88iKnRi--fiKy2iKnpi--Ri-88i-82i--fi-88iKnRi--4iK.Xi-2X' -H 'Connection: keep-alive' --compressed",
    'lianlun244814@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=1bf4f5455c5f234f4080cade7aadda58; ALF=1484142049; SUB=_2A251StixDeTxGeNH41EV8i7FzD6IHXVWtPj5rDV8PUJbkNBeLXb3kW0vaQuVva05QWuzRygwJ4YsMhuFnA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWQFhUAYE1naBJ573eiiXDv5NHD95Qf1Kn0Shz71KMEWs4Dqcj_i--RiKnXiKn4i--fiKn7i-2pi--ci-8siK.Ei--NiKnfiKyhi--RiKnRiKnf; YF-Page-G0=e3ff5d70990110a1418af5c145dfe402' -H 'Connection: keep-alive' --compressed",
    'jueqdarx5082@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=00e83b542dbeea5fad74231e574e2c62; ALF=1484142364; SUB=_2A251StpMDeTxGeNH41AQ9SvOyjSIHXVWtOYErDV8PUJbkNBeLRPikW005ufuzZ43969DOkGdoeFi8Y0_1A..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh_.GcL.vbRv1iRvH61shmP5NHD95Qf1KnEeK-feo2RWs4Dqcj_i--Xi-isiK.Ri--4iKnNiKy8i--Xi-i2iK.fi--ci-iWi-8Wi--ciKn4iK.0' -H 'Connection: keep-alive' --compressed",
    'bangsxq1239@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=95f30d3ae2db2bc5b855dbe1a18612c0; ALF=1484142451; SUB=_2A251StojDeTxGeNH41YT9ivFzzyIHXVWtOZrrDV8PUJbkNBeLWXakW1dvCgMx4Z54ibFe8g8QAijK6VMpQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFasYWsNq37aym4uvjxEYoY5NHD95Qf1KnXeoqf1KB7Ws4Dqcj_i--Ni-i2iKLWi--RiKn7iK.fi--fi-z7iKysi--Ri-zRi-2Ei--4i-i8iKnX; YF-Page-G0=1ac418838b431e81ff2d99457147068c' -H 'Connection: keep-alive' --compressed",
    # 'zhuang37335731@163.com': "",
    'ben36327616@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=6f5082c8c93164a6c2ab442e10ba6d72; ALF=1484143432; SUB=_2A251St4YDeTxGeNH7FcY9y_MwjWIHXVWtOJQrDV8PUJbkNBeLU_WkW1z3uRxNE7A6IoVMSBplqVBBpFfmg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhO.MZrx41PJRfMq_TmLSS05NHD95Qf1KMf1KMpeh.4Ws4Dqcj_i--NiKnRi-zci--fi-2Ni-2Ri--fiKLsiKy8i--fiKnfi-i2i--ciKL2i-27' -H 'Connection: keep-alive' --compressed",
    'suituw937563@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=1594d757e2b05e30f7992683e2c3b592; ALF=1484143591; SUB=_2A251St63DeTxGeNH41cS8inIzjSIHXVWtOL_rDV8PUJbkNBeLUfjkW1IUkjD_MHHVbs_PQ6_kkcWkaDg1A..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWZ47QUj2RGrWEGol_pH.Fm5NHD95Qf1Knfe0zNSh-RWs4Dqcj_i--Ri-88i-24i--NiKLFiK.Ri--fiKnfiK.Xi--fiKysiK.ci--fiK.7i-8s' -H 'Connection: keep-alive' --compressed",
    'zhanchuangyingy@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=4c283bc2c1e8b76eae384fd534e96ed2; ALF=1484143661; SUB=_2A251St98DeTxGeNH7FEV9S3MzD2IHXVWtOE0rDV8PUJbkNBeLWjnkW1B0CRR2W_s0dtVy3SXCPiIl0UQZw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5cbpkZO.9xjEKVaQpNGGWP5NHD95Qf1KM0Sh-0ehMpWs4Dqcj_i--Ni-zpiKy2i--Ni-2Ni-2Xi--RiKyhiKnXi--Ri-88i-2Ei--fiKnEi-8h' -H 'Connection: keep-alive' --compressed",
    'wbw08541466yous@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=becfec41dab824b745a3fdec5622d577; ALF=1484144427; SUB=_2A251SsJ7DeRxGeNH41ET9ivJyjSIHXVWtO4zrDV8PUJbkNBeLUb3kW0q95qJKZl_dht5c6rS0yGCUAgwUQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5m4_nFr5r5pY-iBQy7cZYp5NHD95Qf1Kn0eoqfSK2RWs4Dqcj_i--NiK.0i-zci--ci-zXiK.Ei--fiK.fiKyWi--fiKn7i-i8i--fi-2Xi-24; YF-Page-G0=0dccd34751f5184c59dfe559c12ac40a' -H 'Connection: keep-alive' --compressed",
    'gaisi574905976@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=fa68576361ad9cb9b09e5cf3fe607d68; ALF=1484197147; SUB=_2A251S_BLDeTxGeNH41YS9i_Mwj2IHXVWt5ADrDV8PUJbkNAKLRnkkW0XCN27QFyRs4watKi1sjVtOBuLuQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhQuDLlco5aM_Q7KJ_x1i2U5JpX5oz75NHD95Qf1KnXe0qpeh.pWs4Dqcj_i--Ri-8si-zfi--fi-i8iKn7i--Ri-zXi-zRi--ciKnXiKn4i--ci-zci-2R; TC-Page-G0=2b304d86df6cbca200a4b69b18c732c4' -H 'Connection: keep-alive' --compressed",
    'duwengluyi@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=9f1fcf358de89c83f91c4d1beb928936; ALF=1484197222; SUB=_2A251S_A2DeTxGeNH41ET9ijLyz2IHXVWt5B-rDV8PUJbkNAKLWjZkW1JGMOEKW38jJQZEzfJ7uo92VMu1w..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whs9W5H6Y3RW4lzwdA-LNsW5JpX5oz75NHD95Qf1Kn0eoqcS05pWs4Dqcj_i--Ni-ihi-24i--ciKLWiK.Ni--fi-2Xi-zXi--Xi-ihi-zci--ciKLWiK.p' -H 'Connection: keep-alive' --compressed",
    'leike811808902@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=75cb789a6e505d838f70677c4e266078; ALF=1484197291; SUB=_2A251S_D7DeTxGeNH41ET9y3IyDmIHXVWt5CzrDV8PUJbkNAKLXT8kW2WwmQR4h2GBFT9NxCGnlmnXDazcA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFH1SQ2f4SRmFN4QpBsGDsA5JpX5oz75NHD95Qf1Kn0eoM0ShefWs4Dqcj_i--ciK.fiKL8i--4iKL8i-27i--Xi-ihi-zXi--RiKnXiKysi--fiK.ciKL2' -H 'Connection: keep-alive' --compressed",
    'pumou791174@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=96037fa32b64d5d554a9010df9ac3bed; ALF=1484197366; SUB=_2A251S_CmDeRxGeNH41ET9y3KyTWIHXVWt5DurDV8PUJbkNAKLXndkW00bZvEzZNgwMRGA3AR56uBXQ8QAA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFr_cyC9sKInuENGDwY3Wg15JpX5oz75NHD95Qf1Kn0eoM0Soz4Ws4Dqcj_i--Ni-z0iK.ci--Ni-i8i-i2i--RiKnRi-z4i--fi-2XiK.fi--Ni-8hiKyF' -H 'Connection: keep-alive' --compressed",
    'kaoke028842@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=0767ad2c54a6fdabaa93df65f668d098; TC-Page-G0=1e758cd0025b6b0d876f76c087f85f2c; login_sid_t=6a16bbf29c3e1a3d71098ae2b5c95453; ALF=1484197436; SUB=_2A251S_FsDeTxGeNH41AR-C_Ezj6IHXVWt58krDV8PUJbkNAKLWbFkW1cQeNxvlLkGcJKsKPZ1M55bnmmiA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvrBzuuuOjQmDPU2S5.CfV5JpX5oz75NHD95Qf1KnEehnp1h-EWs4Dqcj_i--Ri-zXi-zfi--ci-8hi-2pi--Ri-20iK.fi--ci-27i-8Wi--fiKyhi-z4; _s_tentry=-; Apache=9948224668013.502.1481605438014; SINAGLOBAL=9948224668013.502.1481605438014; ULV=1481605438027:1:1:1:9948224668013.502.1481605438014:' -H 'Connection: keep-alive' --compressed",
    # 'zhemtbsg503417@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=ea321c9453f106237a6b97d9bc730d69; ALF=1484197517; SUB=_2A251S_HdDeTxGeNH41EQ9i_JwjWIHXVWt5-VrDV8PUJbkNAKLUb1kW2dynPUhEvuA5LI4IYcqcyftTHSzQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFjxSQXDRBW2qnjQGgbQldm5JpX5oz75NHD95Qf1Kn0eKqpSK.4Ws4Dqcj_i--4iKLWiK.7i--4iKnpi-20i--Ri-z7iKLhi--4iK.Ni-88i--Xi-z4iK.c' -H 'Connection: keep-alive' --compressed",
    'f4998616haozi2600@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: login_sid_t=6c0ad8212dde64e670178a43211cd779; _s_tentry=-; Apache=5329075014049.809.1481607783971; SINAGLOBAL=5329075014049.809.1481607783971; ULV=1481607783979:1:1:1:5329075014049.809.1481607783971:; SCF=AhOhnLQ3KuegC7rUVwXkjDIWDrxrkNfZKBmTu661l83Gg6L_AfqZXfSzIuIfRkd1nGd8hje-6GRV51klnSGA1Ww.; SUB=_2A251S_rQDeTxGeNH41MY9yzLwz6IHXVWIWsYrDV8PUNbmtAKLW7akW9TSAicfZYky18Lh_NuDs37y3KXuA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW1xpFIiumhFlsahcJzzS-f5JpX5K2hUgL.Fo-41h24S0zN1hz2dJLoIEBLxKML1KBL1-eLxK-L1h-LBoBLxK-L1h-LBoBLxK-L1K-L122t; SUHB=0eb9ArnetLlRU0; ALF=1513143802; SSOLoginState=1481607808; un=f4998616haozi2600@163.com; wvr=6' -H 'Connection: keep-alive' --compressed",
    'ke42536379dongya6@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: login_sid_t=76689e1ba1e9905fa5d7a411330632e5; _s_tentry=-; Apache=4478161254936.588.1481608727327; SINAGLOBAL=4478161254936.588.1481608727327; ULV=1481608727332:1:1:1:4478161254936.588.1481608727327:; SCF=ApI7dV9NGZu9kITEWH0ch56RMH79mw7F85VT0tRh5cCx7NqzFDh2a6UZ5RMcsQ-qL5oZql6gr5ZrH_bfch8gG-8.; SUB=_2A251S_5LDeTxGeNH41MY9y3MyziIHXVWIWiDrDV8PUNbmtAKLW3mkW8ilF5c4ERXlcgOSUnIfS5EUoHDfQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5LIRA6-vTP8JXDE61XwPD_5JpX5K2hUgL.Fo-41h24S0e7ehB2dJLoIcXLxK-L1h-LBoBLxK-L1-BLBKnLxK-LBo5LBo2LxK-L1h2L12qLxK-L1h2L12qLxK-LB--LBK5LxKqL1hnL1K2LxKBLBonL1h5LxKBLB.2LB.2LxK-L1hBLB.qLxK-LBo5L12qLxK-L12qLBoMR; SUHB=05iq4XY604F-IA; ALF=1513144728; SSOLoginState=1481608731; un=ke42536379dongya6@163.com; wvr=6' -H 'Connection: keep-alive' --compressed",
    'zhengayp14161@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: login_sid_t=23b6a69a62e928d3661adcb58b54856c; _s_tentry=-; Apache=4185558838430.0234.1481608798281; SINAGLOBAL=4185558838430.0234.1481608798281; ULV=1481608798291:1:1:1:4185558838430.0234.1481608798281:; SCF=AnFU8yUGLrkcfQUgIoTTAsdesiHk9MD4kv1rbqQOXMvcadOSRjLC_KCv_HAuIRj7nEANGltu79bpxYwz19y7NPE.; SUB=_2A251S_4gDeTxGeNH41YT9i_MzDSIHXVWIWjorDV8PUNbmtAKLXfnkW-PdTcEXYvZXjOQJb_AO7BHMwT3Zw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TaHkMA4ywqmrMiJBWhcrX5JpX5K2hUgL.Fo-41hBESo27S0n2dJLoIEXLxK-L1KeLB-2LxK.LBonLBK2LxKML1h.LBKzLxKnLBonLBKzLxKnL12zLBo2t; SUHB=0u5BFi9KTc5RwO; ALF=1513144814; SSOLoginState=1481608816; un=zhengayp14161@163.com' -H 'Connection: keep-alive' --compressed",
    'zhecguyv547456@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=5919cac7756d1231f94b8890a9fba87d; ALF=1484203464; SUB=_2A251S-iYDeTxGeNH41EQ-SrIyTiIHXVWt4jQrDV8PUJbkNAKLUqhkW0O1_iDSzrka8-sQbdG3GBi2yFTgQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWBfbbj8PYzHTFjha-uYRSA5JpX5oz75NHD95Qf1Kn0eK.XShzXWs4Dqcj_i--fiKnfi-zXi--RiKn0i-zRi--ci-zpiKnEi--fiKysiK.ci--4i-z4iKnf; TC-Page-G0=0dba63c42a7d74c1129019fa3e7e6e7c; _s_tentry=-; Apache=6380947090029.669.1481611481644; SINAGLOBAL=6380947090029.669.1481611481644; ULV=1481611481663:1:1:1:6380947090029.669.1481611481644:' -H 'Connection: keep-alive' --compressed",
    'zhutim404592@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=7c5800f28d40632277fa1ebc79a3ed57; ALF=1484203621; SUB=_2A251S-k1DeTxGeNH41YS8CrJyjmIHXVWt_d9rDV8PUJbkNAKLWmnkW1ICUkOdCfYy_tPeEUQaAT7qIFMPA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW7kBp3Xl0z09Va2sk.km_h5JpX5oz75NHD95Qf1KnXe05XSK2fWs4Dqc_ZdG-LxKqL1hnL1K2LxKnLBKqL1h2LxK-LBonLBKqLxKBLB.BLBK5LxK-L1-zL1--LxKqL1hnL1K2LxKnL1h5L1h2LxK-LB--LBoqt' -H 'Connection: keep-alive' --compressed",
    'zhangrfnu03375@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=0130797e33c32bd57b335e559120003d; ALF=1484203743; SUB=_2A251S-mPDeTxGeNH41ET8S7EzTyIHXVWt_fHrDV8PUJbkNAKLU3akW2JGKAw2RKGZxP7a0MYRq9Vz193mw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFyTIU5OuoyMp7Jj8C3YUcK5JpX5oz75NHD95Qf1Kn0eo271hq7Ws4Dqcj_i--ci-2Ri-2pi--NiK.XiKLWi--4iK.RiKnfi--fi-88i-2pi--Ni-27iK.c' -H 'Connection: keep-alive' --compressed",
    'cizhaopangna@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=24dd03c66b0fbbce5c7eff5902ac9aa3; ALF=1484203826; SUB=_2A251S-piDeTxGeNH41YS8CfIzziIHXVWt_YqrDV8PUJbkNAKLRCnkW17CFCgO31HepwMVpcwJTozXmePtA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF9nVg06TAYARJMUrMEMnXk5JpX5oz75NHD95Qf1KnXe054ShBXWs4Dqcj_i--NiKyWi-zci--fi-zEiK.Xi--RiKn7iKnfi--4iK.Ni-82i--Xi-iWiKnR' -H 'Connection: keep-alive' --compressed",
    'hunfentunhuan@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=192aa5cebef0d5108db9e458a6b3e536; ALF=1484203888; SUB=_2A251S-ogDeTxGeNH41AR8izIzDWIHXVWt_ZorDV8PUJbkNAKLUP8kW0kII3oQKQE50bMx3KS0yI9WcwiiA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Ry4GkcW7ehmcwGAYTkRzw5JpX5oz75NHD95Qf1KnEehzEShM4Ws4Dqcj_i--Xi-iFi-iFi--Ni-2Ni-24i--ci-zfiKnfi--fiKy2iK.ci--ciKn0i-2R' -H 'Connection: keep-alive' --compressed",
    'douyuan8480430@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=d59a3a5f5efdba8a880c3b35c4ce8b42; ALF=1484203963; SUB=_2A251S-rrDeTxGeNH41YS8S7Fyz6IHXVWt_ajrDV8PUJbkNAKLWrZkW0GNHaq7Z9qP4-93YaRmUYI8C4oYQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TDFb8pHFfEW5hSioPDOA25JpX5oz75NHD95Qf1KnXe0271K5EWs4Dqcj_i--Xi-zRiKL2i--fiKnRiKL2i--Xi-isi-2pi--fi-iWiKLsi--ciKyFi-z0; TC-Page-G0=9183dd4bc08eff0c7e422b0d2f4eeaec' -H 'Connection: keep-alive' --compressed",
    'renglan868025@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=ea1d41f6d8c6bbbde76d0590916af491; ALF=1484204045; SUB=_2A251S-tdDeTxGeNH41YS8SzFyj6IHXVWt_UVrDV8PUJbkNAKLVPfkW2PNV1EuK3DRe1FWe2Abnbe5Yu_rA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhFJqH4VZG06gFLy0Urcxb75JpX5oz75NHD95Qf1KnXe02E1K2EWs4DqcjIqc8XUcvE9FH8SCHWSFHWSEH8SEHFeCHFeEXt; TC-Page-G0=fd45e036f9ddd1e4f41a892898506007' -H 'Connection: keep-alive' --compressed",
    'chuiwu53010044@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cookie: _T_WM=8e31ea9dfde58cbcbb5d50920812fd3b; ALF=1484204110; SUB=_2A251S-seDeTxGeNH41cS-SjEyDmIHXVWt_VWrDV8PUJbkNAKLVrskW2giGYYALYoF4bUHne38ZYJH_2YqQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW6d1P8VYzPWpz88m4Gky0y5JpX5oz75NHD95Qf1Knfe0.c1hefWs4Dqcj_i--ci-z0i-2Ri--ciKLsiK.7i--fi-z4i-zRi--ciKyFi-2fi--fi-iFi-zc' -H 'Connection: keep-alive' --compressed",
    'anu96881166cheng@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=1bffc224d378090226b7430ece85593c; ALF=1484204195; SUB=_2A251S-vzDeTxGeNH41YS8i_PzjmIHXVWt_W7rDV8PUJbkNAKLRX5kW1Vn6SudCOJSJvySawPbNgln1X9iA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Q951V2GE_AbxNqpTF6FkK5JpX5oz75NHD95Qf1KnXe0zpe0-fWs4Dqcj_i--Xi-iWiK.Ei--ciKy2iKysi--RiKn7iKy2i--fiKysiKyWi--4i-24i-ih; TC-Page-G0=0cd4658437f38175b9211f1336161d7d' -H 'Connection: keep-alive' --compressed",
    'yuelun2072@163.com': "curl 'http://d.weibo.com/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: zh-CN,zh;q=0.8' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: _T_WM=52765f5018c5d34c5f77302463042cdf; ALF=1484204272; SUB=_2A251S-ugDeTxGeNH41cV8CbLyTWIHXVWt_XorDV8PUJbkNAKLWbBkW0_fe7_8gLTd0veLjcMNIpRdG9dKA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhZLMdo2m4y1PHxGYdNTkzk5JpX5oz75NHD95Qf1KnfSh5RS0z4Ws4Dqcj_i--ciKLsi-z0i--RiK.pi-2pi--ci-zfiK.0i--fi-zEi-zRi--ciKy2i-2E; TC-Page-G0=cdcf495cbaea129529aa606e7629fea7' -H 'Connection: keep-alive' --compressed",
}
WEIBO_ACCOUNT_PASSWD = 'tttt5555'
WEIBO_ACCOUNT_LIST = [

    'yinxiong07181@163.com',  # ok
    # 'daozhi02217467@163.com',
    'eid24153345bei@163.com',
    'wengdang264408@163.com',
    'tengmi27162@163.com',
    'q0306469pinchigu@163.com',
    'lianlun244814@163.com',
    # 2.5th part
    'jueqdarx5082@163.com',
    'bangsxq1239@163.com',
    # 'zhuang37335731@163.com',
    'suituw937563@163.com',
    'zhanchuangyingy@163.com',
    'ben36327616@163.com',
    'wbw08541466yous@163.com',
    'gaisi574905976@163.com',
    'duwengluyi@163.com',
    'leike811808902@163.com',
    'pumou791174@163.com',
    'kaoke028842@163.com',
    # 3rd part
    # 'zhemtbsg503417@163.com',
    'f4998616haozi2600@163.com',
    'ke42536379dongya6@163.com',
    'zhengayp14161@163.com',
    'zhecguyv547456@163.com',
    'zhutim404592@163.com',
    'zhangrfnu03375@163.com',
    'cizhaopangna@163.com',
    'hunfentunhuan@163.com',
    'douyuan8480430@163.com',
    'renglan868025@163.com',
    'chuiwu53010044@163.com',
    'anu96881166cheng@163.com',
    'yuelun2072@163.com',
    'daoci3547710@163.com',
    's2604943yueta@163.com',
    'zhong52301065@163.com',
    'y1933330jiaob@163.com',
    'wafwl51831@163.com',
    'feisakdy984205@163.com',
    'chouodnk72706@163.com',
    'o55971612shizhi@163.com',
    'zhasuvuw575223@163.com',
    'lz0590475huaimie@163.com',
    'pangfgitz7124@163.com',
    'moahb79819@163.com',
    'zhenfav24521@163.com',
    'niesbuw880403@163.com',
    'meiacun40017@163.com',
    'mo59373676xiaduan@163.com',
    'gangqazcu1908@163.com',
    'xunpso7762@163.com',
    'e12463113tuyu@163.com',
    'rs4322648zhant@163.com',
    'yuejyaf71973@163.com',
    'gs84928966jiong@163.com',
    'hedrlff139314@163.com',
    'tukgx04930@163.com',
    'b2547303zetanl@163.com',
    'kukmixp891899@163.com',
    'ey7268547luy@163.com',
    'zhengbthw91258@163.com',
    'liekeoth27678@163.com',
    'rongcico2454@163.com',
    'huangrhufa91572@163.com',
    'g2358104gangz@163.com',
    'g0489084meis@163.com',
    'lf53942582naochui@163.com',
    'linxrsnl699461@163.com',
]
"""
    'zhaivphn85109@163.com',
    'lingulll267958@163.com',
    'xixfxmd113424@163.com',
    'dc54914076lesh@163.com',
    'chadrq591817@163.com',
    'zuovrw8820@163.com',
    'i88738331jiu@163.com',
    'shiymdw2385@163.com',
    'zhiyxplf60717@163.com',
    'najx9686100gongz@163.com',
    'yihkgba7754@163.com',
    'py15032479xingzh@163.com',
    'mianmgt16357@163.com',
    'se9662468zhuikon3@163.com',
    'aa7033949qiaoq@163.com',
    'xingzhi6515@163.com',
    'dangguposhan@163.com',
    'laiyou2773@163.com',
    'tuodang523867@163.com',
    'lunmei058754@163.com',
    'dl35987347yayu@163.com',
    'xing42477567@163.com',
    'gudushantou@163.com',
    'e62774620xiam@163.com',
    'q18256685naochun@163.com',
    'zhanepze69488@163.com',
    'zhaisuqvl1951@163.com',
    'bantyjxh863944@163.com',
    'naisjoc745970@163.com',
    'chuhyi252677@163.com',
    'minkut336354@163.com',
    'c4998984lubazh@163.com',
    'ciltvn64731@163.com',
    'e60800766jilu@163.com',
    'e10338479kenai@163.com',
    'shulyt89142@163.com',
    'yingypqt5797@163.com',
    'multzdl088789@163.com',
    'zhongvwdxr016972@163.com',
    'ia4404749bail@163.com',
    'du2311048beifu26@163.com',
    'bp0833729biguan@163.com',
    'ranyipkc2290@163.com',
    'xiangpvceu378212@163.com',
    'neific065270@163.com',
    'jiakrag674169@163.com',
    'e52771661yiguanso@163.com',
    'lingrelme185754@163.com',
    'diaooiv3923@163.com',
    'li11257752guj@163.com',
]

Abandond:
    # 0th part
    # 'zhejxoxv185015@163.com',
    # 'yejljz606482@163.com',
    # 'manggylv618836@163.com',
    # 'muvsqd834154@163.com',
    # 'choubcsx105093@163.com',
    # 'x55120806qinping@163.com',
    # 1st part
    # 'tujie966764@163.com',
    # 'yonghao7509@163.com',
    # 'laizhongdang@163.com',
    # 'siche9149457@163.com',
    # 'didou3620167@163.com',
    # 'handao5460023@163.com',
    # 'laoshi968020@163.com',
    # 'zhanshi5224@163.com',
    # 'dimimei775827@163.com',
    # 2nd part
    # 'jide8992411492@163.com',
    # 'yanba246472@163.com',
    # 'wengyunfengbenpi@163.com',
    # 'yidu6056500@163.com',
    # 'tuizou0070@163.com',
    # 'xingjiao6677013@163.com',
    # 'yanbeng5380905@163.com',
    # 'zhuo46756868@163.com',
    # 'jiangqiang559478@163.com',
    # 'chuolun15199@163.com',
    # 'bogu7289774@163.com',
"""
