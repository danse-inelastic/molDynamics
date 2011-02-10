#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#              (C) 2007 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
import os, sys
from time import asctime
from vsat.Trajectory import Trajectory
from vsat.trajectory.ParnasisFileCreate import ParnasisFileCreate

class MdAnalysis(object):
    '''base class for common md analysis'''
    
    selected_atoms = 'All'
    #matter = None
    
    def __init__(self):
        #self.abbrev = None
        self._trajectory = None
        self._outputFiles = None
        self._outputFileBase = None
        self._basename = 'analysis'

    def _getTrajectory(self):
        return self._trajectory
    def _setTrajectory(self, traj):
        self._trajectory = traj
        self._initializeAtomAndTimeSelection()
    trajectory=property(_getTrajectory,_setTrajectory)
    
    def _getInputData(self):
        self._initializeAtomAndTimeSelection()
#        vars = ['selected_atoms', 'q_range_iso', 'q_resolution', 
#                'weights', 'time_steps_sampled']
        settings={}
#        v= vars(self)
#        b = dict(self.__class__.__dict__)
#        b.update(self.__dict__)
        d = dir(self)
#        class Hi: pass
#        def hi(): pass
        publicFunctions = ['writeInputFile','Inventory','customizeLubanObjectDrawer']
        for key in d:#.iteritems():
            #if key[0]=='_' or type(key)==type(Hi) or type(key)==type(hi):
            if key[0]=='_' or key in publicFunctions:
                pass
            else:
                #settings[key] = val#getattr(self, key)
                settings[key] = getattr(self, key)
        #hack--because need to update value
        settings['output_files'] = self.output_files
        self.parnasisFileCreate = ParnasisFileCreate(self, settings)
        return self.parnasisFileCreate.createInputFile()  
    
    def _prepareAttributeVals(self, attributes): 
        varVals = []
        for attribute in attributes:
            val=getattr(self, attribute)
            if type(val)==str:
                val= "'"+val+"'"
            varVals.append((attribute, val))
        return varVals
    
    @property
    def _calcKeyword(self):
        return self.__class__.__name__
    
    @property
    def _inputFileName(self):
        return self._calcKeyword+'.inp'
    
    def _getInputFile(self):
        inputFileLines = self._getInputData()
        fileText = ''
        for inputFileLine in inputFileLines:
            fileText+=inputFileLine[0]+'\n' 
        return fileText
    
    def writeInputFile(self,path='.'):
        inputFileContents = self._getInputData()
        #open('csfiso.inp','w').write(inputFileContents)
        self._saveText(data = inputFileContents,path=path)
    
    def _initializeAtomAndTimeSelection(self):
        if self.trajectory: #sometimes trajectory is set to None so this doesn't execute
            if self.selected_atoms=='All':
                self.selected_atoms = dict([(specie,'All') for specie in self.trajectory.species])
            if self.time_steps_sampled[0]==0 and self.time_steps_sampled[1]==0 and \
            self.time_steps_sampled[2]==1:
                self.time_steps_sampled = (0, self.trajectory.num_timesteps, 1)
            self._basename = self.trajectory.base_name
            
    def _get_time_steps_sampled(self):
        if not hasattr(self, '_time_steps_sampled'):
            if self.trajectory:
                self._time_steps_sampled = (0, self.trajectory.num_timesteps, 1)
            else:
                self._time_steps_sampled = (0,0,1)
        return self._time_steps_sampled
    def _set_time_steps_sampled(self, val):
        self._time_steps_sampled = val
    time_steps_sampled=property(_get_time_steps_sampled, _set_time_steps_sampled)
    
    def _formatSelectedAtoms(self, speciesList):
        formatted = {}
        for species in speciesList:
            formatted[species] = ['*']
        return str(formatted)
    
    def _saveText(self, data = None, path='.', filename = None, title = None, units = None):
        """
        This function write some data in a text file line by line.
        Arguments:
            data: 2D list. The data to write in the text file.
            filename: string. The name of the text file. If None, a Tkinter file dialog is opened for selecting
            the file name.
            title: string. The header of the text file. If None, 'pMoldyn data' is used as default.
            units: list of  strings. The list of units for each column.
        """
        if data is None:
            raise ValueError, "no data to be saved"
        if title is None:
            title = "parnasis data"
        if filename==None:
            filename = self._type+'.inp'
            if sys.platform == 'win32':
                from win32api import GetUserName
                # Stores in |owner| who owns the session where nMoldyn was executed.
                owner = GetUserName()
            else:
                from pwd import getpwuid
                from os import getuid
                owner = getpwuid(getuid())[0]
            file = open(os.path.join(path,filename),'w')
            line = '#\n# '
            line += title + '\n'
            line += "# Created by: " + owner + '\n' 
            line += "# Date of creation: " + asctime() + '\n'
            if units is not None:
                line += "# Units:\n"
                line += "# "
                for unit in units:
                    line += unit + '\t'
                line += '\n'
            line += '#\n'
            file.write(line)
            for i in range(len(data)):
                line = ''
                for ia in range(len(data[i])):
                    line = line + str(data[i][ia]) + ' '
                line = line + '\n'
                file.write(line)
            file.close()
    
        return filename
        
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        #drawer.mold.sequence = ['trajectory','','']
        def _createfield_for_trajectory(obj):
            # this is a method of mold.
            self = drawer.mold
            # imports
            #try:
            import luban.content as lc
            from luban.content import load, select
#            from luban.content.FormSelectorField import FormSelectorField
            # utils
            orm = self.orm
            # data 
            record = self.orm(obj)
            referred_record = record.trajectory and record.trajectory.id \
                              and record.trajectory.dereference(self.orm.db)
            # widget
            doc = lc.document(Class='container', id='neutrons-selector-container')
            sp = doc.splitter(orientation='horizontal')
            left = sp.section(); right = sp.section()
            #
#            selector = FormSelectorField(label='Neutrons:', name='neutrons')
#            left.add(selector)
            viewcontainer = right.document(Class='container')
            loadview = lambda uid: load(
                actor='orm/trajectory', routine='display',
                uid=uid)
            # default selection
            if referred_record:
                value=orm.db.getUniqueIdentifierStr(referred_record)
                viewcontainer.oncreate = select(element=viewcontainer).append(
                    loadview(value))
            else:
                value=None           
            return doc
        drawer.mold._createfield_for_trajectory = _createfield_for_trajectory
    
try:
    from dsaw.model.Inventory import Inventory as InvBase
    from matter.orm.Structure import Structure
    class Inventory(InvBase):
        time_steps_sampled = InvBase.d.array(name = 'time_steps_sampled', elementtype='int',
                                             shape=(3,), default=[0, 0, 1])
        time_steps_sampled.label = 'Time steps to use in calculation (start,stop,increment)'
        time_steps_sampled.help = 'start, stop and interval of time steps sampled (should all be integers)'
        # we shouldn't really have a reference to a structure--it's implicit in the trajectory
        matter = InvBase.d.reference(name='matter', targettype=Structure, owned=False)
        trajectory = InvBase.d.reference(name = 'trajectory', targettype = Trajectory, owned=False)
        trajectory.help = 'the trajectory used to compute the analysis'
        selected_atoms = InvBase.d.str(name = 'selected_atoms', default = 'All')
        selected_atoms.label = 'Atoms to use in the calculation'
        selected_atoms.help = 'the trajectory atoms used to compute this analysis'
    MdAnalysis.Inventory = Inventory
except:
    pass
