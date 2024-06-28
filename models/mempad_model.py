
import markdown
import os

from beep import Beep

class MemPadModel:
    
  def __init__(self):
    self.__pages = []
    self.__num_pages = 0
    self.__filename = ''
   
  def open(self, filename):
    "read lst mempad file"   
    self.__dir = os.path.dirname(os.path.realpath(__file__))
    str = MemPadModel.__readFile(filename)
  
    if not str.startswith('MeMpAd.'):
      import sys
      sys.exit(filename + ' is NOT a Mempad file.')
  
    index = str.index('\1')
    str = str[index:].rstrip('\0')
    arr = str.split('\0')

    pages = []
    index = 0
     
    for i, item in enumerate(arr):
      if i & 1 == 0 : # titles
        level = ord(item[0])
        title = item[1:]
      else:
        pages.append([ len(pages), level, title, item])
        index += 1 
      
    self.__pages = pages
    self.__num_pages = len(pages)
    self.__filename = filename

     
    Beep.dispatch('new_file', self, self.__filename)

 

  @property
  def pages(self):
      return self.__pages
  
  def getPageById(self, id):
      id = int(id)
      return self.__pages[id]
  
  def setPageById(self, id, level, title, content):
      
      self.__pages[id] = [ id, level, title, content]
  
  def toHtmlFile(self,filename = None):
    "write to html"  
    
    links = ''
    pages = ''

    if not filename :
      filename = f'{self.__filename[0:-4]}.html'

    for id, level, title, page in self.__pages :
      dots = ' ' * (level - 1)
      links += f'<a href="javascript:show({id})">{dots}{title}</a>\n'
     
      if title[:-4] != '.ini' :
        page = markdown.markdown(page)
      pages += f'<div id="id{id}">{page}</div>\n'

    html = MemPadModel.__readFile(self.__dir + '/assets/template.html')
    css = MemPadModel.__readFile(self.__dir + '/assets/mempad.css')
    js = MemPadModel.__readFile(self.__dir + '/assets/mempad.js')
    html = html.format(links=links, pages = pages, css = css, js = js)

    
    f = open(filename, 'w', encoding='utf-8')
    f.write(html)
    f.close()
    
  def get_data(self):
      return str(self.__num_pages) + ' pages'
  @property
  def num_pages(self):
      return self.__num_pages

  @staticmethod
  def __readFile(filename) :
    "read file"  
    f = open(filename, 'r', encoding='utf-8')
    str = f.read()
    f.close()  
    return str

  def add_page(self, parent_id, level_increment):
      parent_page = None
      for page in self.pages:
          if page.id == parent_id:
              parent_page = page
              break
      
      new_id = max(page.id for page in self.pages) + 1
      new_level = parent_page.level + level_increment if parent_page else 0
      new_page = Page(new_id, new_level, f"New Page {new_id}", f"Content of New Page {new_id}")
      self.pages.append(new_page)
      return new_page

  def delete_page(self, page_id):
      self.pages = [page for page in self.pages if page.id != page_id]

  def rename_page(self, page_id, new_title):
        for page in self.pages:
            if page.id == page_id:
                page.title = new_title
                break