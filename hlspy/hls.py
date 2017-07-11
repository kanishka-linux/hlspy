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
import re
import time
import calendar
from datetime import datetime

from PyQt5 import QtCore,QtNetwork,QtWidgets,QtWebEngineWidgets,QtWebEngineCore
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl,pyqtSlot,pyqtSignal
from netmon import NetWorkManager


				
class BrowserPage(QWebEnginePage):  
	cookie_signal = pyqtSignal(str)
	media_signal = pyqtSignal(str)
	media_received = pyqtSignal(str)
	#val_signal = pyqtSignal(str)
	def __init__(self,url,set_cookie=None,use_cookie=None,end_point=None,
			domain_name=None,user_agent=None,tmp_dir=None,js_file=None,
			out_file=None,wait_for_cookie=None,print_request=None,
			print_cookies=None,timeout=None,block_request=None,default_block=None,
			select_request=None,tab_web=None,grab_window=None,print_pdf=None):
		super(BrowserPage, self).__init__()
		self.user_agent = user_agent
		self.set_cookie = set_cookie
		self.use_cookie = use_cookie
		self.end_point = end_point
		self.domain_name = domain_name
		self.tmp_dir = tmp_dir
		self.js_file = js_file
		self.out_file = out_file
		self.print_cookies = print_cookies
		self.wait_for_cookie = wait_for_cookie
		self.timeout = timeout
		self.js_content = None
		self.tab_web = tab_web
		self.grab_window = grab_window
		self.print_pdf = print_pdf
		if self.js_file:
			f = open(self.js_file,encoding='utf-8',mode='r')
			self.js_content = f.read()
			f.close()
		x = ''
		self.m = self.profile().cookieStore()
		self.profile().setHttpUserAgent(self.user_agent)
		self.loadFinished.connect(self._loadFinished)
		self.loadProgress.connect(self._loadProgress)
		self.loadStarted.connect(self._loadstart)
		self.pdfPrintingFinished.connect(self._pdf_finished)
		p = NetWorkManager(self,url,print_request,block_request,default_block,select_request)
		p.netS.connect(lambda y = x : self.urlMedia(y))
		self.media_received.connect(lambda y = x : self.urlMedia(y))
		self.profile().setRequestInterceptor(p)
		#self.profile().clearHttpCache()
		self.profile().setCachePath(self.tmp_dir)
		self.profile().setPersistentStoragePath(self.tmp_dir)
		self.url = url
		z = ''
		self.c_list = []
		t = ''
		self.cnt = 0
		print(self.use_cookie)
		if self.use_cookie:
			self.m.deleteAllCookies()
			self._set_cookie(use_cookie)
		else:
			self.m.deleteAllCookies()
			self.m.cookieAdded.connect(lambda  x = t : self._cookie(x))
			
		self.got_cookie = False
		self.text = ''
		self.final_url_got = False
		self.html_file = ''
		
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.quit_browser)
		self.timer.setSingleShot(True)
	
	def quit_browser(self):
		sys.exit(0)
		
	@pyqtSlot(str)
	def urlMedia(self,info):
		lnk = os.path.join(self.tmp_dir,'lnk.txt')
		if os.path.exists(lnk):
			os.remove(lnk)
		print('*******')
		print(info)
		f = open(lnk,'w')
		f.write(info)
		f.close()
		print(self.url,'--url---','--312---')
		self.media_signal.emit(info)
		print('********')
		
	@pyqtSlot(str)
	def val_found(self,info):
		print(info,'*******info*********')
		self.val = info
	
	def javaScriptAlert(self,url,msg):
		print(msg,'--msg--',url.url())
	
	def javaScriptConsoleMessage(self,level,msg,line,source):
		print(msg)
		
	def _set_cookie(self,cookie_file):
		cookie_arr = QtNetwork.QNetworkCookie()
		c = []
		f = open(cookie_file,'r')
		lines = f.readlines()
		f.close()
		for i in lines:
			k = re.sub('\n','',i)
			if k:
				l = k.split('	')
				d = QtNetwork.QNetworkCookie()
				d.setDomain(l[0])
				#print(l[0],'--setting--')
				if l[1]== 'TRUE':
					l1= True
				else:
					l1= False
				d.setHttpOnly(l1)
				d.setPath(l[2])
				#print(l1)
				#print(l[2])
				if l[3]== 'TRUE':
					l3= True
				else:
					l3= False
				d.setSecure(l3)
				#print(l[3])
				l4 = int(l[4])
				#print(l4)
				d.setExpirationDate(QtCore.QDateTime.fromTime_t(l4))
				l5 = bytes(l[5],'utf-8')
				d.setName((l5))
				l6 = bytes(l[6],'utf-8')
				d.setValue(l6)
				c.append(d)
				self.profile().cookieStore().setCookie(d)
				#print('--cookie--set--')
		
		
	def _cookie(self,x):
		result = ''
		l = str(x.toRawForm())
		l = re.sub("b'|'",'',l)
		l = self._getTime(l)
		if self.print_cookies:
			print(l)
		if not self.got_cookie:
			self._writeCookies(l)
		if self.end_point:
			if self.end_point in l and not self.got_cookie:
				self.cookie_signal.emit("Cookie Found")
				self.got_cookie = True
		
	def cookie_split(self,i):
		m = []
		j = i.split(';')
		index = 0
		for k in j:
			if '=' in k:
				l = k.split('=',1)
				l[0] = re.sub(' ','',l[0])
				t = (l[0],l[1])
			else:
				k = re.sub(' ','',k)
				t = (k,'TRUE')
			m.append(t)
			if index == 0 and '=' in k:
				m.append(('name_id',l[0]))
			index = index + 1
		d = dict(m)
		return(d)
		
	def _writeCookies(self,i):
		cfc = ''
		cfd = ''
		asp = ''
		idt = ''
		utmc = ''
		reqkey = ''
		dm = False
		if self.domain_name:
			reqkey = self.cookie_split(i)
			try:
				if self.domain_name in reqkey['domain']:
					dm = True
			except:
				pass
			try:
				reqkey['expiry']
			except:
				reqkey.update({'expiry':'0'})
			try:
				reqkey['HttpOnly']
			except:
				reqkey.update({'HttpOnly':'False'})
		if dm:
			str1 = ''
			if reqkey:
				str1 = reqkey['domain']+'	'+'FALSE'+'	'+reqkey['path']+'	'+'FALSE'+'	'+reqkey['expiry']+'	'+reqkey['name_id']+'	'+reqkey[reqkey['name_id']]
			cc = os.path.join(self.set_cookie)
			if not os.path.exists(cc):
				f = open(cc,'w')
				f.write(str1)
			else:
				f = open(cc,'a')
				f.write('\n'+str1)
			
			f.close()
			
	def _getTime(self,i):
		j = re.findall('expires=[^;]*',i)
		if j:
			l = re.sub('expires=','',j[0])
			d = datetime.strptime(l,"%a, %d-%b-%Y %H:%M:%S %Z")
			t = calendar.timegm(d.timetuple())
			k = '; expiry='+str(int(t))
		else:
			k = '; expiry='+str(0)
		i = re.sub('; expires=[^;]*',k,i)
		return i
						
	def _loadstart(self):
		result = ''
		
	def htm_src(self,x):
		self.html_file = x
	
	def _pdf_finished(self,path,val):
		print(val,path)
		if not self.timeout:
			sys.exit(0)
	
	def val_scr(self,x):
		print('===============java----------scr')
		val = x
		print(val)
		print('===============java----------scr')
		if self.timeout:
			self.timer.start(self.timeout*1000)
		else:
			sys.exit(0)
		
	def _loadProgress(self):
		result =''
		self.toHtml(self.htm_src)
		self.cnt = self.cnt+1
		
	def _loadFinished(self):
		result = ""
		print('Finished')
		if self.grab_window:
			self.tab_web.grab().save(self.grab_window)
			
		if not self.out_file:
			print(self.html_file)
		else:
			f = open(self.out_file,'wb')
			f.write(self.html_file.encode('utf-8'))
			f.close()
		if self.js_content:
			self.runJavaScript(self.js_content,self.val_scr)
			if self.print_pdf:
				self.printToPdf(self.print_pdf)
			#print(self.js_content)
		else:
			if not self.wait_for_cookie and not self.timeout and not self.print_pdf:
				sys.exit(0)
			elif self.print_pdf and not self.timeout:
				self.printToPdf(self.print_pdf)
			elif self.timeout:
				if self.print_pdf:
					self.printToPdf(self.print_pdf)
				self.timer.start(self.timeout*1000)

class BrowseUrlT(QWebEngineView):
	#cookie_s = pyqtSignal(str)
	def __init__(self,url,set_cookie=None,use_cookie=None,end_point=None,
			domain_name=None,user_agent=None,tmp_dir=None,js_file=None,
			out_file=None,wait_for_cookie=None,print_request=None,
			print_cookies=None,timeout=None,block_request=None,default_block=None,
			select_request=None,show_window=None,window_dim=None,grab_window=None,
			print_pdf=None):
		super(BrowseUrlT, self).__init__()
		#QtWidgets.__init__()
		self.url = url
		self.add_cookie = True
		self.media_val = ''
		self.cnt = 0
		self.set_cookie = set_cookie
		self.use_cookie = use_cookie
		self.value_encode = ''
		if end_point:
			self.end_point = end_point
		else:
			self.end_point = None
		
		self.domain_name = domain_name
		self.user_agent = user_agent
		self.tmp_dir = tmp_dir
		self.js_file = js_file
		self.out_file = out_file
		self.wait_for_cookie = wait_for_cookie
		self.print_request = print_request
		self.print_cookies = print_cookies
		self.timeout = timeout
		self.block_request = block_request
		self.default_block = default_block
		self.select_request = select_request
		self.show_window = show_window
		self.window_dim = window_dim
		self.grab_window = grab_window
		self.print_pdf = print_pdf
		self.Browse(self.url)
		
	def Browse(self,url):
		win_hide = False
		show_max = False
		self.tab_web = QtWidgets.QWidget()
		self.tab_web.hide()
		if self.window_dim is None:
			self.tab_web.setMaximumSize(500,500)
		else:
			win_dim = self.window_dim.lower()
			if win_dim == 'max':
				show_max = True
			else:
				if 'x' in win_dim:
					w,h = win_dim.split('x')
				else:
					w = h = win_dim
				if win_dim == '0':
					show_max = True
					win_hide = True
				else:
					self.tab_web.setMaximumSize(int(w),int(h))
		self.tab_web.setWindowTitle('Wait!')
		self.horizontalLayout_5 = QtWidgets.QVBoxLayout(self.tab_web)
		self.horizontalLayout_5.addWidget(self)
		
		self.web = BrowserPage(url,self.set_cookie,self.use_cookie,self.end_point,
					self.domain_name,self.user_agent,self.tmp_dir,self.js_file,
					self.out_file,self.wait_for_cookie,self.print_request,
					self.print_cookies,self.timeout,self.block_request,self.default_block,
					self.select_request,self.tab_web,self.grab_window,self.print_pdf)
		
		self.web.cookie_signal.connect(self.cookie_found)
		#self.web.media_signal.connect(self.media_source_found)
		self.setPage(self.web)
		print('add_cookie')
		self.load(QUrl(url))
		print('--')
		#self.load(QUrl(url))
		self.cnt = 1
		
		QtWidgets.QApplication.processEvents()
		if self.show_window:
			if win_hide:
				self.tab_web.hide()
			else:
				if show_max:
					self.tab_web.showMaximized()
				else:
					self.tab_web.show()
		else:
			self.tab_web.hide()
		
	@pyqtSlot(str)
	def cookie_found(self):
		#global web
		print('cookie')
		self.add_cookie = False
		self.setHtml('<html>cookie Obtained</html>')
		sys.exit(0)

	@pyqtSlot(str)
	def media_source_found(self):
		#global web
		self.setHtml('<html>Media Source Obtained</html>')
		print('media found')
		sys.exit(0)
	



