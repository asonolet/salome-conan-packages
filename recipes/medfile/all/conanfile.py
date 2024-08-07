from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import get


class MedRecipe(ConanFile):
    name = "medfile"
    version = "4.1.1"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "parallel": [True, False],
        "is_32bit": [True, False],
    }
    default_options = {
        "shared": True,
        "fPIC": True,
        "parallel": False,
        "is_32bit": False,
    }

    # Sources are located in the same place as this recipe, copy them to the recipe
    # exports_sources = "CMakeLists.txt", "src/*", "include/*", "config/cmake_files/*", "tools/*", "tests/*", "doc/*"

    def source(self):
        # get(self, "https://files.salome-platform.org/Salome/medfile/med-4.1.1.tar.gz", strip_root=True)
        print(self.conan_data)
        get(self, **self.conan_data["sources"][self.version])

    def requirements(self):
        self.requires("hdf5/1.10.5")
        if self.options.parallel:
            self.requires("openmpi/4.1.0")

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.24]")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        if self.options.is_32bit:
            tc.cache_variables["MED_MEDINT_TYPE"] = "int"
        else:
            tc.cache_variables["MED_MEDINT_TYPE"] = "long"
        tc.cache_variables["MEDFILE_INSTALL_DOC"] = False
        tc.cache_variables["MEDFILE_USE_MPI"] = self.options.parallel
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