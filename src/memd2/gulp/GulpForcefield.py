# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

class GulpForcefield:

    import pd
    path = pd.str(default='../content/data/gulppotentials')
    filename = pd.str()
    elements = pd.strArray(default = ['H'])
    description = pd.str()
    creator = pd.str()
    date = pd.date()
    potential_name = pd.str()
    dispersionInRecipSpace = pd.bool(default = False)
    dispersionInRecipSpace.meta['tip'] = '''whether to calculate dispersion forces 
partly in reciprocal space'''
    useInitialBondingOnly = pd.bool(label = 'Assign Bonding Based on Initial Geometry Only', default = False)
    useInitialBondingOnly.meta['tip'] = '''instead of reassigning bonding based on every optimization or time step, use intial geometry only to
assign bonding'''
    moleculeIdentification = pd.str(label = 'Try to Identify Molecules', default = "None")
    moleculeIdentification.meta['tip'] = '''identify molecules based on covalent radii 
and deal with intramolecular coulomb interactions'''
    moleculeIdentification.validator = pd.choice(['None','identify molecules; remove intramolecular Coulomb forces',
                                                 'identify molecules; retain intramolecular Coulomb forces'])
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
#    this should be the name of the primary key...for now we *have* to name it 'id'
#    potential_name = dsaw.db.varchar(name="potential_name", length=64)
#    potential_name.constraints = 'PRIMARY KEY'
#    potential_name.meta['tip'] = "the unique id"


# version
__id__ = "$Id$"

# End of file 
