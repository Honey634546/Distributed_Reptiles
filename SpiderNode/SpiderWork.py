from multiprocessing.managers import BaseManager
# from HTMLDownloader import HTMLDownloader
# from HTMLParser import HTMLParser


from SpiderNode.HTMLDownloader import HTMLDownloader
from SpiderNode.HTMLParser import HTMLParser
from SpiderNode.URL import URL


class SpiderWork(object):
    def __init__(self):
        BaseManager.register('get_task_queue')
        BaseManager.register('get_result_queue')
        BaseManager.register('get_key_queue')

        # server_addr = '127.0.0.1'
        server_addr='139.224.113.238'
        print("connect to server %s" % server_addr)

        self.m = BaseManager(address=(server_addr, 8001), authkey='honey'.encode('utf-8'))
        self.m.connect()
        # 获取Queue的对象
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.key = self.m.get_key_queue()
        self.downloader = HTMLDownloader()
        self.parser = HTMLParser()
        print("初始画完成")

    def crwal(self):
        key = self.key.get()
        while True:
            try:
                if not self.task.empty():
                    URL = self.task.get()
                    if URL == "end":
                        print("控制节点通知爬虫节点停止共工作")
                        return
                    url = URL.url
                    print("正在解析:%s" % url.encode('utf-8'))
                    new_urls = self.parser.parser_url(URL)
                    self.result.put(new_urls)
                    # self.task.put(new_urls)
                    self.downloader.download(url)
                    if self.downloader.find_key(url, key):
                        self.result.put('end')
                        return
            except EOFError:
                print("连接工作节点失败")
                return
            except Exception:
                print("crwal fail")


if __name__ == "__main__":
    spider = SpiderWork()
    spider.crwal()
