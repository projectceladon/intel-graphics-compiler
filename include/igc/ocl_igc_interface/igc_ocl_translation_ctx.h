/*========================== begin_copyright_notice ============================

Copyright (C) 2017-2021 Intel Corporation

SPDX-License-Identifier: MIT

============================= end_copyright_notice ===========================*/

#pragma once

#include <cinttypes>

#include "cif/builtins/memory/buffer/buffer.h"
#include "cif/common/id.h"
#include "cif/common/cif.h"

#include "ocl_igc_interface/ocl_translation_output.h"

#include "cif/macros/enable.h"

// Interface : IGC_OCL_TRAC
//             "IGC - OCL" Translation Context
// Interface for invoking IGC translations from OCL runtime

namespace IGC {

CIF_DECLARE_INTERFACE(IgcOclTranslationCtx, "IGC_OCL_TRAC");

CIF_DEFINE_INTERFACE_VER(IgcOclTranslationCtx, 1) {
  CIF_INHERIT_CONSTRUCTOR();

  template <typename OclTranslationOutputInterface = OclTranslationOutputTagOCL>
  CIF::RAII::UPtr_t<OclTranslationOutputInterface> Translate(CIF::Builtins::BufferSimple *src,
                                                             CIF::Builtins::BufferSimple *options,
                                                             CIF::Builtins::BufferSimple *internalOptions,
                                                             CIF::Builtins::BufferSimple *tracingOptions,
                                                             uint32_t tracingOptionsCount) {
      auto p = TranslateImpl(OclTranslationOutputInterface::GetVersion(), src, options, internalOptions, tracingOptions, tracingOptionsCount);
      return CIF::RAII::Pack<OclTranslationOutputInterface>(p);
  }

protected:
  virtual OclTranslationOutputBase *TranslateImpl(CIF::Version_t outVersion,
                                                  CIF::Builtins::BufferSimple *src,
                                                  CIF::Builtins::BufferSimple *options,
                                                  CIF::Builtins::BufferSimple *internalOptions,
                                                  CIF::Builtins::BufferSimple *tracingOptions,
                                                  uint32_t tracingOptionsCount);
};

CIF_DEFINE_INTERFACE_VER_WITH_COMPATIBILITY(IgcOclTranslationCtx, 2, 1) {
  using IgcOclTranslationCtx<1>::TranslateImpl;
  using IgcOclTranslationCtx<1>::Translate;

  CIF_INHERIT_CONSTRUCTOR();

  template <typename OclTranslationOutputInterface = OclTranslationOutputTagOCL>
  CIF::RAII::UPtr_t<OclTranslationOutputInterface> Translate(CIF::Builtins::BufferSimple *src,
                                                             CIF::Builtins::BufferSimple *options,
                                                             CIF::Builtins::BufferSimple *internalOptions,
                                                             CIF::Builtins::BufferSimple *tracingOptions,
                                                             uint32_t tracingOptionsCount,
                                                             void *gtPinInput) {
      auto p = TranslateImpl(OclTranslationOutputInterface::GetVersion(), src, options, internalOptions, tracingOptions, tracingOptionsCount, gtPinInput);
      return CIF::RAII::Pack<OclTranslationOutputInterface>(p);
  }

protected:
  virtual OclTranslationOutputBase *TranslateImpl(CIF::Version_t outVersion,
                                                  CIF::Builtins::BufferSimple *src,
                                                  CIF::Builtins::BufferSimple *options,
                                                  CIF::Builtins::BufferSimple *internalOptions,
                                                  CIF::Builtins::BufferSimple *tracingOptions,
                                                  uint32_t tracingOptionsCount,
                                                  void *gtPinInput);
};

CIF_DEFINE_INTERFACE_VER_WITH_COMPATIBILITY(IgcOclTranslationCtx, 3, 2) {
  using IgcOclTranslationCtx<2>::TranslateImpl;
  using IgcOclTranslationCtx<2>::Translate;

  CIF_INHERIT_CONSTRUCTOR();

  template <typename OclTranslationOutputInterface = OclTranslationOutputTagOCL>
  CIF::RAII::UPtr_t<OclTranslationOutputInterface> Translate(CIF::Builtins::BufferSimple *src,
                                                             CIF::Builtins::BufferSimple *specConstantsIds,
                                                             CIF::Builtins::BufferSimple *specConstantsValues,
                                                             CIF::Builtins::BufferSimple *options,
                                                             CIF::Builtins::BufferSimple *internalOptions,
                                                             CIF::Builtins::BufferSimple *tracingOptions,
                                                             uint32_t tracingOptionsCount,
                                                             void *gtPinInput) {
      auto p = TranslateImpl(OclTranslationOutputInterface::GetVersion(), src, specConstantsIds, specConstantsValues, options, internalOptions, tracingOptions, tracingOptionsCount, gtPinInput);
      return CIF::RAII::Pack<OclTranslationOutputInterface>(p);
  }

  virtual bool GetSpecConstantsInfoImpl(CIF::Builtins::BufferSimple *src,
                                CIF::Builtins::BufferSimple *outSpecConstantsIds,
                                CIF::Builtins::BufferSimple *outSpecConstantsSizes);

protected:
  virtual OclTranslationOutputBase *TranslateImpl(CIF::Version_t outVersion,
                                                  CIF::Builtins::BufferSimple *src,
                                                  CIF::Builtins::BufferSimple *specConstantsIds,
                                                  CIF::Builtins::BufferSimple *specConstantsValues,
                                                  CIF::Builtins::BufferSimple *options,
                                                  CIF::Builtins::BufferSimple *internalOptions,
                                                  CIF::Builtins::BufferSimple *tracingOptions,
                                                  uint32_t tracingOptionsCount,
                                                  void *gtPinInput);
};

CIF_GENERATE_VERSIONS_LIST_AND_DECLARE_INTERFACE_DEPENDENCIES(IgcOclTranslationCtx, IGC::OclTranslationOutput, CIF::Builtins::Buffer);
CIF_MARK_LATEST_VERSION(IgcOclTranslationCtxLatest, IgcOclTranslationCtx);
using IgcOclTranslationCtxTagOCL = IgcOclTranslationCtxLatest; // Note : can tag with different version for
                                                               //        transition periods

}

#include "cif/macros/disable.h"
