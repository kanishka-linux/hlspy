import os
import sys
from functools import partial
from hlspy.hls import *

global count_arr
count_arr = []

def hello(i,web,url):
	print('hello completed {0}:{1}'.format(i,url))
	obj = web[i]
	#print(obj.getcookie_string())
	#print(obj.gethtml())
	obj.get_window_object().close()
		
	
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	url = ['https://en.wikipedia.org','https://duckduckgo.com','https://www.google.com']
	web_arr = []
	j = 0
	for i in url:
		web_arr.append(BrowseUrlT(i,out_file=False,quit_now=False,
			show_window=True,window_dim='500',
			js_file='console.log("java script hello world")'))
		web_arr[len(web_arr)-1].loadFinished.connect(partial(hello,j,web_arr,i))
		web_arr[len(web_arr)-1]._start()
		j = j+1

	ret = app.exec_()
	sys.exit(ret)
