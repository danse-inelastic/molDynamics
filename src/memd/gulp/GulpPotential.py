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

class GulpPotential:

    path = '../content/data/gulppotentials'
    filename = 'potential.lib'
    elements = []
    description = ''
    creator = ''
    date = ''
    potential_name = ''
#    this should be the name of the primary key...for now we *have* to name it 'id'
#    potential_name = dsaw.db.varchar(name="potential_name", length=64)
#    potential_name.constraints = 'PRIMARY KEY'
#    potential_name.meta['tip'] = "the unique id"


# version
__id__ = "$Id$"

# End of file 
