import tkinter as tk
import os
from tkinter import simpledialog
from tkinter import ttk
from tkinter import filedialog
class ScrollableImage(tk.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0,  sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set, 
                           yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled 
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
        self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)

    def mouse_scroll(self, evt):
        if evt.state == 0 :
            self.cnvs.yview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
        if evt.state == 1:
            self.cnvs.xview_scroll(-1*(evt.delta), 'units') # For MacOS
            self.cnvs.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
def record_user(gui):
    answer = simpledialog.askstring("Input", "What is your first name?",
                                parent=gui)
    if answer is not None:
        print("Your first name is ", answer)
        return answer
def show_progress():
    opinion = check_opinion(curation_dic,img_dir)
    status_label['text']= "{N}/{num} have been checked\n Current Opinin:\n{opinion}".format(N=len(curation_dic),num=num_figures,opinion=opinion)
    current_label['text'] = "Figure {N}/{num}".format(N=N+1,num=num_figures)
def last_update():
    global N
    global img_dir
    N = N - 1
    if N<0 :
        tk.messagebox.showinfo(title="No more figures", message="This is the first one")
        N = 0
    img_dir = folder_selected+"/"+pngs[N]
    img_show(gui,img_dir)
    show_progress()
def next_update():
    global N
    global img_dir
    N = N + 1
    if N >= num_figures :
        tk.messagebox.showinfo(title="No more figures", message="This is the last one")
        N = num_figures-1
    img_dir = folder_selected+"/"+pngs[N]
    img_show(gui,img_dir)
    show_progress()
def goto_update(answer):
    global N
    global img_dir
    N = int(answer)-1
    if N >= num_figures or N <0 :
        tk.messagebox.showinfo(title="No such figures", message="try something else, directing to Figure1 now")
        N = 0
    img_dir = folder_selected+"/"+pngs[N]
    img_show(gui,img_dir)
    show_progress()
def info_update():
    global N
    global img_dir
    global def_source_val
    global def_real_val
    real = def_real_val.get()
    source = def_source_val.get()
    curation_dic[img_dir]=[real,source,user_id]
    #output.write("{figure}\t{denovo}\t{source}\t{user}\n".format(figure=img_dir,denovo=real,source=source,user=user_id))
    show_progress()
    print(check_opinion(curation_dic,img_dir))
    if 0<= N < num_figures-1:
        N = N + 1
        img_dir = folder_selected+"/"+pngs[N]
        img_show(gui,img_dir)
        novo_option = ["Yes", "No", "Uncertain"]
        def_real_val = tk.StringVar(gui)
        def_real_val.set("Is it denovo mutation?")
        source_option = ["Father", "Mother", "Uncertain"]
        def_source_val = tk.StringVar(gui)
        def_source_val.set("What is the source of mutation?")
        novo_menu = tk.OptionMenu(gui, def_real_val, *novo_option)
        novo_menu.grid(row=0,column=0,sticky='ew')
        source_menu = tk.OptionMenu(gui, def_source_val, *source_option)
        source_menu.grid(row=0,column=1,sticky='ew')
        show_progress()
        if len(curation_dic)==num_figures:
            tk.messagebox.showinfo(title="All curated!", message="Manual Curation of {} is done".format(folder_selected))
    else:
        tk.messagebox.showinfo(title="No more figures", message="There is no more figures after")
def img_show(gui,img_dir):
    global img
    img = tk.PhotoImage(file=img_dir)
    image_window = ScrollableImage(gui, image=img, scrollbarwidth=30, 
                               width=1200, height=800)
    image_window.grid(row = 1, column = 0,columnspan = 3,sticky='wn')
    #image_label = tk.Label(gui,image=img)
    #image_label.grid(row = 1, column = 0,columnspan = 3,sticky='wn')
def check_opinion(curation_dic,img_dir):
    if img_dir not in curation_dic:
        opinion = "Not curated"
    else:
        if_real = curation_dic[img_dir][0] 
        which_source = curation_dic[img_dir][1]
        opinion = "Denvo:{if_real}\tSource:{which_source}".format(if_real=if_real,which_source=which_source) 
    return opinion
def goto_figure():
    goto_N = simpledialog.askstring("Input", "Which figure would you like to check?",
                                parent=gui)
    goto_update(goto_N)
if __name__ == "__main__":
    # create a GUI window
    N = 0
    output = open("test.txt","w")
    gui = tk.Tk()
    user_id = "empty"
    # set the background colour of GUI window
    gui.configure(background="light green")
 
    # set the title of GUI window
    gui.title("Is this de novo?")
 
    # set the configuration of GUI window
    #gui.geometry("1200x800")
    #if user_id == "empty":
    #    user_id = record_user(gui)
    
    folder_selected = filedialog.askdirectory()
    pngs = os.listdir(folder_selected)
    num_figures = len(pngs)
    curation_dic = {}
    img_dir = folder_selected+"/"+pngs[N]
    img_show(gui,img_dir)
    # Create the list of options
    opinion = check_opinion(curation_dic,img_dir)
    status_label = tk.Label(gui, text="{N}/{num} have been checked\n Current Opinin of this:\n{opinion}".format(N=len(curation_dic),num=num_figures,opinion=opinion))
    status_label.grid(row=0,column=3)
    novo_option = ["Yes", "No", "Uncertain"]
    def_real_val = tk.StringVar(gui)
    def_real_val.set("Is it denovo mutation?")
    source_option = ["Father", "Mother", "Uncertain"]
    def_source_val = tk.StringVar(gui)
    def_source_val.set("What is the source of mutation?")
    novo_menu = tk.OptionMenu(gui, def_real_val, *novo_option)
    novo_menu.grid(row=0,column=0,sticky='ew')
    source_menu = tk.OptionMenu(gui, def_source_val, *source_option)
    source_menu.grid(row=0,column=1,sticky='ew')
    B = tk.Button(gui, text ="submit", command = info_update)
    B.grid(row=0,column=2,sticky='ew')
    Last = tk.Button(gui, text ="Last Figure", command = last_update)
    Next= tk.Button(gui, text ="Next Figure", command = next_update)
    Last.grid(row=2,column=0,sticky='ew')
    Next.grid(row=2,column=1,sticky='ew')
    goto_figure = tk.Button(gui,text="Go to Figure Number",command = goto_figure).grid(row=2,column=2,sticky="ew")
    current_label = tk.Label(gui,text = "Figure {N}/{num}".format(N=N+1,num=num_figures))
    current_label.grid(row=3,column=0,columnspan=3)
    gui.mainloop()
