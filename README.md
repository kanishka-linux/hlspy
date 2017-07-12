# hlspy

A simple headless browser based on QtWebEngine. Main objective is to create curl/wget like terminal based utility but for javascript heavy web-pages. However, it can be also used as a python library for asynchronous web-scrapping.

## Dependencies

		Python 3.5+, PyQt5 5.9+

# Installation

		$ git clone https://github.com/kanishka-linux/hlspy
		$ cd hlspy
		$ python3 setup.py sdist (or python setup.py sdist)
		$ cd dist
		$ sudo pip3 install pkg_available_in_directory (or pip install pkg_available_in_directory)
			
# Uninstall

		$ sudo pip3 uninstall hlspy
			
# Documentation

		$ hlspy URL [options]
		
		options:
		
		--help (display some help options)
		
		--set-cookie-file=COOKIE_FILE
				
		--use-cookie-file=COOKIE_FILE
		
		--js-file=file.js (run javascript file.js)
		
		--output=out.html
		
		--cookie-end-pt=last_desired_cookie_id
		
		--cookie-domain-name=domain_name
		
		--tmp-dir=TMP_DIR (If not mentioned, default TMP_DIR will be ~/.config/hlspy/)
		
		--user-agent=USER_AGENT
		
		--wait-for-cookie (Do not quit till desired cookie_id obtained)
		
		--print-request (print resource requested by webpage on terminal)
		
		--select-request= (print only request with particular substring on terminal)
		
		--print-cookies (print cookies on terminal)
		
		--default-block (enable default adblock)
		
		--block-request=(comma separated list of resources to be blocked)
		
		--timeout=IN_SECONDS (quit only after this many seconds)
		
		--show-window (show browser window)
		
		--show-window=wxh (w=width,h=height: show browser window of given dimension)
		
		--show-window=max (maximize browser window)
		
		--show-window=min (minimize browser window)
		
		--grab-window=name.png (image of window will be saved as name.png in current directory)
		
		--print-pdf=name.pdf (generate pdf of webpage and save it as name.pdf in current directory)
		
		
		Examples:
		
		$ hlspy 'https://duckduckgo.com' (will print html output to terminal)
		
		$ hlspy 'https://duckduckgo.com' --output=out.html (will write html output to out.html)
		
		$ hlspy 'https://duckduckgo.com' --print-request --output=out.html
		
		$ hlspy 'https://duckduckgo.com' --output=out.html --block-request=.jpg,.png,.gif
		
		$ hlspy 'https://duckduckgo.com' --output=out.html --print-pdf=name.pdf
		
		
## Use as a Library

Once hlspy is installed use following command

		from hlspy.hls import *
		
		web = BrowseUrlT(url,quit_now=False) {check arguments of __init__ function of BrowseUrlT in hls.py for more parameters}
		
		use **web.loadFinished** signal to connect to another function asynchronously
		
		then use **web._start()** to start loading page
		
Some methods to use on web instance:
		
1. web.gethtml() : gets html
		
2. web.getcookie_string() : get cookies
		
3. web.get_window_object() : gets widget of webview. Users need to close the widget manually once desired information has been obtained, otherwise every widget will remain active in the background and will consume memory.

Sample code is located in **sample** directory. Users can directly execute the program if hlspy is installed properly with PyQt5 5.9+.
		

		
## Notes:

1. --block-request: It will check if given substring is in the requested resource or not and will accordingly block the resource

2. --timeout: Normally hlspy will quit once loading of page has finished, however this option will allow the hlspy to quit after page_loading_time+timeout.   

3. --js-file: It will execute javascript and will also display console.log messages.

4. COOKIE_FILE, JS_FILE, OUT_FILE and all external file path name should be relative to current working directory.

5. --cookie-end-pt should be used with --wait-for-cookie. In this way hlspy will wait till the particular cookie_id appears and only then it will quit. (useful for webpage redirection)

6. printing pdf does not require --show-window option, however screenshot captured using --grab-window will require --show-window option.

7. --print-pdf works only with PyQt5 5.9+
