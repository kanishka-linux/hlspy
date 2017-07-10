"""
Copyright (C) 2017 kanishka-linux kanishka.linux@gmail.com

This file is part of hlspy.

hlspy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

hlspy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with hlspy.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import os

if getattr(sys,'frozen',False):
	BASEDIR,BASEFILE = os.path.split(os.path.abspath(sys.executable))
else:
	BASEDIR,BASEFILE = os.path.split(os.path.abspath(__file__))
print(BASEDIR,BASEFILE,os.getcwd())
sys.path.insert(0,BASEDIR)

print(sys.path,'---path---')    

from PyQt5 import QtWidgets
from hls import BrowseUrlT

def main():
	app = QtWidgets.QApplication(sys.argv)
	print('---------------679--------Engine--start--')
	home = os.path.join(os.path.expanduser('~'),'.config','hlspy')
	if not os.path.exists(home):
		os.makedirs(home)
	url = sys.argv[-1]
	if url.startswith('--'):
		url = sys.argv[1]
	set_cookie = end_point = domain_name = user_agent = t_dir = use_cookie = None
	out_file = js_file = block_request = select_request = window_dim = None
	wait_for_cookie = print_request = print_cookies = default_block = False
	show_window = grab_window = False
	timeout = 0
	for  i in sys.argv:
		if i.startswith('--set-cookie-file='):
			set_cookie = i.split('=')[1]
		elif i.startswith('--use-cookie-file='):
			use_cookie = i.split('=')[1]
		elif i.startswith('--cookie-end-pt='):
			end_point = i.split('=')[1]
		elif i.startswith('--cookie-domain-name='):
			domain_name = i.split('=')[1]
		elif i.startswith('--user-agent='):
			user_agent = i.split('=')[1]
		elif i.startswith('--tmp-dir='):
			t_dir = i.split('=')[1]
		elif i.startswith('--js-file='):
			js_file = i.split('=')[1]
		elif i.startswith('--output='):
			print(i.split('='))
			out_file = i.split('=')[1]
		elif i.startswith('--wait-for-cookie'):
			wait_for_cookie = True
		elif i.startswith('--print-request'):
			print_request = True
		elif i.startswith('--print-cookies'):
			print_cookies = True
		elif i.startswith('--timeout='):
			timeout = int(i.split('=')[1])
		elif i.startswith('--block-request='):
			block_request = i.split('=')[1]
		elif i.startswith('--default-block'):
			default_block = True
		elif i.startswith('--show-window'):
			show_window = True
			if '=' in i:
				window_dim = i.split('=')[1]
		elif i.startswith('--select-request='):
			select_request = i.split('=')[1]
		elif i.startswith('--grab-window'):
			grab_window = True
	print(url)
	print(sys.argv)
	if t_dir is None:
		t_dir = home
	if set_cookie is None:
		set_cookie = os.path.join(home,'cookie.txt')
	else:
		set_cookie = os.path.join(os.getcwd(),set_cookie)
		
	if use_cookie:
		use_cookie = os.path.join(os.getcwd(),use_cookie)
	
	if js_file:
		js_file = os.path.join(os.getcwd(),js_file)
	
	if out_file:
		out_file = os.path.join(os.getcwd(),out_file)
		
	if domain_name is None:
		if url.startswith('http'):
			domain_name = url.split('/')[2]
		else:
			domain_name = url
		domain_name = domain_name.replace('www.','',1)
	print(domain_name)
	if user_agent is None:
		user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
		
	if os.path.isfile(set_cookie):
		os.remove(set_cookie)
		
	web = BrowseUrlT(url,set_cookie=set_cookie,use_cookie=use_cookie,
			end_point=end_point,domain_name=domain_name,user_agent=user_agent,
			tmp_dir=t_dir,js_file=js_file,out_file=out_file,
			wait_for_cookie=wait_for_cookie,print_request=print_request,
			print_cookies=print_cookies,timeout=timeout,block_request=block_request,
			default_block=default_block,select_request=select_request,
			show_window=show_window,window_dim=window_dim,grab_window=grab_window)
			
	ret = app.exec_()
	sys.exit(ret)

if __name__ == "__main__":
	main()
