# hlspy

A simple headless browser based on QtWebEngine. Main objective is to create curl/wget like terminal based utility but for javascript heavy web-pages.

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
		
		--js-file=file.js
		
		--output=out.html
		
		--cookie-end-pt=last_desired_cookie_id
		
		--cookie-domain-name=domain_name
		
		--tmp-dir=TMP_DIR
		
		--user-agent=USER_AGENT
		
		--wait-for-cookie (Do not quit till desired cookie_id obtained)
		
		--print-request (print resource requested on terminal)
		
		--print-cookies (print cookies requested on terminal)
		
		--default-block (enable default adblock)
		
		--block-request=(comma separated list of resources to be blocked)
		
		--timeout=IN_SECONDS (quit only after this many seconds)
		
		--show-window (show browser window)
		
		--show-window=wxh (w=width,h=height: show browser window of given dimension)
		
		--show-window=max (maximize browser window)
		
		--grab-window (image of window will be saved as image.png in TMP_DIR)
		
		
		Examples:
		
		$ hlspy 'https://duckduckgo.com' 
		
		$ hlspy 'https://duckduckgo.com' --output=out.html
		
		$ hlspy 'https://duckduckgo.com' --print-request --output=out.html
		
		
		
