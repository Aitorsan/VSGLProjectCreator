from urllib import request
import os
import zipfile
import shutil
import time
import argparse
import re
import subprocess
# this script dowloads, builds and install glfw and glew.In windows you will need to start a vcvarsall.bat sesion with
# the desire configuration x64 or x32 bit and launch the script from that terminal. The reason is because cmake will
# look for the compiler so the windows build enviroment must be prepare that means set or the enviroments and so on
# if no it will fail to build the libraries. Currently builds the shared libraries
# There is no current support for linux at the moment
class DependencyManager:
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

 
    def install_glew(self):
        # install glew in its place
        if not self.glewdir_name:
            self.glewdir_name = [ item for item in os.listdir(self.dependencies_dir) if item.strip().split('-')[0] == self.glew_str ]

        top_level_dir = os.path.join(self.glewdir_name[0],'build')
        src_subdir = os.path.join(top_level_dir,'cmake')
        dll_dir = os.path.join(src_subdir,'bin')
        lib_dir = os.path.join(src_subdir,'lib')
        print('DLL dir:')
        print(dll_dir)
        print('LIB dir:')
        print(lib_dir)
        shutil.copy(os.path.join(dll_dir,self.glew_dll_debug),self.install_dir)
        shutil.copy(os.path.join(lib_dir,self.glew_lib_debug),self.install_dir)
        shutil.copy(os.path.join(self.install_dir,self.glew_dll_debug),'../')
        
    
    def install_glfw(self,build_type):
        print(os.getcwd())
        if not self.glfwdir_name:
            self.glfwdir_name = [ item for item in os.listdir(self.dependencies_dir) if item.strip().split('-')[0] == self.glfw_str ]
        print('GLFW:')
        libs_dir = os.path.join(self.glfwdir_name[0],build_type)
        libs_dir = os.path.join(libs_dir,'src')
        shutil.copy(os.path.join(libs_dir,self.glfw_dll), self.install_dir)
        shutil.copy(os.path.join(libs_dir,self.glfw_lib), self.install_dir)
        shutil.copy(os.path.join(self.install_dir,self.glfw_dll),'../')
       

    def find_dep(self,dep_name):
        pattern = re.compile(r''.join(dep_name))
        list_dirs = [ item for item in os.listdir(self.dependencies_dir)]
        matches_it = pattern.finditer(' '.join(list_dirs))

        if all(False for _ in matches_it):
            return False
        else:
            return True

    def download_lib(self, name,lib_zip):
        print("----> Downloading {}.....".format(name))
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

    def build_glew(self, cmake_generator:str = 'NMake Makefiles'):
        self.glewdir_name = [ item for item in os.listdir(self.dependencies_dir) if item.strip().split('-')[0] == self.glew_str ]
        old_path = os.getcwd()
        print(old_path)
        # assume there is only one glew folder in the directory
        os.chdir(self.glewdir_name[0])
        # I assume they will keep this cmake folder in the package, if glew changes the way it build
        # with cmake then this should be updated
        os.chdir(os.path.join('build','cmake'))
        cmake_cmd = 'cmake . -G "{}"'.format(cmake_generator)
        os.system(cmake_cmd)
        os.system('nmake')
        # restore the path
        os.chdir(old_path)

    # To make this build work, it is important to execute the script from a cmd that have executed the vcvarsall.bat x64
    # This will set up the cl build enviroment for c++, if not cmake will not find the compiler and will fail the build
    def build_glfw(self, build_type, cmake_generator:str = 'NMake Makefiles'):
        self.glfwdir_name = [ item for item in os.listdir(self.dependencies_dir) if item.strip().split('-')[0] == self.glfw_str ]
        os.chdir(os.path.join(self.dependencies_dir, self.glfwdir_name[0]))
        # create out dir build tree. Build stuff in a folder with the name of the build type
        os.mkdir(build_type)
        os.chdir(build_type)
        cmake_cmd = 'cmake -G "{}" -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE={} -DGLFW_BUILD_TESTS=ON -DGLFW_BUILD_EXAMPLES=ON ..'.format(cmake_generator,build_type)
        os.system(cmake_cmd)
        os.system(self.build_tool)
        # restore the path
        os.chdir(self.dependencies_dir)
    
def parse_args():
   
    parser = argparse.ArgumentParser(description="depency build parameters")
    parser.add_argument('-b','--build_type',type=str ,metavar='',help='build type Debug or Release')
    parser.add_argument('-t','--build_tool', type=str,metavar='',help='NMake, make, VS')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    old_path = os.getcwd()

    b_type = 'Debug'
    b_tool = 'NMake Makefiles'
   
    if args.build_type:
        b_type = args.build_type

    if args.build_tool :
        b_tool = args.build_tool
    curr_dir = os.path.join(os.getcwd(),'ProjectTemplate_GL')
    curr_dir = os.path.join(curr_dir,'dependencies')
    os.chdir(curr_dir)
    dependency_manager = DependencyManager(curr_dir,'../lib')
    # Check if the library is already there
    if not dependency_manager.find_dep('glfw'):
        print("---> glfw not found...")
        dependency_manager.download_lib(DependencyManager.download_link_glfw,DependencyManager.glfw_str_zip)
        print("---> Building glfw...")
        dependency_manager.build_glfw(b_type,b_tool)

    if not dependency_manager.find_dep('glew'):
        print("---> glew not found...")
        dependency_manager.download_lib(DependencyManager.download_link_glew,DependencyManager.glew_str_zip)       
        print("---> Building glew...")
        dependency_manager.build_glew(b_tool)
        print(' Dependencies sucessfully build ')


    # Install librariers
    dependency_manager.install_glew()
    dependency_manager.install_glfw(b_type)
    os.chdir(old_path)

  
