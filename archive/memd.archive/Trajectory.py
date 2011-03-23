# This module implements trajectories and trajectory generators.
#

"""
Trajectory files and their contents
"""

__docformat__ = 'epytext'

#from MMTK import Collections, Units, Universe, Utility, \
#                 ParticleProperties, Visualization
from Scientific.Geometry import Vector
from Scientific import N
import copy, os

# Report error if the netCDF module is not available.
try:
    from Scientific.IO import NetCDF
except ImportError:
    raise "Trajectories are not available because the netCDF module is missing."

#
# Trajectory class
#
class Trajectory(object):

    """
    Trajectory file

    The data in a trajectory file can be accessed by step or by
    variable. If C{t} is a Trajectory object, then:

     - C{len(t)} is the number of steps

     - C{t[i]} is the data for step C{i}, in the form of a dictionary that
       maps variable names to data

     - C{t[i:j]} and C{t[i:j:n]} return a L{SubTrajectory} object that refers
       to a subset of the total number of steps (no data is copied)

     - C{t.variable} returns the value of the named variable at all
       time steps. If the variable is a simple scalar, it is read
       completely and returned as an array. If the variable contains
       data for each atom, a L{TrajectoryVariable} object is returned
       from which data at specific steps can be obtained by further
       indexing operations.

    The routines that generate trajectories decide what variables
    are used and what they contain. The most frequently used variable
    is "configuration", which stores the positions of all atoms.
    Other common variables are "time", "velocities", "temperature",
    "pressure", and various energy terms whose name end with "_energy".
    """

    def __init__(self, object, filename, mode = 'r', comment = None,
                 double_precision = False, cycle = 0, block_size = 1):
        """
        @param object: the object whose data is stored in the trajectory file.
                       This can be 'None' when opening a file for reading;
                       in that case, a universe object is constructed from the
                       description stored in the trajectory file. This universe
                       object can be accessed via the attribute 'universe'
                       of the trajectory object.
        @type object: L{MMTK.ChemicalObjects.ChemicalObject}
        @param filename: the name of the trajectory file
        @type filename: C{str}
        @param mode: one of "r" (read-only), "w" (create new file for writing),
                     or "a" (append to existing file or create if the file does
                     not exist)
        @type mode: C{str}
        @param comment: optional comment that is stored in the file;
                        allowed only with mode="r"
        @type comment: C{str}
        @param double_precision: if C{True}, data in the file is stored using
                                 double precision; default is single precision.
                                 Note that all I/O via trajectory objects is
                                 double precision; conversion from and to
                                 single precision file variables is handled
                                 automatically.
        @type double_precision: C{bool}
        @param cycle: if non-zero, a trajectory is created for a fixed number
                      of steps equal to the value of cycle, and these steps
                      are used cyclically. This is meant for restart
                      trajectories.
        @type cycle: C{int}
        @param block_size: an optimization parameter that influences the file
                           structure and the I/O performance for very large
                           files. A block size of 1 is optimal for sequential
                           access to configurations etc., whereas a block size
                           equal to the number of steps is optimal for reading
                           coordinates or scalar variables along the time axis.
                           The default value is 1. Note that older MMTK releases
                           always used a block size of 1 and cannot handle
                           trajectories with different block sizes.
        @type block_size: C{int}
        """
        filename = os.path.expanduser(filename)
        self.filename = filename
        if object is None and mode == 'r':
            file = NetCDF.NetCDFFile(filename, 'r')
            description = file.variables['description'][:].tostring()
            try:
                self.block_size = file.dimensions['minor_step_number']
            except KeyError:
                self.block_size = 1
            conf = None
            cell = None
            if self.block_size == 1:
                try:
                    conf_var = file.variables['configuration']
                    conf = conf_var[0, :, :]
                except KeyError: pass
                try:
                    cell = file.variables['box_size'][0, :]
                except KeyError: pass
            else:
                try:
                    conf_var = file.variables['configuration']
                    conf = conf_var[0, :, :, 0]
                except KeyError: pass
                try:
                    cell = file.variables['box_size'][0, :, 0]
                except KeyError: pass
            file.close()
            import Skeleton
            local = {}
            skeleton = eval(description, vars(Skeleton), local)
            universe = skeleton.make({}, conf)
            universe.setCellParameters(cell)
            object = universe
            initialize = 1
        else:
            universe = object.universe()
            if universe is None:
                raise ValueError("objects not in the same universe")
            description = None
            initialize = 0
        universe.configuration()
        if object is universe:
            index_map = None
            inverse_map = None
        else:
            if mode == 'r':
                raise ValueError("can't read trajectory for a non-universe")
            index_map = N.array([a.index for a in  object.atomList()])
            inverse_map = universe.numberOfPoints()*[None]
            for i in range(len(index_map)):
                inverse_map[index_map[i]] = i
            toplevel = set()
            for o in Collections.Collection(object):
                toplevel.add(o.topLevelChemicalObject())
            object = Collections.Collection(list(toplevel))
        if description is None:
            description = universe.description(object, inverse_map)
        import MMTK_trajectory
        self.trajectory = MMTK_trajectory.Trajectory(universe, description,
                                                     index_map, filename,
                                                     mode + 's',
                                                     double_precision, cycle,
                                                     block_size)
        self.universe = universe
        self.index_map = index_map
        try:
            self.block_size = \
                       self.trajectory.file.dimensions['minor_step_number']
        except KeyError:
            self.block_size = 1
        if comment is not None:
            if mode == 'r':
                raise IOError('cannot add comment in read-only mode')
            self.trajectory.file.comment = comment
        if initialize and conf is not None:
            self.universe.setFromTrajectory(self)
        self.particle_trajectory_reader = ParticleTrajectoryReader(self)

    def flush(self):
        """
        Make sure that all data that has been written to the trajectory
        is also written to the file.
        """
        self.trajectory.flush()

    def close(self):
        """
        Close the trajectory file. Must be called after writing to
        ensure that all buffered data is written to the file. No data
        access is possible after closing a file.
        """
        self.trajectory.close()

    def __len__(self):
        return self.trajectory.nsteps

    def __getitem__(self, item):
        if not isinstance(item, int):
            return SubTrajectory(self, N.arange(len(self)))[item]
        if item < 0:
            item += len(self)
        if item >= len(self):
            raise IndexError
        data = {}
        for name, var in self.trajectory.file.variables.items():
            if 'step_number' not in var.dimensions:
                continue
            if 'atom_number' in var.dimensions:
                if 'xyz' in var.dimensions:
                    array = ParticleProperties.ParticleVector(self.universe,
                                self.trajectory.readParticleVector(name, item))
                else:
                    array = ParticleProperties.ParticleScalar(self.universe,
                                self.trajectory.readParticleScalar(name, item))
            else:
                bs = self.block_size
                if bs == 1:
                    array = var[item]
                else:
                    if len(var.shape) == 2:
                        array = var[item/bs, item%bs]
                    else:
                        array = var[item/bs, ..., item%bs]
            data[name] = 0.+array
        if data.has_key('configuration'):
            box = data.get('box_size', None)
            if box is not None:
                box = box.astype(N.Float)
            conf = data['configuration']
            data['configuration'] = \
               ParticleProperties.Configuration(conf.universe, conf.array, box)
        return data

    def __getslice__(self, first, last):
        return self[(slice(first, last),)]

    def __getattr__(self, name):
        try:
            var = self.trajectory.file.variables[name]
        except KeyError:
            raise AttributeError("no variable named " + name)
        if 'atom_number' in var.dimensions:
            return TrajectoryVariable(self.universe, self, name)
        else:
            return N.ravel(N.array(var))[:len(self)]

    def defaultStep(self):
        try:
            step = int(self.trajectory.file.last_step[0])
        except AttributeError:
            step = 0
        return step

    def readParticleTrajectory(self, atom, first=0, last=None, skip=1,
                               variable = "configuration"):
        """
        Read trajectory information for a single atom but for multiple
        time steps.

        @param atom: the atom whose trajectory is requested
        @type atom: L{MMTK.ChemicalObjects.Atom}
        @param first: the number of the first step to be read
        @type first: C{int}
        @param last: the number of the first step not to be read.
                     A value of C{None} indicates that the
                     whole trajectory should be read.
        @type last: C{int}
        @param skip: the number of steps to skip between two steps read
        @type skip: C{int}
        @param variable: the name of the trajectory variable to be read.
                         If the variable is "configuration", the resulting
                         trajectory is made continuous by eliminating all
                         jumps caused by periodic boundary conditions.
                         The pseudo-variable "box_coordinates" can be read
                         to obtain the values of the variable "configuration"
                         scaled to box coordinates. For non-periodic universes
                         there is no difference between box coordinates
                         and real coordinates.
        @type variable: C{str}
        @returns: the trajectory for a single atom
        @rtype: L{ParticleTrajectory}
        """
        return ParticleTrajectory(self, atom, first, last, skip, variable)

    def readRigidBodyTrajectory(self, object, first=0, last=None, skip=1,
                                reference = None):
        """
        Read the positions for an object at multiple time steps
        and extract the rigid-body motion (center-of-mass position plus
        orientation as a quaternion) by an optimal-transformation fit.

        @param object: the object whose rigid-body trajectory is requested
        @type object: L{MMTK.Collections.GroupOfAtoms}
        @param first: the number of the first step to be read
        @type first: C{int}
        @param last: the number of the first step not to be read.
                     A value of C{None} indicates that the
                     whole trajectory should be read.
        @type last: C{int}
        @param skip: the number of steps to skip between two steps read
        @type skip: C{int}
        @param reference: the reference configuration for the fit
        @type reference: L{MMTK.ParticleProperties.Configuration}
        @returns: the trajectory for a single rigid body
        @rtype: L{RigidBodyTrajectory}
        """
        return RigidBodyTrajectory(self, object, first, last, skip, reference)

    def variables(self):
        """
        @returns: a list of the names of all variables that are stored
                  in the trajectory
        @rtype: C{list} of C{str}
        """
        vars = copy.copy(self.trajectory.file.variables.keys())
        vars.remove('step')
        try:
            vars.remove('description')
        except ValueError: pass
        return vars

#    def view(self, first=0, last=None, skip=1, object = None):
#        """
#        Show an animation of the trajectory using an external visualization
#        program.
#
#        @param first: the number of the first step in the animation
#        @type first: C{int}
#        @param last: the number of the first step not to include in the
#                     animation. A value of C{None} indicates that the
#                     whole trajectory should be used.
#        @type last: C{int}
#        @param skip: the number of steps to skip between two steps read
#        @type skip: C{int}
#        @param object: the object to be animated, which must be in the
#                       universe stored in the trajectory. C{None}
#                       stands for the whole universe.
#        @type object: L{MMTK.Collections.GroupOfAtoms}
#        """
#        Visualization.viewTrajectory(self, first, last, skip, object)

#    def _boxTransformation(self, pt_in, pt_out, to_box=0):
#        from MMTK_trajectory import boxTransformation
#        try:
#            box_size = self.trajectory.recently_read_box_size
#        except AttributeError:
#            return
#        boxTransformation(self.universe._spec,
#                          pt_in, pt_out, box_size, to_box)


class SubTrajectory(object):

    """
    Reference to a subset of a trajectory

    A SubTrajectory object is created by slicing a Trajectory object
    or another SubTrajectory object. It provides all the operations
    defined on Trajectory objects.
    """

    def __init__(self, trajectory, indices):
        self.trajectory = trajectory
        self.indices = indices
        self.universe = trajectory.universe

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.trajectory[self.indices[item]]
        else:
            return SubTrajectory(self.trajectory, self.indices[item])

    def __getslice__(self, first, last):
        return self[(slice(first, last),)]

    def __getattr__(self, name):
        return SubVariable(getattr(self.trajectory, name), self.indices)

    def readParticleTrajectory(self, atom, first=0, last=None, skip=1,
                               variable = "configuration"):
        if last is None:
            last = len(self.indices)
        indices = self.indices[first:last:skip]
        first = indices[0]
        last = indices[-1]+1
        if len(self.indices) > 1:
            skip = self.indices[1]-self.indices[0]
        else:
            skip = 1
        return self.trajectory.readParticleTrajectory(atom, first, last,
                                                      skip, variable)

    def readRigidBodyTrajectory(self, object, first=0, last=None, skip=1,
                                reference = None):
        if last is None:
            last = len(self.indices)
        indices = self.indices[first:last:skip]
        first = indices[0]
        last = indices[-1]+1
        if len(self.indices) > 1:
            skip = self.indices[1]-self.indices[0]
        else:
            skip = 1
        return RigidBodyTrajectory(self.trajectory, object,
                                   first, last, skip, reference)

    def variables(self):
        return self.trajectory.variables()

    def view(self, first=0, last=None, step=1, subset = None):
        Visualization.viewTrajectory(self, first, last, step, subset)

    def close(self):
        del self.trajectory

    def _boxTransformation(self, pt_in, pt_out, to_box=0):
        Trajectory._boxTransformation(self.trajectory, pt_in, pt_out, to_box)

#
# Trajectory variables
#
class TrajectoryVariable(object):

    """
    Variable in a trajectory

    A TrajectoryVariable object is created by extracting a variable from
    a Trajectory object if that variable contains data for each atom and
    is thus potentially large. No data is read from the trajectory file
    when a TrajectoryVariable object is created; the read operation
    takes place when the TrajectoryVariable is indexed with a specific
    step number.

    If C{t} is a TrajectoryVariable object, then:

     - C{len(t)} is the number of steps

     - C{t[i]} is the data for step C{i}, in the form of a ParticleScalar,
       a ParticleVector, or a Configuration object, depending on the
       variable

     - C{t[i:j]} and C{t[i:j:n]} return a SubVariable object that refers
       to a subset of the total number of steps
    """
    
    def __init__(self, universe, trajectory, name):
        self.universe = universe
        self.trajectory = trajectory
        self.name = name
        self.var = self.trajectory.trajectory.file.variables[self.name]
        if self.name == 'configuration':
            try:
                self.box_size = \
                        self.trajectory.trajectory.file.variables['box_size']
            except KeyError:
                self.box_size = None

    def __len__(self):
        return len(self.trajectory)

    def __getitem__(self, item):
        if not isinstance(item, int):
            return SubVariable(self, N.arange(len(self)))[item]
        if item < 0:
            item = item + len(self.trajectory)
        if item >= len(self.trajectory):
            raise IndexError
        if self.name == 'configuration':
            if self.box_size is None:
                box = None
            elif len(self.box_size.shape) == 3:
                bs = self.trajectory.block_size
                box = self.box_size[item/bs, :, item%bs].astype(N.Float)
            else:
                box = self.box_size[item].astype(N.Float)
            array = ParticleProperties.Configuration(self.universe,
                self.trajectory.trajectory.readParticleVector(self.name, item),
                box)
        elif 'xyz' in self.var.dimensions:
            array = ParticleProperties.ParticleVector(self.universe,
                self.trajectory.trajectory.readParticleVector(self.name, item))
        else:
            array = ParticleProperties.ParticleScalar(self.universe,
                self.trajectory.trajectory.readParticleScalar(self.name, item))
        return array

    def __getslice__(self, first, last):
        return self[(slice(first, last),)]

    def average(self):
        sum = self[0]
        for value in self[1:]:
            sum = sum + value
        return sum/len(self)

class SubVariable(TrajectoryVariable):

    """
    Reference to a subset of a L{TrajectoryVariable}

    A SubVariable object is created by slicing a TrajectoryVariable
    object or another SubVariable object. It provides all the operations
    defined on TrajectoryVariable objects.
    """

    def __init__(self, variable, indices):
        self.variable = variable
        self.indices = indices

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.variable[self.indices[item]]
        else:
            return SubVariable(self.variable, self.indices[item])

    def __getslice__(self, first, last):
        return self[(slice(first, last),)]

#
# Trajectory consisting of multiple files
#

#
class ParticleTrajectoryReader(object):

    def __init__(self, trajectory):
        self.trajectory = trajectory
        self.natoms = self.trajectory.universe.numberOfAtoms()
        self._trajectory = trajectory.trajectory
        self.cache = {}
        self.cache_lifetime = 2

    def __call__(self, atom, variable, first, last, skip, correct, box):
        if isinstance(atom, int):
            index = atom
        else:
            index = atom.index
            if atom.universe() is not self.trajectory.universe:
                raise ValueError("objects not in the same universe")
        key = (index, variable, first, last, skip, correct, box)
        data, count = self.cache.get(key, (None, 0))
        if data is not None:
            self.cache[key] = (data, self.cache_lifetime)
            return data
        delete = []
        for k, value in self.cache.items():
            data, count = value
            count -= 1
            if count == 0:
                delete.append(k)
            else:
                self.cache[k] = (data, count)
        for k in delete:
            del self.cache[k]
        cache_size = min(10, max(1, 100000/max(1, len(self.trajectory))))
        natoms = min(cache_size, self.natoms-index)
        data = self._trajectory.readParticleTrajectories(index, natoms,
                                                         variable,
                                                         first, last, skip,
                                                         correct, box)
        for i in range(natoms):
            key = (index+i, variable, first, last, skip, correct, box)
            self.cache[key] = (data[i], self.cache_lifetime)
        return data[0]

#
# Single-atom trajectory
#
class ParticleTrajectory(object):

    """
    Trajectory data for a single particle

    A ParticleTrajectory object is created by calling the method
    C{readParticleTrajectory} on a L{Trajectory} object.

    If C{pt} is a ParticleTrajectory object, then

     - C{len(pt)} is the number of steps stored in it

     - C{pt[i]} is the value at step C{i} (a vector)
    """
    
    def __init__(self, trajectory, atom, first=0, last=None, skip=1,
                 variable = "configuration"):
        if last is None:
            last = len(trajectory)
        if variable == "box_coordinates":
            variable = "configuration"
            box = 1
        else:
            box = 0
        reader = trajectory.particle_trajectory_reader
        self.array = reader(atom, variable, first, last, skip,
                            variable == "configuration", box)

    def __len__(self):
        return self.array.shape[0]

    def __getitem__(self, index):
        return Vector(self.array[index])

    def translateBy(self, vector):
        """
        Adds a vector to the values at all steps. This does B{not}
        change the data in the trajectory file.
        @param vector: the vector to be added
        @type vector: C{Scientific.Geometry.Vector}
        """
        N.add(self.array, vector.array[N.NewAxis, :], self.array)

#
# Rigid-body trajectory
#
class RigidBodyTrajectory(object):

    """
    Rigid-body trajectory data

    A RigidBodyTrajectory object is created by calling the method
    C{readRigidBodyTrajectory} on a L{Trajectory} object.

    If C{rbt} is a RigidBodyTrajectory object, then

     - C{len(rbt)} is the number of steps stored in it

     - C{rbt[i]} is the value at step C{i} (a vector for the center of mass
       and a quaternion for the orientation)
    """
    
    def __init__(self, trajectory, object, first=0, last=None, skip=1,
                 reference = None):
        self.trajectory = trajectory
        universe = trajectory.universe
        if last is None: last = len(trajectory)
        first_conf = trajectory.configuration[first]
        offset = universe.contiguousObjectOffset([object], first_conf, True)
        if reference is None:
            reference = first_conf
        reference = universe.contiguousObjectConfiguration([object], reference)
        steps = (last-first+skip-1)/skip
        mass = object.mass()
        ref_cms = object.centerOfMass(reference)
        atoms = object.atomList()

        possq = N.zeros((steps,), N.Float)
        cross = N.zeros((steps, 3, 3), N.Float)
        rcms = N.zeros((steps, 3), N.Float)

        # cms of the CONTIGUOUS object made of CONTINUOUS atom trajectories 
        for a in atoms:
            r = trajectory.readParticleTrajectory(a, first, last, skip,
                                                  "box_coordinates").array
            w = a._mass/mass
            N.add(rcms, w*r, rcms)
            if offset is not None:
                N.add(rcms, w*offset[a].array, rcms)
        
        # relative coords of the CONTIGUOUS reference
        r_ref = N.zeros((len(atoms), 3), N.Float)
        for a in range(len(atoms)):
            r_ref[a] = atoms[a].position(reference).array - ref_cms.array

        # main loop: storing data needed to fill M matrix 
        for a in range(len(atoms)):
            r = trajectory.readParticleTrajectory(atoms[a],
                                                  first, last, skip,
                                                  "box_coordinates").array
            r = r - rcms # (a-b)**2 != a**2 - b**2
            if offset is not None:
                N.add(r, offset[atoms[a]].array,r)
            trajectory._boxTransformation(r, r)
            w = atoms[a]._mass/mass
            N.add(possq, w*N.add.reduce(r*r, -1), possq)
            N.add(possq, w*N.add.reduce(r_ref[a]*r_ref[a],-1),
                        possq)
            N.add(cross, w*r[:,:,N.NewAxis]*r_ref[N.NewAxis,
                                                              a,:],cross)
        self.trajectory._boxTransformation(rcms, rcms)

        # filling matrix M (formula no 40)
        k = N.zeros((steps, 4, 4), N.Float)
        k[:, 0, 0] = -cross[:, 0, 0]-cross[:, 1, 1]-cross[:, 2, 2]
        k[:, 0, 1] = cross[:, 1, 2]-cross[:, 2, 1]
        k[:, 0, 2] = cross[:, 2, 0]-cross[:, 0, 2]
        k[:, 0, 3] = cross[:, 0, 1]-cross[:, 1, 0]
        k[:, 1, 1] = -cross[:, 0, 0]+cross[:, 1, 1]+cross[:, 2, 2]
        k[:, 1, 2] = -cross[:, 0, 1]-cross[:, 1, 0]
        k[:, 1, 3] = -cross[:, 0, 2]-cross[:, 2, 0]
        k[:, 2, 2] = cross[:, 0, 0]-cross[:, 1, 1]+cross[:, 2, 2]
        k[:, 2, 3] = -cross[:, 1, 2]-cross[:, 2, 1]
        k[:, 3, 3] = cross[:, 0, 0]+cross[:, 1, 1]-cross[:, 2, 2]
        del cross
        for i in range(1, 4):
            for j in range(i):
                k[:, i, j] = k[:, j, i]
        N.multiply(k, 2., k)
        for i in range(4):
            N.add(k[:,i,i], possq, k[:,i,i])
        del possq

        quaternions = N.zeros((steps, 4), N.Float)
        fit = N.zeros((steps,), N.Float)
        from Scientific.LA import eigenvectors
        for i in range(steps):
            e, v = eigenvectors(k[i])
            j = N.argmin(e)
            if e[j] < 0.:
                fit[i] = 0.
            else:
                fit[i] = N.sqrt(e[j])
            if v[j,0] < 0.: quaternions[i] = -v[j] # eliminate jumps
            else: quaternions[i] = v[j]
        self.fit = fit
        self.cms = rcms
        self.quaternions = quaternions

    def __len__(self):
        return self.cms.shape[0]

    def __getitem__(self, index):
        from Scientific.Geometry.Quaternion import Quaternion
        return Vector(self.cms[index]), Quaternion(self.quaternions[index])

#
# Type check for trajectory objects
#
def isTrajectory(object):
    """
    @param object: any Python object
    @returns C{True} if object is a trajectory
    """
    import MMTK_trajectory
    return isinstance(object, (Trajectory, MMTK_trajectory.trajectory_type))


#
# Print information about trajectory file
#
def trajectoryInfo(filename):
    """
    @param filename: the name of a trajectory file
    @type filename: C{str}
    @returns: a string with summarial information about the trajectory
    """
    from Scientific.IO import NetCDF
    file = NetCDF.NetCDFFile(filename, 'r')
    nsteps = file.variables['step'].shape[0]
    if 'minor_step_number' in file.dimensions.keys():
        nsteps = nsteps*file.variables['step'].shape[1]
    s = 'Information about trajectory file ' + filename + ':\n'
    try:
        s += file.comment + '\n'
    except AttributeError:
        pass
    s += `file.dimensions['atom_number']` + ' atoms\n'
    s += `nsteps` + ' steps\n'
    s += file.history
    file.close()
    return s
