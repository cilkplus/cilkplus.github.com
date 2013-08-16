Intel® Cilk™ Plus is an extension to the C and C++ languages to support data and task parallelism.  It is one of the easiest, quickest way to harness the power of both multicore and vector processing.  Visit [cilkplus.org](http://cilkplus.org) for details.

This project implements the Intel® Cilk™ Plus language extensions in the [Clang](http://clang.llvm.org) frontend for [LLVM](http://llvm.org).  There are two other implementations available.  A commercial version of Cilk Plus is available as part of the [Intel® C++ Composer XE compiler](http://software.intel.com/en-us/intel-composer-xe/).  There is also an open source version available in the "cilkplus" branch of the GCC C/C++ compiler.  More information is available on [cilkplus.org](http://cilkplus.org/which-license).

News
====
June 7, 2013 - All known exception handling issues have been resolved.
May 7, 2013 - cilk\_for is now supported, including #pragma grainsize. The runtime was updated to the [latest version](http://cilkplus.org/download#runtime-sources).
March 26, 2013 - Autoconf/Make build is now supported. The known issue regarding exceptions in initializers is resolved.

<a name="try"></a>
Try Cilk Plus/LLVM
==================

_Note: Cilk Plus/LLVM does not yet support all of the Intel® Cilk™ Plus extensions.  See [Status](#status)._

### Requirements

Most software and hardware requirements are the same as for [LLVM](http://llvm.org/docs/GettingStarted.html#requirements).  However, support is currently limited to 64 bit Linux and Mac OS X - see [status](#status) for details on supported configurations and known issues.

CMake *version 2.8.8 or greater* is required to compile compiler-rt when using the recommended build process. Alternatively, it is also possible to use configure/make by following the directions at http://clang.llvm.org/get_started.html.

### Getting the source code

```
$ git clone -b cilkplus https://github.com/cilkplus/llvm
$ git clone -b cilkplus https://github.com/cilkplus/clang llvm/tools/clang
$ git clone -b cilkplus https://github.com/cilkplus/compiler-rt llvm/projects/compiler-rt
```

The source code structure follows Clang/LLVM: http://llvm.org/docs/GettingStarted.html.

### Building

The recommended way to build Cilk Plus/LLVM is using CMake.  Detailed instructions on how to build Clang/LLVM/Compiler-rt with CMake can be found in the following page: http://llvm.org/docs/CMake.html.  In the following command, make sure to replace `/install/prefix` with the location where you would like to install the binaries.

```
$ cd llvm
$ mkdir build && cd build
$ cmake -DCMAKE_INSTALL_PREFIX=/install/prefix -DCMAKE_BUILD_TYPE=Release \
        -DLLVM_TARGETS_TO_BUILD=X86 ..
$ make && make install
```

_Mac OS X_

The basic steps are the same as above.  However, on Mac OS X it is recommended to build with the Clang compiler shipped with the OS.  Add the following definitions to the cmake command above.

```
-DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++
```

### Using

To use the newly installed compiler, add the following to your environment.  On Mac OS X, replace LD_LIBRARY_PATH with DYLD_LIBRARY_PATH.

```
export PATH=/install/prefix/bin:$PATH
export C_INCLUDE_PATH=/install/prefix/include:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=/install/prefix/include:$CPLUS_INCLUDE_PATH
export LIBRARY_PATH=/install/prefix/lib:$LIBRARY_PATH
export LD_LIBRARY_PATH=/install/prefix/lib:$LD_LIBRARY_PATH
```

When you build a program that uses Intel® Cilk™ Plus extensions, add the following option to enable Cilk Plus support and link to the runtime library.
```
-fcilkplus
```

### A simple program

```
#include <cilk/cilk.h>
#include <assert.h>

int fib(int n) {
  if (n < 2)
    return n;
  int a = cilk_spawn fib(n-1);
  int b = fib(n-2);
  cilk_sync;
  return a + b;
}

int main() {
  int result = fib(30);
  assert(result == 832040);
  return 0;
} 
```

Confirm that the compiler is working correctly by saving the above code code to a file.

```
$ clang -fcilkplus test.c -o test
$ ./test
```

You can check that the code is executing in parallel by using the time command and CILK_NWORKERS environment variable to control the number of workers.

```
$ CILK_NWORKERS=1 time ./test
$ CILK_NWORKERS=2 time ./test
$ CILK_NWORKERS=4 time ./test
```

<a name="status"></a>
Status
======

### What works right now

[check]: images/green_check.png "Yes"

|  Feature                | Supported?    |
|-------------------------|:-------------:|
| cilk\_spawn, cilk\_sync | ![check]      |
| cilk\_for               | ![check]      |
| hyperobjects            | ![check]      |
| #pragma simd            |               | 
| elemental functions     |               | 
| array notation          |               | 

### Supported platforms

OS: Linux or Mac OS X
Architecture: x86-64

### Known issues

* Using variable-length arrays in a spawning function does not work yet.

<a name="license"></a>
License
=======

LLVM, Clang, and Compiler-rt are distributed under LLVM's ["UIUC" BSD-Style license](http://llvm.org/docs/DeveloperPolicy.html#license).  For details, including information about third-party components, see LICENSE.txt in the code repositories.

The Intel® Cilk™ Plus runtime library is distributed under a [BSD 3-Clause license](http://opensource.org/licenses/BSD-3-Clause).

<a name="contact"></a>
Contact
=======

If you would like to report a bug, or make a feature request, you can submit an issue in Github [here](https://github.com/cilkplus/clang/issues).

You can also contact us via the the [Intel Cilk Plus forum](http://software.intel.com/en-us/forums/intel-cilk-plus/) on the Intel Developer Zone.
