from fft.calc import fft, GaussianWindow
from Scientific.IO.NetCDF import NetCDFFile

class VanHoveTransform:
    '''transform G(r,t) to S(Q,E)
    
G(r,t) is expected to be a grid of Nx by Ny by Nz points over a given volume prefaced by time in the following format:
0.0
x1 y1 z1
x1 y1 z2
x1 y1 z3
...
x1 y1 zNz
x1 y2 z1
x1 y2 z2
...
xNx yNy zNz
0.1  
x1 y1 z1
...
xNx yNy zNz
0.2
x1 y1 z1
...
xNx yNy zNz
..
0.2
x1 y1 z1
...
xNx yNy zNz
'''

    def __init__(self, Grt):
        self.Grt=Grt

    def IncoherentScatteringFunctionRTransform(traj,qVect,ncDataFN,
                                     atoms=None,bincoh=None,timeInfo=None,
                                     nsteps=None):
    
        file, filename = logfileInit('isf')
    
        if atoms is None: atoms = traj.universe
        if bincoh is None: bincoh = BincohList(traj.universe,atoms)
        tim    = timePrepare(traj,timeInfo)
        if nsteps is None:
            nsteps = len(tim)
        nsteps = min(nsteps, len(tim))
        Fincoh = zeros((nsteps,len(qVect[1])),Float)
     
        comment = ''
        try:
            comment = comment + 'Trajectory: ' + traj.filename + '\n'
        except AttributeError:
            pass
        
        file2 = NetCDFFile(ncDataFN, 'w', comment)
        file2.title = 'Incoherent Scattering Function'
        file2.createDimension('Q', None)
        file2.createDimension('TIME', nsteps)
        SF      = file2.createVariable('sf', Float, ('Q','TIME'))
        Time    = file2.createVariable('time', Float, ('TIME',))
        Qlength = file2.createVariable('q', Float, ('Q',))
        Time[:]=tim[:nsteps]
     
        for j in range(len(qVect[1])):
            qVect[1][j] = transpose(array(map(lambda v: v.array, qVect[1][j])))
    
        normFact = len(qVect[0])
        for j in range(len(qVect[0])):
            for at in atoms.atomList():
                sekw        = traj.readParticleTrajectory(at,first=timeInfo[0],\
                                   last=timeInfo[1],skip=timeInfo[2]).array
                series      = exp(1j*dot(sekw, qVect[1][j]))
                res         = AutoCorrelationFunction(series)[:nsteps]
                Fincoh[:,j] = Fincoh[:,j] + add.reduce(bincoh[at]*res,1)/\
                                            qVect[1][j].shape[1]
            SF[j,:]    = Fincoh[:,j]
            Qlength[j] = qVect[0][j]
            file2.flush()
            gj = logfileUpdate(file,j,normFact)
    
        cleanUp(file,filename)
        file2.close()
        return 

        
    def TimeTransform(ncResultsFN,ncDataFN,nfreq,alpha=5.):
        """ perform fft on previously calculated scattering functions """
        file, filename = logfileInit('sf_fft')

        ncin = NetCDFFile(ncResultsFN,'r')
        tim = ncin.variables['time']
        TimeStep = tim[1] - tim[0]
        frequencies = arange(len(tim))/(2.*len(tim)*TimeStep)
        sample = max(1, len(frequencies)/nfreq)
        nfreq = (len(frequencies)+sample-1)/sample
        ncout = NetCDFFile(ncDataFN,'w')
        ncout.title = 'Dynamic Structure Factor'
        ncout.createDimension('Q',None)
        ncout.createDimension('FREQUENCY',nfreq)
        SF    = ncout.createVariable('dsf',Float, ('Q','FREQUENCY'))
        FREQ  = ncout.createVariable('frequency',Float, ('FREQUENCY',))
        QLEN  = ncout.createVariable('q',Float, ('Q',))
    
        FREQ[:] = frequencies[::sample]
        gj = ncin.variables['q'][:]
        QLEN[0:len(gj):1] = gj
    
        i = 0
        normFact = len(ncin.variables['sf'])
        for qlen in range(normFact):
            SF[qlen] = 0.5*TimeStep * \
                       fft(GaussianWindow(ncin.variables['sf'][qlen],
                                          alpha)).real[:nfreq*sample:sample]
            i = logfileUpdate(file,i,normFact)
    
        cleanUp(file,filename)
        ncin.close()
        ncout.close()
        
        
        