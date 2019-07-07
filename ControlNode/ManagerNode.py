from multiprocessing.managers import BaseManager
from ControlNode.URLManager import URLManager
from ControlNode.DataOutput import DataOutput
from ControlNode.URL import URL
import time
from multiprocessing import Process
from multiprocessing import Queue


class ManagerNode(object):
    """
    url_q:url管理进程将url传递给爬虫节点的通道
    result_q:爬虫节点将数据返回给数据提取进程的通道
    conn_q:数据提取进程将新的url数据提交给url管理进程的通道
    store_q:数据提取进程将获取到的数据交给数据储存进程的通道
    """

    def start_Manager(self, url_q, result_q, key_q):
        """
        创建一个分布式管理器
        :param url_q:url队列
        :param result_q:结果队列
        :return 
        """
        # 把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象
        # 将Queue对象在网络中暴露
        BaseManager.register('get_task_queue', callable=lambda: url_q)
        BaseManager.register('get_result_queue', callable=lambda: result_q)
        BaseManager.register('get_key_queue', callable=lambda: key_q)
        # 绑定端口8001，设置验证口令“honey”。这个相当于对象的初始化
        manager = BaseManager(address=('', 8001),
                              authkey='honey'.encode('utf-8'))
        return manager

    def url_manager_proc(self, url_q, key_q, conn_q, root_url, key):
        """
        url管理进程
        :param url_q:url管理进程将url传递给爬虫节点的通道
        :param conn_q:数据提取进程将新的url数据提交给url管理进程的通道
        :param root_url 初始url
        :return 
        """
        ROOT = URL(root_url, 1)
        url_manager = URLManager()
        url_manager.add_new_URL(ROOT)
        key_q.put(key)
        while True:
            while (url_manager.has_new_URL()):
                new_URL = url_manager.get_new_URL()
                url_q.put(new_URL)
                print("new_url=", url_manager.new_url_size())
                print("old_url=", url_manager.old_url_size())
                if (new_URL.depth > 5):
                    url_q.put('end')
                    print("控制节点发起结束通知")
                    url_manager.save_progress(
                        "new_urls.txt", url_manager.new_URLs)
                    url_manager.save_progress(
                        "old_urls.txt", url_manager.old_URLs)
                    return 0
            try:
                if not conn_q.empty():
                    URLs = conn_q.get()
                    # print(URLs)
                    if URLs == 'end':
                        return 0
                    url_manager.add_new_URLs(URLs)
            except BaseException:
                time.sleep(0.1)

    def result_solve_porc(self, result_q, conn_q):
        """
        :param result_q:爬虫节点将数据返回给数据提取进程的通道
        :param conn_q:数据提取进程将新的url数据提交给url管理进程的通道
        :param store_q:数据提取进程将获取到的数据交给数据储存进程的通道
        :return
        """
        while True:
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content == 'end':
                        return
                    print(content)
                    conn_q.put(content)
                else:
                    time.sleep(0.1)
                    # print("wait---")
            except BaseException:
                time.sleep(0.1)
                # print("wait---")

    # def store_porc(self, store_q):
    #     output = DataOutput()
    #     while True:
    #         if not store_q.empty():
    #             data = store_q.get()
    #             if data == 'end':
    #                 print("储存进程接受通知然后结束")
    #                 output.output_end(output.filepath)
    #                 return
    #             output.store_data(data)
    #         else:
    #             time.sleep(0.1)


if __name__ == "__main__":
    url_q = Queue()
    result_q = Queue()
    key_q = Queue()
    conn_q = Queue()

    node = ManagerNode()
    manager = node.start_Manager(url_q, result_q, key_q)
    url_manager_pro = Process(target=node.url_manager_proc, args=(
        url_q, key_q, result_q, "https://movie.douban.com/explore", "绿皮书"))
    result_por = Process(target=node.result_solve_porc, args=(result_q, conn_q,))
    url_manager_pro.start()
    result_por.start()
    manager.get_server().serve_forever()
