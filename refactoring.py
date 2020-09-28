import shutil
import os
import re
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


def open_file(file,visual_studio_projects_directory):
    file_to_open = os.path.join(visual_studio_projects_directory,file)
    os.system('"%s"'% file_to_open)

def read_file(dir):
    f = open(dir,'r')
    template_file = f.read()
    f.close()
    return template_file

app_logger = logging.getLogger(__name__)

class QueueHandler(logging.Handler):
    
    def __init_(self,log_queue):
      super.__init__()
      self.log_queue = log_queue

    def emit(self,msg):
      self.log_queue.put(msg)



class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        app_logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)

# DependcyLoader, builds and install glfw and glew.In windows you will need to start a vcvarsall.bat sesion with
# the desire configuration x64 or x32 bit and launch the script from that terminal. The reason is because cmake will
# look for the compiler so the windows build enviroment must be prepare that means set or the enviroments and so on
# if no it will fail to build the libraries. Currently builds the shared libraries
# There is no current support for linux at the moment
class DependencyLoader:
    # provide the folder where the libraries will be downloaded and the directory to be installed
    # I assume both glew and glfw libraries will be place under the same directory
    def __init__(self, dependencies_directory, install_dir):
        # this links can be change for updated ones when a new version is available
        self.download_link_glfw = 'https://github.com/glfw/glfw/releases/download/3.3.2/glfw-3.3.2.zip'
        self.download_link_glew = 'https://sourceforge.net/projects/glew/files/glew/2.1.0/glew-2.1.0.zip/download'
        self.glew_str = 'glew'
        self.glfw_str = 'glfw'
        # this must be match the dowloaded zip files which will change version most likely and the rest will remain
        self.glfw_str_zip = 'glfw-3.3.2.zip'
        self.glew_str_zip = 'glew-2.1.0-win32.zip'
        self.build_tool = 'nmake'
        # The names of the dlls and .lib files that want to install TODO: add corresponding for linux future?
        self.glew_dll_debug = 'glew32.dll'
        self.glew_lib_debug = 'glew32.lib'
        self.glfw_dll = 'glfw3.dll'
        self.glfw_lib = 'glfw3dll.lib'
        # names of the unziped directories
        self.glewdir_name = []
        self.glfwdir_name = []
        self.dependencies_dir = dependencies_directory
        self.install_dir = install_dir
        self.glew_str_version_zip = os.path.join(dependencies_directory, self.glew_str_zip)
        self.glfw_str_version_zip = os.path.join(dependencies_directory, self.glfw_str_zip)

    def donwload_and_build_deps_ifnot_exist(self,controller,build_type):
        glew_pattern = re.compile(r'glew')
        glfw_pattern = re.compile(r'glfw')
        print("current dir:")
        print(os.getcwd())
        list_dirs = [ item for item in os.listdir(self.dependencies_dir)]
        glew_matches_it = glew_pattern.finditer(' '.join(list_dirs))
        glfw_matches_it = glfw_pattern.finditer(' '.join(list_dirs))

        if all(False for _ in glew_matches_it):
             self.download_lib(self.download_link_glew,self.glew_str_version_zip)
             self.build_glew()
             controller.app.show_console_out()

        if all(False for _ in glfw_matches_it):
            self.download_lib(self.download_link_glfw,self.glfw_str_version_zip)
            self.build_glfw(build_type)
            controller.app.show_console_out()

    def download_lib(self, name,lib_zip):
        # check if the dependencies are there before donwloading them
        download_zip = request.urlopen(name)
        lib_data = download_zip.read()
        file = open(lib_zip, 'bw')
        file.write(lib_data)
        file.close()
        self.unzip_dependencies(self.dependencies_dir,lib_zip)
        os.remove(lib_zip)

    def unzip_dependencies(self, directory_to_extract_to,lib_zip):
        with zipfile.ZipFile(lib_zip, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)

    # To make this build work, it is important to execute the script from a cmd that have executed the vcvarsall.bat x64
    # This will set up the cl build enviroment for c++, if not cmake will not find the compiler and will fail the build
    def build_glfw(self, build_type, cmake_generator:str = 'NMake Makefiles'):
        self.glfwdir_name = [ item for item in os.listdir(self.dependencies_dir) if item.strip().split('-')[0] == self.glfw_str ]
        old_path = os.getcwd()
        dir_to_change = os.path.join('ProjectTemplate_GL','dependencies')
        os.chdir(os.path.join(dir_to_change, self.glfwdir_name[0]))
        # create out dir build tree. Build stuff in a folder with the name of the build type
        os.makedirs(build_type)
        os.chdir(build_type)
        cmake_cmd = 'cmake -G "{}" -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE={} -DGLFW_BUILD_TESTS=ON -DGLFW_BUILD_EXAMPLES=ON ..'.format(cmake_generator,build_type)
        os.system(cmake_cmd)
        os.system(self.build_tool)
        # restore the path
        os.chdir(old_path)

    def build_glew(self, cmake_generator:str = 'NMake Makefiles'):
        self.glewdir_name = [ item for item in os.listdir(self.dependencies_dir) if item.strip().split('-')[0] == self.glew_str ]
        old_path = os.getcwd()
        dir_to_change = os.path.join('ProjectTemplate_GL','dependencies')
        # assume there is only one glew folder in the directory
        os.chdir(os.path.join(dir_to_change,self.glewdir_name[0]))
        # I assume they will keep this cmake folder in the package, if glew changes the way it build
        # with cmake then this should be updated
        os.chdir(os.path.join('build','cmake'))
        cmake_cmd = 'cmake . -G "{}"'.format(cmake_generator)
        os.system(cmake_cmd)
        os.system(self.build_tool)
        # restore the path
        os.chdir(old_path)

    def install_glew(self):
        # install glew in its place
        top_level_dir = os.path.join(self.glewdir_name[0],'build')
        src_subdir = os.path.join(top_level_dir,'cmake')
        dll_dir = os.path.join(src_subdir,'bin')
        lib_dir = os.path.join(src_subdir,'lib')
        shutil.copy(os.path.join(dll_dir,self.glew_dll_debug),self.install_dir)
        shutil.copy(os.path.join(lib_dir,self.glew_lib_debug),self.install_dir)

    def install_glfw(self,build_type):
        # install glfw in its place
        pass

#/////////////////////////////////////////////////////////////
# Project builder is somehow the model contains the data and
# the actions to build a visual studio project
#///////////////////////////////////////////////////////////
class ProjectBuilder:

  def __init__(self,controller):
    self.project_name = 'ProjectTemplate_GL'
    self.dependency_manager = DependencyLoader(os.path.join(self.project_name,'dependencies'), os.path.join(self.project_name,'lib'))
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
    self.set_up_dependencies(build_type)
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

    # move the libs to ../Debug folder
    shutil.move('glew32d.dll', '../Debug')
    shutil.move('glfw3.dll', '../Debug')

    self.new_created_projects.append(project_name)
    os.chdir(self.visual_studio_projects_directory)

  def set_up_dependencies(self,build_type):
      self.dependency_manager.donwload_and_build_deps_ifnot_exist(self.controller,build_type)


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
      for project in new_created_projects:
        if project == delete_project:
          can_be_deleted = True
          break
      if can_be_deleted :
        shutil.rmtree(os.path.join(self.visual_studio_projects_directory,delete_project))
        # remove item from the list of all new created projects
        new_created_projects.remove(delete_project)
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

  def create_project(self):
    project_name = self.app.entry.get()
    self.project_builder.create_project(project_name,self.app.build_type_combo_box.get())
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
    self.console = ConsoleUi(subframe_2)
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
    self.create_button = tk.Button(self.subframe_2, text = "Create", command= self.app_controller.create_project)
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

  def show_console_out(self):
    top = tk.Toplevel()
    console_out_window = ConsoleUi(top)
    console_out_window.display("testing")




def main():
  app = App()
  app.run()

if __name__ == "__main__":
  main()

