from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps


class MedRecipe(ConanFile):
    name = "medfile"
    version = "4.1.1"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}

    # Sources are located in the same place as this recipe, copy them to the recipe
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "config/cmake_files/*", "tools/*", "tests/*", "doc/*"

    def requirements(self):
        self.requires("hdf5/1.10.5")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.cache_variables["MED_MEDINT_TYPE"] = "long"
        tc.cache_variables["MEDFILE_INSTALL_DOC"] = False
        tc.cache_variables["MEDFILE_USE_MPI"] = False
        tc.cache_variables["CMAKE_Fortran_COMPILER"] = ""
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["medC", "medimport"]
