# -*- coding: utf-8 -*-
import sublime, sublime_plugin
from sublime import active_window

class KeymapmanagerCommand(sublime_plugin.TextCommand):
    def run(self, edit, mod="switch"):
        print 'this my plugin'
        # self.view.insert(edit, 0, "Hello, World!")
        if mod == "switch":
            self.next_focus_view()
        elif mod == "add":
            self.py_file_add_head()
        

    def next_focus_view(self):
        # 将焦点切换到当前视图的下一个视图
        window = active_window()
        views = window.views()
        id = self.view.id()
        if views:
            ids = map(lambda x: x.id(), views)
            l = len(ids)

            if ids.count(id):
                index = ids.index(id)
                next_index = index + 1
                if next_index >= l:
                    view = views[0]
                else:
                    view = views[next_index]
            else:
                view = views[0]
            window.focus_view(view)    

    def py_file_add_head(self):
        # 给当前的的py文件添加# -*- coding: utf-8 -*-
        current_name = self.view.file_name()
        if current_name and current_name[-3:] == ".py":
            edit = self.view.begin_edit()
            self.view.insert(edit, 0, "# -*- coding: utf-8 -*-\n")
            self.view.end_edit(edit)