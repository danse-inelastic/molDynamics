from pycdf import *
d=CDF('test.nc',NC.WRITE|NC.CREATE)
d.automode()
d3=d.def_dim('d1',3)
v1=d.def_var('v1',NC.INT,d3)            # 3-elem vector
v1[:]=[1,2,3]                           # assign 3-elem python list
v2=d.def_var('d2',NC.INT,(d3,d3))       # create 3x3 variable
           # The list assigned to v2 is composed
           # of 3 lists, each representing a row