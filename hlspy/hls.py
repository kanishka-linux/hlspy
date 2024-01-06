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
import subprocess
from threading import Lock
from datetime import datetime
from functools import partial
from PyQt5 import QtCore, QtNetwork, QtWidgets, QtWebEngineWidgets, QtWebEngineCore, QtGui
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, pyqtSlot, pyqtSignal
from netmon import NetWorkManager

                
class BrowserPage(QWebEnginePage):  
    
    cookie_signal = pyqtSignal(str)
    link_signal = pyqtSignal(str)
    link_received = pyqtSignal(str)
    #val_signal = pyqtSignal(str)
    
    def __init__(
            self, url=None, set_cookie=None, use_cookie=None, end_point=None, 
            domain_name=None, user_agent=None, tmp_dir=None, js_file=None, 
            out_file=None, wait_for_cookie=None, print_request=None, 
            print_cookies=None, timeout=None, block_request=None, default_block=None, 
            select_request=None, tab_web=None, grab_window=None, print_pdf=None, 
            quit_now=None, parent=None, get_link=None, taking_screenshot=False):
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
        if self.js_file is not None:
            if os.path.isfile(self.js_file):
                with open(self.js_file, encoding='utf-8', mode='r') as f:
                    self.js_content = f.read()
            else:
                self.js_content = self.js_file
        x = ''
        self.m = self.profile().cookieStore()
        self.profile().setHttpUserAgent(self.user_agent)
        self.loadFinished.connect(self._loadFinished)
        self.loadProgress.connect(self._loadProgress)
        self.loadStarted.connect(self._loadstart)
        self.pdfPrintingFinished.connect(self._pdf_finished)
        p = NetWorkManager(
            self, url, print_request, block_request, default_block, select_request, 
            get_link)
        p.netS.connect(lambda y = x : self.url_link(y))
        self.link_received.connect(lambda y = x : self.url_link(y))
        self.profile().setRequestInterceptor(p)
        #self.profile().clearHttpCache()
        self.profile().setCachePath(self.tmp_dir)
        self.profile().setPersistentStoragePath(self.tmp_dir)
        self.url = url
        z = ''
        self.c_list = []
        t = ''
        self.cnt = 0
        self.lock = Lock()
        #print(self.use_cookie)
        if self.use_cookie:
            self.m.deleteAllCookies()
            self._set_cookie(use_cookie)
        else:
            self.m.deleteAllCookies()
            self.m.cookieAdded.connect(lambda  x = t : self._cookie(x))
        self.parent = parent
        self.got_cookie = False
        self.text = ''
        self.final_url_got = False
        self.html_file = ''
        self.cookie_string = ''
        self.quit_now = quit_now
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._decide_quit)
        self.timer.setSingleShot(True)
        self.link_request = None
        self.taking_screenshot = taking_screenshot
        self.total_tasks = 0
        self.total_tasks_dict = {}
        if self.grab_window:
            self.total_tasks += 1
            self.total_tasks_dict.update({'grab-window':False})
        if self.print_pdf:
            self.total_tasks += 1
            self.total_tasks_dict.update({'print-pdf':False})
        print(self.total_tasks, '--tasks--')
        self.document_height = None
        self.doc_progress_ht = 0
        
    @pyqtSlot(str)
    def url_link(self, info):
        lnk = os.path.join(self.tmp_dir, 'lnk.txt')
        if os.path.exists(lnk):
            os.remove(lnk)
        print('*******')
        print(info)
        self.link_request = info
        with open(lnk, 'w') as f:
            f.write(info)
        print(self.url, '--url---', '--312---')
        self.link_signal.emit(info)
        print('********')
        
    @pyqtSlot(str)
    def val_found(self, info):
        print(info, '*******info*********')
        self.val = info
    
    def javaScriptAlert(self, url, msg):
        print(msg, '--msg--', url.url())
    
    def javaScriptConsoleMessage(self, level, msg, line, source):
        print(msg, self.total_tasks, line)
        if self.total_tasks == 0 and msg == 'screenshot-page-over':
            print(self.total_tasks, msg)
            self.parent.grab().save(self.grab_window)
            print(self.scrollPosition(), '--pos--')
            self.taking_screenshot = None
            self._decide_quit('after-screenshot')
        
    def _set_cookie(self, cookie_file):
        cookie_arr = QtNetwork.QNetworkCookie()
        c = []
        f = open(cookie_file, 'r')
        lines = f.readlines()
        f.close()
        for i in lines:
            k = re.sub('\n', '', i)
            if k:
                l = k.split('	')
                d = QtNetwork.QNetworkCookie()
                d.setDomain(l[0])
                #print(l[0], '--setting--')
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
                l5 = bytes(l[5], 'utf-8')
                d.setName((l5))
                l6 = bytes(l[6], 'utf-8')
                d.setValue(l6)
                c.append(d)
                self.profile().cookieStore().setCookie(d)
                #print('--cookie--set--')
        
    def _cookie(self, x):
        result = ''
        l = str(x.toRawForm())
        l = re.sub("b'|'", '', l)
        l = self._getTime(l)
        if self.print_cookies:
            print(l)
        if not self.got_cookie:
            self._writeCookies(l)
        if self.end_point:
            if self.end_point in l and not self.got_cookie:
                self.cookie_signal.emit("Cookie Found")
                self.got_cookie = True
        
    def cookie_split(self, i):
        m = []
        j = i.split(';')
        index = 0
        for k in j:
            if '=' in k:
                l = k.split('=', 1)
                l[0] = re.sub(' ', '', l[0])
                t = (l[0], l[1])
            else:
                k = re.sub(' ', '', k)
                t = (k, 'TRUE')
            m.append(t)
            if index == 0 and '=' in k:
                m.append(('name_id', l[0]))
            index = index + 1
        d = dict(m)
        return(d)
        
    def _writeCookies(self, i):
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
                self.cookie_string = self.cookie_string + str1 + '\n'
            if self.set_cookie is not None:
                cc = self.set_cookie
                if not os.path.exists(cc):
                    with open(cc, 'w') as f:
                        f.write(str1)
                else:
                    with open(cc, 'a') as f:
                        f.write('\n'+str1)
            
    def _getTime(self, i):
        j = re.findall('expires=[^;]*', i)
        if j:
            l = re.sub('expires=', '', j[0])
            d = datetime.strptime(l, "%a, %d-%b-%Y %H:%M:%S %Z")
            t = calendar.timegm(d.timetuple())
            k = '; expiry='+str(int(t))
        else:
            k = '; expiry='+str(0)
        i = re.sub('; expires=[^;]*', k, i)
        return i
                        
    def _loadstart(self):
        result = ''
        
    def htm_src(self, x):
        self.html_file = x
    
    def _pdf_finished(self, path, val):
        print(val, path, 'pdf-finished')
        if not self.total_tasks_dict.get('print-pdf'):
            self.lock.acquire()
            self.total_tasks -= 1
            self.lock.release()
            self.total_tasks_dict.update({'print-pdf':True})
        print(self.total_tasks, '--pdf--task--')
        if not self.timeout and self.total_tasks == 0:
            if self.grab_window and self.taking_screenshot:
                pass
            else:
                self._decide_quit('after-pdf-finished')
    
    def val_scr(self, val):
        print(val, '==JS==')
        if self.timeout:
            self.timer.start(self.timeout*1000)
        else:
            self._decide_quit()
            
    def _decide_quit(self, value=None):
        print('quitting: {}'.format(value))
        self.write_external_file()
        if self.quit_now:
            sys.exit(0)
        elif not self.quit_now and self.timeout:
            self.parent.tab_web.close()
            
    def _loadProgress(self, val):
        result =''
        self.toHtml(self.htm_src)
        self.cnt = self.cnt+1
        if self.taking_screenshot is False and self.grab_window:
            self.runJavaScript('document.body.scrollHeight', self.void_function)
    
    def void_function(self, val):
        print(val, '>>')
        if val and self.doc_progress_ht < int(val):
            self.doc_progress_ht = int(val)
    
    def write_external_file(self):
        if self.out_file is None:
            print(self.html_file)
        elif type(self.out_file) is bool:
            pass
        else:
            with open(self.out_file, 'wb') as f:
                f.write(self.html_file.encode('utf-8'))
    
    def val_scr_height(self, val):
        print(val, '-------')
        if self.doc_progress_ht > int(val):
            print(self.document_height, self.doc_progress_ht, 'new-value')
            self.document_height = self.doc_progress_ht
        else:
            self.document_height = 1.5*int(val)
            print('old-value')
        self.parent.tab_web.setMinimumHeight(int(self.document_height))
        self.parent.reload()
        self.taking_screenshot = True
    
    def val_scr_height_scroll(self, val):
        print(val, '=========')
        if not self.total_tasks_dict.get('grab-window'):
            self.lock.acquire()
            self.total_tasks -= 1
            self.lock.release()
            self.total_tasks_dict.update({'grab-window':True})
        print('screenshot-taken')
        print(self.total_tasks, '==++==')
    
    js_file_script = """
    function scroll_to_document(val){
        var total_height = document.body.scrollHeight;
        window.scrollTo(0,val);
        console.log(val);
        console.log(`total_document_height=${total_height}`);
        if (val == 0){
            window.scrollTo(0,0);
            console.log('screenshot-page-over');
        }else if(val < document.body.scrollHeight){
            console.log(val)
            setTimeout(scroll_to_document, 200, val+document.body.clientHeight);
        }else{
            setTimeout(scroll_to_document, 200, 0);
            setTimeout(window.scrollTo, 100, 0, 0);
        }
    }
    setTimeout(scroll_to_document, 200, document.body.clientHeight);
    """
    
    js_file_script_height = """
    function scroll_to_document_end(val){
        var total_height = document.body.scrollHeight;
        window.scrollTo(0, val*document.body.clientHeight);
        console.log(val);
        if (val > 100){
            console.log(`total_document_height=${total_height}`);
        }else if(val <= 100){
            setTimeout(scroll_to_document_end, 200, val+1);
        }
    }
    setTimeout(scroll_to_document_end, 200, 1);
    """
    
    def _loadFinished(self):
        result = ""
        print('Load Finished')
        print(self.parent.tab_web.maximumHeight())
        if self.grab_window:
            if self.taking_screenshot is False:
                self.runJavaScript('document.body.scrollHeight', self.val_scr_height)
            elif self.taking_screenshot:
                self.runJavaScript(self.js_file_script, self.val_scr_height_scroll)
        
        margins = QtCore.QMarginsF(15, 15, 15, 15)
        layout = QtGui.QPageLayout(QtGui.QPageSize(QtGui.QPageSize.A4),
                                   QtGui.QPageLayout.Portrait,
                                   margins)
        if self.js_content is not None:
            self.runJavaScript(self.js_content, self.val_scr)
            if self.print_pdf and not self.total_tasks_dict.get('print-pdf'):
                self.printToPdf(self.print_pdf, layout)
        else:
            if not self.wait_for_cookie and not self.timeout and not self.print_pdf and not self.grab_window:
                self._decide_quit()
            elif self.print_pdf and not self.timeout and not self.total_tasks_dict.get('print-pdf'):
                self.printToPdf(self.print_pdf, layout)
            elif self.timeout:
                if self.print_pdf and not self.total_tasks_dict.get('print-pdf'):
                    self.printToPdf(self.print_pdf, layout)
                else:
                    self.timer.start(self.timeout*1000)


class BrowseUrlT(QWebEngineView):
    #cookie_s = pyqtSignal(str)
    def __init__(
            self, url=None, set_cookie=None, use_cookie=None, end_point=None, 
            domain_name=None, user_agent=None, tmp_dir=None, js_file=None, 
            out_file=None, wait_for_cookie=None, print_request=None, 
            print_cookies=None, timeout=None, block_request=None, default_block=None, 
            select_request=None, show_window=None, window_dim=None, grab_window=None, 
            print_pdf=None, quit_now=None, set_html=None, set_html_path=None, 
            get_link=None):
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
        if domain_name is None:
            dm = self.url
            if self.url.startswith('http'):
                dm = self.url.split('/')[2]
            if dm.startswith('www.'):
                dm = dm.replace('www.', '', 1)
            self.domain_name = dm
        else:
            self.domain_name = domain_name
        self.user_agent = user_agent
        self.tmp_dir = tmp_dir
        self.js_file = js_file
        self.set_html = set_html
        self.set_html_path = set_html_path
        self.out_file = out_file
        self.get_link = get_link
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
        self.tab_web = None
        self.web = None
        self.taking_screenshot = False
        if quit_now is None:
            self.quit_now = True
        else:
            self.quit_now = quit_now
        if self.quit_now:
            self.Browse(self.url)
        
    def get_window_object(self):
        return self.tab_web
    
    def start_loading(self):
        self.Browse(self.url)
        
    def gethtml(self):
        return self.web.html_file
    
    def getcookie_string(self):
        return self.web.cookie_string
        
    def Browse(self, url):
        win_hide = False
        show_max = False
        show_min = False
        self.tab_web = QtWidgets.QWidget()
        self.tab_web.hide()
        if self.window_dim is None:
            self.tab_web.setMinimumSize(1920, 1080)
        elif self.window_dim.endswith('xreload'):
            self.window_dim = self.window_dim.replace('xreload', '').lower()
            w, h = self.window_dim.split('x')
            self.tab_web.setMinimumSize(int(w), int(h))
            self.tab_web.setMaximumSize(int(w), int(h))
            self.taking_screenshot = True
        else:
            win_dim = self.window_dim.lower()
            if win_dim == 'max':
                show_max = True
            elif win_dim == 'min':
                show_min = True
            else:
                if 'x' in win_dim:
                    w, h = win_dim.split('x')
                else:
                    w = h = win_dim
                if win_dim == '0':
                    show_max = True
                    win_hide = True
                else:
                    self.tab_web.setMaximumSize(int(w), int(h))
        self.tab_web.setWindowTitle(self.domain_name)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_web)
        self.horizontalLayout_5.addWidget(self)
        
        self.web = BrowserPage(
                    url, self.set_cookie, self.use_cookie, self.end_point, 
                    self.domain_name, self.user_agent, self.tmp_dir, self.js_file, 
                    self.out_file, self.wait_for_cookie, self.print_request, 
                    self.print_cookies, self.timeout, self.block_request, 
                    self.default_block, self.select_request, self.tab_web, 
                    self.grab_window, self.print_pdf, self.quit_now, self, 
                    self.get_link, self.taking_screenshot)
        
        self.web.cookie_signal.connect(self.cookie_found)
        self.web.link_signal.connect(self.link_source_found)
        self.setPage(self.web)
        if self.set_html or self.set_html_path:
            if self.set_html_path is not None:
                if os.path.isfile(self.set_html_path):
                    with open(self.set_html_path, encoding='utf-8', mode='r') as f:
                        self.set_html = f.read()
            self.setHtml(self.set_html)
        elif self.url is not None:
            self.load(QUrl(url))
        self.cnt = 1
        
        #QtWidgets.QApplication.processEvents()
        if self.show_window:
            if win_hide:
                self.tab_web.hide()
            else:
                if show_max:
                    self.tab_web.showMaximized()
                elif show_min:
                    self.tab_web.showMinimized()
                else:
                    self.tab_web.show()
                    pass
        else:
            self.tab_web.hide()
        
    @pyqtSlot(str)
    def cookie_found(self):
        print('cookie')
        self.add_cookie = False
        if self.quit_now and not self.timeout:
            sys.exit(0)

    @pyqtSlot(str)
    def link_source_found(self):
        print('link found')
        if self.quit_now and not self.timeout:
            sys.exit(0)
    



