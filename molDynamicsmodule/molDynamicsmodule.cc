// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>

#include <Python.h>

#include "exceptions.h"
#include "bindings.h"


char pymolDynamics_module__doc__[] = "";

// Initialization function for the module (*must* be called initmolDynamics)
extern "C"
void
initmolDynamics()
{
    // create the module and add the functions
    PyObject * m = Py_InitModule4(
        "molDynamics", pymolDynamics_methods,
        pymolDynamics_module__doc__, 0, PYTHON_API_VERSION);

    // get its dictionary
    PyObject * d = PyModule_GetDict(m);

    // check for errors
    if (PyErr_Occurred()) {
        Py_FatalError("can't initialize module molDynamics");
    }

    // install the module exceptions
    pymolDynamics_runtimeError = PyErr_NewException("molDynamics.runtime", 0, 0);
    PyDict_SetItemString(d, "RuntimeException", pymolDynamics_runtimeError);

    return;
}

// version
// $Id$

// End of file
