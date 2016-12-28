#coding=utf-8
import re
import json
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
from zc_spider.weibo_spider import WeiboSpider
from zc_spider.weibo_utils import catch_parse_error

class WeiboFollowSpider(WeiboSpider):
    def __init__(self, start_url, account, password, timeout=10, delay=1, proxy={}):
        WeiboSpider.__init__(self, start_url, account, password, timeout=timeout, delay=delay, proxy=proxy)
        self.pageno = 1

    @catch_parse_error((AttributeError, Exception))
    def get_max_page_no(self):
        max_page = 0
        if not self.page:
            return max_page
        # Parse game is on !!!
        # cut_code = '\n'.join(self.page.split('\n')[100:])
        # elminate_white = re.sub(r'\\r|\\t|\\n', '', self.page)
        # elminate_quote = re.sub(r'\\"', '"', elminate_white)
        # short_code = re.sub(r'\\/', '/', elminate_quote)
        parser = bs(self.page, "html.parser")
        # parsing is on!!!
        # only 2: http://weibo.com/xbxmjddwtl/follow
        # nothing: http://weibo.com/3121104750/follow?page=11
        # import ipdb; ipdb.set_trace()
        target_script = [sc for sc in parser.find_all('script') if 'follow_list' in sc.text]
        script_parser = bs(json.loads(target_script[0].text[8:-1])['html'], 'html.parser')
        page_list_parser = script_parser.find('div', {'class': re.compile('WB_cardpage'), 'node-type': 'pageList'})
        if script_parser and not page_list_parser:
            max_page = 1
        elif page_list_parser:
            max_page = int(page_list_parser.find_all('a', {'class': 'page S_txt1'})[-1].text.strip())
        else:
            print >>open('./html/max_page_error_%s.html' % dt.now().strftime("%Y-%m-%d %H:%M:%S"), 'w'), parser
        print "%s has %s pages of follows" % (self.url, max_page)
        if max_page > 5:
            self.pageno = 5
        else:
            self.pageno = max_page
        return self.pageno


    @catch_parse_error((AttributeError, Exception))
    def get_user_follow_list(self):
        follow_list = []
        if not self.page:
            return follow_list
        # Parse game is on !!!
        parser = bs(self.page, "html.parser")
        print 'Parsing page: %s' % self.url
        try:
            name_script =  [sc for sc in parser.find_all('script') if 'pf_username' in sc.text]
        except IndexError as e:
            print str(e)
            print >>open('./html/unknown_error_%s.html' % dt.now().strftime("%Y-%m-%d %H:%M:%S"), 'w'), parser
        target_script = [sc for sc in parser.find_all('script') if 'follow_list' in sc.text]
        if not (target_script and name_script):
            print >>open('./html/whole_parse_error_%s.html' % dt.now().strftime("%Y-%m-%d %H:%M:%S"), 'w'), parser
            return follow_list
        script_parser = bs(json.loads(target_script[0].text[8:-1])['html'], 'html.parser')
        name_parser = bs(json.loads(name_script[0].text[8:-1])['html'], 'html.parser')
        follow_parser = script_parser.find('ul', {'class': 'follow_list', 'node-type': 'userListBox'})
        if not (follow_parser and name_parser and follow_parser):
            print >>open('./html/follows_parse_error_%s.html' % dt.now().strftime("%Y-%m-%d %H:%M:%S"), 'w'), follow_parser
            return follow_list
        myname = name_parser.find('div', {'class': 'pf_username'}).text.encode('utf8').strip()
        if not myname:
            print >>open('./html/name_parse_error_%s.html' % dt.now().strftime("%Y-%m-%d %H:%M:%S"), 'w'), name_parser
            return follow_list
        # parse list of follows
        for li_tag in follow_parser.find_all('li', {'class': re.compile('follow_item')}):
            info_dict = {}
            try:
                topic_tag = li_tag.find('a', {'href': re.compile('^/p/100\w+')})
                if topic_tag:
                    print 'Ignore topic: %s' % topic_tag.get('title', '').encode('utf8')
                    continue
                name_tag = li_tag.find('a', {'usercard': re.compile('id=')})
                if name_tag:
                    info_dict['name'] = name_tag.text.encode('utf8')
                    info_dict['usercard'] = re.search(r'id=(\d+)', name_tag.get('usercard', '')).group(1)
                    # info_dict['info_url'] = info_dict['usercard'] + '/info'
                if li_tag.find('i', {'class': 'W_icon icon_approve'}):
                    info_dict['type'] = 'W_icon icon_approve'
                elif li_tag.find('i', {'class': 'W_icon icon_approve_co'}):
                    info_dict['type'] = 'W_icon icon_approve_co'
                    # info_dict['info_url'] = info_dict['usercard'] + '/about'
                elif li_tag.find('i', {'class': 'W_icon icon_approve_gold'}):
                    info_dict['type'] = 'W_icon icon_approve_gold'
                else:
                    pass
                stat_tag = li_tag.find('div', {'class': 'info_connect'})
                if stat_tag:
                    # import ipdb; ipdb.set_trace()
                    info_dict['follows'] = stat_tag.find('a', {'href': re.compile(r'follow$')}).text
                    info_dict['fans'] = stat_tag.find('a', {'href': re.compile(r'fans$')}).text
                    # info_dict['blogs'] = stat_tag.find('a', {'href': re.compile(r'^/\w+$')}).text
                    info_dict['blogs'] = stat_tag.find_all('a')[-1].text  # /charactr or /u/u_id
                info_dict['myname'] = myname
                info_dict['url'] = '/'.join(self.url.split('/')[:-1])
                info_dict['date'] = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                follow_list.append(info_dict)
                # for k, v in info_dict.items():
                #     print k, v
            except Exception as e:
                print dt.now().strftime("%Y-%m-%d %H:%M:%S"), str(e)
        return follow_list