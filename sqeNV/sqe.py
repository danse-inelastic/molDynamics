#from crystal import CrystalStructure
from math import tanh


class sqeFactory:
    
    gammaPointCalc=False
    hbar=6.58211899e-16*10e12*10e3#eV*s * ps/s * meV/eV = meV*ps
    kB=8.61734315e-5*10e3 #ev/K * meV/eV
    
    #eventually this can be generalized to liquids or polymers
    def __init__(self,eigenvalues=[],eigenvectors=[[]],atoms=[['Fe',0.0,0.0,0.0],['Fe',0.5,0.5,0.5]],
                 lattice=[[2.8665,0.0,0.0],[0.0,2.8665,0.0],[0.0,0.0,2.8665]],temperature=300.0):
        self.eigvals = eigenvalues
        self.eigvecs = eigenvectors
        self.atoms = atoms
        self.lattice = lattice
        self.nd=len(atoms)
        self.temperature=temperature
    
        
    def Sqe(self):
        pass
        
    def Sqomega(self,Q,omega): 
        '''omega should be in ps'''
        sqomega=self.nd/2.0*Q**2/omega*self.boseFactorPlus1(omega)
        
        return sqomega
        
    def beta(self):
        return 1./(self.kB*self.temperature)
        
    def boseFactorPlus1(self,omega):
        trig=tanh(0.5*self.hbar*omega*self.beta())
        return 0.5*((1+trig)/trig)