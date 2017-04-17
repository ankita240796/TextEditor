import os
import time
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog,messagebox
from tkinter.colorchooser import *
from tkinter import font
from fontbox import *
filename=None
val=None
search_from=None
search_until=None
key_word=None
repkey_word=None
case_sensitive=None
st=None
ed=None
prev=None
window = Tk( )
window.title("Untitled-TextOditor")
window.iconbitmap(default="i1.ico")
font1=font.Font()
text = ScrolledText(window, width=200, height=80,font=font1)
text.pack()
title="TextOditor"
def set_title(name):
    if(name==None):
       window.title("Untitled-"+title)
    else:
       window.title(os.path.basename(name)+"-"+title)
#Methods
#filemenu_methods
def new():
    if text.edit_modified():
        ans=messagebox.askquestion(title="Save File",message="This document has been modified.Do you want to save changes?")
        if ans=="yes":
           save_as()
    text.delete("1.0",END)
    set_title(None)
    text.edit_modified(False)
def  open_file():
     new()
     file=filedialog.askopenfilename()
     if file!=None and file!='':
         text.insert(INSERT,open(file, 'rb').read())
         text.edit_modified(False)
         filename=file
         set_title(filename)
def save_as():
    global filename
    if(filename==None):
     path=filedialog.asksaveasfilename(filetypes=(('Text files', '*.txt'), ('Rich Text Format files', '*.rtf'), ('All files', '*.*')))
    else:
     path=filename 
    if(path!=''):
      filename=path
      set_title(filename) 
      write=open(path,mode='w')
      write.write(text.get("1.0",END),)
      text.edit_modified(False)
def save():
      save_as()
def close():
    if text.edit_modified():
          ans=messagebox.askyesnocancel(title="Save File",message="This document has been modified.Do you want to save changes?")
          #print(ans)
          if ans==True:
             save()
             window.quit() 
          if ans==False:
             window.quit()  
    else:
            window.quit()  
def close1():
     if text.edit_modified():
          ans=messagebox.askyesnocancel(title="Save File",message="This document has been modified.Do you want to save changes?")
          #print(ans)
          if ans==True:
             save()
             window.quit() 
          if ans==False:
             window.quit()  
     else:
            ans=messagebox.askquestion(title="Close",message="Do you really want to quit?")     
            if(ans=="yes"):
               window.quit()             
#editmenu_methods  
def cut():
    window.clipboard_clear()
    text.clipboard_append(string=text.selection_get())
    text.delete(index1=SEL_FIRST,index2=SEL_LAST)
def copy():
    window.clipboard_clear()
    text.clipboard_append(string=text.selection_get())
def paste():
    text.insert(INSERT,text.clipboard_get())
def select_all():
    text.tag_add(SEL, "1.0", END)
    text.mark_set(INSERT, "1.0")
    text.see(INSERT)
def undo():
    text.edit_undo()
def redo():   
    text.edit_redo() 
def find(event=None):
    w1 = Toplevel(window)
    w1.searchlabel = Label(w1, text="Find what:")
    w1.searchlabel.pack()
    w1.key_word_entry = Entry(w1, text="Find what...")
    w1.key_word_entry.pack()
    w1.matchcasevar = IntVar()
    w1.matchcasevar.set(1)
    w1.matchcase = Checkbutton(w1, text="Match case", variable=w1.matchcasevar)
    w1.matchcase.pack()
    w1.searcharea = StringVar()
    w1.searcharea.set("all")
    w1.group = LabelFrame(w1, text="Direction to find", padx=5, pady=5)
    w1.group.pack(padx=1, pady=3, anchor=W)
    Radiobutton(w1.group, text="Up", variable=w1.searcharea, value="up").pack(anchor=W)
    Radiobutton(w1.group, text="Down", variable=w1.searcharea, value="down").pack(anchor=W)
    Radiobutton(w1.group, text="All", variable=w1.searcharea, value="all").pack(anchor=W)
    w1.key_word_entry.focus()
    def get_parameters():
        global val
        global key_word
        global search_until 
        global search_from
        global case_sensitive
        key_word= w1.key_word_entry.get()
        if val==None:
            val=key_word
        if w1.searcharea.get() == "up":
            w1.search_from = "1.0"
            w1.search_until = INSERT
        elif w1.searcharea.get() == "down":
            w1.search_from = INSERT
            w1.search_until = END
        elif w1.searcharea.get() == "all":
            w1.search_from = "1.0"
            w1.search_until = END
        w1.case_sensitive = w1.matchcasevar.get()
        search_until=w1.search_until
        case_sensitive=w1.case_sensitive
        if search_from==None or val!=key_word:
           search_from=w1.search_from
    def findnextcmd():
            get_parameters()   
            global key_word
            global search_until 
            global search_from
            global case_sensitive
            global val
            global st
            global ed
            if st!=None:
                text.tag_remove("search",index1=st,index2=ed)    
            start_kw = text.search(key_word, search_from, stopindex=search_until, nocase=case_sensitive)
            if start_kw != "" and  start_kw != None:
                st=start_kw
                val=key_word
                text.tag_configure("search", background="green")
                text.tag_add("search", start_kw, "%s + %sc"%(start_kw, len(key_word)))
                search_from = "%s + %sc "%(start_kw, len(key_word))
                ed=search_from
            else:
                 messagebox.showinfo("Textoditor","Cannot find "+key_word)  
                 cancelcmd()       
    w1.findnext = Button(w1, text="Find Next", command=findnextcmd)
    w1.findnext.pack(anchor=W)
    def cancelcmd():
        global val
        global search_from
        global st
        w1.unbind("<Return>")
        text.focus()
        search_from=None
        val=None
        st=None
        ed=None
        w1.destroy()
    w1.cancel = Button(w1, text="Cancel", command=cancelcmd)
    w1.cancel.pack(anchor=W)
    w1.protocol('WM_DELETE_WINDOW',cancelcmd)
def goto():
    from tkinter.simpledialog import askinteger
    line = askinteger('Goto', 'Enter line number:')
    text.update()
    text.focus()
    if line is not None:
        maxindex = text.index(END+'-1c')
        maxline  = int(maxindex.split('.')[0])
        if line > 0 and line <= maxline:
            text.mark_set(INSERT, '%d.0' % line)      # goto line
            text.tag_remove(SEL, '1.0', END)          # delete selects
            text.tag_add(SEL, INSERT, 'insert + 1l')  # select line
            text.see(INSERT)                          # scroll to line
        else:
            from tkinter.messagebox import showerror
            showerror('PyEdit', 'Bad line number')    
def  replace():
    w1 = Toplevel(window)
    w1.searchlabel = Label(w1, text="Replace what:")
    w1.searchlabel.pack()
    w1.key_word_entry = Entry(w1, text="Replace what...")
    w1.key_word_entry.pack()
    w1.searchlabel = Label(w1, text="Replace with:")
    w1.searchlabel.pack()
    w1.repkey_word_entry = Entry(w1, text="Replace with...")
    w1.repkey_word_entry.pack()
    w1.matchcasevar = IntVar()
    w1.matchcasevar.set(1)
    w1.matchcase = Checkbutton(w1, text="Match case", variable=w1.matchcasevar)
    w1.matchcase.pack()
    w1.searcharea = StringVar()
    w1.searcharea.set("all")
    w1.group = LabelFrame(w1, text="Direction", padx=5, pady=5)
    w1.group.pack(padx=1, pady=3, anchor=W)
    Radiobutton(w1.group, text="Up", variable=w1.searcharea, value="up").pack(anchor=W)
    Radiobutton(w1.group, text="Down", variable=w1.searcharea, value="down").pack(anchor=W)
    Radiobutton(w1.group, text="All", variable=w1.searcharea, value="all").pack(anchor=W)
    w1.key_word_entry.focus()
    def get_parameters():
        global val
        global key_word
        global repkey_word
        global search_until 
        global search_from
        global case_sensitive
        key_word= w1.key_word_entry.get()
        repkey_word=w1.repkey_word_entry.get()
        if val==None:
            val=key_word
        if w1.searcharea.get() == "up":
            w1.search_from = "1.0"
            w1.search_until = INSERT
        elif w1.searcharea.get() == "down":
            w1.search_from = INSERT
            w1.search_until = END
        elif w1.searcharea.get() == "all":
            w1.search_from = "1.0"
            w1.search_until = END
        w1.case_sensitive = w1.matchcasevar.get()
        search_until=w1.search_until
        case_sensitive=w1.case_sensitive
        if search_from==None or val!=key_word:
           search_from=w1.search_from
    def repnextcmd(r):
            get_parameters()   
            global key_word
            global repkey_word
            global search_until 
            global search_from
            global case_sensitive
            global val
            global st
            global ed  
            global prev
            start_kw = text.search(key_word, search_from, stopindex=search_until, nocase=case_sensitive)   
            if prev==1 and r==2 and start_kw=="":
                text.tag_remove("search",st,ed)
                text.delete(index1=st,index2=ed)
                text.insert(st,repkey_word)
                prev=r
            elif start_kw != "" and  start_kw != None:
                val=key_word
                search_from = "%s + %sc "%(start_kw, len(key_word))
                if prev==None:
                    if r==1:
                        text.tag_configure("search", background="green")
                        text.tag_add("search", start_kw, "%s + %sc"%(start_kw, len(key_word)))
                    else:
                        text.delete(index1=start_kw,index2=search_from)
                        text.insert(start_kw,repkey_word)
                elif prev==1:
                     text.tag_remove("search",st,ed)
                     if r==1:
                         text.tag_configure("search", background="green")
                         text.tag_add("search", start_kw, "%s + %sc"%(start_kw, len(key_word)))   
                     else:
                         text.delete(index1=st,index2=ed)
                         text.insert(st,repkey_word)
                         search_from=ed
                else:
                     if r==1:
                         text.tag_configure("search", background="green")
                         text.tag_add("search", start_kw, "%s + %sc"%(start_kw, len(key_word)))  
                     else:
                          text.delete(index1=start_kw,index2=search_from)
                          text.insert(start_kw,repkey_word)
                          search_from=ed     
                st=start_kw
                ed=search_from
                prev=r                       
            else:
                 if prev==1:
                     text.tag_remove("search",st,ed)
                 messagebox.showinfo("Textoditor","Cannot find "+key_word)  
                 cancelcmd()
    w1.findnext = Button(w1, text="Find Next", command=lambda:repnextcmd(1))
    w1.findnext.pack(anchor=W)
    w1.repnext = Button(w1, text="Replace", command=lambda:repnextcmd(2))
    w1.repnext.pack(anchor=W)
    def cancelcmd():
        global val
        global search_from
        global st
        global prev
        w1.unbind("<Return>")
        text.focus()
        search_from=None
        val=None
        st=None
        ed=None
        prev=None
        w1.destroy()
    w1.cancel = Button(w1, text="Cancel", command=cancelcmd)
    w1.cancel.pack(anchor=W)
    w1.protocol('WM_DELETE_WINDOW',cancelcmd)
def delete():
    text.delete(index1=SEL_FIRST,index2=SEL_LAST)    
def timedate():
     time_string = time.strftime('%H:%M:%S')
     from datetime import date
     today=str(date.today())
     text.insert(INSERT," "+time_string+" "+today)  
#formatmenu_methods
def bgcolor():
    color = askcolor() 
    text.config(background=color[1])
    if color[1]!='#ffffff' :
        text.edit_modified(True)
def fontstyle():
       Font_wm(Font=font1)
def fontcolor():
      color=askcolor()   
      text.config(foreground=color[1])
#viewmenu_methods
def stview():
        str1=str(text.index(INSERT))
        pos=str1.index('.')
        line=str1[:pos]
        col=str1[pos+1:]
        msg="Line Number is "+line+" and Column Number is "+col
        messagebox.showinfo("Status Info",msg)
#helpmenu_methods
def about():
       msg1="TextOditor :- Minimalstic Text Editor\n"
       msg2="Version 1.0\n"
       msg3="User Manual at :-github.com/ankita240796/TextEditor"
       messagebox.showinfo("TextOditor",msg1+msg2+msg3)
#Menubar
menubar=Menu(window)
window.config(menu=menubar)
#filemenu
filemenu=Menu(menubar)
menubar.add_cascade(label="File",menu=filemenu)
filemenu.add_command(label="New",command=new,accelerator="Ctrl+N")
filemenu.add_command(label="Open",command=open_file,accelerator="Ctrl+O")
filemenu.add_separator()
filemenu.add_command(label="Save",command=save,accelerator="Ctrl+S")
filemenu.add_command(label="Save As",command=save_as,accelerator="Ctrl+Alt+S")
filemenu.add_command(label="Close",command=close,accelerator="Alt+F4")
#editmenu
editmenu=Menu(menubar)
menubar.add_cascade(label="Edit",menu=editmenu)
editmenu.add_command(label="Undo",command=undo, accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=redo, accelerator="Ctrl+Y")
editmenu.add_separator()
editmenu.add_command(label="Cut",command=cut, accelerator="Ctrl+X")
editmenu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
editmenu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
editmenu.add_command(label="Delete", command=delete, accelerator="Del")
editmenu.add_separator()
editmenu.add_command(label="Find...", command=find, accelerator="Ctrl+F")
editmenu.add_command(label="Replace...", command=replace, accelerator="Ctrl+H")
editmenu.add_command(label="Go To...", command=goto, accelerator="Ctrl+G")
editmenu.add_separator()
editmenu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
editmenu.add_command(label="Time/Date", command=timedate, accelerator="F5")
#formatmenu
formatmenu=Menu(menubar)
menubar.add_cascade(label="Format",menu=formatmenu)
formatmenu.add_command(label="Change Background Color",command=bgcolor)
formatmenu.add_command(label="Change Font Style",command=fontstyle)
formatmenu.add_command(label="Change Font Color",command=fontcolor)
#viewmenu
viewmenu=Menu(menubar)
menubar.add_cascade(label="View",menu=viewmenu)
viewmenu.add_command(label="View Status Info",command=stview)
#helpmenu
helpmenu=Menu(menubar)
menubar.add_cascade(label="Help",menu=helpmenu)
helpmenu.add_command(label="About",command=about)
window.protocol('WM_DELETE_WINDOW',close1)
window.mainloop()

