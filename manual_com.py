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
def info_update():
    global N
    global img_dir
    real = def_real_val.get()
    source = def_source_val.get()
    output.write("{figure}\t{denovo}\t{source}\t{user}\n".format(figure=img_dir,denovo=real,source=source,user=user_id))
    if N < num_figures:
        N = N + 1
        img_dir = folder_selected+"/"+pngs[N]
        img_show(gui,img_dir)
    else:
        tk.messagebox.showinfo(title="Finished", message="Manual Curation of {} is done".format(folder_selected))
def img_show(gui,img_dir):
    global img
    img = tk.PhotoImage(file=img_dir)
    image_window = ScrollableImage(gui, image=img, scrollbarwidth=30, 
                               width=1200, height=800)
    image_window.grid(row = 1, column = 0,columnspan = 3,sticky='wn')
    #image_label = tk.Label(gui,image=img)
    #image_label.grid(row = 1, column = 0,columnspan = 3,sticky='wn')
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
    img_dir = folder_selected+"/"+pngs[N]
    img_show(gui,img_dir)
    # Create the list of options    
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
    tk.Label(gui, text="{N}/{num} have been checked".format(N=N+1,num=num_figures)).grid(row=0,column=3)
    gui.mainloop()
