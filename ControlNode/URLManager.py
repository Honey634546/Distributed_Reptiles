import pickle
import hashlib


class URLManager(object):
    def __init__(self):
        self.new_URLs = self.load_progress('new_urls.txt')
        self.old_URLs = self.load_progress('old_urls.txt')

    def new_url_size(self):
        """
        获取未爬去url集合的大小
        """
        return len(self.new_URLs)

    def old_url_size(self):
        """
        获取已爬去url集合的大小
        """
        return len(self.old_URLs)

    def has_new_URL(self):
        """判断是否有未爬取的URL"""
        return self.new_url_size()

    def get_new_URL(self):
        """
        获取一个未爬去的URL
        """
        new_URL = self.new_URLs.pop()
        m = hashlib.md5()
        # m.update(new_URL.encode('utf-8'))
        self.old_URLs.add(m.hexdigest()[8:-8])
        return new_URL

    def add_new_URL(self, URL):
        """
        将新的URL添加到未爬去的URL集合中
        :param url:单个URL
        """
        if URL is None:
            return
        m = hashlib.md5()
        m.update(URL.url.encode('utf-8'))
        url_md5 = m.hexdigest()[8:-8]
        if URL not in self.new_URLs and url_md5 not in self.old_URLs:
            self.new_URLs.add(URL)

    def add_new_URLs(self, URLs):
        """
        将新的URL添加到未爬取的URL集合中
        :param urls:url集合
        """
        if URLs is None or len(URLs) == 0:
            return
        for URL in URLs:
            self.add_new_URL(URL)

    def load_progress(self, path):
        """
        从本地文件加载进度
        :param path:文件路径
        :return:返回set集合
        """
        print("从文件加载进度:%s" % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print("无进度文件，创建:%s" % path)
        return set()
