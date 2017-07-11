import unittest
import sys
import os
from PyQt5 import QtWidgets,QtWebEngineWidgets,QtWebEngineCore

class TestBrowser(unittest.TestCase):
	tmp_dir = os.path.join(os.path.expanduser('~'),'.config','hlspy')
	url = 'https://duckduckgo.com'
	dm = 'duckduckgo.com'
	ua = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0'
	out_file = os.path.join(tmp_dir,'test.html')
	
	def test_url(self):
		app = QtWidgets.QApplication(sys.argv)
		self.assertTrue(BrowseUrlT(self.url,tmp_dir=self.tmp_dir,domain_name=self.dm,
			user_agent=self.ua,out_file=self.out_file))
		ret = app.exec_()
		sys.exit(ret)
		
	def test_request_print(self):
		app = QtWidgets.QApplication(sys.argv)
		self.assertTrue(BrowseUrlT(self.url,tmp_dir=self.tmp_dir,print_request=True,
			domain_name=self.dm,user_agent=self.ua,out_file=self.out_file))
		ret = app.exec_()
		sys.exit(ret)
		
	def test_browser_show(self):
		app = QtWidgets.QApplication(sys.argv)
		self.assertTrue(BrowseUrlT(self.url,tmp_dir=self.tmp_dir,print_request=True,
			domain_name=self.dm,user_agent=self.ua,show_window=True,out_file=self.out_file))
		ret = app.exec_()
		sys.exit(ret)	
		
if __name__ == '__main__':
	home = os.path.join(os.path.expanduser('~'),'.config','hlspy')
	if not os.path.exists(home):
		os.makedirs(home)
	BASEDIR,BASEFILE = os.path.split(os.path.abspath(__file__))
	parent_basedir,__ = os.path.split(BASEDIR)
	print(parent_basedir)
	sys.path.insert(0,parent_basedir)
	k_dir = os.path.join(parent_basedir,'hlspy')
	sys.path.insert(0,k_dir)
	from hls import BrowseUrlT
	unittest.main()
	
