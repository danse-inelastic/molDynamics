from pylab import *
from matplotlib.figure import Figure as MFigure

def extractColumns(filename,skipRows=0):
    'gets the columns from a file and returns them as arrays'
    f=file(filename,'r')
    lines=f.readlines()
    x=[];y=[]
    for line in lines[skipRows:]:
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


#x,y=extractColumns('KRdf.out')
#subplot(221)
#plot(x,y)
#title('K')
#axis(limits)

x,y=extractColumns('allRdf.out')
subplot(221)
plot(x,y)
#x,y=extractColumns('KC24_Experiment.txt',skipRows=1)
#plot(x,y)
title('all')
axis([0,20,0,0.004])


x,y=extractColumns('h2KRdf.out')
subplot(222)
plot(x,y)
title('H-K')
axis(limits)

subplot(223)
x,y=extractColumns('KC24_Experiment.txt',skipRows=1)
plot(x,y)
title('experiment')
#axis(limits)

x,y=extractColumns('h2Rdf.out')
subplot(224)
plot(x,y)


title('H')
axis(limits)

show()