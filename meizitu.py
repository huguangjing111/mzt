# -*- encoding:utf-8 --
import random
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import requests
from lxml import etree
import time
import urllib


class MeizituSpider:
    def __init__(self):
        self.index_urls = ["http://www.mzitu.com/page/" + str(page) + "/" for page in range(24, 177)]
        self.headers = {
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate",
            # "Accept-Language": "zh-CN,zh;q=0.9",
            # "Connection": "keep-alive",
            # "Cookie": "Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1524561240; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1524561244",
            # "Host": "www.mzitu.com",
            # "Referer": "http://www.mzitu.com/",
            # "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36"
        }
        self.proxies = {}
        self.count = 1
        self.img_url_list = []

    def send_request(self, url):
        # time.sleep(random.randint(0, 3))
        print u"[INFO] 正在请求网站主页 %s" % url
        response = requests.get(url, headers=self.headers, proxies=self.proxies)
        self.parse_page(response)

    def parse_page(self, response):
        html = etree.HTML(response.content)
        # 所有的个人中心url
        detail_index_urls = html.xpath("//ul[@id='pins']/li/a/@href")
        # 遍历个人页面
        for detail_index_url in detail_index_urls:
            try:
                # time.sleep(random.randint(0, 3))
                response = self.send_request_detail_index(detail_index_url)
                detail_html = etree.HTML(response.content)
                images_count = detail_html.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]
                images_count = int(images_count)
                # 个人详情页的所有urls
                detail_urls = [detail_index_url + "/" + str(num) for num in range(1, images_count + 1)]
                for detail_url in detail_urls:
                    try:
                        # time.sleep(random.randint(0, 3))
                        print u"[INFO] 正在请求个人详情页面 %s" % detail_url
                        response = requests.get(detail_url, headers=self.headers, proxies=self.proxies)
                        html = etree.HTML(response.content)
                        img_url = html.xpath('//div[@class="main-image"]//img/@src')[0]
                        self.send_request_img(img_url, detail_index_url,detail_url)
                    except Exception as e:
                        print e
            except Exception as e:
                print e

    def send_request_img(self, img_url, detail_index_url,detail_url):
        # time.sleep(random.randint(0, 3))
        while True:
            html = None
            try:
                headers = {
                    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                    "Host": "i.meizitu.net",
                    "Proxy-Authorization": "Basic maozhaojun:ntkn0npx",
                    "Proxy-Connection": "keep-alive",
                    "Referer": detail_url,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36"
                }
                print u"[INFO] 正在请求图片地址 %s" % img_url
                if img_url in self.img_url_list:
                    break
                else:
                    html = requests.get(img_url, headers=headers,proxies=self.proxies).content
            except Exception as e:
                print e
            if not html:
                print u"请重新连接"
                continue
            else:
                print u"[INFO] 写入图片第 %d 张" % self.count
                with open("./images/" + detail_index_url[-6:] + img_url[-9:], "wb") as f:
                    f.write(html)
                    print u"[INFO] 完成图片第 %d 张" % self.count
                    self.img_url_list.append(img_url)
                    self.count += 1
                break


    def send_request_detail_index(self, url):
        # time.sleep(random.randint(0, 3))
        try:
            response = requests.get(url,proxies=self.proxies)
            return response
        except Exception as e:
            print e

    def main(self):
        for url in self.index_urls:
            try:
                self.send_request(url)
            except Exception as e:
                print e


if __name__ == '__main__':
    spider = MeizituSpider()
    spider.main()
