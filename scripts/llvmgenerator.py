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
import re
from androidbpgenerator import INDENT, CCDefaults, ModuleInfo, Generator, NOVERBOSE, BUILD_DIR

# suffix 'Ocl' at end of every module in LLVM
UPDATE_STATIC = {"libclangBasic" : "libclangBasicOcl",
    "libclangCodeGen" : "libclangCodeGenOcl",
    "libclangDriver" : "libclangDriverOcl",
    "libclangFrontend" : "libclangFrontendOcl",
    "libclangFrontendTool" : "libclangFrontendToolOcl",
    "libclangRewriteFrontend" : "libclangRewriteFrontendOcl",
    "libclangARCMigrate" : "libclangARCMigrateOcl",
    "libclangStaticAnalyzerFrontend" : "libclangStaticAnalyzerFrontendOcl",
    "libclangStaticAnalyzerCheckers" : "libclangStaticAnalyzerCheckersOcl",
    "libclangStaticAnalyzerCore" : "libclangStaticAnalyzerCoreOcl",
    "libclangCrossTU" : "libclangCrossTUOcl",
    "libclangIndex" : "libclangIndexOcl",
    "libclangParse" : "libclangParseOcl",
    "libclangSerialization" : "libclangSerializationOcl",
    "libclangSema" : "libclangSemaOcl",
    "libclangAnalysis" : "libclangAnalysisOcl",
    "libclangEdit" : "libclangEditOcl",
    "libclangFormat" : "libclangFormatOcl",
    "libclangToolingInclusions" : "libclangToolingInclusionsOcl",
    "libclangToolingCore" : "libclangToolingCoreOcl",
    "libclangRewrite" : "libclangRewriteOcl",
    "libclangASTMatchers" : "libclangASTMatchersOcl",
    "libclangAST" : "libclangASTOcl",
    "libclangLex" : "libclangLexOcl",
    "libLLVMSPIRVLib" : "libLLVMSPIRVLibOcl",
    "libLLVMAnalysis" : "libLLVMAnalysisOcl",
    "libLLVMAsmParser" : "libLLVMAsmParserOcl",
    "libLLVMAsmPrinter" : "libLLVMAsmPrinterOcl",
    "libLLVMBitReader" : "libLLVMBitReaderOcl",
    "libLLVMBitWriter" : "libLLVMBitWriterOcl",
    "libLLVMCodeGen" : "libLLVMCodeGenOcl",
    "libLLVMCore" : "libLLVMCoreOcl",
    "libLLVMIRReader" : "libLLVMIRReaderOcl",
    "libLLVMInstCombine" : "libLLVMInstCombineOcl",
    "libLLVMInstrumentation" : "libLLVMInstrumentationOcl",
    "libLLVMMC" : "libLLVMMCOcl",
    "libLLVMMCDisassembler" : "libLLVMMCDisassemblerOcl",
    "libLLVMMCParser" : "libLLVMMCParserOcl",
    "libLLVMObjCARCOpts" : "libLLVMObjCARCOptsOcl",
    "libLLVMObject" : "libLLVMObjectOcl",
    "libLLVMOption" : "libLLVMOptionOcl",
    "libLLVMProfileData" : "libLLVMProfileDataOcl",
    "libLLVMScalarOpts" : "libLLVMScalarOptsOcl",
    "libLLVMSelectionDAG" : "libLLVMSelectionDAGOcl",
    "libLLVMSupport" : "libLLVMSupportOcl",
    "libLLVMTarget" : "libLLVMTargetOcl",
    "libLLVMTransformUtils" : "libLLVMTransformUtilsOcl",
    "libLLVMVectorize" : "libLLVMVectorizeOcl",
    "libLLVMX86AsmParser" : "libLLVMX86AsmParserOcl",
    "libLLVMX86AsmPrinter" : "libLLVMX86AsmPrinterOcl",
    "libLLVMX86CodeGen" : "libLLVMX86CodeGenOcl",
    "libLLVMX86Desc" : "libLLVMX86DescOcl",
    "libLLVMX86Disassembler" : "libLLVMX86DisassemblerOcl",
    "libLLVMX86Info" : "libLLVMX86InfoOcl",
    "libLLVMX86Utils" : "libLLVMX86UtilsOcl",
    "libLLVMCoroutines" : "libLLVMCoroutinesOcl",
    "libLLVMCoverage" : "libLLVMCoverageOcl",
    "libLLVMLTO" : "libLLVMLTOOcl",
    "libLLVMPasses" : "libLLVMPassesOcl",
    "libLLVMipo" : "libLLVMipoOcl",
    "libLLVMLinker" : "libLLVMLinkerOcl",
    "libLLVMGlobalISel" : "libLLVMGlobalISelOcl",
    "libLLVMAggressiveInstCombine" : "libLLVMAggressiveInstCombineOcl",
    "libLLVMDebugInfoCodeView" : "libLLVMDebugInfoCodeViewOcl",
    "libLLVMDebugInfoMSF" : "libLLVMDebugInfoMSFOcl",
    "libLLVMBinaryFormat" : "libLLVMBinaryFormatOcl",
    "libLLVMDemangle" : "libLLVMDemangleOcl",
} 


class LLVMGenerator(Generator):
    def __init__(self, root):
        # It is necessary that patching on LLVM before generating Android.bp
        self.proj = path.join(root, "llvm_build/")
        src = path.join(root, BUILD_DIR, "igc/IGC/llvm/src/")

        os.system("cp -rf " + path.join(root, "igc/bp") + " " + src + NOVERBOSE)

        super(LLVMGenerator, self).__init__(src, root)

        self.root = root
        # the final path of source code after patching
        build_llvm_dir = "../../../../../llvm_build/"

        self.allmoduleinfo[0] = ModuleInfo("libLLVMAnalysisOcl", build_llvm_dir + "LLVMAnalysisOcl.bp",
            "lib/Analysis/CMakeFiles/LLVMAnalysis.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMAnalysis" : ""}, addstatic = [
                "libLLVMBinaryFormatOcl", "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMObjectOcl",
                "libLLVMProfileDataOcl"], )

        self.allmoduleinfo[1] = ModuleInfo("libLLVMAsmParserOcl", build_llvm_dir + "LLVMAsmParserOcl.bp",
            "lib/AsmParser/CMakeFiles/LLVMAsmParser.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMAsmParser" : ""}, addstatic = [
                "libLLVMBinaryFormatOcl", "libLLVMCoreOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[2] = ModuleInfo("libLLVMBinaryFormatOcl", build_llvm_dir + "LLVMBinaryFormatOcl.bp",
            "lib/BinaryFormat/CMakeFiles/LLVMBinaryFormat.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMBinaryFormat" : ""}, addstatic = [
                "libLLVMSupportOcl"], )

        self.allmoduleinfo[3] = ModuleInfo("libLLVMBitReaderOcl", build_llvm_dir + "LLVMBitReaderOcl.bp",
            "lib/Bitcode/Reader/CMakeFiles/LLVMBitReader.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMBitReader" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[4] = ModuleInfo("libLLVMBitWriterOcl", build_llvm_dir + "LLVMBitWriterOcl.bp",
            "lib/Bitcode/Writer/CMakeFiles/LLVMBitWriter.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMBitWriter" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMObjectOcl", "libLLVMMCOcl"], )

        self.allmoduleinfo[5] = ModuleInfo("libLLVMCodeGenOcl", build_llvm_dir + "LLVMCodeGenOcl.bp",
            "lib/CodeGen/CMakeFiles/LLVMCodeGen.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMCodeGen" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMBitReaderOcl", "libLLVMBitWriterOcl", "libLLVMCoreOcl",
                "libLLVMMCOcl", "libLLVMProfileDataOcl", "libLLVMScalarOptsOcl", "libLLVMSupportOcl",
                "libLLVMTargetOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[6] = ModuleInfo("libLLVMAsmPrinterOcl", build_llvm_dir + "LLVMAsmPrinterOcl.bp",
            "lib/CodeGen/AsmPrinter/CMakeFiles/LLVMAsmPrinter.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMAsmPrinter" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMBinaryFormatOcl", "libLLVMCodeGenOcl", "libLLVMCoreOcl",
                "libLLVMDebugInfoCodeViewOcl", "libLLVMDebugInfoMSFOcl", "libLLVMMCOcl", "libLLVMMCParserOcl",
                "libLLVMSupportOcl", "libLLVMTargetOcl"], )

        self.allmoduleinfo[7] = ModuleInfo("libLLVMGlobalISelOcl", build_llvm_dir + "LLVMGlobalISelOcl.bp",
            "lib/CodeGen/GlobalISel/CMakeFiles/LLVMGlobalISel.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMGlobalISel" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCodeGenOcl", "libLLVMCoreOcl", "libLLVMMCOcl", "libLLVMSupportOcl",
                "libLLVMTargetOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[8] = ModuleInfo("libLLVMMIRParserOcl", build_llvm_dir + "LLVMMIRParserOcl.bp",
            "lib/CodeGen/MIRParser/CMakeFiles/LLVMMIRParser.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMMIRParser" : ""}, addstatic = [
                "libLLVMAsmParserOcl", "libLLVMBinaryFormatOcl", "libLLVMCodeGenOcl", "libLLVMCoreOcl",
                "libLLVMMCOcl", "libLLVMSupportOcl", "libLLVMTargetOcl"], )

        self.allmoduleinfo[9] = ModuleInfo("libLLVMSelectionDAGOcl", build_llvm_dir + "LLVMSelectionDAGOcl.bp",
            "lib/CodeGen/SelectionDAG/CMakeFiles/LLVMSelectionDAG.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMSelectionDAG" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCodeGenOcl", "libLLVMCoreOcl", "libLLVMMCOcl", "libLLVMSupportOcl",
                "libLLVMTargetOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[10] = ModuleInfo("libLLVMDebugInfoCodeViewOcl", build_llvm_dir + "LLVMDebugInfoCodeViewOcl.bp",
            "lib/DebugInfo/CodeView/CMakeFiles/LLVMDebugInfoCodeView.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMDebugInfoCodeView" : ""}, addstatic = [
                "libLLVMSupportOcl", "libLLVMDebugInfoMSFOcl"], )

        self.allmoduleinfo[11] = ModuleInfo("libLLVMDebugInfoDWARFOcl", build_llvm_dir + "LLVMDebugInfoDWARFOcl.bp",
            "lib/DebugInfo/DWARF/CMakeFiles/LLVMDebugInfoDWARF.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"DebugInfoDWARF" : ""}, addstatic = [
                "libLLVMBinaryFormatOcl", "libLLVMObjectOcl", "libLLVMMCOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[12] = ModuleInfo("libLLVMDebugInfoMSFOcl", build_llvm_dir + "LLVMDebugInfoMSFOcl.bp",
            "lib/DebugInfo/MSF/CMakeFiles/LLVMDebugInfoMSF.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMDebugInfoMSF" : ""}, addstatic = [
                "libLLVMSupportOcl"], )

        self.allmoduleinfo[13] = ModuleInfo("libLLVMDebugInfoPDBOcl", build_llvm_dir + "LLVMDebugInfoPDBOcl.bp",
            "lib/DebugInfo/PDB/CMakeFiles/LLVMDebugInfoPDB.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMDebugInfoPDB" : ""}, addstatic = [
                "libLLVMObjectOcl", "libLLVMSupportOcl", "libLLVMDebugInfoCodeViewOcl", "libLLVMDebugInfoMSFOcl"], )

        self.allmoduleinfo[14] = ModuleInfo("libLLVMSymbolizeOcl", build_llvm_dir + "LLVMSymbolizeOcl.bp",
            "lib/DebugInfo/Symbolize/CMakeFiles/LLVMSymbolize.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMSymbolize" : ""}, addstatic = [
                "libLLVMDebugInfoDWARFOcl", "libLLVMDebugInfoPDBOcl", "libLLVMObjectOcl", "libLLVMSupportOcl",
                "libLLVMDemangleOcl"], )

        self.allmoduleinfo[15] = ModuleInfo("libLLVMDemangleOcl", build_llvm_dir + "LLVMDemangleOcl.bp",
            "lib/Demangle/CMakeFiles/LLVMDemangle.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMDemangle" : ""}, )

        self.allmoduleinfo[16] = ModuleInfo("libLLVMExecutionEngineOcl", build_llvm_dir + "LLVMExecutionEngineOcl.bp",
            "lib/ExecutionEngine/CMakeFiles/LLVMExecutionEngine.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMExecutionEngine" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMMCOcl", "libLLVMObjectOcl", "libLLVMRuntimeDyldOcl",
                "libLLVMSupportOcl", "libLLVMTargetOcl"], )

        self.allmoduleinfo[17] = ModuleInfo("libLLVMInterpreterOcl", build_llvm_dir + "LLVMInterpreterOcl.bp",
            "lib/ExecutionEngine/Interpreter/CMakeFiles/LLVMInterpreter.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMInterpreter" : ""}, addstatic = [
                "libLLVMCodeGenOcl", "libLLVMCoreOcl", "libLLVMExecutionEngineOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[18] = ModuleInfo("libLLVMMCJITOcl", build_llvm_dir + "LLVMMCJITOcl.bp",
            "lib/ExecutionEngine/MCJIT/CMakeFiles/LLVMMCJIT.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMMCJIT" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMExecutionEngineOcl", "libLLVMObjectOcl", "libLLVMRuntimeDyldOcl",
                "libLLVMSupportOcl", "libLLVMTargetOcl"], )

        self.allmoduleinfo[19] = ModuleInfo("libLLVMOrcJITOcl", build_llvm_dir + "LLVMOrcJITOcl.bp",
            "lib/ExecutionEngine/Orc/CMakeFiles/LLVMOrcJIT.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMOrcJIT" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMExecutionEngineOcl", "libLLVMObjectOcl", "libLLVMMCOcl",
                "libLLVMRuntimeDyldOcl", "libLLVMSupportOcl", "libLLVMTargetOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[20] = ModuleInfo("libLLVMRuntimeDyldOcl", build_llvm_dir + "LLVMRuntimeDyldOcl.bp",
            "lib/ExecutionEngine/RuntimeDyld/CMakeFiles/LLVMRuntimeDyld.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMRuntimeDyld" : ""}, addstatic = [
                "libLLVMMCOcl", "libLLVMObjectOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[21] = ModuleInfo("libLLVMFuzzMutateOcl", build_llvm_dir + "LLVMFuzzMutateOcl.bp",
            "lib/FuzzMutate/CMakeFiles/LLVMFuzzMutate.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMFuzzMutate" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMBitReaderOcl", "libLLVMBitWriterOcl", "libLLVMCoreOcl",
                "libLLVMScalarOptsOcl", "libLLVMSupportOcl", "libLLVMTargetOcl"], )

        self.allmoduleinfo[22] = ModuleInfo("libLLVMCoreOcl", build_llvm_dir + "LLVMCoreOcl.bp",
            "lib/IR/CMakeFiles/LLVMCore.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMCore" : ""}, addstatic = [
                "libLLVMBinaryFormatOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[23] = ModuleInfo("libLLVMIRReaderOcl", build_llvm_dir + "LLVMIRReaderOcl.bp",
            "lib/IRReader/CMakeFiles/LLVMIRReader.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMIRReader" : ""}, addstatic = [
                "libLLVMAsmParserOcl", "libLLVMBitReaderOcl", "libLLVMCoreOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[24] = ModuleInfo("libLLVMLineEditorOcl", build_llvm_dir + "LLVMLineEditorOcl.bp",
            "lib/LineEditor/CMakeFiles/LLVMLineEditor.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMLineEditor" : ""}, addstatic = [
                "libLLVMSupportOcl"], )

        self.allmoduleinfo[25] = ModuleInfo("libLLVMLinkerOcl", build_llvm_dir + "LLVMLinkerOcl.bp",
            "lib/Linker/CMakeFiles/LLVMLinker.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMLinker" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[26] = ModuleInfo("libLLVMLTOOcl", build_llvm_dir + "LLVMLTOOcl.bp",
            "lib/LTO/CMakeFiles/LLVMLTO.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMLTO" : ""}, addstatic = [
                "libLLVMAggressiveInstCombineOcl", "libLLVMAnalysisOcl", "libLLVMBitReaderOcl",
                "libLLVMBitWriterOcl", "libLLVMCodeGenOcl", "libLLVMCoreOcl", "libLLVMipoOcl",
                "libLLVMInstCombineOcl", "libLLVMLinkerOcl", "libLLVMMCOcl", "libLLVMObjCARCOptsOcl",
                "libLLVMObjectOcl", "libLLVMPassesOcl", "libLLVMScalarOptsOcl", "libLLVMSupportOcl",
                "libLLVMTargetOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[27] = ModuleInfo("libLLVMMCOcl", build_llvm_dir + "LLVMMCOcl.bp",
            "lib/MC/CMakeFiles/LLVMMC.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMMC" : ""}, addstatic = [
                "libLLVMSupportOcl", "libLLVMBinaryFormatOcl", "libLLVMDebugInfoCodeViewOcl"], )

        self.allmoduleinfo[28] = ModuleInfo("libLLVMMCDisassemblerOcl", build_llvm_dir + "LLVMMCDisassemblerOcl.bp",
            "lib/MC/MCDisassembler/CMakeFiles/LLVMMCDisassembler.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMMCDisassembler" : ""}, addstatic = [
                "libLLVMMCOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[29] = ModuleInfo("libLLVMMCParserOcl", build_llvm_dir + "LLVMMCParserOcl.bp",
            "lib/MC/MCParser/CMakeFiles/LLVMMCParser.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMMCParser" : ""}, addstatic = [
                "libLLVMMCOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[30] = ModuleInfo("libLLVMObjectOcl", build_llvm_dir + "LLVMObjectOcl.bp",
            "lib/Object/CMakeFiles/LLVMObject.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMObject" : ""}, addstatic = [
                "libLLVMBitReaderOcl", "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMMCOcl",
                "libLLVMBinaryFormatOcl", "libLLVMMCParserOcl"], )

        self.allmoduleinfo[31] = ModuleInfo("libLLVMObjectYAMLOcl", build_llvm_dir + "LLVMObjectYAMLOcl.bp",
            "lib/ObjectYAML/CMakeFiles/LLVMObjectYAML.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMObjectYAML" : ""}, addstatic = [
                "libLLVMSupportOcl", "libLLVMDebugInfoCodeViewOcl"], )

        self.allmoduleinfo[32] = ModuleInfo("libLLVMOptionOcl", build_llvm_dir + "LLVMOptionOcl.bp",
            "lib/Option/CMakeFiles/LLVMOption.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMOption" : ""}, addstatic = [
                "libLLVMSupportOcl"], )

        self.allmoduleinfo[33] = ModuleInfo("libLLVMPassesOcl", build_llvm_dir + "LLVMPassesOcl.bp",
            "lib/Passes/CMakeFiles/LLVMPasses.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMPasses" : ""}, addstatic = [
                "libLLVMAggressiveInstCombineOcl", "libLLVMAnalysisOcl", "libLLVMCodeGenOcl", "libLLVMCoreOcl",
                "libLLVMipoOcl", "libLLVMInstCombineOcl", "libLLVMScalarOptsOcl", "libLLVMSupportOcl",
                "libLLVMTargetOcl", "libLLVMTransformUtilsOcl", "libLLVMVectorizeOcl", "libLLVMInstrumentationOcl"], )

        self.allmoduleinfo[34] = ModuleInfo("libLLVMProfileDataOcl", build_llvm_dir + "LLVMProfileDataOcl.bp",
            "lib/ProfileData/CMakeFiles/LLVMProfileData.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMProfileData" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[35] = ModuleInfo("libLLVMCoverageOcl", build_llvm_dir + "LLVMCoverageOcl.bp",
            "lib/ProfileData/Coverage/CMakeFiles/LLVMCoverage.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMCoverage" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMObjectOcl", "libLLVMProfileDataOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[36] = ModuleInfo("libLLVMSupportOcl", build_llvm_dir + "LLVMSupportOcl.bp",
            "lib/Support/CMakeFiles/LLVMSupport.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMSupport" : ""}, addstatic = [
                "libLLVMDemangleOcl"], )

        self.allmoduleinfo[37] = ModuleInfo("libLLVMTableGenOcl", build_llvm_dir + "LLVMTableGenOcl.bp",
            "lib/TableGen/CMakeFiles/LLVMTableGen.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMTableGen" : ""}, addstatic = [
                "libLLVMSupportOcl"], )

        self.allmoduleinfo[38] = ModuleInfo("libLLVMTargetOcl", build_llvm_dir + "LLVMTargetOcl.bp",
            "lib/Target/CMakeFiles/LLVMTarget.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMTarget" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMMCOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[39] = ModuleInfo("libLLVMAggressiveInstCombineOcl", build_llvm_dir + "LLVMAggressiveInstCombineOcl.bp",
            "lib/Transforms/AggressiveInstCombine/CMakeFiles/LLVMAggressiveInstCombine.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMAggressiveInstCombine" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[40] = ModuleInfo("libLLVMCoroutinesOcl", build_llvm_dir + "LLVMCoroutinesOcl.bp",
            "lib/Transforms/Coroutines/CMakeFiles/LLVMCoroutines.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMCoroutines" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMipoOcl", "libLLVMScalarOptsOcl",
                "libLLVMSupportOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[41] = ModuleInfo("libLLVMInstCombineOcl", build_llvm_dir + "LLVMInstCombineOcl.bp",
            "lib/Transforms/InstCombine/CMakeFiles/LLVMInstCombine.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMInstCombine" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[42] = ModuleInfo("libLLVMInstrumentationOcl", build_llvm_dir + "LLVMInstrumentationOcl.bp",
            "lib/Transforms/Instrumentation/CMakeFiles/LLVMInstrumentation.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMInstrumentation" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMMCOcl", "libLLVMSupportOcl", "libLLVMTransformUtilsOcl",
                "libLLVMProfileDataOcl"], )

        self.allmoduleinfo[43] = ModuleInfo("libLLVMipoOcl", build_llvm_dir + "LLVMipoOcl.bp",
            "lib/Transforms/IPO/CMakeFiles/LLVMipo.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMipo" : ""}, addstatic = [
                "libLLVMAggressiveInstCombineOcl", "libLLVMAnalysisOcl", "libLLVMBitReaderOcl", "libLLVMBitWriterOcl",
                "libLLVMCoreOcl", "libLLVMInstCombineOcl", "libLLVMIRReaderOcl", "libLLVMLinkerOcl", "libLLVMObjectOcl",
                "libLLVMProfileDataOcl", "libLLVMScalarOptsOcl", "libLLVMSupportOcl", "libLLVMTransformUtilsOcl",
                "libLLVMVectorizeOcl", "libLLVMInstrumentationOcl"], )

        self.allmoduleinfo[44] = ModuleInfo("libLLVMObjCARCOptsOcl", build_llvm_dir + "LLVMObjCARCOptsOcl.bp",
            "lib/Transforms/ObjCARC/CMakeFiles/LLVMObjCARCOpts.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMObjCARCOpts" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[45] = ModuleInfo("libLLVMScalarOptsOcl", build_llvm_dir + "LLVMScalarOptsOcl.bp",
            "lib/Transforms/Scalar/CMakeFiles/LLVMScalarOpts.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMScalarOpts" : ""}, addstatic = [
                "libLLVMAggressiveInstCombineOcl", "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMInstCombineOcl",
                "libLLVMSupportOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[46] = ModuleInfo("libLLVMTransformUtilsOcl", build_llvm_dir + "LLVMTransformUtilsOcl.bp",
            "lib/Transforms/Utils/CMakeFiles/LLVMTransformUtils.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMTransformUtils" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[47] = ModuleInfo("libLLVMVectorizeOcl", build_llvm_dir + "LLVMVectorizeOcl.bp",
            "lib/Transforms/Vectorize/CMakeFiles/LLVMVectorize.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMVectorize" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMCoreOcl", "libLLVMSupportOcl", "libLLVMTransformUtilsOcl"], )

        self.allmoduleinfo[48] = ModuleInfo("libLLVMX86CodeGenOcl", build_llvm_dir + "LLVMX86CodeGenOcl.bp",
            "lib/Target/X86/CMakeFiles/LLVMX86CodeGen.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMX86CodeGenOcl" : ""}, addstatic = [
                "libLLVMX86DescOcl", "libLLVMX86AsmPrinterOcl", "libLLVMX86InfoOcl", "libLLVMX86UtilsOcl",
                "libLLVMAnalysisOcl", "libLLVMAsmPrinterOcl", "libLLVMBinaryFormatOcl", "libLLVMSelectionDAGOcl",
                "libLLVMCodeGenOcl", "libLLVMGlobalISelOcl", "libLLVMCoreOcl", "libLLVMMCOcl", "libLLVMSupportOcl",
                "libLLVMTargetOcl"], )

        self.allmoduleinfo[49] = ModuleInfo("libLLVMX86AsmParserOcl", build_llvm_dir + "LLVMX86AsmParserOcl.bp",
            "lib/Target/X86/AsmParser/CMakeFiles/LLVMX86AsmParser.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMX86AsmParser" : ""}, addstatic = [
                "libLLVMX86DescOcl", "libLLVMX86AsmPrinterOcl", "libLLVMX86InfoOcl", "libLLVMMCOcl",
                "libLLVMMCParserOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[50] = ModuleInfo("libLLVMX86DisassemblerOcl", build_llvm_dir + "LLVMX86DisassemblerOcl.bp",
            "lib/Target/X86/Disassembler/CMakeFiles/LLVMX86Disassembler.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMX86Disassembler" : ""}, addstatic = [
                "libLLVMX86InfoOcl",  "libLLVMMCDisassemblerOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[51] = ModuleInfo("libLLVMX86AsmPrinterOcl", build_llvm_dir + "LLVMX86AsmPrinterOcl.bp",
            "lib/Target/X86/InstPrinter/CMakeFiles/LLVMX86AsmPrinter.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMX86AsmPrinter" : ""}, addstatic = [
                "libLLVMX86UtilsOcl", "libLLVMMCOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[52] = ModuleInfo("libLLVMX86DescOcl", build_llvm_dir + "LLVMX86DescOcl.bp",
            "lib/Target/X86/MCTargetDesc/CMakeFiles/LLVMX86Desc.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMX86Desc" : ""}, addstatic = [
                "libLLVMX86AsmPrinterOcl", "libLLVMX86InfoOcl", "libLLVMMCOcl", "libLLVMMCDisassemblerOcl",
                "libLLVMObjectOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[53] = ModuleInfo("libLLVMX86InfoOcl", build_llvm_dir + "LLVMX86InfoOcl.bp",
            "lib/Target/X86/TargetInfo/CMakeFiles/LLVMX86Info.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMX86Info" : ""}, addstatic = [
                "libLLVMSupportOcl"], )

        self.allmoduleinfo[54] = ModuleInfo("libLLVMX86UtilsOcl", build_llvm_dir + "LLVMX86UtilsOcl.bp",
            "lib/Target/X86/Utils/CMakeFiles/LLVMX86Utils.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMX86Utils" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[55] = ModuleInfo("libLLVMSPIRVLibOcl", build_llvm_dir + "LLVMSPIRVLibOcl.bp",
            "projects/llvm-spirv/lib/SPIRV/CMakeFiles/LLVMSPIRVLib.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libLLVMSPIRVLib" : ""}, )

        self.allmoduleinfo[56] = ModuleInfo("llvm-spirv-ocl", build_llvm_dir + "llvm-spirv-ocl.bp",
            "projects/llvm-spirv/tools/llvm-spirv/CMakeFiles/llvm-spirv.dir/", "binary", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = UPDATE_STATIC)

        self.allmoduleinfo[57] = ModuleInfo("libcommon_clang", build_llvm_dir + "common_clang.bp",
            "projects/opencl-clang/CMakeFiles/common_clang.dir/", "library_shared", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = UPDATE_STATIC)

        self.allmoduleinfo[58] = ModuleInfo("linux_resource_linker_ocl", build_llvm_dir + "linux_resource_linker_ocl.bp",
            "projects/opencl-clang/linux_linker/CMakeFiles/linux_resource_linker.dir/", "binary", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", )

        self.allmoduleinfo[59] = ModuleInfo("libclangAnalysisOcl", build_llvm_dir + "clangAnalysisOcl.bp",
            "tools/clang/lib/Analysis/CMakeFiles/clangAnalysis.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangAnalysis" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangLexOcl"], )

        self.allmoduleinfo[60] = ModuleInfo("libclangARCMigrateOcl", build_llvm_dir + "clangARCMigrateOcl.bp",
            "tools/clang/lib/ARCMigrate/CMakeFiles/clangARCMigrate.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangARCMigrate" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangAnalysisOcl", "libclangBasicOcl", "libclangEditOcl",
                "libclangFrontendOcl", "libclangLexOcl", "libclangRewriteOcl", "libclangSemaOcl", "libclangSerializationOcl",
                "libclangStaticAnalyzerCheckersOcl"], )

        self.allmoduleinfo[61] = ModuleInfo("libclangASTOcl", build_llvm_dir + "clangASTOcl.bp",
            "tools/clang/lib/AST/CMakeFiles/clangAST.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangAST" : ""}, addstatic = [
                "libLLVMBinaryFormatOcl", "libLLVMSupportOcl", "libclangBasicOcl", "libclangLexOcl"], )

        self.allmoduleinfo[62] = ModuleInfo("libclangASTMatchersOcl", build_llvm_dir + "clangASTMatchersOcl.bp",
            "tools/clang/lib/ASTMatchers/CMakeFiles/clangASTMatchers.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangASTMatchers" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl"], )

        self.allmoduleinfo[63] = ModuleInfo("libclangDynamicASTMatchersOcl", build_llvm_dir + "clangDynamicASTMatchersOcl.bp",
            "tools/clang/lib/ASTMatchers/Dynamic/CMakeFiles/clangDynamicASTMatchers.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangDynamicASTMatchers" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangASTMatchersOcl", "libclangBasicOcl"], )

        self.allmoduleinfo[64] = ModuleInfo("libclangBasicOcl", build_llvm_dir + "clangBasicOcl.bp",
            "tools/clang/lib/Basic/CMakeFiles/clangBasic.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangBasic" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMMCOcl", "libLLVMSupportOcl"], )

        self.allmoduleinfo[65] = ModuleInfo("libclangCodeGenOcl", build_llvm_dir + "clangCodeGenOcl.bp",
            "tools/clang/lib/CodeGen/CMakeFiles/clangCodeGen.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangCodeGen" : ""}, addstatic = [
                "libLLVMAnalysisOcl", "libLLVMBitReaderOcl", "libLLVMBitWriterOcl", "libLLVMCoreOcl",
                "libLLVMCoroutinesOcl", "libLLVMCoverageOcl", "libLLVMipoOcl", "libLLVMIRReaderOcl",
                "libLLVMAggressiveInstCombineOcl", "libLLVMInstCombineOcl", "libLLVMInstrumentationOcl",
                "libLLVMLTOOcl", "libLLVMLinkerOcl", "libLLVMMCOcl", "libLLVMObjectOcl", "libLLVMObjCARCOptsOcl",
                "libLLVMPassesOcl", "libLLVMProfileDataOcl", "libLLVMScalarOptsOcl", "libLLVMSupportOcl",
                "libLLVMTargetOcl", "libLLVMTransformUtilsOcl", "libclangAnalysisOcl", "libclangASTOcl",
                "libclangBasicOcl", "libclangFrontendOcl", "libclangLexOcl"], )

        self.allmoduleinfo[66] = ModuleInfo("libclangCrossTUOcl", build_llvm_dir + "clangCrossTUOcl.bp",
            "tools/clang/lib/CrossTU/CMakeFiles/clangCrossTU.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangCrossTU" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangFrontendOcl", "libclangIndexOcl"], )

        self.allmoduleinfo[67] = ModuleInfo("libclangDriverOcl", build_llvm_dir + "clangDriverOcl.bp",
            "tools/clang/lib/Driver/CMakeFiles/clangDriver.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangDriver" : ""}, addstatic = [
                "libLLVMBinaryFormatOcl", "libLLVMSupportOcl", "libLLVMOptionOcl", "libclangBasicOcl"], )

        self.allmoduleinfo[68] = ModuleInfo("libclangEditOcl", build_llvm_dir + "clangEditOcl.bp",
            "tools/clang/lib/Edit/CMakeFiles/clangEdit.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangEdit" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangLexOcl"], )

        self.allmoduleinfo[69] = ModuleInfo("libclangFormatOcl", build_llvm_dir + "clangFormatOcl.bp",
            "tools/clang/lib/Format/CMakeFiles/clangFormat.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangFormat" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangBasicOcl", "libclangLexOcl", "libclangToolingInclusionsOcl",
                "libclangToolingCoreOcl"], )

        self.allmoduleinfo[70] = ModuleInfo("libclangRewriteFrontendOcl", build_llvm_dir + "clangRewriteFrontendOcl.bp",
            "tools/clang/lib/Frontend/Rewrite/CMakeFiles/clangRewriteFrontend.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangRewriteFrontend" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangEditOcl", "libclangFrontendOcl",
                "libclangLexOcl", "libclangRewriteOcl", "libclangSerializationOcl"], )

        self.allmoduleinfo[71] = ModuleInfo("libclangFrontendOcl", build_llvm_dir + "clangFrontendOcl.bp",
            "tools/clang/lib/Frontend/CMakeFiles/clangFrontend.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangFrontend" : ""}, addstatic = [
                "libLLVMBitReaderOcl", "libLLVMOptionOcl", "libLLVMProfileDataOcl", "libLLVMSupportOcl",
                "libclangASTOcl", "libclangBasicOcl", "libclangDriverOcl", "libclangEditOcl", "libclangLexOcl",
                "libclangParseOcl", "libclangSemaOcl", "libclangSerializationOcl"], )

        self.allmoduleinfo[72] = ModuleInfo("libclangFrontendToolOcl", build_llvm_dir + "clangFrontendToolOcl.bp",
            "tools/clang/lib/FrontendTool/CMakeFiles/clangFrontendTool.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangFrontendTool" : ""}, addstatic = [
                "libLLVMOptionOcl", "libLLVMSupportOcl", "libclangBasicOcl", "libclangCodeGenOcl",
                "libclangDriverOcl", "libclangFrontendOcl", "libclangRewriteFrontendOcl"], )

        self.allmoduleinfo[73] = ModuleInfo("libclangIndexOcl", build_llvm_dir + "clangIndexOcl.bp",
            "tools/clang/lib/Index/CMakeFiles/clangIndex.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangIndex" : ""}, addstatic = [
                "libLLVMCoreOcl", "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangFormatOcl",
                "libclangFrontendOcl", "libclangLexOcl", "libclangRewriteOcl", "libclangSerializationOcl",
                "libclangToolingCoreOcl"], )

        self.allmoduleinfo[74] = ModuleInfo("libclangLexOcl", build_llvm_dir + "clangLexOcl.bp",
            "tools/clang/lib/Lex/CMakeFiles/clangLex.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangLex" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangBasicOcl"], )

        self.allmoduleinfo[75] = ModuleInfo("libclangParseOcl", build_llvm_dir + "clangParseOcl.bp",
            "tools/clang/lib/Parse/CMakeFiles/clangParse.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangParse" : ""}, addstatic = [
                "libLLVMMCOcl", "libLLVMMCParserOcl", "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl",
                "libclangLexOcl", "libclangSemaOcl"], )

        self.allmoduleinfo[76] = ModuleInfo("libclangRewriteOcl", build_llvm_dir + "clangRewriteOcl.bp",
            "tools/clang/lib/Rewrite/CMakeFiles/clangRewrite.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangRewrite" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangBasicOcl", "libclangLexOcl"], )

        self.allmoduleinfo[77] = ModuleInfo("libclangSemaOcl", build_llvm_dir + "clangSemaOcl.bp",
            "tools/clang/lib/Sema/CMakeFiles/clangSema.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangSema" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangAnalysisOcl", "libclangBasicOcl",
                "libclangEditOcl", "libclangLexOcl"], )

        self.allmoduleinfo[78] = ModuleInfo("libclangSerializationOcl", build_llvm_dir + "clangSerializationOcl.bp",
            "tools/clang/lib/Serialization/CMakeFiles/clangSerialization.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangSerialization" : ""}, addstatic = [
                "libLLVMBitReaderOcl", "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangLexOcl",
                "libclangSemaOcl"], )

        self.allmoduleinfo[79] = ModuleInfo("libclangStaticAnalyzerCoreOcl", build_llvm_dir + "clangStaticAnalyzerCoreOcl.bp",
            "tools/clang/lib/StaticAnalyzer/Core/CMakeFiles/clangStaticAnalyzerCore.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangStaticAnalyzerCore" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangASTMatchersOcl", "libclangAnalysisOcl",
                "libclangBasicOcl", "libclangCrossTUOcl", "libclangLexOcl", "libclangRewriteOcl"], )

        self.allmoduleinfo[80] = ModuleInfo("libclangStaticAnalyzerCheckersOcl", build_llvm_dir + "clangStaticAnalyzerCheckersOcl.bp",
            "tools/clang/lib/StaticAnalyzer/Checkers/CMakeFiles/clangStaticAnalyzerCheckers.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangStaticAnalyzerCheckers" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangASTMatchersOcl", "libclangAnalysisOcl",
                "libclangBasicOcl", "libclangLexOcl", "libclangStaticAnalyzerCoreOcl"], )

        self.allmoduleinfo[81] = ModuleInfo("libclangStaticAnalyzerFrontendOcl", build_llvm_dir + "clangStaticAnalyzerFrontendOcl.bp",
            "tools/clang/lib/StaticAnalyzer/Frontend/CMakeFiles/clangStaticAnalyzerFrontend.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangStaticAnalyzerFrontend" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangAnalysisOcl", "libclangBasicOcl", "libclangCrossTUOcl",
                "libclangFrontendOcl", "libclangLexOcl", "libclangStaticAnalyzerCheckersOcl", "libclangStaticAnalyzerCoreOcl"], )

        self.allmoduleinfo[82] = ModuleInfo("libclangToolingASTDiffOcl", build_llvm_dir + "clangToolingASTDiffOcl.bp",
            "tools/clang/lib/Tooling/ASTDiff/CMakeFiles/clangToolingASTDiff.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangToolingASTDiff" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangLexOcl"], )

        self.allmoduleinfo[83] = ModuleInfo("libclangToolingOcl", build_llvm_dir + "clangToolingOcl.bp",
            "tools/clang/lib/Tooling/CMakeFiles/clangTooling.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangTooling" : ""}, addstatic = [
                "libLLVMOptionOcl", "libLLVMSupportOcl", "libclangASTOcl", "libclangASTMatchersOcl", "libclangBasicOcl",
                "libclangDriverOcl", "libclangFormatOcl", "libclangFrontendOcl", "libclangLexOcl", "libclangRewriteOcl",
                "libclangToolingCoreOcl"], )

        self.allmoduleinfo[84] = ModuleInfo("libclangToolingCoreOcl", build_llvm_dir + "clangToolingCoreOcl.bp",
            "tools/clang/lib/Tooling/Core/CMakeFiles/clangToolingCore.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangToolingCore" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangBasicOcl", "libclangLexOcl", "libclangRewriteOcl"], )

        self.allmoduleinfo[85] = ModuleInfo("libclangToolingInclusionsOcl", build_llvm_dir + "clangToolingInclusionsOcl.bp",
            "tools/clang/lib/Tooling/Inclusions/CMakeFiles/clangToolingInclusions.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangToolingInclusions" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangBasicOcl", "libclangLexOcl", "libclangRewriteOcl", "libclangToolingCoreOcl"], )

        self.allmoduleinfo[86] = ModuleInfo("libclangToolingRefactorOcl", build_llvm_dir + "clangToolingRefactorOcl.bp",
            "tools/clang/lib/Tooling/Refactoring/CMakeFiles/clangToolingRefactor.dir/", "library_static", "llvm-ocl-defaults",
            middledir = "IGC/llvm/build/src/", updatestatic = {"libclangToolingRefactor" : ""}, addstatic = [
                "libLLVMSupportOcl", "libclangASTOcl", "libclangASTMatchersOcl", "libclangBasicOcl", "libclangFormatOcl",
                "libclangLexOcl", "libclangRewriteOcl", "libclangToolingCoreOcl"], )

        self.allmoduledefaults = CCDefaults(self.proj, "llvm-ocl-defaults",
            cppflags = ["-Wno-error"],
            clang_cflags = ["-finline-functions", "-fexceptions", "-Wno-error=unused-lambda-capture",
                "-Wno-error=non-virtual-dtor", "-Wno-error=missing-field-initializers",
                "-Wno-error=user-defined-warnings", "-Wno-error=unused-const-variable",
                "-Wno-error=unused-variable", "-Wno-error=sign-compare", "-Wno-error=missing-braces"],
            include_dirs = ["external/zlib",
                "hardware/intel/external/opencl/llvm_build/include",
                "hardware/intel/external/opencl/llvm_build/device/include",
                "hardware/intel/external/opencl/llvm_build/device/include/gen/aarch64",
                "hardware/intel/external/opencl/llvm_build/device/include/gen/x86"],
            static_libs = ["libz"],
            bpfiles = ["LLVMAnalysisOcl.bp", "LLVMAsmParserOcl.bp", "LLVMBinaryFormatOcl.bp", "LLVMBitReaderOcl.bp",
                "LLVMBitWriterOcl.bp", "LLVMCodeGenOcl.bp", "LLVMAsmPrinterOcl.bp", "LLVMGlobalISelOcl.bp",
                "LLVMMIRParserOcl.bp", "LLVMSelectionDAGOcl.bp", "LLVMDebugInfoCodeViewOcl.bp", "LLVMDebugInfoDWARFOcl.bp",
                "LLVMDebugInfoMSFOcl.bp", "LLVMDebugInfoPDBOcl.bp", "LLVMSymbolizeOcl.bp", "LLVMDemangleOcl.bp",
                "LLVMExecutionEngineOcl.bp", "LLVMInterpreterOcl.bp", "LLVMMCJITOcl.bp", "LLVMOrcJITOcl.bp",
                "LLVMRuntimeDyldOcl.bp", "LLVMFuzzMutateOcl.bp", "LLVMCoreOcl.bp", "LLVMIRReaderOcl.bp",
                "LLVMLineEditorOcl.bp", "LLVMLinkerOcl.bp", "LLVMLTOOcl.bp", "LLVMMCOcl.bp",
                "LLVMMCDisassemblerOcl.bp", "LLVMMCParserOcl.bp", "LLVMObjectOcl.bp", "LLVMObjectYAMLOcl.bp",
                "LLVMOptionOcl.bp", "LLVMPassesOcl.bp", "LLVMProfileDataOcl.bp", "LLVMCoverageOcl.bp",
                "LLVMSupportOcl.bp", "LLVMTableGenOcl.bp", "LLVMTargetOcl.bp", "LLVMAggressiveInstCombineOcl.bp",
                "LLVMCoroutinesOcl.bp", "LLVMInstCombineOcl.bp", "LLVMInstrumentationOcl.bp", "LLVMipoOcl.bp",
                "LLVMObjCARCOptsOcl.bp", "LLVMScalarOptsOcl.bp", "LLVMTransformUtilsOcl.bp", "LLVMVectorizeOcl.bp",
                "LLVMX86CodeGenOcl.bp", "LLVMX86AsmParserOcl.bp", "LLVMX86DisassemblerOcl.bp", "LLVMX86AsmPrinterOcl.bp",
                "LLVMX86DescOcl.bp", "LLVMX86InfoOcl.bp", "LLVMX86UtilsOcl.bp", "LLVMSPIRVLibOcl.bp",
                "llvm-spirv-ocl.bp", "common_clang.bp", "linux_resource_linker_ocl.bp", "clangAnalysisOcl.bp",
                "clangARCMigrateOcl.bp", "clangASTOcl.bp", "clangASTMatchersOcl.bp", "clangDynamicASTMatchersOcl.bp",
                "clangBasicOcl.bp", "clangCodeGenOcl.bp", "clangCrossTUOcl.bp", "clangDriverOcl.bp",
                "clangEditOcl.bp", "clangFormatOcl.bp", "clangRewriteFrontendOcl.bp", "clangFrontendOcl.bp",
                "clangFrontendToolOcl.bp", "clangIndexOcl.bp", "clangLexOcl.bp", "clangParseOcl.bp",
                "clangRewriteOcl.bp", "clangSemaOcl.bp", "clangSerializationOcl.bp", "clangStaticAnalyzerCoreOcl.bp",
                "clangStaticAnalyzerCheckersOcl.bp", "clangStaticAnalyzerFrontendOcl.bp", "clangToolingASTDiffOcl.bp",
                "clangToolingOcl.bp", "clangToolingCoreOcl.bp", "clangToolingInclusionsOcl.bp", "clangToolingRefactorOcl.bp"
            ], )

    def getTemplate(self):
        return "igc.tpl"

    def adjustSources(self, mode, all_sources):
        for i, l in enumerate(all_sources):
            all_sources[i] = INDENT * 2 + "\"" + re.sub(r".*?: " + self.allmoduleinfo[mode].Mid_Dir, "",
                re.sub("CMakeFiles/.*?\\.dir/", "", l.replace("__/", "../")))

    def adjustLibrary(self, mode, all_libs, is_static = True): 
        update_libs = self.allmoduleinfo[mode].Update_Static if is_static else self.allmoduleinfo[mode].Update_Shared
        add_libs = self.allmoduleinfo[mode].Add_Static if is_static else self.allmoduleinfo[mode].Add_Shared

        for i, l in enumerate(update_libs):
            all_libs = re.sub(INDENT * 2 + "\"" + l + "\",\n",
                (INDENT * 2 + "\"" + update_libs[l] + "\",\n") if 0 < len(update_libs[l]) else "",
                    all_libs)

        for i, l in enumerate(add_libs):
            all_libs += INDENT * 2 + "\"" + l + "\",\n"

        return all_libs

    def adjustFiles(self):
        print("It is adjusting some files for LLVM ... ")
        build_dir = self.getBuildDir()
        cmd = "mkdir -p " + self.proj + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/AST/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/Basic/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/Config/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/Driver/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/Parse/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/Sema/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/Serialization/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/clang/StaticAnalyzer/Checkers/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/gen/x86/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/gen/aarch64/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/llvm/IR/") + NOVERBOSE
        cmd += "mkdir -p " + path.join(self.proj, "device/include/llvm/Support/") + NOVERBOSE
        cmd += "cp -rf " + path.join(build_dir, "IGC/llvm/src/*") + " " + self.proj + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/AST/*.inc") + " " + path.join(self.proj, "device/include/clang/AST/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/Basic/*.inc") + " " + path.join(self.proj, "device/include/clang/Basic/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/Config/*.h") + " " + path.join(self.proj, "device/include/clang/Config/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/Driver/*.inc") + " " + path.join(self.proj, "device/include/clang/Driver/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/Parse/*.inc") + " " + path.join(self.proj, "device/include/clang/Parse/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/Sema/*.inc") + " " + path.join(self.proj, "device/include/clang/Sema/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/Serialization/*.inc") + " " + path.join(self.proj, "device/include/clang/Serialization/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/tools/clang/include/clang/StaticAnalyzer/Checkers/*.inc") + " " + path.join(self.proj, "device/include/clang/StaticAnalyzer/Checkers/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/lib/Target/X86/*.inc") + " " + path.join(self.proj, "device/include/gen/x86/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/lib/Target/AArch64/*.inc") + " " + path.join(self.proj, "device/include/gen/aarch64/") + NOVERBOSE
        cmd += "cp -rf " + path.join(build_dir, "IGC/llvm/build/src/include/llvm/Config") + " " + path.join(self.proj, "device/include/llvm/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/include/llvm/IR/*.inc") + " " + path.join(self.proj, "device/include/llvm/IR/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/include/llvm/Support/*.h") + " " + path.join(self.proj, "device/include/llvm/Support/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/lib/IR/*.inc") + " " + path.join(self.proj, "device/include/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/lib/Transforms/InstCombine/*.inc") + " " + path.join(self.proj, "device/include/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/projects/opencl-clang/*.inc") + " " + path.join(self.proj, "device/include/") + NOVERBOSE
        cmd += "cp -f " + path.join(build_dir, "IGC/llvm/build/src/projects/opencl-clang/cl_headers/opencl-c.h.cpp") + " " + path.join(self.proj, "projects/opencl-clang/cl_headers/") + NOVERBOSE
        cmd += "cp -rf " + path.join(self.root, "igc/bp") + " " + self.proj + NOVERBOSE 
        cmd += "cd " + self.root + \
            " && patch -p1 < igc/patches/llvm/0001-add-marco-to-avoid-call-backtrace.patch" + NOVERBOSE
        os.system(cmd)
