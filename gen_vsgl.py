import shutil
import os
import tkinter as tk
import tkinter.ttk as ttk
import zipfile
import threading
import logging
import queue
from argparse import ArgumentParser
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
from urllib import request
from enum import Enum
import subprocess
from threading import Thread
import re

def open_file(file,visual_studio_projects_directory):
    file_to_open = os.path.join(visual_studio_projects_directory,file)
    os.system('"%s"'% file_to_open)

def read_file(dir):
    f = open(dir,'r')
    template_file = f.read()
    f.close()
    return template_file

#/////////////////////////////////////////////////////////////
# Project builder is somehow the model contains the data and
# the actions to build a visual studio project
#///////////////////////////////////////////////////////////
class ProjectBuilder:

  def __init__(self,controller):
    self.project_name = 'ProjectTemplate_GL'
    self.controller = controller
    self.visual_studio_projects_directory = 'C:/Users/aitor/source/repos'
    self.template_dir = os.path.join(os.getcwd(), self.project_name)
    # visual studio project file string template
    self.vcxproj = read_file(os.path.join(self.template_dir,'template.vcxproj'))
    # visual studio filters file template string
    self.vcxproj_filters = read_file(os.path.join(self.template_dir,'template_filters.vcxproj.filters'))
    # visual studio users file template string
    self.vcxprojuser  = read_file(os.path.join(self.template_dir,'template_user.vcxproj.user'))
    # list of recently created projects. We create a list with the new created projects to
    # delete. The reason of that is to protect deliting existing projects that have not
    # been created in the current sesion. It could be usefull to delte projects old projects from
    # the tool but this is a bit dangerous and I don't want to delete projects by accident
    self.new_created_projects = []
    self.solution_file = read_file(os.path.join(self.template_dir,'template.sln'))

  # create an openGL project with the given name
  def create_project(self,project_name,build_type):  
    os.chdir(self.visual_studio_projects_directory)
    # create solution directory in the folder where all visual studio projects are by default
    os.makedirs(os.path.join(project_name, build_type))
    # cd into this directory
    os.chdir(project_name)
    # create solution file
    self.create_solution_file(project_name)
    # copy the template folders, files and create the project directory
    shutil.copytree(self.template_dir, os.path.join(os.getcwd(),project_name))
    # cd into project file
    os.chdir(project_name)
    # create all the files
    self.create_project_file(project_name)
    self.create_project_user(project_name)
    self.create_project_filters(project_name)
    print('before moving dlls')
    print(os.getcwd())
    folder_to_move = os.path.join('..',build_type)
    # move the libs to ../Debug folder
    shutil.move('glew32.dll', folder_to_move)
    shutil.move('glfw3.dll', folder_to_move)
    self.new_created_projects.append(project_name)
    os.chdir(self.visual_studio_projects_directory)

  def find_dep(self,dep_name):
        pattern = re.compile(r''.join(dep_name))
        list_dirs = [ item for item in os.listdir(os.path.join('ProjectTemplate_GL','lib'))]
        matches_it = pattern.finditer(' '.join(list_dirs))

        if all(False for _ in matches_it):
            return False
        else:
            return True
            
  def set_up_dependencies(self,build_type,build_tool = 'NMake Makefiles'):
    deps = self.find_dep('glew') or self.find_dep('glfw')
    if not deps:
      self.process = subprocess.call(['python3','buildTool.py','-b',build_type,'-t',build_tool])

  def create_solution_file(self,project_name):
      solution_file_extension = '.sln'
      file_content = self.solution_file.replace('project_name',project_name)
      with open(project_name + solution_file_extension, 'w') as f:
        f.write(file_content)

  def create_project_file(self,project_name):
      vcxproj_file_extension = '.vcxproj'
      file_content = self.vcxproj.replace('project_name', project_name)
      with open(project_name+vcxproj_file_extension, 'w') as f:
        f.write(file_content)

  def create_project_filters(self,project_name):
      vcxproj_filters_file_extension = '.vcxproj.filters'
      with open(project_name + vcxproj_filters_file_extension, 'w') as f:
        f.write(self.vcxproj_filters)

  def create_project_user(self,project_name):
      vcxproj_usr_file_extension = '.vcxproj.user'
      with open(project_name+vcxproj_usr_file_extension, 'w') as f:
        f.write(self.vcxprojuser)

  def delete_project(self,delete_project):
      can_be_deleted = False
      for project in self.new_created_projects:
        if project == delete_project:
          can_be_deleted = True
          break
      if can_be_deleted :
        shutil.rmtree(os.path.join(self.visual_studio_projects_directory,delete_project))
        # remove item from the list of all new created projects
        self.new_created_projects.remove(delete_project)
      return can_be_deleted

  # open the created project
  def open_visual_studio(self,open_project):
      if len(open_project) > 0 :
        project_folder = os.path.join(visual_studio_projects_directory,open_project)
        solution_file = os.path.join(project_folder,open_project+'.sln')
        os.system('"%s"'% solution_file)
        return True
      else:
        return False

#/////////////////////////////////////////////////////////////
# Controller callback is the bridge between the view and the model
#  or the Project Builder
#///////////////////////////////////////////////////////////
class CallbacksController:

  def __init__(self,view_app):
    self.app = view_app
    self.project_builder = ProjectBuilder(self)

  def delete_project(self):
    delete_project = self.app.entry.get()
    suceed = self.project_builder.delete_project(delete_project)
    if suceed :
      self.app.show_message("Project Deleted","open gl project: "+ delete_project + " has been deleted")
      self.app.update_tree_view(self.get_visualStudio_proj_dir())
    else:
      self.app.show_message("Delete Error", "you can onlt delete projects that\nbeing created in this session for safety")

  def create_project_call(self):
    project_name = self.app.entry.get()
    # arguments
    build_type = self.app.build_type_combo_box.get()
    self.project_builder.set_up_dependencies(build_type)
    self.project_builder.create_project(project_name,build_type)
    self.app.update_tree_view(self.get_visualStudio_proj_dir())
    msg = "Project created","open gl project:"+ project_name + " succesfully created"
    self.app.show_message("Project created", msg, self.app.MSG_TYPE.INFO)

  def open_visual_studio(self):
    open_project = self.app.entry.get()
    succeed = self.project_builder.open_visual_studio(open_project)
    if succeed == False:
      self.app.show_message("project not found","select a project to open!",self.app.MSG_TYPE.ERROR)

  def get_visualStudio_proj_dir(self):
    return self.project_builder.visual_studio_projects_directory

  def change_vsprojects_dir(self):
    self.project_builder.visual_studio_projects_directory = \
        filedialog.askdirectory(initialdir = self.get_visualStudio_proj_dir(),\
        title="Select project directory")
    vsproj_dir = self.get_visualStudio_proj_dir()
    self.app.update_tree_view(vsproj_dir)
   # os.chdir(vsproj_dir)
    self.app.dir_label_text.set(vsproj_dir)

   #callbacks
  def current_selected_items_callback(self,event):
    item = self.app.project_list_box.selection()[0]
    text_item = self.app.project_list_box.item(item,"text")
    if os.path.isdir(os.path.join(self.get_visualStudio_proj_dir(),text_item)):
      self.app.entry.delete(0,"end")
      self.app.entry.insert(0, text_item)
      old_path = os.getcwd()
      os.chdir(os.path.join(self.get_visualStudio_proj_dir(),text_item))
      self.project_builder.visual_studio_projects_directory = os.getcwd()
      self.app.dir_label_text.set(self.get_visualStudio_proj_dir())
      self.app.update_tree_view(self.get_visualStudio_proj_dir())
      # restore path
      os.chdir(old_path)
    else:
      open_file(text_item,self.get_visualStudio_proj_dir())

  def back_directory(self):
      old_path = os.getcwd()
      os.chdir('..')
      self.project_builder.visual_studio_projects_directory = os.getcwd()
      vsproject_dir = self.get_visualStudio_proj_dir()
      self.app.update_tree_view(vsproject_dir)
      self.app.dir_label_text.set(vsproject_dir)
      # restore path
      os.chdir(old_path)


###########################################
# this is the main Gui app or the View
###########################################
class App:
  class MSG_TYPE(Enum):
    INFO = 1
    WARN = 2
    ERROR = 3

  def __init__(self):
    self.icons_dir = os.path.join(os.getcwd(),'icons')
    self.app_controller = CallbacksController(self)
    self.init_tkinter()
    self.load_icons()
    self.init_gui_elements()
    
  def run(self):
    self.root.mainloop()

  def load_icons(self):
    size = 35,35
    folder_icon_path = os.path.join(self.icons_dir,"ficon.png")
    photo_folder = Image.open(folder_icon_path)
    self.folder_icon = ImageTk.PhotoImage(photo_folder)
    # file icon
    file_icon_path = os.path.join(self.icons_dir,"file.png")
    photo_file = Image.open(file_icon_path).resize(size,Image.ANTIALIAS)
    self.file_icon = ImageTk.PhotoImage(photo_file)
    # exec icon
    exec_icon_path = os.path.join(self.icons_dir,"exec.png")
    photo_exec = Image.open(exec_icon_path).resize(size,Image.ANTIALIAS)
    self.exec_icon = ImageTk.PhotoImage(photo_exec)
    # back dir icon
    back_icon_path = os.path.join(self.icons_dir,"backdir.png")
    back_folder = Image.open(back_icon_path).resize(size,Image.ANTIALIAS)
    self.back_dir_icon = ImageTk.PhotoImage(back_folder)

  def init_tkinter(self):
    #initialize the tkinter library
    self.root = tk.Tk()
    self.root.title('VS openGl project creator ')
    self.root.geometry("300x600")
    self.root.minsize(600,600)
    self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=os.path.join(self.icons_dir,"opengl.png")))
    self.root.resizable(True,True)

  def init_gui_elements(self):
    #create and config menu
    self.menu = tk.Menu(self.root)
    #create menu items
    self.options = tk.Menu(self.menu)
    self.menu.add_cascade(label="options", menu = self.options)
    self.options.add_command(label = "change project directory", \
                             command = self.app_controller.change_vsprojects_dir)
    self.root.config(menu = self.menu)
    #main top level frame
    self.main_frame = tk.Frame(self.root,relief=tk.RAISED )
    # create 2 subframes
    self.subframe_1 =  tk.LabelFrame(self.main_frame)
    self.subframe_2 =  tk.LabelFrame(self.main_frame)
    #create the entry for the new project name
    self.entry = tk.Entry(self.subframe_2)
    # create list box with a new style to avoid icon overlaping
    self.s = ttk.Style()
    self.s.configure('treeStyle.Treeview', rowheight=40)
    self.project_list_box = ttk.Treeview(self.subframe_1, height=4, style='treeStyle.Treeview')
    #change select mode to not allow multiple selection of items
    self.project_list_box.config(selectmode='browse')
    # configure the heigh of the tree
    self.project_list_box.config(height=10)
    # some labels
    self.label1 = tk.Label(self.subframe_1, text="vs projects list")
    self.dir_label_text = tk.StringVar()
    self.dir_label_text.set(self.app_controller.get_visualStudio_proj_dir())

    self.curr_dir_label = tk.Label(self.subframe_1,textvariable = self.dir_label_text,\
    text = self.app_controller.get_visualStudio_proj_dir(),width = 100)

    self.curr_dir_label.pack(anchor='ne',padx=50)
    self.label = tk.Label(self.subframe_2, text="Project name")
    self.label.grid(row = 0, column=0)
    # create buttons
    self.delete_button = tk.Button(self.subframe_2,text="Delete", command = self.app_controller.delete_project)
    self.create_button = tk.Button(self.subframe_2, text = "Create", command= self.app_controller.create_project_call)
    self.openproj_button = tk.Button(self.subframe_2, text = "Open", command = self.app_controller.open_visual_studio)
    self.back_button = tk.Button(self.subframe_1,image = self.back_dir_icon, command = self.app_controller.back_directory)
    self.back_button.pack(anchor="nw")
    # set tree view callbacks and fill in the tree
    self.project_list_box.bind('<Double-1>',self.app_controller.current_selected_items_callback)
    self.project_list_box.bind('<<TreeviewSelect>>',self.write_selected )
    self.fill_tree_view(self.app_controller.get_visualStudio_proj_dir())
    # create comboBox for choosing build type
    self.build_options = ['Debug','Release']
    self.build_type_combo_box = ttk.Combobox(self.subframe_2,value = self.build_options,state = 'readonly')
    self.build_type_combo_box.current(0)
    self.build_type_combo_box.grid(row=0,column = 3, sticky = "we")
    #position elements in subrame_2
    self.entry.grid(row = 0, column = 2,sticky="we")
    self.delete_button.grid(row=1,column=0, padx=2,pady=10,sticky="we")
    self.create_button.grid(row= 1, column= 2,padx=2, pady=10,sticky="we")
    self.openproj_button.grid(row=1,column=1,padx=1, pady=10,sticky="we")
    #positon elements in subrame_1
    self.label1.pack()
    self.project_list_box.pack(fill=tk.BOTH,expand=True,padx = 4,pady=4)
    self.label.grid(row=0)
    self.subframe_1.pack(fill=tk.BOTH,expand=True)
    self.subframe_2.pack(fill=tk.BOTH,expand=True)
    self.main_frame.pack(fill=tk.BOTH,expand=True)


  def update_tree_view(self,visual_studio_projects_directory):
    self.project_list_box.delete(*self.project_list_box.get_children())
    self.fill_tree_view(visual_studio_projects_directory)


  def fill_tree_view(self,visual_studio_projects_directory):
    for d in os.listdir(visual_studio_projects_directory):
      path = os.path.join(visual_studio_projects_directory, d)
      if os.path.isdir(path):
        self.project_list_box.insert('','end',d, text = d,image= self.folder_icon )
      elif os.path.isfile(path):
        try:
          filename, extension = path.split(".")
        except ValueError:
          self.project_list_box.insert('','end',d, text = d,image = self.file_icon )
        else:
          if extension == '.exe':
            self.project_list_box.insert('','end',d,text=d,image = self.exec_icon)
          else:
            self.project_list_box.insert('','end',d, text = d,image = self.file_icon)

  def write_selected(self,event):
    item = self.project_list_box.selection()[0]
    text_item = self.project_list_box.item(item,"text")
    self.entry.delete(0,"end")
    self.entry.insert(0, text_item)

  def show_message(self,title,msg,type):
    if type == self.MSG_TYPE.INFO :
      messagebox.showinfo(title,msg)
    elif type == self.MSG_TYPE.ERROR :
      messagebox.showerror(title,msg)

def main():
  app = App()
  app.run()

if __name__ == "__main__":
  main()

