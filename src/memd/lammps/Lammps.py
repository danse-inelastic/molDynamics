from memd.MolDynamics import MolDynamics
from os import linesep

class Lammps(MolDynamics):
    """Lammps engine for MolDynamics interface.  
    """
        
    def __init__(self, **kwds):
        MolDynamics.__init__(self, **kwds)
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        
    def getInputfile(self,o):
        lines=''
        lines+=o.units+linesep
        if True:#o.how_to_input_atoms=='specify atom creation parameters':
            #print dir(o)
            for region in o.lammpsregion_set.all():
                lines+='region '+region.region_id+' '+region.style+' '+region.args+linesep
                lines+='create_box '+str(len(o.structure.getMatterObject().getSpecies()))+\
                    ' '+region.region_id+linesep
    #        lattice = o.structure.lattice
    #        al,be,ga=lattice.abcABG[3:]
    #        if self.appEqual(al, 90.0) and self.appEqual(be, 90.0) and self.appEqual(ga, 90.0):
    #            lines+='region '+ o.region_name+' '+o.region+' '+o.region_parameters+linesep
    #            lines+='create_box '+str(len(o.structure.getSpecies()))+' '+o.region_name+linesep
    #        else:
    #            lines+=''
            lines+='create_atoms '+o.number_of_atom_species_to_create+' '+o.style_of_atom_creation+\
                ' '+o.style_of_atom_creation_args
            lines+='mass '+o.atom_masses+linesep
            lines+='velocity '+o.style_of_atom_velocity+' '+o.style_of_atom_velocity_options+linesep
        else:
            pass
        lines+='pair_style '+o.pair_interaction_potential+' '+o.pair_interaction_options+linesep
        lines+='pair_coeff '+o.pair_interaction_coefficients
        if o.skin_distance_for_pairwise_neighbor_lists!='default':
            lines+='neighbor '+o.skin_distance_for_pairwise_neighbor_lists+o.neighbor_list_algorithm+linesep
        lines+='neigh_modify '+o.neighbor_list_options+' '+o.neighbor_list_option_args+' '
        if o.only_build_neighbor_list_if_atom_has_moved_more_than_half_skin_distance:
            lines+='check yes '
        if o.only_build_neighbor_list_at_beginning_of_run:
            lines+='once yes '
        lines+=linesep
        # fix commands
        for fix in o.lammpsfix_set.all():
            lines+=fix.fix_id+' '+fix.group_id+' '+fix.style+' '+fix.options+linesep
        for dump in o.lammpsdump_set.all():
            lines+='dump '+dump.dump_id+' '+dump.style+' '+dump.style_args+' '+\
                dump.dump_every_n_timesteps+' '+dump.dump_filename+linesep
        lines+='thermo '+o.output_thermodynamics_every_n_timesteps+linesep
        # execution
        lines+='run '+o.number_of_timesteps+' '+o.run_options+' '+o.run_option_args+linesep
        
        return lines
    
    def writeInputfile(self,o):
        contents = self.getInputfile(o)
        #now write them
        file(o.input_files.split()[0],'w').write(contents)
        
    def _ind(self,list):
        """gives the indices of the list to iterate over"""
        return range(len(list))
    
    def appEqual(self,v1,v2):
        if abs(v1-v2)<10**-6:
            return True
        else:
            return False
