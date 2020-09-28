from urllib import request
import os
import zipfile
import shutil
import time

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



loader = DependencyLoader(os.getcwd(), '.')
print("downloading libs")
time.sleep(0.1)
loader.download_libs()

loader.build_glfw('Debug')
loader.build_glew()
loader.install_glew()
