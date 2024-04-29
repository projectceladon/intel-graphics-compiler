# Intel® Graphics Compiler for OpenCL™ - Build Instructions for Celadon

For Celadon, there are already one copy of llvm and its related libraries, but the version is too old and IGC needs to link with the latest one. While we have no plan to change IGC and llvm code a lot or frequently, additionally compiling IGC and LLVM on Celadon are complex and time consuming, so we decided to only upload prebuilt libraries to Celadon.

While if you want to compile or try different verison of IGC/LLVM by yourself, can refer to the following steps:

## 1. Prerequisite

### 1.1 Ubuntu 22.04
Using Ubuntu 22.04 as development environment.

Follow https://github.com/intel/intel-graphics-compiler/blob/master/documentation/build_ubuntu.md to setup ubuntu build environment, make sure subproject lock on the release version

### 1.2 Android NDK
IGC is prebuilt on the ubuntu host and NDK is needed for cross-compiling for android. Download Android NDK (r25c) and unzip it.

## 2. Build IGC on Ubuntu 22.04
We need produce some intermediate files generated during cmake/make in Ubuntu, which are necessary for Celadon compiling.
Build native igc library firstly as following cmake command: 
```shell
$ export IGC_WS={the IGC workspace path}
$ cmake -DCMAKE_BUILD_TYPE=Release \
$      -DLLVM_BUILD_TYPE=Release \
$      -DIGC_BUILD__VC_ENABLED=OFF \  // disable vector compiler module due to not needed for OCL
$      -DCMAKE_INSTALL_PREFIX="$IGC_WS/install_native" \
$      -B build_native $IGC_WS/igc/
$ cd build_native && make -j$(nproc)
```
After native igc built successfully, build android igc 64 bit version by following cmake command:
```shell
$ cmake -DCMAKE_BUILD_TYPE=Release \
$      -DIGC_BUILD__VC_ENABLED=OFF \
$      -DCMAKE_TOOLCHAIN_FILE={android-ndk-r25c install path}/build/cmake/android.toolchain.cmake \
$      -DANDROID_ABI=x86_64 \
$      -DANDROID_PLATFORM=android-33 \  // according to target android os
$      -DANDROID_STL=c++_static \
$      -DCMAKE_FIND_ROOT_PATH_MODE_INCLUDE=BOTH \
$      -DLLVM_TABLEGEN="$IGC_WS/build_native/IGC/llvm-deps/build/src/bin/llvm-tblgen" \
$      -DCLANG_TABLEGEN="$IGC_WS/build_native/IGC/llvm-deps/build/src/bin/clang-tblgen" \
$      -DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-unknown-linux-android \
$      -DCMAKE_INSTALL_PREFIX="$IGC_WS/install" \
$      -B build_android $IGC_WS/igc/
$ cd build_android && make -j$(nproc)
```


