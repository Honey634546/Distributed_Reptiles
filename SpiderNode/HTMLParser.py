import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
#pycharm写法
from SpiderNode.URL import URL
import urllib.robotparser


class HTMLParser(object):
    def parser_url(self, page_URL):
        """
        解析网页内url获取url集合
        :param page_URL: 下载页面的URL
        :return:返回URL集合
        """
        if page_URL.url is None:
            return
        headers = {
            'user-Agent': "Chrome/75.0.3770.100"
        }
        res = requests.get(page_URL.url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        new_URLs = self._get_new_urls(page_URL, soup)
        return new_URLs

    def _get_new_urls(self, page_URL, soup):
        """
        抽取新的url集合
        :param page_URL:下载页面的URL
        :param soup:soup
        :return:返回新的url集合
        """
        new_URLs = set()
        links = soup.findAll('a', href=re.compile(r'http.*'))
        # print(links)
        for link in links:
            new_url = link['href']
            # print(new_url)
            new_full_url = urllib.parse.urljoin(page_URL.url, new_url)
            parsed_url = urllib.parse.urlparse(new_full_url)
            # print(parsed_url)
            action = "follow"
            if self.parseRobot(new_full_url) is False:
                action = "robots_ignore"
            print("LINK:host=%s;port=%s;respath=%s;action=%s" % (parsed_url.netloc, 80, parsed_url.path, action))
            if page_URL.depth < 5:
                new_full_URL = URL(new_full_url, page_URL.depth + 1)
                new_URLs.add(new_full_URL)
        return new_URLs

    def parseRobot(self, url):
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(url + "/robot.txt")
        rp.read()
        user_agent = "ee122-KeywordHunter"
        res = rp.can_fetch(user_agent, url)
        return res
    # def find_key(self, url, key):
    #     """
    #     寻找关键字
    #     :param url: 页面url
    #     :param key: 关键字
    #     :return:
    #     """
    #     parsed_url = urllib.parse.urlparse(url)
    #     line = self.get_line(url, key)
    #     print("FOUND_KEYWORD:host=%s;port=%s;respath=%s;line=%s" % (parsed_url.netloc, 80, parsed_url.path, line))
    #
    # def get_line(self, url, key):
    #     """
    #     获取关键字所在行
    #     :param url:
    #     :param key:
    #     :return:
    #     """

# if __name__ == "__main__":
#     parser = HTMLParser()
#     ROOT = URL("https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB", 1)
#     parser.parser_url(ROOT)
