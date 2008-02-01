from pylab import *
from matplotlib.figure import Figure as MFigure

def extractColumns(filename):
    'gets the columns from a file and returns them as arrays'
    f=file(filename,'r')
    lines=f.readlines()
    x=[];y=[]
    for line in lines:
        if line[0]=="#":continue 
        words=line.split()
        if words==[]: continue
        x.append(float(words[0]))
        y.append(float(words[1]))
#            from decimal import Decimal
#            x.append(float(Decimal(eval(words[0]))))
#            y.append(float(Decimal(eval(words[1]))))
    import numpy as nx
    return nx.array(x),nx.array(y)

paths='KRdf.out','h2KRdf.out','kH2Rdf.out','h2Rdf.out'

limits = [0, 20, 0, 0.08]


x,y=extractColumns('KRdf.out')
subplot(221)
plot(x,y)
title('K')
axis(limits)


x,y=extractColumns('h2KRdf.out')
subplot(222)
plot(x,y)
title('H-K')
axis(limits)

x,y=extractColumns('allRdf.out')
subplot(223)
plot(x,y)
title('all')
axis(limits)

x,y=extractColumns('h2Rdf.out')
subplot(224)
plot(x,y)
x,y=extractColumns('h2Rdf.out')
plot(x,y)

title('H')
axis(limits)

show()