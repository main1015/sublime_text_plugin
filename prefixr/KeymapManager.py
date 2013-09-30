# -*- coding: utf-8 -*-
import sublime, sublime_plugin
from sublime import active_window

class KeymapmanagerCommand(sublime_plugin.TextCommand):
    def run(self, edit, mod="left"):
        print 'this my plugin'
        # self.view.insert(edit, 0, "Hello, World!")
        if mod == "right":
            self.next_focus_view()
        elif mod == "left":
            self.next_focus_view(False)
        elif mod == "add":
            self.py_file_add_head()
        
    def next_focus_view(self, isNext=True):
        # 将焦点切换到当前视图的下一个视图
        window = active_window()
        views = window.views()
        id = self.view.id()
        if views:
            ids = map(lambda x: x.id(), views)
            l = len(ids)

            if ids.count(id):
                index = ids.index(id)
                if isNext:
                    next_index = index + 1
                else:
                    next_index = index - 1

                if next_index >= l:
                    view = views[0]
                elif next_index < 0:
                    view = views[l-1]
                else:
                    view = views[next_index]
            else:
                view = views[0]
            window.focus_view(view)    

    def py_file_add_head(self):
        # 给当前的的py文件添加# -*- coding: utf-8 -*-
        current_name = self.view.file_name()
        add_text = '# -*- coding: utf-8 -*-'
        env_text = '#!'
        self.scroll()
        if current_name and current_name[-3:] == ".py":
            first_row = 0
            insert_row = 0
            first_region = self.view.line(first_row)     
            first_text =  self.view.substr(first_region)
            if first_text: 
                if first_text.startswith(add_text):
                    return
                if first_text.startswith(env_text):
                    if self.view.size() == first_region.end():
                        insert_row = self.view.size()
                        add_text = '\n%s' % add_text
                    else:
                        second_region = self.view.line(first_region.end()+1)
                        second_text = self.view.substr(second_region)
                        if second_text and second_text.startswith(add_text):
                            return
                        else:
                            insert_row = second_region.begin()
            edit = self.view.begin_edit()
            self.view.insert(edit, insert_row, '%s\n' % add_text)
            self.view.end_edit(edit)
            

    def scroll(self):
        #滚动
        print '~'*50
        # first_row = 0
        # first_region = self.view.line(first_row)   
        # print first_region
        # _region = self.view.line(1502)  
        # self.view.show(_region)
        self.automatic_scroll()


    def automatic_scroll(self):
        """
        自动滚动
        """
        import threading
        import time

        class _scroll(threading.Thread):
            def __init__(self, this, row=0):
                threading.Thread.__init__(self)
                self.this = this
                self.row = row

            def run(self):
                
                while True:
                    _region = self.this.view.line(self.row)
                    self.this.view.show(_region)
                    print self.row
                    if self.this.view.size() <= _region.end():
                        return
                    self.row = _region.end() + 1
                    time.sleep(1)   

        settings = self.view.settings()
        print dir(settings)
        print type(settings)
        run = _scroll(self)
        # run.start()


