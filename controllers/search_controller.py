# controllers/app_controller.py


from beep import Beep

from views.search_window import SearchWindow 

class SearchController:

    def __init__(self, model, view, controller):
        self.model = model
        self.view = view
        self.controller = controller

        self.search_results = []
        self.search_index = -1
        self.last_search_term = None
        self.last_search_param = None
        self.search_window = None

        self.pos_x = 0
        self.pos_y = 0

        Beep.listen('search_text', self.search_text)
        Beep.listen('replace_text', self.replace_text)
        Beep.listen('on_close_search_window', self.on_close_search_window)
        
 
        self.view.bind("<Control-f>", lambda e:self.open_search_window())






    # search_text, match_case, whole_word, regex_mode, from_top, search_forward
    def search_text(self, *args):
        # self.model.set_text(self.view.get_text())

        (_, search_term, match_case, whole_word, regex_mode, from_top, replace, forward) = args
        # search_term, match_case, whole_word, regex_mode, from_top, forward
        if search_term == '':
            return
        
        selected_item = self.view.treeview.tree.selection()[0] 
        m_id = self.view.treeview.get_item_mid(selected_item)
        self.model.current_page = m_id
        self.model.set_content_by_id(m_id, self.view.textarea.content)

        #self.model.set_content_by_id(self.model.current_page, view_content)
        
        # we create a tuple with the search term and params, if any change we build the search result again
        search_exp = (search_term, match_case, whole_word, regex_mode, from_top)
      
        if self.last_search_term != search_exp:
            self.search_results = []
            self.search_index = -1
            self.search_results = self.model.search(search_term, match_case, whole_word, regex_mode, from_top)
            self.last_search_term = search_exp
            self.last_search_param = (search_term, match_case, whole_word, regex_mode, from_top, replace)
            self.view.textarea.highlight_text(None, None)

            items = []
            
            # list of ids in the tree (to keep model ids to tree ids track)
            for m_id, _, _  in self.search_results:
                items.append(self.controller.model_to_view_id[m_id])

            self.view.treeview.change_treeview_item_color(items)

        self.search_window.replace_button["state"] = "disabled"
        
        if self.search_results:
            if forward:
                self.search_index = (self.search_index + 1) % len(self.search_results)
            else:
                self.search_index = (self.search_index - 1) % len(self.search_results)

            m_id, start, end = self.search_results[self.search_index]
            self.search_window.update_results_label(self.search_index +1, len(self.search_results))
           # if self.search_index != m_id:

            #print(search_term, forward,  m_id, match,  self.search_index, len(self.search_results))
                
            self.controller.select_tree_item_with_model_id(m_id)
            
            start_pos = f"1.0+{start}c"
            end_pos = f"1.0+{end}c"
            self.view.textarea.highlight_text(start_pos, end_pos)
            self.current_selected = (m_id, start, end)
            self.search_window.replace_button["state"] = "normal"
        else: 
            self.search_window.update_results_label(0 , 0)

    def replace_text(self, _, search_term, replace_term):
        # self.model.set_text(self.view.get_text())
        # self.model.replace(search_term, replace_term, match_case, whole_word, regex_mode)
        # self.view.set_text(self.model.get_text())

        (m_id, start, end) = self.current_selected 

        idx = f"1.0+{start}c"
        lastidx = f"1.0+{end}c"

        if(m_id != self.model.current_page):
             print (m_id, self.model.current_page)
             self.search_window.replace_button["state"] = "disabled"
             return
        
        self.view.textarea.text.delete(idx, lastidx)
        self.view.textarea.text.insert(idx, replace_term)

       
        # after the text is replaced, we save it to the model
        view_content = self.view.textarea.content
        self.model.set_content_by_id(m_id, view_content)

        del self.search_results[self.search_index] 

        delta = len(replace_term) - len(search_term) 
        index = self.search_index

        for m_id_n, start_n, end_n  in self.search_results[self.search_index:]:
            if m_id_n != m_id:
                break
            self.search_results[index] = (m_id_n, start_n + delta, end_n + delta)
            index += 1
             
        self.search_index -= 1
        self.search_window.replace_button["state"] = "disabled"

        self.search_window.update_results_label(self.search_index+1, len(self.search_results))

        
    def on_close_search_window(self, _, pos_x, pos_y):
        # Implement the data cleanup logic here
        self.search_results = []
        self.search_index = -1
        self.last_search_term = None
        self.search_window = None
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.view.treeview.remove_treeview_item_color()
        self.view.textarea.highlight_text(None,None)

    def open_search_window(self):
        # to ensure we open it only one instance
        
        if self.search_window:
            return
 
        self.search_window = SearchWindow(self.view, self.pos_x, self.pos_y, self.last_search_param)

        self.search_window.bind("<Control-f>", lambda e:self.search_window.on_close_search_window())
        self.search_window.bind("<Escape>", lambda e:self.on_escape())
    

    def on_escape(self):
        self.search_window.on_close_search_window()
          