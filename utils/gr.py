#!/usr/bin/python
"""
gr.py 
calculate radial distribution function of ATOMS_AROUND atoms type
around atomas of a type given as ATOM_CENTRAL using the trajectory
given in xyz format file
In the output file it prints: g(r)_id_gas_norm normalized to the number of
particles in the ideal gas and its integral gives 1,
g(r)_unnorm (where: g(r)_id_gas_norm = g(r)_unnorm / n_ideal), and g(r)_unnorm_cumsum - cumulative sum of g(r)_unnorm multiplied by number of
ATOMS_AROUND type atoms, i.e., g(r)_unnorm_cumsum gives coordination number
for atoms ATOMS_AROUND around atoms ATOMS_CENTRAL (maximum value of g(r)_unnorm_cumsum
gives number of atoms ATOMS_AROUND in the box)


Usage:
gr.py [OPTIONS] ATOMS_CENTRAL ATOMS_AROUND LX LY LZ

ATOMS1, ATOM2
symbols of atoms for which pair analysis will be performed
(may be the same in order to get self-correlation function)

LX, LY, LZ
periodic box lengths on x, y and z direction (not needed if
-n option is set)

Options:
--help or -h
print this message
-i argument
name in input file (in xyz format, coords.xyz is default)
-o argument
name of output file (gr.out as default)
-f argument
number of first time frame to analysis, first frame is default
-t argument
number of last time frame to analysis, last frame is default
-b argument
bean size (0.02 is default)
-n
turn off periodic boundary conditions (pbc are assumed by
default), LX, LY, LZ not needed
-x
take into account all atoms (ATOM1 and ATOM2 must not be set)
"""

import sys, os, math, glob, getopt, string

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class Opts:
    "A class for input options"
    def __init__(self):
        self.in_filename = "coords.xyz"
        self.out_filename = "gr.out"
        self.first_frame = 0
        self.last_frame = 0
        self.bean = 0.02
        self.atom1 = ""
        self.atom2 = ""
        self.lx = 0.0
        self.ly = 0.0
        self.lz = 0.0
        self.non_periodic = False
        self.all_atoms = False
        self.err=""
    def check(self):
        if self.bean <= 0:
            self.err = "bean must be a positive number"
            return False
        if self.first_frame < 0:
            self.err = "first frame number must be greater than 0"
            return False
        if self.last_frame < 0:
            self.err = "last frame number must be greater than 0"
            return False
        if self.in_filename != "" and not(os.path.isfile(self.in_filename)):
             self.err = "cannot find input file: " + self.in_filename
             return False
        if (self.non_periodic == False) and (self.lx<=0 or self.ly<=0 or self.lz<=0):
            self.err = "Box lengths must be greater than zero for p.b.c."
            return False
        if (self.atom1 == "" or self.atom2 == "") and (self.all_atoms == False):
            self.err = "Symbols of two types of atoms are required"
            return False
        if (self.atom1 != "" or self.atom2 != "") and (self.all_atoms == True):
            self.err = "Symbols of atoms cannot be specified when -x option is used"
            return False
        return True

class TimeFrame:
    "A single time frame"
    def __init__(self):
        self.symbol = []
        self.coords = []
        self.n_analyzed = 0 #number of analyzed pairs * 2 (Allen's concept ;))
        self.n_atoms = 0
    def getGrHistogram(self, opts):
        "Returns g(r) histogram"
        hist = []
        #based on Allen Ch. 6.2)
        self.n_analyzed = 0
        ##atoms_list = [opts.atom1, opts.atom2]
        atoms_list = [opts.atom2] #only atoms of the second type are taken for normalization
        #calculation of number of considered atoms (needed for ideal-gas normalization later)
        for ac in self.symbol:
            if (opts.all_atoms == False):
                if ac in atoms_list:
                    self.n_atoms += 1
            else:
                self.n_atoms = len(self.symbol)
        
        for i in range(len(self.symbol)-1):
            for j in range(i+1, len(self.symbol)):
                if (opts.all_atoms == False):
                    if not ((self.symbol[i]==opts.atom1 and self.symbol[j]==opts.atom2) \
                            or (self.symbol[i]==opts.atom2 and self.symbol[j]==opts.atom1)):
                        continue

                self.n_analyzed += 2 #+2 (pairs of atoms)
                #calculation of minimum image distance (Allen Ch. 1.5.4) (if periodicity was enabled)
                xi, yi, zi = self.coords[i]
                xj, yj, zj = self.coords[j]
                rxij = abs(float(xi) - float(xj))
                ryij = abs(float(yi) - float(yj))
                rzij = abs(float(zi) - float(zj))
                if (opts.non_periodic == False): # pbc are used
                    rxij = rxij - opts.lx * round(float(rxij) / opts.lx)
                    ryij = ryij - opts.ly * round(float(ryij) / opts.ly)
                    rzij = rzij - opts.lz * round(float(rzij) / opts.lz)
                #end of calculation of minimum image distance
                rijsq = rxij * rxij + ryij * ryij + rzij * rzij
                rij = math.sqrt(rijsq)
                bin = int(rij / opts.bean) # in Allen: bin = int(rij / bean) + 1 but we have zero-based indexing in Python :)
                while (len(hist) < bin+1): # 'bin+1' due to zero-based indexing too :)
                    hist.append(0)
                hist[bin] = hist[bin] + 2
        return hist
    def getMinMax(self, symbols_to_consider):
        a_min = 0.0
        a_max = 0.0
        for i in range(len(self.symbol)):
            if i==0: # initial setting of a_min and a_max
                a_min = self.coords[0]
                a_max = self.coords[0]
            if len(symbols_to_consider) > 0:
                if self.symbol[i] in symbols_to_consider:
                    if self.coords[i] < a_min:
                        a_min = self.coords[i]
                    if self.coords[i] > a_max:
                        a_max = self.coords[i]
            else:
                if self.coords[i] < a_min:
                    a_min = self.coords[i]
                if self.coords[i] > a_max:
                    a_max = self.coords[i]
        return (a_min, a_max)

def main(argv=None):

    debug = False
    
    if argv == None:
        argv = sys.argv

    try:

        #command line arguments parsing
        try:
            options, args = getopt.getopt(argv[1:], "hi:o:f:t:b:nx", ["help"])
        except getopt.GetoptError, msg:
            print msg
            sys.exit(2)

        #first step: parsing options (if any)
        opts = Opts()
        for o, a in options:
            if o == "-h" or o == "--help" :
                print __doc__
                raise Usage, ""
            if o == "-i":
                opts.in_filename = a
            if o == "-o":
                opts.out_filename = a
            if o == "-f":
                opts.first_frame = int(a)
            if o == "-t":
                opts.last_frame = int(a)
            if o == "-b":
                opts.bean = float(a)
            if o == "-n":
                opts.non_periodic = True
            if o == "-x":
                opts.all_atoms = True

        #second step: parsing remaining arguments

        if (opts.all_atoms == False):
            if len(args) >= 2:
                opts.atom1 = str(args[0])
                opts.atom2 = str(args[1])
            if len(args) >= 5:
                opts.lx = float(args[2])
                opts.ly = float(args[3])
                opts.lz = float(args[4])
        else:
            if len(args)>=3:
                opts.lx = float(args[0])
                opts.ly = float(args[1])
                opts.lz = float(args[2])
        
        if not(opts.check()):
            raise Usage, opts.err
        #end of command line arguments parsing

        print "# 1/3 Opening coordinates file:", opts.in_filename
        f = open(opts.in_filename, "r")

        print "# 2/3 Calculating"
        grHistogram = []
        totalFramesCounter = 0
        analyzedFramesCounter = 0
        n_atoms_in_file = -1 #only at the beginning
        numberParsed = False
        commentParsed = False
        atomsCounter = 0

        print "#  from frame :", opts.first_frame
        print "#  to frame   :", opts.last_frame

        n_atoms = 0
        n_analyzed = 0
        for line in f:
            
            if (not numberParsed):
                n_atoms_in_file = int(line)
                currentFrame = TimeFrame()
                numberParsed = True
            elif (not commentParsed):
                commentParsed = True
            else:
                spl = line.split()
                currentFrame.symbol.append(str(spl[0]))
                x = spl[1]
                y = spl[2]
                z = spl[3]
                currentFrame.coords.append((x, y, z))
                atomsCounter += 1
                if atomsCounter == n_atoms_in_file:
                    totalFramesCounter += 1
                    if ((totalFramesCounter)%100 == 0 \
                        or totalFramesCounter == 1 \
                        or totalFramesCounter == opts.first_frame \
                        or totalFramesCounter == opts.last_frame) :
                        print "#  -> frame no.", totalFramesCounter
                    if (totalFramesCounter >= opts.first_frame and \
                        (opts.last_frame == 0 or totalFramesCounter <= opts.last_frame)):
                        analyzedFramesCounter += 1

                        currentGrHistogram = currentFrame.getGrHistogram(opts)

                        if n_analyzed == 0: #at the beginning
                            n_analyzed = currentFrame.n_analyzed
                        else:
                            if n_analyzed != currentFrame.n_analyzed:
                                err = "Error: number of analyzed atom pairs changes along trajectory"
                                raise Usage, err
                        if (currentFrame.n_analyzed <= 0):
                            err = "Error: no pair for analysis found! Check atoms list!"
                            raise Usage, err

                        if (n_atoms == 0): #at the beginning
                            n_atoms = currentFrame.n_atoms
                        else:
                            #checking if number of atoms is constant along trajectory
                            if (n_atoms != currentFrame.n_atoms):
                                err = "Error: number of atoms changes along trajectory"
                                raise Usage, err

                        while (len(grHistogram) < len(currentGrHistogram)):
                            grHistogram.append(0)

                        for i in range(len(currentGrHistogram)):
                            grHistogram[i] += currentGrHistogram[i]
                        if debug:
                            print currentFrame.symbol
                            print currentFrame.coords
                    frameParsed = False
                    numberParsed = False
                    commentParsed = False
                    atomsCounter = 0

        f.close()

        #normalization (second phase)
        # a/ normalize with respect to the number of analyzed frames and divided by number of atoms of second type (i.e., n_atoms)
        if (n_atoms <= 0):
                err = "Error during normalization! ( n_atoms ==" + str(n_atoms) + ")"
                raise Usage, err
        
        for i_normf in range(len(grHistogram)):
            grHistogram[i_normf] = float(grHistogram[i_normf]) / analyzedFramesCounter / n_analyzed
        # storing unnormalized to the ideal gas data and cumulative sum (for printing)
        #and multiplying by number of atoms of second type!
        grHistogramUnnorm = []
        grCumSumm = []
        csumm = 0.0
        for nnh in range(len(grHistogram)):
            grHistogramUnnorm.append(grHistogram[nnh])
            csumm += grHistogram[nnh]
            grCumSumm.append(csumm*n_atoms)
        
        # b/ normalize with respect to the ideal gas
        if (opts.non_periodic == False): # if pbc are used 
            volume = float(opts.lx * opts.ly * opts.lz)
        else:
            volume = 1.0 # volume=unity / why not ;)
        rho = float(n_atoms) / volume
        ideal_constant = 4.0 * math.pi * rho / 3.0
        for i_norm in range(len(grHistogram)):
            #Allen Ch. 6.2 (but here with zero-based indexing)
            rlower = i_norm * opts.bean
            rupper = rlower + opts.bean
            nideal = ideal_constant * (math.pow(rupper,3) - math.pow(rlower,3))
            grHistogram[i_norm] = float(grHistogram[i_norm]) / nideal

        fo = open(opts.out_filename, "w")

        out_line = "# gr.py output, gr.py by Lukasz Cwiklik, cwiklik<at>gmail.com\n"
        fo.write(out_line)
        out_line = "# radial distribution function for"
        if (opts.all_atoms == False):
            out_line += " atoms: " + opts.atom1 + " and " + opts.atom2
        else:
            out_line += " all atoms"
        out_line += "\n"
        fo.write(out_line)
        out_line = "# periodic boundary conditions "
        if (opts.non_periodic == False):
            out_line += "used (box size: " + str(opts.lx) + " x " \
                        + str(opts.ly) + " x " + str(opts.lz) + ")\n"
        else:
            out_line += "not used\n"
        fo.write(out_line)
        out_line =  "# number of analyzed time frames: " + str(analyzedFramesCounter) + "\n"
        fo.write(out_line)
        out_line = "#r".ljust(20) + \
              "g(r)_id_gas_norm".ljust(20) + \
              "g(r)_unnonorm".ljust(20) + \
              "g(r)_unnorm_cumsum".ljust(20) + "\n"
        fo.write(out_line)
        for i in range(len(grHistogram)):
            curr_r = 0.5*opts.bean + i * opts.bean
            out_line = str("%.5f"%curr_r).ljust(20) + \
                  str("%.5f"%grHistogram[i]).ljust(20) + \
                  str("%.5f"%grHistogramUnnorm[i]).ljust(20) + \
                  str("%.5f"%grCumSumm[i]).ljust(20) + "\n"
            fo.write(out_line)

        out_line = "# end\n"
        fo.write(out_line)
        
        fo.close()

        print "# 3/3 Finished successfully ( results in:", opts.out_filename, ")"
        sys.exit()
        
        
    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())

