import os
import glob
import torch
from platform import system
from setuptools import find_packages, setup
from torch.utils.cpp_extension import CUDAExtension, CppExtension, BuildExtension

SYSTEM = system()

remesh_root_path = os.getcwd() + "/iso_remesh/Cpp/"
remesh_lib_path = os.getcwd() + "/iso_remesh/Lib/"
remesh_src_path = remesh_root_path + "src/"
remesh_sources = glob.glob(remesh_src_path + "*.cpp")
remesh_include_dirs = [
    remesh_root_path + "include",
    remesh_lib_path + "eigen",
    remesh_lib_path + "libigl/include",
]

remesh_extra_compile_args = [
    "-O3",
    "-DCMAKE_BUILD_TYPE=Release",
    "-D_GLIBCXX_USE_CXX11_ABI=0",
    "-DTORCH_USE_CUDA_DSA",
]

if SYSTEM == "Darwin":
    remesh_extra_compile_args.append("-std=c++17")
elif SYSTEM == "Linux":
    remesh_extra_compile_args.append("-std=c++17")

if torch.cuda.is_available():
    cc = torch.cuda.get_device_capability()
    arch_str = f"{cc[0]}.{cc[1]}"
    os.environ["TORCH_CUDA_ARCH_LIST"] = arch_str

    remesh_sources += glob.glob(remesh_src_path + "*.cu")

    extra_compile_args = {
        "cxx": remesh_extra_compile_args
        + [
            "-DUSE_CUDA",
            "-DTORCH_USE_CUDA_DSA",
        ],
        "nvcc": [
            "-O3",
            "-Xfatbin",
            "-compress-all",
            "-DUSE_CUDA",
            "-std=c++17",
            "-DTORCH_USE_CUDA_DSA",
        ],
    }

    remesh_module = CUDAExtension(
        name="remesh_cpp",
        sources=remesh_sources,
        include_dirs=remesh_include_dirs,
        extra_compile_args=extra_compile_args,
    )

else:
    remesh_module = CppExtension(
        name="remesh_cpp",
        sources=remesh_sources,
        include_dirs=remesh_include_dirs,
        extra_compile_args=remesh_extra_compile_args,
    )

setup(
    name="REMESH-CPP",
    version="1.0.0",
    author="Changhao Li",
    packages=find_packages(),
    ext_modules=[remesh_module],
    cmdclass={"build_ext": BuildExtension},
    include_package_data=True,
)
