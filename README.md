# Intel® Graphics Compiler for OpenCL™ - Build Instructions for Celadon

For Celadon, there are already one copy of llvm and its related libraries, but the version is too old and IGC needs to link with the latest one. While we have no plan to change IGC and llvm code a lot or frequently, additionally compiling IGC and LLVM on Celadon are complex and time consuming, so we decided to only upload prebuilt libraries to Celadon.

While if you want to compile or try different verison of IGC/LLVM by yourself, can refer to the following steps:

## 1. Prerequisite

### 1.1 Ubuntu 16.04
Using Ubuntu 16.04 as development environment.

Building IGC on Ubuntu needs flex, bison, libz, git and cmake version at least 3.4.3. You can install the required packages on Ubuntu using this command: 
```shell
$ sudo apt-get install flex bison libz-dev git cmake 
```

### 1.2 Celadon Q
We need clone Celadon Q latest source code, please refer to the documents under https://01.org/projectceladon/documentation/getting_started.

For building IGC on the project of Celadon, our workspace tree may look like this:
```
<Celadon>
      |- hardware
            |- intel
                  |- external
                        |- <workspace: opencl>
```

## 2. Clone Source Code
In this step you need to prepare LLVM, OpenCL-Clang libraries and Clang for IGC.

### 2.1 Download all dependencies and create the workspace folder for opencl as below:
```
<workspace: opencl>
      |- intel-graphics-compiler
      |- igc
      |- llvm_patches
      |- llvm_source
            |- projects/opencl-clang
            |- projects/llvm-spirv
            |- tools/clang
```

### 2.2 Clone IGC Source Code
You can use the following commands:
```shell
$ cd <workspace>
$ git clone http://github.com/intel/intel-graphics-compiler igc
$ cd igc && git checkout b0409b893508e55d9548a1d6658788e7cd9963bd
```

### 2.3 Clone LLVM Source Code
You can use the following commands:
```shell
$ cd <workspace>
$ git clone -b release_70 http://github.com/llvm-mirror/llvm llvm_source
$ cd llvm_source && git checkout dd3329aeb25d87d4ac6429c0af220f92e1ba5f26
$ cd <workspace>
$ git clone -b release_70 http://github.com/llvm-mirror/clang llvm_source/tools/clang
$ cd llvm_source/tools/clang && git checkout 4519e2637fcc4bf6e3049a0a80e6a5e7b97667cb
$ cd <workspace>
$ git clone -b ocl-open-70 http://github.com/intel/opencl-clang.git llvm_source/projects/opencl-clang
$ cd llvm_source/projects/opencl-clang && git checkout 6257ffe137a2c8df95a3f3b39fa477aa8ed15837
$ cd <workspace>
$ git clone -b llvm_release_70 http://github.com/KhronosGroup/SPIRV-LLVM-Translator.git llvm_source/projects/llvm-spirv
$ cd llvm_source/projects/llvm-spirv && git checkout 8ce6443ec1020183eafaeb3410c7d1edc2355dc3
$ cd <workspace>
$ git clone http://github.com/intel/llvm-patches llvm_patches
$ cd llvm_patches && git checkout 3d4449ff6f8ae8b8f1f4258c36a57f77f9ca8491
```

Make sure to specify correct branch for desired version. In this example we use LLVM7/Clang7.

## 3. Build IGC on Ubuntu 16.04
We need produce some intermediate files generated during cmake/make in Ubuntu, which are necessary for Celadon compiling.
Please use the following compiling commands:
```shell
$ cd <workspace>
$ mkdir build_igc; cd build_igc
$ cmake ../igc/IGC
$ make -j$(nproc)  
```

## 4. Build IGC on Celadon Q

### 4.1 Prepare workspace
If you are using [Clone Source Code](#2-clone-source-code) method, IGC will automatically build all dependencies (provided that the workspace structure is preserved) and link statically to LLVM and OpenCL Clang.

You can use the following commands to build IGC:
```shell
$ cd <workspace>/intel-graphics-compiler
$ cp -rf bp ../igc
$ cp -rf patches ../igc
$ cp -rf scripts ../igc
$ cd ../igc/scripts
$ python3 ./intelgraphicscompilergenerator.py
$ [Then, it will take some time to generate some bp files for compiling LLVM and IGC.]
$ 
$ cd <Celadon>
$ source build/envsetup.sh
$ lunch celadon_tablet-userdebug
$ mmm <workspace>/llvm_build -j$(nproc)
$ [compile LLVM firstly]
$ mmm <workspace>/igc -j$(nproc)
```
After compiling succeed, push libigc.so, libigdfcl.so and libcommon_clang.so to device.

### 4.2 Clean IGC's compilation on Celadon:
You can use the following commands to clean:
```shell
$ cd <workspace>/igc/scripts
$ python3 ./cleangenerator.py
$ [It will remove all folders of building, igc, llvm_source, llvm_build, and llvm_patches.]
```
