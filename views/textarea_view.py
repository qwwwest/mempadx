# views/textarea_view.py
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

import re

class TextAreaView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill=tk.BOTH)
        self.text = tk.Text(self, undo=True, font=("monospace", 12), wrap = tk.WORD)

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the tree and the scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text.pack(expand=True, fill=tk.BOTH)

            # Add the binding
        self.text.bind("<Control-Key-a>", lambda e: self.select_all() )
        self.text.bind('<<Modified>>', self.onModification)  
        self.text.bind("<KeyRelease>", self.onKey)
 
    # using property decorator 
    # a getter function for the content
    @property
    def content(self):
        return self.text.get(1.0, tk.END)
    
    # a setter function for the content
    @content.setter 
    def content(self, content):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)

    # Select all the text in textbox
    def select_all(self):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        


    def config_markdown(self):

        default_font = tkfont.nametofont(self.cget("font"))

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = tkfont.Font(**default_font.configure())
        italic_font = tkfont.Font(**default_font.configure())

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")

        # Small subset of markdown. Just enough to make text look nice.
        self.tag_configure("**", font=bold_font)
        self.tag_configure("*", font=italic_font)
        self.tag_configure("_", font=italic_font)
        self.tag_chars = "*_"
        self.tag_char_re = re.compile(r"[*_]")

        max_heading = 3
        for i in range(1, max_heading + 1):
            header_font = tkfont.Font(**default_font.configure())
            header_font.configure(size=int(default_size * i + 3), weight="bold")
            self.tag_configure(
                "#" * (max_heading - i), font=header_font, spacing3=default_size
            )

        lmargin2 = em + default_font.measure("\u2022 ")
        self.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)
        lmargin2 = em + default_font.measure("1. ")
        self.tag_configure("numbered", lmargin1=em, lmargin2=lmargin2)

        self.numbered_index = 1

    def insert_bullet(self, position, text):
        self.insert(position, f"\u2022 {text}", "bullet")

    def insert_numbered(self, position, text):
        self.insert(position, f"{self.numbered_index}. {text}", "numbered")
        self.numbered_index += 1

    def insert_markdown(self, mkd_text):

        for line in mkd_text.split("\n"):
            if line == "":
                # Blank lines reset numbering
                self.numbered_index = 1
                self.insert("end", line)

            elif line.startswith("#"):
                tag = re.match(r"(#+) (.*)", line)
                line = tag.group(2)
                self.insert("end", line, tag.group(1))

            elif line.startswith("* "):
                line = line[2:]
                self.insert_bullet("end", line)

            elif line.startswith("1. "):
                line = line[2:]
                self.insert_numbered("end", line)

            elif not self.tag_char_re.search(line):
                self.insert("end", line)

            else:
                tag = None
                accumulated = []
                skip_next = False
                for i, c in enumerate(line):
                    if skip_next:
                        skip_next = False
                        continue
                    if c in self.tag_chars and (not tag or c == tag[0]):
                        if tag:
                            self.insert("end", "".join(accumulated), tag)
                            accumulated = []
                            tag = None
                        else:
                            self.insert("end", "".join(accumulated))
                            accumulated = []
                            tag = c
                            next_i = i + 1
                            if len(line) > next_i and line[next_i] == tag:
                                tag = line[i : next_i + 1]
                                skip_next = True

                    else:
                        accumulated.append(c)
                self.insert("end", "".join(accumulated), tag)

            self.insert("end", "\n")


    def onModification(self,_):

        text = self.content
        print('modified')




    
    def config(self):
        
        default_font = self.tkFont.nametofont(self.cget("font"))

        default_size = default_font.cget("size")
        bold_font = self.tkFont.Font(**default_font.configure())
        italic_font = self.tkFont.Font(**default_font.configure())
        h1_font = self.tkFont.Font(**default_font.configure())

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        h1_font.configure(size=int(default_size*2), weight="bold")

        self.tag_configure("bold", font=bold_font,  bg='#fff', fg='#f00',)
        self.tag_configure("italic", font=italic_font)
        self.tag_configure("h1", font=h1_font, spacing3=default_size)

    
    def onKey(self,_):

 
        print('key up')

        self.text.tag_remove('bold', "1.0", tk.END)
        self.re_replace_all(r'\*\*(.+?)\*\*(?!\*)', 'bold')
            
    
    def re_replace_all(self, pattern, tag):
        for match in self.search_re(pattern):
            self.text.tag_add(tag, match[0], match[1])

    def search_re(self, pattern):
        """
        Uses the python re library to match patterns.

        Arguments:
            pattern - The pattern to match.
        Return value:
            A list of tuples containing the start and end indices of the matches.
            e.g. [("0.4", "5.9"]
        """
        matches = []
        text = self.text.get("1.0", tk.END).splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
                print(f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
        return matches