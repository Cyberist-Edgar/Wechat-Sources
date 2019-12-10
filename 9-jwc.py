import requests
import re
import os
import time


def get_html(url):
	header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0"}
	response = requests.get(url,headers=header,timeout=5)
	try:
		response.raise_for_status()
	except Exception as e:
		print(e)
	else:
		return response.text

def get_notice_to_student():
	"""
	爬取面向学生通知的内容
	"""
	flag = False
	# pattern = re.complile("<table.*class=\"main_r_font_bt\">(.*?)<a.*")
	if os.path.exists("notice_to_student.txt"):
		os.remove("notice_to_student.txt")
	file = open("notice_to_student.txt", mode="a", encoding="utf-8")
	html = get_html("http://jwc.sjtu.edu.cn/rss/rss_notice.aspx?SubjectID=198076&TemplateID=221038")
	pattern = re.compile("<item><title>(.*?)</title><link>(.*?)</link><pubDate>(.*?)</pubDate></item>", flags=re.S)
	print("面向学生通知:")
	for item in re.findall(pattern, html):
		title = item[0]
		link = item[1]
		pubDate = item[2]
		if get_current_time() in pubDate:
			print(title+"\t"+link+"\t"+pubDate)
			flag = True
		file.write(title+"\t"+link+"\t"+pubDate+"\n")
	file.close()
	return flag


def get_news():
	"""
	获取新闻资讯
	"""
	flag = False
	if os.path.exists("news.txt"):
		os.remove("news.txt")
	file = open("news.txt",mode="a",encoding="utf-8")
	html = get_html("http://jwc.sjtu.edu.cn/rss/rss_notice.aspx?SubjectID=198059&TemplateID=221026")
	pattern = re.compile("<item><title>(.*?)</title><link>(.*?)</link><pubDate>(.*?)</pubDate></item>", flags=re.S)
	print("新闻资讯: ")
	for item in re.findall(pattern, html):
		title = item[0]
		link = item[1]
		pubDate = item[2]
		if get_current_time() in pubDate:
			print(title+"\t"+link+"\t"+pubDate)
			flag = True
		file.write(title+"\t"+link+"\t"+pubDate+"\n")
	file.close()
	return flag

def get_notice():
	"""
	获取通知报告
	"""
	flag = False
	if os.path.exists("notice.txt"):
		os.remove("notice.txt")
	file = open("notice.txt",mode="a",encoding="utf-8")
	html = get_html("http://jwc.sjtu.edu.cn/rss/rss_notice.aspx?SubjectID=198015&TemplateID=221027")
	pattern = re.compile("<item><title>(.*?)</title><link>(.*?)</link><pubDate>(.*?)</pubDate></item>", flags=re.S)
	print("通知报告:")
	for item in re.findall(pattern, html):
		title = item[0]
		link = item[1]
		pubDate = item[2]
		if get_current_time() in pubDate:
				print(title+"\t"+link+"\t"+pubDate)
				flag = True
		file.write(title+"\t"+link+"\t"+pubDate+"\n")
	file.close()
	return flag

def get_current_time():
	struct = time.localtime()
	year = struct.tm_year
	month = struct.tm_mon
	day = struct.tm_mday
	return f"{year}-{month}-{day}"



def main():
	start = time.time()
	flag1 = get_notice_to_student()
	flag2 = get_news()
	flag3 = get_notice()
	if not (flag1 or flag2 or flag3):
		print("Today there is no news or notices ")
	end = time.time()
	print("Finished in {}".format(end-start))

if __name__ == '__main__':
	curr_time = get_current_time()
	print(curr_time)
	main()

