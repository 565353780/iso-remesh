#include "adaptive_kernel.h"
#include "kernel.h"

#include <pybind11/pybind11.h>

PYBIND11_MODULE(remesh_cpp, m) {
  m.doc() = "pybind11 remesh cpp plugin";

  m.def("isoRemeshing", &isoRemeshing, "kernel.isoRemeshing");
  m.def("adaptiveIsoRemeshing", &adaptiveIsoRemeshing,
        "adaptive_kernel.adaptiveIsoRemeshing");
}
