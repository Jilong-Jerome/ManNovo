import tkinter as tk
import numpy as np
import os
from tkinter import simpledialog
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors
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
    answer = simpledialog.askstring("Input", "Please define your user ID?",
                                parent=gui)
    if answer is not None:
        print("Your User ID is ", answer)
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
        #tk.messagebox.showinfo(title="No more figures", message="There is no more figures after")
        goto_non()
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
def goto_non():
    un_curated_list = []
    for i in range(len(pngs)):
       temp_img = folder_selected+"/"+pngs[i]
       opinion = check_opinion(curation_dic,temp_img)
       if opinion == "Not curated":
           un_curated_list.append(i)
    if len(un_curated_list) == 0: 
        goto_N = 1
        tk.messagebox.showinfo(title="All curated!", message="All done, directing back to the first figure now")
    else:
        if N > max(un_curated_list):
            goto_N = min(un_curated_list)+1
        else:
            for n in un_curated_list:
                if n > N:
                    goto_N = n+1
                    break
    goto_update(goto_N)
def print_out():
    output = open(outfile,"w")
    for key in curation_dic:
        output.write(key+"\t")
        for i in range(len(curation_dic[key])):
            output.write(curation_dic[key][i])
            if i!=2:
                output.write("\t")
            else:
                output.write("\n")
def plot_curated():
    figures = []
    site = []
    color = []
    for i in range(len(pngs)):
        figures.append(i+1)
        site.append(0)
        temp_img =folder_selected+"/"+pngs[i] 
        if temp_img in curation_dic:
            if curation_dic[temp_img][0] == "Yes":
                color.append(1)
            else:
                color.append(-1)
        else:
            color.append(0)
    fig, ax = plt.subplots(figsize=(10,80), dpi=10)
    #ax.scatter(site, figures, c=color)
    #ax.set(xlim=(-1, 1),ylim=(1, len(pngs)), yticks=np.arange(1, len(pngs)))
    Z = np.array(color).reshape((len(pngs),1))
    cmap = colors.ListedColormap(['red','grey','blue'])
    bounds = [-1.5,-0.5,0.5,1.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    ax.imshow(Z, cmap=cmap, norm=norm)
    plt.yticks(np.arange(0,len(pngs),1),np.arange(1, len(pngs)+1, 1)) 
    ax.tick_params(axis='y', which='major', pad=1)
    plt.xticks([])
    scatter = FigureCanvasTkAgg(fig, gui) 
    scatter.get_tk_widget().grid(row=1,column=3)
def checking_previous():
    global outfile
    if os.path.isfile(outfile) and os.stat(outfile).st_size != 0:
        temp_file = open(outfile)
        for line in temp_file:
            info = line.strip("\n").split("\t")
            curation_dic[info[0]]=[info[1],info[2],info[3]]
        temp_file.close()
def cancel_c():
    curation_dic.pop(img_dir)
    show_progress()
if __name__ == "__main__":
    # create a GUI window
    N = 0
    gui = tk.Tk()
    user_id = "empty"
    # set the background colour of GUI window
    gui.configure(background="light green")
 
    # set the title of GUI window
    gui.title("Is this de novo?")
 
    # set the configuration of GUI window
    #gui.geometry("1200x800")
    if user_id == "empty":
        user_id = record_user(gui)
    folder_selected = filedialog.askdirectory()
    outfile = folder_selected.split("/")[-1]+"_"+user_id
    pngs = os.listdir(folder_selected)
    num_figures = len(pngs)
    curation_dic = {}
    checking_previous()
    img_dir = folder_selected+"/"+pngs[N]
    img_show(gui,img_dir)
    # Create the list of options
    #show_progress()
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
    current_label.grid(row=3,column=1)
    plot = tk.Button(gui,text = "Plot Curation", command = plot_curated)
    goto_non_b = tk.Button(gui,text = "Go to next uncurated", command = goto_non)
    plot.grid(row=2,column=3,sticky="ew")
    goto_non_b.grid(row=3,column=3,sticky="ew")
    print_b = tk.Button(gui,text = "Print out",command = print_out)
    print_b.grid(row=3,column=2,sticky="ew")
    cancel_b = tk.Button(gui,text = "Cancel Curation",command = cancel_c)
    cancel_b.grid(row=3,column=0,sticky ="ew")
    gui.mainloop()
