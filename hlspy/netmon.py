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

from PyQt5 import QtWebEngineCore
from PyQt5.QtCore import pyqtSignal

class NetWorkManager(QtWebEngineCore.QWebEngineUrlRequestInterceptor):
	netS = pyqtSignal(str)
	def __init__(self,parent,url,print_request,block_request,default_block,select_request):
		super(NetWorkManager, self).__init__(parent)
		self.url = url
		self.print_request = print_request
		if block_request:
			self.block_request = block_request.split(',')
		else:
			self.block_request = []
		self.default_block = default_block
		self.select_request = select_request
		
	def interceptRequest(self,info):
		t = info.requestUrl()
		urlLnk = t.url()
		block_url = ''
		
		#print(self.select_request,'--select-request--')
		lower_case = urlLnk.lower()
		lst = []
		if self.default_block:
			lst = [
			"doubleclick.net","ads",'.jpg','.gif','.css','facebook','.aspx',
			r"||youtube-nocookie.com/gen_204?", r"youtube.com###watch-branded-actions",
			"imagemapurl","b.scorecardresearch.com","rightstuff.com","scarywater.net",
			"popup.js","banner.htm","_tribalfusion","||n4403ad.doubleclick.net^$third-party",
			".googlesyndication.com","graphics.js","fonts.googleapis.com/css",
			"s0.2mdn.net","server.cpmstar.com","||banzai/banner.$subdocument",
			"@@||anime-source.com^$document","/pagead2.","frugal.gif",
			"jriver_banner.png","show_ads.js",'##a[href^="http://billing.frugalusenet.com/"]',
			"||contextweb.com^$third-party",".gutter",".iab",'revcontent'
			]
		if self.block_request:
			lst = lst + self.block_request
		block = False
		for l in lst:
			if lower_case.find(l) != -1:
				block = True
				break
		if block:
			info.block(True)
			
		if (self.select_request and self.select_request in urlLnk) or self.print_request:
			print(urlLnk)
			if block:
				print('-----------blocking: {0}-----------'.format(urlLnk))