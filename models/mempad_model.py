
import markdown
import os
import re
from settings import MemPadSettings

from beep import Beep

class MemPadModel:
    
  def __init__(self):
    self._reset()

  def _reset(self):
     
    self.__pages = []
    self.__current_page = 0
    self.__filename = ''
    self.__dir = ''
   
  
  def relpath(self, filename):
      try:
        relpath =  os.path.relpath(filename,MemPadSettings.app_path )
      except:
        relpath = filename
     
      print("filename relpath", relpath)
      return relpath
  
  def open(self, filename):
    "read lst mempad file" 
    
    if not os.path.isfile(filename):
       Beep.dispatch('alert', "info",  f"File {filename} NOT found.")
       return False
    
    
    self.__dir = os.path.dirname(os.path.realpath(__file__))
    mempad_str = self._read_mempad_file(filename)

    if not mempad_str:
       return False
 
    index = mempad_str.index('\0')
  
    self.__current_page = int(mempad_str[7:index]) if (index > 7) else 0
    
    index = mempad_str.index('\1')
    mempad_str = mempad_str[index:-1] # remove last ZERO '\0'
    arr = mempad_str.split('\0')

    pages = []
    
     
    for i, item in enumerate(arr):
      if i & 1 == 0 : # titles
        if item == '':
           break
        level = ord(item[0])
        title = item[1:]
      else:
        #pages.append([ len(pages), level, title, item])
        pages.append({
           "id": len(pages), 
           "level": level, 
           "title": title, 
           "content": item})
      
    filename = self.relpath(filename)
    self.__pages = pages
    self.__filename = filename
     
    Beep.dispatch('new_file', self, self.__filename)
    return True


  @property
  def filename(self):
      return self.__filename
  
  @property
  def pages(self):
      return self.__pages
  
  def set_pages(self, pages, selected_item = None):
      self.__pages = pages
      
  
  def get_page_by_id(self, id):
      id = int(id)
      return self.__pages[id]
  
  def set_page_by_id(self, id, level, title, content):
      
      self.__pages[id] = {
           "id": id, 
           "level": level, 
           "title": title, 
           "content": content}

  def set_content_by_id(self, id, content):
      p = self.__pages[id] 
      p["content"] = content     

  def get_content_by_id(self, id):
      p = self.__pages[id] 
      return p["content"]
  
  def get_page_title(self, id):
      p = self.__pages[id] 
      return p["title"]
     
  def set_page_title(self, id, title):
      p = self.__pages[id] 
      p["title"] = title   

  def export_to_html(self,filename = None):
    "write to html"  
    
    links = ''
    pages = ''

    if not filename :
      filename = f'{self.__filename[0:-4]}.html'

    for page in self.__pages :
      id, level, title, content = page.id, page.level, page.title, page.content 
      dots = ' ' * (level - 1)
      links += f'<a href="javascript:show({id})">{dots}{title}</a>\n'
     
      if title[:-4] != '.ini' :
        content = markdown.markdown(content)
      pages += f'<div id="id{id}">{content}</div>\n'

    html = MemPadModel.__readFile(self.__dir + '/assets/template.html')
    css = MemPadModel.__readFile(self.__dir + '/assets/mempad.css')
    js = MemPadModel.__readFile(self.__dir + '/assets/mempad.js')
    html = html.format(links=links, pages = pages, css = css, js = js)

    
    f = open(filename, 'w', encoding='utf-8')
    f.write(html)
    f.close()
    
  def ________get_data(self):
      return str(self.__num_pages) + ' pages'
  
  @property
  def num_pages(self):
      return len(self.__pages)

  @property
  def current_page(self):
      return self.__current_page
 
  @current_page.setter
  def current_page(self, val):
      self.__current_page = val
  
  def _read_mempad_file(self, filename) :
 
    # f = open(filename, 'r', encoding='utf-8',  errors='ignore')
    try:
      with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        start7 = f.read(7)
        if start7 != 'MeMpAd.':
          raise ValueError( f"File {filename} is not a Mempad file")
        f.close()

      with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
        f.close()  
      return data
    except Exception as e:
      Beep.dispatch('alert', "error", str(e))
      return False


 

  def add_page_child(self, parent_id, title):
      found = False
      new_pages = []

      for page in self.pages:
        new_pages.append({
          "id": len(new_pages), 
          "level": page['level'], 
          "title": page['title'], 
          "content": page['content']})
        
        if page['id'] == parent_id:
          found = True
          self.__current_page = len(new_pages)
          new_pages.append({
          "id": len(new_pages), 
          "level": page['level'] + 1, 
          "title": title, 
          "content": ''})
               
      if found:
        self.__pages = new_pages

      return found
  
  def _______add_page_after(self, page_id, title):
    found = False
    page_level = 0
    added = False
    new_pages = []

    for page in self.pages:
      new_pages.append({
        "id": len(new_pages), 
        "level": page['level'], 
        "title": page['title'], 
        "content": page['content']})
      
      if page['id'] == id:
        found = True
        page_level = page['level']

        new_pages.append({
        "id": len(new_pages), 
        "level": page['level'] + 1, 
        "title": title, 
        "content": ''})
              
    if found:
      self.__pages = new_pages

    return found

  def save(self, filename = None):
      
    if filename == None :
        filename = self.__filename
    
    if filename == None :
        return

    print('saving...', filename)
    "write lst mempad file"   
    self.__dir = os.path.dirname(os.path.realpath(__file__))
    mempad = 'MeMpAd.' + str(self.__current_page) + '\0\0'
         
    for page in self.__pages:
      mempad += chr(page['level']) + page['title'] + chr(0) + page['content'] + chr(0)

    mempad += chr(0)  

    try:
      abspath = os.path.abspath("filename")
      f = open(abspath, 'w', encoding='utf-8')
      f.write(mempad)
      f.close()
    except:
      Beep.dispatch('alert', "error", f"Cannot save: {filename}")
      return False
    
    Beep.dispatch('info', f"{filename} was saved")
    return True

  def close(self):
    "Save and close lst mempad file"

    self.save()
    
    self.__pages = []
    self.__num_pages = 0
    self.__current_page = 0
    self.__filename = ''
    self.__dir = ''


 
  def new_mempad_file(self, filename = None):
      
    # self.__filename = filename
    # self.__dir = os.path.dirname(os.path.realpath(__file__))

    mempad = 'MeMpAd.0\0\0\1New Page\0\0'    
    # mempad += chr(1) + "New Page" + chr(0) + "" + chr(0)
    # mempad += chr(0)  
    try:
      f = open(filename, 'w', encoding='utf-8')
      f.write(mempad)
      f.close()
      Beep.dispatch('Model_new_mempad_file_saved', self, filename)
      return True
    except Exception as e:
    
      Beep.dispatch('alert', "error", str(e)) 
      return False