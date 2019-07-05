# hlspy

*A simple headless browser based on QtWebEngine (Chromium) as backend*

Main objective is to create curl/wget like terminal based utility but for javascript heavy web pages. However, it can be also used as a python library for accessing dynamic web pages asynchronously.

### Brief Description

1. The project initially started as a command-line utility to mimic curl/wget but for javascript heavy web pages. It is possible to use chrome from version 59 as a headless browser, but as of now it provides only limited command-line functionalities. hlspy provides easy way to set up and use cookies, allows inspecting requested network resource urls and cookie ids on terminal in realtime, provides default adblock and customized way to block url requests - and all these functionalities with just passing few command line arguments, without writing any javascript. 

2. It is possible to use hlspy as a python library for accessing dynamic, javascript heavy web pages and that too in a complete asynchronous manner. This feature can be useful for both asynchronous scraping and testing. Testing is possible only with the help of javascript, and javascript console messages will be displayed on terminal. 

3. hlspy also allows creating custom launchers for web sites using command-line. It is useful feature for creating web shortcut. Launchers can be launched with hlspy and will open website in a lightweight hlspy browser in windowed mode.

## Dependencies

		Python 3.5+, PyQt5 5.9+
		
# Installation

Direct via pip:

```bash
$ sudo pip3 install git+https://github.com/kanishka-linux/hlspy
```

Via source code:

```bash
$ git clone https://github.com/kanishka-linux/hlspy
$ cd hlspy
$ python3 setup.py sdist  # (or python setup.py sdist)
$ cd dist
$ sudo pip3 install pkg_available_in_directory  # (or pip install pkg_available_in_directory) 
```

**Notes:**

 - Use `sudo` depending on whether you want to install package system-wide or not
 - Use `pip` or `pip3` depending on what is available on your system
			
# Uninstall

Uninstalling hlspy:
```
sudo pip3 uninstall hlspy 
```

Uninstalling dependencies:

```
sudo pip3 uninstall PyQt5 sip
```

# Documentation

```
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
--user-agent=USER_AGENT_STRING
--wait-for-cookie (Do not quit till desired cookie_id obtained)
--print-request (print resource requested by webpage on terminal)
--select-request= (print only request with particular substring on terminal)
--print-cookies (print cookies on terminal)
--default-block (enable default adblock)
--block-request=(comma separated list of resources to be blocked
--timeout=IN_SECONDS (quit only after this many seconds)
--show-window (show browser window)
--show-window=wxh (w=width,h=height: show browser window of given dimension)
--show-window=max (maximize browser window)
--show-window=min (minimize browser window)
--grab-window=name.png (full-page screenshot of window will be saved as name.png in current directory.
			It should be used with --show-window option)
--print-pdf=name.pdf (generate pdf of webpage and save it as name.pdf in current directory)
--create-launcher=name (create launcher with 'name' for particular hlspy command as shortcut to website)
--launch name (launch launcher created with create-launcher command)
```

## Examples

```bash
hlspy 'https://duckduckgo.com'  # will print html output to terminal
hlspy 'https://duckduckgo.com' --output=out.html  # will write html output to out.html
hlspy 'https://duckduckgo.com' --print-request --output=out.html
```
Blocking request to images:
```
hlspy 'https://duckduckgo.com' --output=out.html --block-request=.jpg,.png,.gif
```

Print pdf:
```
hlspy 'https://duckduckgo.com' --output=out.html --print-pdf=name.pdf
```

Creating launcher and launching sites:
```
hlspy 'https://duckduckgo.com' --output=false --show-window=max --timeout=1000 --create-launcher=ddg
hlspy --launch ddg
```
		
## Use as a Library

Once hlspy is installed, use the following command:

```Python
from hlspy.hls import *
web = BrowseUrlT(url, quit_now=False)  # check sample code for more explanation
# use web.loadFinished signal to connect to another function asynchronously
# then use web.start_loading() to start loading page
```
		
Some methods to use on web instance:
		
1. `web.gethtml()`: gets html
		
2. `web.getcookie_string()`: get cookies
		
3. `web.get_window_object()`: gets widget of webview. Users need to close the widget manually using command `web.get_window_object().close()` once desired information has been obtained, otherwise every widget will remain active in the background and will consume memory.

Sample code is located in ![sample](/sample/sample_async.py) directory. Users can directly execute the program if hlspy is installed properly with PyQt5 5.9+.
		

		
## Notes:

1. `--block-request`: It will check if given substring is in the requested resource or not and will accordingly block the resource

2. `--timeout`: Normally hlspy will quit once loading of page has finished, however this option will allow the hlspy to quit after `page_loading_time+timeout`.   

3. `--js-file`: It will execute javascript and will also display console.log messages.

4. `--cookie-end-pt` should be used with `--wait-for-cookie`. In this way hlspy will wait till the particular `cookie_id` appears and only then it will quit. (useful for webpage redirection)

5. printing pdf does not require `--show-window` option, however screenshot captured using `--grab-window` will require `--show-window` option.

6. `--print-pdf` works only with PyQt5 5.9+

7. In most of the gnu/linux systems, PyQt5 available in official repositories is old and some of them do not package qtwebengine which is based on chromium browser. Therefore it is advisable to use pip to install PyQt5 which always contains latest updated version. 

8. If official repository of gnu/linux system contains latest PyQt5 with qtwebengine, then user should install PyQt5 from official repository instead of using pip. After that user should remove or comment out `install_requires` field in the setup.py before proceeding installation.
