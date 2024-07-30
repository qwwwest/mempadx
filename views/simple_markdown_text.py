
import re
import tkinter as tk
import tkinter.font as tkfont
import tkinter.scrolledtext as tkscroll


class SimpleMarkdownText(tkscroll.ScrolledText):
    """
    Really basic Markdown display. Thanks to Bryan Oakley's RichText:
    https://stackoverflow.com/a/63105641/79125
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        """A very basic markdown parser.

        Helpful to easily set formatted text in tk. If you want actual markdown
        support then use a real parser.
        """
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


def test_markdown_display():
    root = tk.Tk()

    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(size=12)

    text = SimpleMarkdownText(root, width=45, height=22, font=default_font)
    text.pack(fill="both", expand=True)

    text.insert_markdown(
        """
# Rich Text Example
Hello, world
This line **has bold** text.
This line _has italicized_ text. Also *italics* using asterisks.
Text _with italics **and bold** does_ not work.

## Sub Heading
This is a more interesting line with _some_ italics, but also **some bold text**.
* Create a list
* With bullets
1. Create a list
1. Or numbers

1. Use blank lines
1. to restart numbering
"""
    )

    root.mainloop()


if __name__ == "__main__":
    test_markdown_display()