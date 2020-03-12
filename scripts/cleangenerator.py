#! /usr/bin/env python3
"""
* Copyright (c) 2019, Intel Corporation
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included
* in all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
* OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
* THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
* OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
* ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
* OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import os.path as path
from androidbpgenerator import BUILD_DIR, NOVERBOSE


class Main:

    def run(self):
        script = path.dirname(__file__)
        root = path.abspath(path.join(script, "../.."))

        print(("script = " + script))
        print(("root = " + root))

        # remove all intermediate files and building directories
        print("It is removing building directories and intermediate files for Intel-Graphics-Compiler ... ")
        cmd = "rm -rf " + path.join(root, BUILD_DIR) + NOVERBOSE
        cmd += "rm -rf " + path.join(root, "igc") + NOVERBOSE
        cmd += "rm -rf " + path.join(root, "llvm_build") + NOVERBOSE
        cmd += "rm -rf " + path.join(root, "llvm_source") + NOVERBOSE
        cmd += "rm -rf " + path.join(root, "llvm_patches") + NOVERBOSE
        os.system(cmd)

        print("Done ! ")
        

m = Main()
m.run()