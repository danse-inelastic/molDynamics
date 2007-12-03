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

#include "bindings.h"

#include "misc.h"          // miscellaneous methods

// the method table

struct PyMethodDef pymolDynamics_methods[] = {

    // dummy entry for testing
    {pymolDynamics_hello__name__, pymolDynamics_hello,
     METH_VARARGS, pymolDynamics_hello__doc__},

    {pymolDynamics_copyright__name__, pymolDynamics_copyright,
     METH_VARARGS, pymolDynamics_copyright__doc__},


// Sentinel
    {0, 0}
};

// version
// $Id$

// End of file
