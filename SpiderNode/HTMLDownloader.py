import requests
import urllib
import codecs
import re


class HTMLDownloader(object):
    def download(self, url):
        """
        下载页面
        :param url: 页面url
        :return: 页面类容
        """
        if url is None:
            return None
        headers = {
            'user-Agent': "ee122-KeywordHunter"
        }
        res = requests.get(url, headers=headers)
        parsed_url = urllib.parse.urlparse(url)

        print("PAGE:host=%s;port=%s;respath=%s;status=%s" % (parsed_url.netloc, 80, parsed_url.path, res.status_code))
        if res.status_code == 200:
            res.encoding = 'utf-8'
            print(url[-8::])
            fout = codecs.open('%s.html' % url[-8::], 'w', encoding='utf-8')
            fout.write(res.text)
            fout.close()
            return res.text
        return None

    def find_key(self, url, key):
        parsed_url = urllib.parse.urlparse(url)
        with open('%s.html' %url[-8::] , 'r', encoding="utf-8") as f:
            num = 1
            while True:
                line = f.readline()
                # print(line)
                p = re.compile(key)
                m = re.search(p, line)
                if m is not None:
                    # print(num)
                    print("FOUND_KEYWORD:host=%s;port=%s;respath=%s;line=%s" % (
                    parsed_url.netloc, 80, parsed_url.path, num))
                    return True
                    # break
                num += 1
                if not line:
                    return False
                    # break


if __name__ == "__main__":
    load = HTMLDownloader()
    load.download("http://www.baidu.com")
    load.find_key("http://www.baidu.com", "百度")
