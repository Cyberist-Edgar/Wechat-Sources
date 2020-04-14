"""
@author: Edgar
@time: 2020/4/14
自动下载PPT模板   http://www.1ppt.com/moban/
"""
# 导入requests库
import requests
# 导入正则库进行信息提取
import re
import os 


class PPT:
    def __init__(self, download_path="PPT"):
        super().__init__()
        self.headers =  {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.mkdir(download_path)
    
    def download_one_ppt(self, link):
        """下载一个链接的ppt"""
        if not link.startswith("http"):
            link = "http://www.1ppt.com" + link
        response = requests.get(link)
        try:
            response.raise_for_status()
        except:
            print(f"请求 {response.url} 失败")
        else:
            response.encoding = response.apparent_encoding
            link_text = response.text
            download_url = re.findall(
                r"<ul class=\"downurllist\">.*?<li.*?href=\"(.*?)\".*?</li>.*?</ul>", link_text, re.S)[0]
            ppt = requests.get(download_url, headers=self.headers)  # 请求对应的文件
            filename = re.findall(r"<title>(.*?)</title>", link_text, re.S)[0]  # 文件名，亦可以自定义，但不能重复
            print("正在下载{}".format(filename))
            with open(self.download_path+"/"+ filename+".zip", "wb") as f:  # 以二进制的形式写入文件
                f.write(ppt.content)

    def download_one_page(self, url):
        """下载一个页面的ppt"""
        r = requests.get(url, headers=self.headers)
        try:
            # 如果请求失败的话报错
            r.raise_for_status()
        except:
            print(f"请求 {r.url} 失败")
            return 

        else:
            r.encoding = r.apparent_encoding
            html = r.text
            
            # 先获取整个 tplist
            tplist = re.findall(r'<ul class="tplist">(.*?)</ul>', html, re.S)[0]

            # 每一个li元素中包含多个需要的 链接，我们取第一个即可
            # 获取界面中需要的所有的链接
            link_list = re.findall(r"<li>.*?<a href=\"(.*?)\"", tplist)
            return link_list
        
    def run(self):
        num = 1
        url = "http://www.1ppt.com/moban/ppt_moban_{}.html"
        while(True):
            try:
                link_list = self.download_one_page(url.format(num))
                for link in link_list:
                    self.download_one_ppt(link)
            except:
                break


if __name__ == "__main__":

    ppt = PPT()
    ppt.run()