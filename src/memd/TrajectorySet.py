class TrajectorySet(object):

    """
    Trajectory file set

    A TrajectorySet permits to treat a sequence of trajectory files
    like a single trajectory for reading data. It behaves exactly like a
    L{Trajectory} object. The trajectory files must all contain data
    for the same system. The variables stored in the individual files
    need not be the same, but only variables common to all files
    can be accessed.

    Note: depending on how the sequence of trajectories was constructed,
    the first configuration of each trajectory might be the same as the
    last one in the preceding trajectory. To avoid counting it twice,
    specify (filename, 1, None, 1) for all but the first trajectory in
    the set.
    """

    def __init__(self, object, filenames):
        """
        @param object: the object whose data is stored in the trajectory files.
                       This can be (and usually is) C{None};
                       in that case, a universe object is constructed from the
                       description stored in the first trajectory file.
                       This universe object can be accessed via the attribute
                       C{universe} of the trajectory set object.
        @param filenames: a list of trajectory file names or
                          (filename, first_step, last_step, increment)
                          tuples.
        """
        first = filenames[0]
        if isinstance(first, tuple):
            first = Trajectory(object, first[0])[first[1]:first[2]:first[3]]
        else:
            first = Trajectory(object, first)
        self.universe = first.universe
        self.trajectories = [first]
        self.nsteps = [0, len(first)]
        self.cell_parameters = []
        for file in filenames[1:]:
            if isinstance(file, tuple):
                t = Trajectory(self.universe, file[0])[file[1]:file[2]:file[3]]
            else:
                t = Trajectory(self.universe, file)
            self.trajectories.append(t)
            self.nsteps.append(self.nsteps[-1]+len(t))
            try:
                self.cell_parameters.append(t[0]['box_size'])
            except KeyError:
                pass
        vars = {}
        for t in self.trajectories:
            for v in t.variables():
                vars[v] = vars.get(v, 0) + 1
        self.vars = []
        for v, count in vars.items():
            if count == len(self.trajectories):
                self.vars.append(v)

    def close(self):
        for t in self.trajectories:
            t.close()

    def __len__(self):
        return self.nsteps[-1]

    def __getitem__(self, item):
        if not isinstance(item, int):
            return SubTrajectory(self, N.arange(len(self)))[item]
        if item >= len(self):
            raise IndexError
        tindex = N.add.reduce(N.greater_equal(item, self.nsteps))-1
        return self.trajectories[tindex][item-self.nsteps[tindex]]

    def __getslice__(self, first, last):
        return self[(slice(first, last),)]

    def __getattr__(self, name):
        if name not in self.vars+['step']:
            raise AttributeError("no variable named " + name)
        var = self.trajectories[0].trajectory.file.variables[name]
        if 'atom_number' in var.dimensions:
            return TrajectorySetVariable(self.universe, self, name)
        else:
            data = []
            for t in self.trajectories:
                var = t.trajectory.file.variables[name]
                data.append(N.ravel(N.array(var))[:len(t)])
            return N.concatenate(data)

    def readParticleTrajectory(self, atom, first=0, last=None, skip=1,
                               variable = "configuration"):
        total = None
        self.steps_read = []
        for i in range(len(self.trajectories)):
            if self.nsteps[i+1] <= first:
                self.steps_read.append(0)
                continue
            if last is not None and self.nsteps[i] >= last:
                break
            n = max(0, (self.nsteps[i]-first+skip-1)/skip)
            start = first+skip*n-self.nsteps[i]
            n = (self.nsteps[i+1]-first+skip-1)/skip
            stop = first+skip*n
            if last is not None:
                stop = min(stop, last)
            stop = stop-self.nsteps[i]
            if start >= 0 and start < self.nsteps[i+1]-self.nsteps[i]:
                t = self.trajectories[i]
                pt = t.readParticleTrajectory(atom, start, stop, skip,
                                              variable)
                self.steps_read.append((stop-start)/skip)
                if total is None:
                    total = pt
                else:
                    if variable == "configuration" \
                       and self.cell_parameters[0] is not None:
                        jump = pt.array[0]-total.array[-1]
                        mult = -(jump/self.cell_parameters[i-1]).astype('i')
                        if len(N.nonzero(mult)) > 0:
                            t._boxTransformation(pt.array, pt.array, 1)
                            N.add(pt.array, mult[N.NewAxis, : ],
                                        pt.array)
                            t._boxTransformation(pt.array, pt.array, 0)
                            jump = pt.array[0] - total.array[-1]
                        mask = N.less(jump,
                                            -0.5*self.cell_parameters[i-1])- \
                               N.greater(jump,
                                               0.5*self.cell_parameters[i-1])
                        if len(N.nonzero(mask)) > 0:
                            t._boxTransformation(pt.array, pt.array, 1)
                            N.add(pt.array, mask[N.NewAxis, :],
                                        pt.array)
                            t._boxTransformation(pt.array, pt.array, 0)
                    elif variable == "box_coordinates" \
                       and self.cell_parameters[0] is not None:
                        jump = pt.array[0]-total.array[-1]
                        mult = -jump.astype('i')
                        if len(N.nonzero(mult)) > 0:
                            N.add(pt.array, mult[N.NewAxis, : ],
                                        pt.array)
                            jump = pt.array[0] - total.array[-1]
                        mask = N.less(jump, -0.5)- \
                               N.greater(jump, 0.5)
                        if len(N.nonzero(mask)) > 0:
                            N.add(pt.array, mask[N.NewAxis, :],
                                        pt.array)
                    total.array = N.concatenate((total.array, pt.array))
            else:
                self.steps_read.append(0)
        return total

    def readRigidBodyTrajectory(self, object, first=0, last=None, skip=1,
                                reference = None):
        return RigidBodyTrajectory(self, object, first, last, skip, reference)

    def _boxTransformation(self, pt_in, pt_out, to_box=0):
        n = 0
        for i in range(len(self.steps_read)):
            t = self.trajectories[i]
            steps = self.steps_read[i]
            if steps > 0:
                t._boxTransformation(pt_in[n:n+steps], pt_out[n:n+steps],
                                     to_box)
            n = n + steps

    def variables(self):
        return self.vars

    def view(self, first=0, last=None, step=1, object = None):
        Visualization.viewTrajectory(self, first, last, step, object)


class TrajectorySetVariable(TrajectoryVariable):

    """
    Variable in a trajectory set

    A TrajectorySetVariable object is created by extracting a variable from
    a TrajectorySet object if that variable contains data for each atom and
    is thus potentially large. It behaves exactly like a TrajectoryVariable
    object.
    """
    
    def __init__(self, universe, trajectory_set, name):
        self.universe = universe
        self.trajectory_set = trajectory_set
        self.name = name

    def __len__(self):
        return len(self.trajectory_set)

    def __getitem__(self, item):
        if not isinstance(item, int):
            return SubVariable(self, N.arange(len(self)))[item]
        if item >= len(self.trajectory_set):
            raise IndexError
        tindex = N.add.reduce(N.greater_equal(item,
                                              self.trajectory_set.nsteps))-1
        step = item-self.trajectory_set.nsteps[tindex]
        t = self.trajectory_set.trajectories[tindex]
        return getattr(t, self.name)[step]

#
# Cache for atom trajectories