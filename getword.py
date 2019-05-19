
import re
import os
import sys
import string
import urllib2


def get_mp3_url(word, headers=None):
	user_agent = ('Mozilla/5.0 (Windows NT 6.1; rv:9.0) '
					  + 'Gecko/20100101 Firefox/9.0')
	if headers is None:
		headers = {'User-Agent' : user_agent}
	url ='http://www.iciba.com/%s/' % urllib2.quote(word)
	request = urllib2.Request(url=url, headers=headers)
	try:
		html = urllib2.urlopen(request).read()
		index = string.find(html, "new-speak-step")
		target_seg = html[index:index+500]
		res_tr = r'[\s\S]+ms-on-mouseover="sound(.+)"></i>[\s\S]+'
		m_tr =  re.findall(res_tr,target_seg,re.S|re.M)
		if len(m_tr) > 0:
			mp3_url = m_tr[0]
			return mp3_url.split("'")[1]
	except:
		print "network failure!"
		return None

def save_mp3(url,word,file_path,headers=None):
	if url is None:
		print ""
	else:
		user_agent = ('Mozilla/5.0 (Windows NT 6.1; rv:9.0) '
                      + 'Gecko/20100101 Firefox/9.0')
		if headers is None:
			headers = {'User-Agent' : user_agent}
		headers['Referer'] = 'http://www.iciba.com/%s/' % urllib2.quote(word)
		# read web content
		request = urllib2.Request(url=url, headers=headers)
		try:
			file_data = urllib2.urlopen(request).read()
		except:
			print "Network failure!"
			return None
		else:
			try:
				with open(file_path,'wb') as output:
					# write data, that is download file
					output.write(file_data)
			except:
				print "Save mp3 fail, maybe dir or something wrong!"
			return file_path

def main():
        if len(sys.argv) < 2:
		print "Please input words, such as: banana or apple,banana"
		return	
	swords = sys.argv[1]
        print "Getting ", swords, " sounds file..." 
	words = swords.split(",")

	if os.path.isdir("sounds") == False:
		os.makedirs("sounds", 0755 )
	for word in words:
		if os.path.isfile("sounds/" + word + ".mp3") == False:
			url = get_mp3_url(word)
			print "Got url: ", url
			target_name = "sounds/"+word+".mp3"
			save_mp3(url, word, target_name)
        
if __name__ == '__main__':
	main()
