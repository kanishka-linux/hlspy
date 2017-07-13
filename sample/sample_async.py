import os
import sys
from functools import partial
from hlspy.hls import *


def hello(i,web,url):
	"""
	Do something with the task
	"""
	print('hello completed {0}:{1}'.format(i,url))
	obj = web[i]
	#print(obj.getcookie_string()) #uncomment to print cookie
	#print(obj.gethtml()) #uncomment to print html
	obj.get_window_object().close() #close widget

	"""
	When BrowseUrlT is initiated with show_window=True, then asynchronous code 
	works properly and all widgets are closed properly when operation is over.
	Users can use window_dim='min' as optional argument, to minimize all the 
	widgets. In a complete headless environment, users need to use xvfb and 
	should run the application by prefixing 
	'xvfb-run --server-args="-screen 0 640x480x16"' to the command of the 
	application.

	In GUI mode if user wants to run headlessly, then they should set 
	'show_window=False', however it has some problems. In GUI mode, 
	while running headlessly, once a task completes and user uses 
	get_window_object().close() then program quits without waiting for 
	completion of other tasks. Therefore, users need to be careful
	and should use the close() method only once and that too only after all 
	tasks have been completed so as to free up memory.
	"""

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	url_arr = [
		'https://en.wikipedia.org','https://duckduckgo.com',
		'https://www.google.com'
		]
	web_arr = []
	
	for i,url in enumerate(url_arr):
		web_obj = BrowseUrlT(
			url,out_file=False,quit_now=False,show_window=True,window_dim='500',
			js_file='console.log("javascript hello world")')
		web_arr.append(web_obj)
		web_arr[len(web_arr)-1].loadFinished.connect(partial(hello,i,web_arr,url))
		web_arr[len(web_arr)-1]._start()

	ret = app.exec_()
	sys.exit(ret)

	"""
	List of Arguments to BrowseUrlT

	1. quit_now=False (It is mandatory when using as library. Command line 
	version of the Program has been designed in such a way that it should quit 
	once task completes, therefore in order to change the default behaviour 
	while using it as a library quit_now needs to be set to False, so that 
	program will continue with the next task asynchronously)

	2. set_cookie=COOKIE_FILE_NAME (Absolute path)

	3. use_cookie=COOKIE_FILE_NAME (Absolute path)

	4. end_point=COOKIE_ID_NAME (Program will wait till this cookie id appears)
	 
	5. domain_name=DOMAIN_NAME_WHOSE_COOKIE_WILL_BE_FETCHED 

	6. user_agent=USER_AGENT_STRING

	7. tmp_dir=TEMP_DIR (for storing temporary data such as cache)

	8. js_file=JS_FILE (absolute path of the javascript file that will be 
		executed last once loading of original page has been finished.
		Instead of file name, users can also supply some javascript string 
		directly.)
		
	9. out_file=None,False or absolute path of file name (By default html 
		output will be displayed on terminal i.e. if None is used. If absolute 
		path of file name is supplied then output will be dumped into that 
		file. If False is used the output will not be showed on terminal and 
		won't be dumped in any file)
		
	10. wait_for_cookie=None or True (don't quit till cookie is obtained, 
		should be used in conjuction with the filed end_point)
		
	11. print_request=None or True (print requested resource urls on terminal 
		in realtime)
		
	12. print_cookies=None or True (print cookies from all domains on terminal 
		in realtime)
		
	13. timeout=IN_SECONDS (wait for this many seconds before closing. This 
		argument is pretty meaningles when used in library at the moment. Users
		need to devise their own logic in the asynchronous function for waiting
		before closing the widget)

	14. block_request= (comma separated list of resources to be blocked. 
		If requested url contain any of these substring then it will be blocked
		e.g.: block_request=.jpg,.png,.css,.ads)
		
	15. default_block=None or True (enables default simple adblock for headless 
		browsing)
		
	16. select_request= (print only particular request on terminal. 
		e.g.: select_resource=.css)
		
	17. show_window=True or False (default is False)

	18. window_dim=wxh,min,max (e.g.: window_dim=800x600, window_dim=400,
		window_dim=min or window_dim=max)
		
	19. grab_window=file_name (get screenshot of page and save as file_name.
		file name should be absolute path)
		
	20. print_pdf=file_name (convert page to pdf and save as file_name.
		File name should absolute path)

	Note: while using application as command line all file path should be 
	relative to directory, but while using as library all file paths must be 
	absolute.
	"""
