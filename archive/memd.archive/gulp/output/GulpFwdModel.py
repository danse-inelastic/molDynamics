###########################################################
# Gulp forwad model for:
# calculation frequency difference cost function
# for using with mystic optimization framework
#
# Chen W. Li
# California Institute of Technology
###########################################################

__author__="Chen W. Li"
__date__ ="$Sep 9, 2009 8:46:13 AM$"

# initial guess param for ZrO2
initial_guess = \
  [1453.8, 0.35000, 0.0, 22764.0, 0.14900, 27.87900, 74.92]
# Zr-O ^      ^      ^ ||O-O  ^     ^       ^   ||O spring^

# experimental Raman frequency as target value
target_freq = [0,0,0,99,0,177,
              0,189,222,0,305,0,
              0,0,0,0,331,343,
              0,376,376,429,0,0,
              498,0,534,0,557,0,
              613,633,0,0,0,0]


def filter(target):
    """    Make a filter by comparing to the target data    """
    from numpy import array
    mask = [int(i) for i in array(target) > 0]
    mask[0] = 1
    mask[1] = 1
    mask[2] = 1
    return mask


def forward(Param):
    """    Forward function for Gulp frequency calculation     """

    from os import system
    potentials = potentialGenerator(Param)
    assemble('gin','templet.gin', potentials)
#   print "forwad calculating..."
#   system('eval "`/usr/bin/use -c`"; use gulpp 2> /dev/null; gulp < gin > gout')
#   setting up gulp envoirment is up to user
    system('gulp < gin > gout')
    freq = parsing('gout')
    return freq


def cost_factory(target):
    """    Cost function generator for Gulp frequency calculation    """

    from numpy import array
    mask = filter(target)

    def cost(Param):
        """    Cost function for Gulp frequency calculation     """

        freq = array(forward(Param)) * array(mask)
        diff = array(target) - freq
#        print "Cost: ",sum(diff*diff)
        return sum(diff*diff)

    return cost


def parsing(OutputFile):
    """    Parsing output file for frequency    """

    from kernelGenerator.gulp.OutputParser import OutputParser as op

    x = op(OutputFile,"phonons")
    x.convertToEnergies = False
    x.numKpoints = 1
    x.numModes = 36

    return x.getGammaPtEigenvalues()

def assemble(InputFile, InputTemplet, Potentials):
    """    Assemble input file from templet    """

    from shutil import copyfile

    copyfile(InputTemplet, InputFile)
    f = open(InputFile,'a')
    for s in Potentials:
        f.write(s)
    f.close()

def potentialGenerator(Param):
    """ Generate potential from Parameters for ZrO2"""

    potentials = ["","","","",""]
    potentials[0] = "buckingham\n"
    potentials[1] = "Zr_4+ core O shel "+str(Param[0])+" "+str(Param[1])+" "+str(Param[2])+" 0.0 10.0\n"
    potentials[2] = "O shel O shel "+str(Param[3])+" "+str(Param[4])+" "+str(Param[5])+" 0.0 12.0\n"
    potentials[3] = "spring\n"
    potentials[4] = "O "+str(Param[6])+" \n"
    
    return potentials
