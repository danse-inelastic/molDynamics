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

#include "misc.h"
#include "libmolDynamics/hello.h"


// copyright

char pymolDynamics_copyright__doc__[] = "";
char pymolDynamics_copyright__name__[] = "copyright";

static char pymolDynamics_copyright_note[] = 
    "molDynamics python module: Copyright (c) 1998-2005 Michael A.G. Aivazis";


PyObject * pymolDynamics_copyright(PyObject *, PyObject *)
{
    return Py_BuildValue("s", pymolDynamics_copyright_note);
}
    
// hello

char pymolDynamics_hello__doc__[] = "";
char pymolDynamics_hello__name__[] = "hello";

PyObject * pymolDynamics_hello(PyObject *, PyObject *)
{
    return Py_BuildValue("s", hello());
}
    
// version
// $Id$

// End of file
