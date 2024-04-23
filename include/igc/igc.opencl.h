/*========================== begin_copyright_notice ============================

Copyright (C) 2018-2021 Intel Corporation

SPDX-License-Identifier: MIT

============================= end_copyright_notice ===========================*/

#ifndef IGC_OPENCL_H
#define IGC_OPENCL_H

#if defined(_WIN64)
  #define IGC_LIBRARY_NAME "igc64.dll"
  #define FCL_LIBRARY_NAME "igdfcl64.dll"
#elif defined(_WIN32)
  #define IGC_LIBRARY_NAME "igc32.dll"
  #define FCL_LIBRARY_NAME "igdfcl32.dll"
#elif defined(ANDROID)
  #define IGC_LIBRARY_NAME "libigc.so"
  #define FCL_LIBRARY_NAME "libigdfcl.so"
#else
  #define IGC_LIBRARY_NAME "libigc.so.1"
  #define FCL_LIBRARY_NAME "libigdfcl.so.1"
#endif

#endif // IGC_OPENCL_H
