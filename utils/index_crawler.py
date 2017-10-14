#!/usr/bin/env python3
import os
import subprocess
import sqlite3 as sqlite
import tkinter
# separate imports needed due to tkinter idiosyncrasies
from tkinter import ttk
from tkinter import filedialog, messagebox



class ExportForm:
    def __init__(self, conn):
        cframe = tkinter.Frame(master)
        cframe.grid()

        self.valueIndex = []
        self.valueEntry = []
        self.valuePages = []
        self.sv_idx = tkinter.StringVar()
        self.sv_ent = tkinter.StringVar()
        self.path_to_reader = os.path.abspath(r'/usr/bin/evince')

        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc", width=20)


        self.txtIndex = tkinter.Entry(master, textvariable=self.sv_idx, width = 40)
        self.txtIndex.grid(row=0, column=0)

        self.txtEntry = tkinter.Entry(master, textvariable=self.sv_ent, width = 30)
        self.txtEntry.grid(row=0, column=2)

        self.lstIndex = tkinter.Listbox(master, selectmode=tkinter.EXTENDED, exportselection=0, width = 40)
        self.lstIndex.grid(row=1, column=0)

        self.lstEntry = tkinter.Listbox(master, selectmode=tkinter.EXTENDED, exportselection=0, width = 30)
        self.lstEntry.grid(row=1, column=2)

        self.lstPages = tkinter.Listbox(master, selectmode=tkinter.SINGLE, exportselection=0, width = 20)
        self.lstPages.grid(row=1, column=4)

        self.btnSelectAll_idx = ttk.Button(master, width=10, text='Select All', style="TButton", command=self.selectall_idx)
        self.btnSelectAll_idx.grid(row=3, column=0, sticky = tkinter.W)

        self.btnSelectAll_entry = ttk.Button(master, width=10, text='Select All', style="TButton", command=self.selectall_ent)
        self.btnSelectAll_entry.grid(row=3, column=2, sticky = tkinter.W)

        self.btnClearAll_idx = ttk.Button(master, width=10, text='Clear All', style="TButton", command=self.clearall_idx)
        self.btnClearAll_idx.grid(row=3, column=0, sticky = tkinter.E)

        self.btnClearAll_entry = ttk.Button(master, width=10, text='Clear All', style="TButton", command=self.clearall_ent)
        self.btnClearAll_entry.grid(row=3, column=2, sticky = tkinter.E)

        self.btnGrab = ttk.Button(master, width=20, text='Export', style="TButton", command=self.grab)
        self.btnGrab.grid(row=3, column=4)

        self.scrollbar_idx_v = tkinter.Scrollbar(master, orient=tkinter.VERTICAL)
        self.lstIndex.config(yscrollcommand=self.scrollbar_idx_v.set)
        self.scrollbar_idx_v.config(command=self.lstIndex.yview)
        self.scrollbar_idx_v.grid(row=1, column=1, sticky=tkinter.N+tkinter.S)
        self.scrollbar_idx_h = tkinter.Scrollbar(master, orient=tkinter.HORIZONTAL)
        self.lstIndex.config(xscrollcommand=self.scrollbar_idx_h.set)
        self.scrollbar_idx_h.config(command=self.lstIndex.xview)
        self.scrollbar_idx_h.grid(row=2, column=0, sticky=tkinter.E+tkinter.W)

        self.scrollbar_ent_v = tkinter.Scrollbar(master, orient=tkinter.VERTICAL)
        self.lstEntry.config(yscrollcommand=self.scrollbar_ent_v.set)
        self.scrollbar_ent_v.config(command=self.lstEntry.yview)
        self.scrollbar_ent_v.grid(row=1, column=3, sticky=tkinter.N+tkinter.S)
        self.scrollbar_ent_h = tkinter.Scrollbar(master, orient=tkinter.HORIZONTAL)
        self.lstEntry.config(xscrollcommand=self.scrollbar_ent_h.set)
        self.scrollbar_ent_h.config(command=self.lstEntry.xview)
        self.scrollbar_ent_h.grid(row=2, column=2, sticky=tkinter.E+tkinter.W)

        exclude = "pubkey || ' ' || version NOT IN ('phb5e original', 'dmg5e original')"

        result = conn.execute("SELECT idx_text FROM dnd_index WHERE {!s} "
                              "GROUP BY idx_text, idx ORDER BY idx_text, idx;".format(exclude))
        for row in result:
            # print(row)
            self.lstIndex.insert(tkinter.END, row[0])

        def onselect_Index(evt):
            self.lstEntry.delete(0, tkinter.END)
            self.lstPages.delete(0, tkinter.END)
            w = evt.widget
            c = w.curselection()
            value = []
            li = len(c)
            for i in range(0, li):
                value.append(w.get(c[i]))
            # print(value)
            self.valueIndex = value
            s = ("SELECT Entry FROM dnd_index WHERE {!s} AND idx_text IN ({!s}) "
                 "GROUP BY entry ORDER BY idx_text, idx;".format(exclude, ','.join('?' * len(self.valueIndex))))
            result = conn.execute(s, self.valueIndex)
            count = 0
            for row in result:
                count += 1
                self.lstEntry.insert(tkinter.END, row[0])
            if count == 1:
                self.lstEntry.selection_set(0)
                self.lstEntry.event_generate("<<ListboxSelect>>")

        def onselect_Entry(evt):
            self.lstPages.delete(0, tkinter.END)
            w = evt.widget
            c = w.curselection()
            value = []
            li = len(c)
            for i in range(0, li):
                value.append(w.get(c[i]))
            # print(value)
            self.valueEntry = value
            s = ("SELECT pubkey, page FROM dnd_index WHERE {!s} AND entry IN ({!s}) "
                 "AND idx_text IN ({!s}) GROUP BY pubkey, page ORDER BY pubkey, page;".format(exclude,','.join('?' * len(self.valueEntry)),
                                                                              ','.join('?' * len(self.valueIndex))))
            result = conn.execute(s,self.valueEntry + self.valueIndex)
            count = 0
            for row in result:
                count += 1
                self.lstPages.insert(tkinter.END, ' | '.join((row[0], str(row[1]))))
            #if count == 1:
            #    self.lstPages.selection_set(0)
            #    self.lstPages.event_generate("<<ListboxSelect>>")

        def onselect_Pages(evt):
            w = evt.widget
            c = w.curselection()
            value = []
            li = len(c)
            for i in range(0, li):
                value.append(tuple(w.get(c[i]).split(' | ')))
            # print(value)
            self.valuePages = value
            for i in self.valuePages:
                pg = int(i[1])
                rec = conn.execute("SELECT link, page_adjust FROM dnd_pub WHERE pubkey = ?;",(i[0],)).fetchone()
                pdf_path = rec[0]
                pg += int(rec[1])
                process = subprocess.Popen([self.path_to_reader, ''.join(('--page-label=',str(pg))), pdf_path], shell=False,  stdout=subprocess.PIPE)


        def callback_idx(sv):
            self.lstEntry.delete(0, tkinter.END)
            self.lstPages.delete(0, tkinter.END)
            cb = sv.get()
            if cb:
                self.lstIndex.delete(0, tkinter.END)
                #print(cb, type(cb))
                result = conn.execute("SELECT idx_text FROM dnd_index WHERE {!s} "
                                      "GROUP BY idx_text, idx HAVING idx_text LIKE '%{!s}%' ORDER BY idx;".format(exclude, cb))
            else:
                result = conn.execute("SELECT idx_text FROM dnd_index WHERE {!s} "
                                      "GROUP BY idx_text, idx ORDER BY idx;".format(exclude))
            for row in result:
                self.lstIndex.insert(tkinter.END, row[0])

        def callback_ent(sv):
            self.lstPages.delete(0, tkinter.END)
            cb = sv.get()
            if cb:
                self.lstEntry.delete(0, tkinter.END)
                #print(cb, type(cb))
                sql = ("SELECT Entry FROM dnd_index WHERE {!s} AND idx_text IN ({!s}) "
                       "GROUP BY entry HAVING entry LIKE '%{!s}%' ORDER BY idx;".format(exclude, ','.join('?' * len(self.valueIndex)), cb))
                result = conn.execute(sql, self.valueIndex)
            else:
                sql = ("SELECT Entry FROM dnd_index WHERE {!s} AND idx_text IN ({!s}) "
                     "GROUP BY entry ORDER BY idx;".format(exclude, ','.join('?' * len(self.valueIndex))))
                result = conn.execute(sql, self.valueIndex)
            for row in result:
                self.lstEntry.insert(tkinter.END, row[0])

        self.lstIndex.bind('<<ListboxSelect>>', onselect_Index)
        self.lstEntry.bind('<<ListboxSelect>>', onselect_Entry)
        self.lstPages.bind('<<ListboxSelect>>', onselect_Pages)
        self.sv_idx.trace("w", lambda name, index, mode, sv=self.sv_idx: callback_idx(sv))
        self.sv_ent.trace("w", lambda name, index, mode, sv=self.sv_ent: callback_ent(sv))

    def selectall_idx(self):
         self.lstIndex.select_set(0, tkinter.END)
         self.lstIndex.event_generate("<<ListboxSelect>>")

    def selectall_ent(self):
         self.lstEntry.select_set(0, tkinter.END)
         self.lstEntry.event_generate("<<ListboxSelect>>")

    def clearall_idx(self):
        self.lstIndex.selection_clear(0, tkinter.END)
        self.lstIndex.event_generate("<<ListboxSelect>>")

    def clearall_ent(self):
        self.lstEntry.selection_clear(0, tkinter.END)
        self.lstEntry.event_generate("<<ListboxSelect>>")

    def grab(self):
        w = self.lstPages
        c = w.curselection()
        value = []
        li = len(c)
        for i in range(0, li):
            value.append(w.get(c[i]))
        print(value)


try:
    scrptdir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    scrptdir = os.getcwd()
scrptpath = os.path.join(scrptdir, "dmdb.sqlite")
conn = sqlite.connect(scrptpath)
master = tkinter.Tk()
master.title("D&D Index Crawler")
mf = ExportForm(conn)
master.mainloop()
conn.close()

