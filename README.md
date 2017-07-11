# hlspy

A simple headless browser based on QtWebEngine. Main objective is to create curl/wget like terminal based utility but for javascript heavy web-pages.

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
		
		--print-cookies (print cookies on terminal)
		
		--default-block (enable default adblock)
		
		--block-request=(comma separated list of resources to be blocked)
		
		--timeout=IN_SECONDS (quit only after this many seconds)
		
		--show-window (show browser window)
		
		--show-window=wxh (w=width,h=height: show browser window of given dimension)
		
		--show-window=max (maximize browser window)
		
		--grab-window=name.png (image of window will be saved as name.png in current directory)
		
		--print-pdf=name.pdf (generate pdf of webpage and save it as name.pdf in current directory)
		
		
		Examples:
		
		$ hlspy 'https://duckduckgo.com' 
		
		$ hlspy 'https://duckduckgo.com' --output=out.html
		
		$ hlspy 'https://duckduckgo.com' --print-request --output=out.html
		
		$ hlspy 'https://duckduckgo.com' --output=out.html --block-request=.jpg,.png,.gif
		
		$ hlspy 'https://duckduckgo.com' --output=out.html --print-pdf=name.pdf
		
## Notes:

1. --block-request: It will check if given substring is in the requested resource or not and will accordingly block the resource

2. --timeout: Normally hlspy will quit once loading of page has finished, however this option will allow the hlspy to quit after page_loading_time+timeout.   

3. --js-file: It will execute javascript and will also display console.log messages.

4. COOKIE_FILE, JS_FILE, OUT_FILE and all external file path name should be relative to current working directory.

5. --cookie-end-pt should be used with --wait-for-cookie. In this way hlspy will wait till the particular cookie_id appears and only then it will quit. (useful for webpage redirection)

6. printing pdf does not require --show-window option, however screenshot captured using --grab-window will require --show-window option.

7. --print-pdf works only with PyQt5 5.9+
