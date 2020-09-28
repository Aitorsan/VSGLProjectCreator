import shutil
import os
from argparse import ArgumentParser
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from urllib import request
import zipfile

# this script dowloads, builds and install glfw and glew.In windows you will need to start a vcvarsall.bat sesion with
# the desire configuration x64 or x32 bit and launch the script from that terminal. The reason is because cmake will
# look for the compiler so the windows build enviroment must be prepare that means set or the enviroments and so on
# if no it will fail to build the libraries. Currently builds the shared libraries
# There is no current support for linux at the moment
class DependencyLoader:
    #this links can be change for updated ones when a new version is available
    download_link_glfw = 'https://github.com/glfw/glfw/releases/download/3.3.2/glfw-3.3.2.zip'
    download_link_glew = 'https://sourceforge.net/projects/glew/files/glew/2.1.0/glew-2.1.0.zip/download'
    glew_str = 'glew'
    glfw_str = 'glfw'
    # this must be match the dowloaded zip files which will change version most likely and the rest will remain
    glfw_str_zip = 'glfw-3.3.2.zip'
    glew_str_zip = 'glew-2.1.0-win32.zip'
    # this can be conan or other build tools, at the moment I will use nmake for windows but
    # I might plan to port this to my linux machine as well so it is usefull to be able to build
    # in any os independently and choose which build tool I want to use. This is not to be confuse
    # by the build system generator which will always be cmake unless I get to old and there is a better
    # tool in the future
    build_tool = 'nmake'

    # The names of the dlls and .lib files that want to install TODO: add corresponding for linux future?
    glew_dll_debug = 'glew32.dll'
    glew_lib_debug = 'glew32.lib'
    # for realease
    glew_dll_rel= 'mm I dont know bro?'
    glew_lib_rel = 'dont know bro need to check it out'
    
    glfw_dll = 'glfw3.dll'
    glfw_lib = 'glfw3dll.lib'
    # names of the unziped directories
    glewdir_name = []
    glfwdir_name = []

    # provide the folder where the libraries will be downloaded and the directory to be installed
    # I assume both glew and glfw libraries will be place under the same directory
    def __init__(self, dependencies_directory, install_dir):
        self.dependencies_dir = dependencies_directory
        self.install_dir = install_dir
        self.glew_str_version = os.path.join(dependencies_directory, self.glew_str_zip)
        self.glfw_str_version = os.path.join(dependencies_directory, self.glfw_str_zip)

    def download_libs(self):
        # check if the dependencies are there before donwloading them
        glew = request.urlopen(self.download_link_glew)
        glfw = request.urlopen(self.download_link_glfw)
        glew_data = glew.read()
        glfw_data = glfw.read()
        glew_file = open(self.glew_str_version, 'bw')
        glew_file.write(glew_data)
        glew_file.close()
        glfw_file = open(self.glfw_str_version, 'bw')
        glfw_file.write(glfw_data)
        glfw_file.close()
        self.unzip_dependencies(self.dependencies_dir)
        self.remove_zip_files()
    
    def remove_zip_files(self):
        os.remove(self.glfw_str_zip)
        os.remove(self.glew_str_zip)

    def unzip_dependencies(self, directory_to_extract_to):
        with zipfile.ZipFile(self.glfw_str_version, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
        with zipfile.ZipFile(self.glew_str_version, 'r') as zip_ref:
            zip_ref.extractall(directory_to_extract_to)
    # To make this build work, it is important to execute the script from a cmd that have executed the vcvarsall.bat x64
    # This will set up the cl build enviroment for c++, if not cmake will not find the compiler and will fail the build
    def build_glfw(self, build_type, cmake_generator:str = 'NMake Makefiles'):
        self.glfwdir_name = [ item for item in os.listdir(self.dependencies_dir) if item.strip().split('-')[0] == self.glfw_str ]
        old_path = os.getcwd()
        os.chdir(self.glfwdir_name[0])
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
        # assume there is only one glew folder in the directory
        os.chdir(self.glewdir_name[0])
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



def read_file(dir):
    f = open(dir,'r')
    template_file = f.read()
    f.close()
    return template_file

#initialize the tkinter library
root = tk.Tk()
#main top level frame
main_frame = tk.Frame(root,relief=tk.RAISED )
# create 2 subframes
subframe_1 =  tk.LabelFrame(main_frame)
subframe_2 =  tk.LabelFrame(main_frame)
#create the entry for the new project name
entry = tk.Entry(subframe_2)
# global variables
visual_studio_projects_directory = 'C:/Users/aitor/source/repos'
project_name: str = None
folder_icon = None 
file_icon = None
exec_icon = None 
back_dir_icon= None
template_dir = os.path.join(os.getcwd(), 'ProjectTemplate_GL')
icons_dir = os.path.join(os.getcwd(),'icons')
solution_file = read_file(os.path.join(template_dir,'template.sln'))
dir_label_text = tk.StringVar()
curr_dir_label = None
# visual studio project file string template
vcxproj = read_file(os.path.join(template_dir,'template.vcxproj'))
# visual studio filters file template string
vcxproj_filters = read_file(os.path.join(template_dir,'template_filters.vcxproj.filters'))
 # visual studio users file template string
vcxprojuser  = read_file(os.path.join(template_dir,'template_user.vcxproj.user'))
# list of recently created projects. We create a list with the new created projects to
# delete. The reason of that is to protect deliting existing projects that have not
# been created in the current sesion. It could be usefull to delte projects old projects from
# the tool but this is a bit dangerous and I don't want to delete projects by accident
new_created_projects = []

# we save the directory where the script was launched because we will chande directories
# and we need to know the python scrip directory to load images or go back where we started
app_launch_dir = os.getcwd()

# create list box with a new style to avoid icon overlaping
s = ttk.Style()
s.configure('treeStyle.Treeview', rowheight=40)
project_list_box = ttk.Treeview(subframe_1, height=4, style='treeStyle.Treeview')

#change select mode to not allow multiple selection of items
project_list_box.config(selectmode='browse')
# configure the heigh of the tree
project_list_box.config(height=10)

def update_tree_view():
	project_list_box.delete(*project_list_box.get_children())
	fill_tree_view(visual_studio_projects_directory)	
#callbacks
def current_selected_items_callback(visual_studio_projects_directory):
  #global visual_studio_projects_directory
  item = project_list_box.selection()[0]
  text_item = project_list_box.item(item,"text")
  if os.path.isdir(os.path.join(visual_studio_projects_directory,text_item)):
    entry.delete(0,"end")
    entry.insert(0, text_item)
    os.chdir(os.path.join(visual_studio_projects_directory,text_item))
    visual_studio_projects_directory = os.getcwd() 
    dir_label_text.set(visual_studio_projects_directory)
    update_tree_view()
  else:
    open_file(text_item)

def write_selected(event):
  item = project_list_box.selection()[0]
  text_item = project_list_box.item(item,"text")
  entry.delete(0,"end")
  entry.insert(0, text_item)

def open_file(file):
   file_to_open = os.path.join(visual_studio_projects_directory,file)
   os.system('"%s"'% file_to_open)
 

def create_solution_file(project_name):
    global solution_file
    solution_file_extension = '.sln'
    file_content = solution_file.replace('project_name',project_name)
    with open(project_name+solution_file_extension, 'w') as f:
        f.write(file_content)


def create_project_file(project_name):
    global vcxproj
    vcxproj_file_extension = '.vcxproj'
    file_content = vcxproj.replace('project_name', project_name)
    with open(project_name+vcxproj_file_extension, 'w') as f:
        f.write(file_content)


def create_project_filters(project_name):
    global vcxproj_filters
    vcxproj_filters_file_extension = '.vcxproj.filters'
    with open(project_name+vcxproj_filters_file_extension, 'w') as f:
        f.write(vcxproj_filters)


def create_project_user(project_name):
    global vcxprojuser
    vcxproj_usr_file_extension = '.vcxproj.user'
    with open(project_name+vcxproj_usr_file_extension, 'w') as f:
        f.write(vcxprojuser)

# open the created project
def open_visual_studio():
  open_project = entry.get()
  if len(open_project) == 0 :
    tk.messagebox.showerror("project not found","select a project to open!")
  else:
    project_folder = os.path.join(visual_studio_projects_directory,open_project)
    solution_file = os.path.join(project_folder,open_project+'.sln')
    os.system('"%s"'% solution_file)

#delete selected project
def delete_project():
  delete_project = entry.get()
  can_be_deleted = False
  for project in new_created_projects:
    if project == delete_project:
      can_be_deleted = True
      break
  if can_be_deleted:
    shutil.rmtree(os.path.join(visual_studio_projects_directory,delete_project))
    messagebox.showinfo("Project Deleted","open gl project: "+ project_name + " has been deleted")
    # remove item from the list from the list
    new_created_projects.remove(delete_project)
    # update tree view
    update_tree_view(visual_studio_projects_directory)
  else:
    messagebox.showerror("Delete Error", "you can't delete projects that \nhave not being created in this session for safety reasons!")


# create an openGL project with the given name
def create_project():
    #loader = download.DependencyLoader(os.getcwd(), '.')
   
    global project_name
    project_name = entry.get()
    os.chdir(visual_studio_projects_directory)
    # create solution directory in the folder where all visual studio projects are by default
    os.makedirs(os.path.join(project_name, 'Debug'))
    # cd into this directory
    os.chdir(project_name)
    # create solution file
    create_solution_file(project_name)
    # copy the template folders, files and create the project directory
    shutil.copytree(template_dir, os.path.join(os.getcwd(),project_name))
    # cd into project file
    os.chdir(project_name)
    # create all the files
    create_project_file(project_name)
    create_project_user(project_name)
    create_project_filters(project_name)
    # move the libs to ../Debug folder
    shutil.move('glew32d.dll', '../Debug')
    shutil.move('glfw3.dll', '../Debug')
    messagebox.showinfo("Prject created","open gl project:"+ project_name+ " succesfully created")
    project_list_box.delete(*project_list_box.get_children())
    fill_tree_view(visual_studio_projects_directory)
    global new_created_projects
    new_created_projects.append(project_name)
    os.chdir(visual_studio_projects_directory)


def change_vsprojects_dir():
  global visual_studio_projects_directory	
  visual_studio_projects_directory = filedialog.askdirectory(initialdir = visual_studio_projects_directory, title="Select project directory")
  update_tree_view(visual_studio_projects_directory)
  os.chdir(visual_studio_projects_directory)
  dir_label_text.set(visual_studio_projects_directory)

def load_icons():
  size = 35,35
  global folder_icon
  global file_icon
  global exec_icon
  global back_dir_icon
  folder_icon_path = os.path.join(icons_dir,"ficon.png")
  photo_folder = Image.open(folder_icon_path)
  folder_icon = ImageTk.PhotoImage(photo_folder)
  # file icon
  file_icon_path = os.path.join(icons_dir,"file.png")
  photo_file = Image.open(file_icon_path).resize(size,Image.ANTIALIAS)
  file_icon = ImageTk.PhotoImage(photo_file)
  # exec icon
  exec_icon_path = os.path.join(icons_dir,"exec.png")
  photo_exec = Image.open(exec_icon_path).resize(size,Image.ANTIALIAS)
  exec_icon = ImageTk.PhotoImage(photo_exec)
  # back dir icon
  back_icon_path = os.path.join(icons_dir,"backdir.png")
  back_folder = Image.open(back_icon_path).resize(size,Image.ANTIALIAS)
  back_dir_icon = ImageTk.PhotoImage(back_folder)

def fill_tree_view(visual_studio_projects_directory):
    for d in os.listdir(visual_studio_projects_directory):
      path = os.path.join(visual_studio_projects_directory, d)
      if os.path.isdir(path):
        project_list_box.insert('','end',d, text = d,image= folder_icon )
      elif os.path.isfile(path):
        try:
          filename, extension = path.split(".")
        except ValueError:
           project_list_box.insert('','end',d, text = d,image = file_icon )
        else:
          if extension == '.exe':
            project_list_box.insert('','end',d,text=d,image = exec_icon)
          else:
            project_list_box.insert('','end',d, text = d,image = file_icon )

def select_build_type(event):
      pass

def back_directory():
      global visual_studio_projects_directory
      os.chdir('..')
      visual_studio_projects_directory = os.getcwd()
      update_tree_view()
      dir_label_text.set(visual_studio_projects_directory)

def run_gui_app():
  global visual_studio_projects_directory
  global curr_dir_label
  root.title('VS openGl project creator ')
  root.geometry("300x600")
  root.minsize(600,600)
  root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=os.path.join(icons_dir,"opengl.png")))
  root.resizable(True,True)
  #create and config menu
  menu = tk.Menu(root)
  root.config(menu = menu)
  
  #create menu items
  options = tk.Menu(menu) 
  menu.add_cascade(label="options", menu = options)
  options.add_command(label = "change project directory", command = change_vsprojects_dir)

  label1 = tk.Label(subframe_1, text="vs projects list")
  global dir_label_text
  dir_label_text.set(visual_studio_projects_directory)
  curr_dir_label = tk.Label(subframe_1,textvariable = dir_label_text, text = visual_studio_projects_directory,width = 100)
  curr_dir_label.pack(anchor='ne',padx=50)
  label = tk.Label(subframe_2, text="Project name")
  label.grid(row = 0, column=0)
  # set tree view callbacks and fill in the tree
  project_list_box.bind('<Double-1>',lambda x: current_selected_items_callback(visual_studio_projects_directory))
  project_list_box.bind('<<TreeviewSelect>>',write_selected )
  fill_tree_view(visual_studio_projects_directory)
  # create buttons
  delete_button = tk.Button(subframe_2,text="Delete", command = delete_project)
  create_button = tk.Button(subframe_2, text = "Create", command= create_project)
  openproj_button = tk.Button(subframe_2, text = "Open", command = open_visual_studio)
  back_button = tk.Button(subframe_1,image = back_dir_icon, command = back_directory)
  back_button.pack(anchor="nw")
  # create comboBox for choosing build type
  build_options =[
    'Debug',
    'Release'
  ]
  build_type_combo_box = ttk.Combobox(subframe_2,value = build_options,state = 'readonly')
  build_type_combo_box.current(0)
  build_type_combo_box.bind("<<ComboboxSelected>>", select_build_type)
  build_type_combo_box.grid(row=0,column = 3, sticky = "we")

  #position elements in subrame_2
  entry.grid(row = 0, column = 2,sticky="we")
  delete_button.grid(row=1,column=0, padx=2,pady=10,sticky="we")
  create_button.grid(row= 1, column= 2,padx=2, pady=10,sticky="we")
  openproj_button.grid(row=1,column=1,padx=1, pady=10,sticky="we")
  #positon elements in subrame_1
  label1.pack()
  project_list_box.pack(fill=tk.BOTH,expand=True,padx = 4,pady=4)

  label.grid(row=0)
  subframe_1.pack(fill=tk.BOTH,expand=True)
  subframe_2.pack(fill=tk.BOTH,expand=True)
  main_frame.pack(fill=tk.BOTH,expand=True)
  root.mainloop()


def main():
  load_icons()
  run_gui_app()

if __name__ == "__main__":
  main()
  

