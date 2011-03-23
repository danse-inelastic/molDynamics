#
# Trajectory action base class
#
class TrajectoryAction(object):

    """
    Trajectory action base class

    Subclasses of this base class implement the actions that can be
    inserted into trajectory generation at regular intervals.
    """

    def __init__(self, first, last, skip):
        self.first = first
        self.last = last
        self.skip = skip

    spec_type = 'function'

    def _getSpecificationList(self, trajectory_generator, steps):
        first = self.first
        last = self.last
        if first < 0:
            first = first + steps
        if last is None:
            import MMTK_trajectory
            last = MMTK_trajectory.maxint
        elif last < 0:
            last = last + steps+1
        return (self.spec_type, first, last, self.skip)

    def getSpecificationList(self, trajectory_generator, steps):
        return self._getSpecificationList(trajectory_generator, steps) \
               + (self.Cfunction, self.parameters)

    def cleanup(self):
        pass

class TrajectoryOutput(TrajectoryAction):

    """
    Trajectory output action

    A TrajectoryOutput object can be used in the action list of any
    trajectory-generating operation. It writes any of the available
    data to a trajectory file. It is possible to use several
    TrajectoryOutput objects at the same time in order to produce
    multiple trajectories from a single run.
    """

    def __init__(self, trajectory, data = None,
                 first=0, last=None, skip=1):
        """
        @param trajectory: a trajectory object or a string, which is
                           interpreted as the name of a file that is opened
                           as a trajectory in append mode
        @param data: a list of data categories. All variables provided by the
                     trajectory generator that fall in any of the listed
                     categories are written to the trajectory file. See the
                     descriptions of the trajectory generators for a list
                     of variables and categories. By default (C{data = None})
                     the categories "configuration", "energy",
                     "thermodynamic", and "time" are written.
        @param first: the number of the first step at which the action is run
        @type first: C{int}
        @param last: the number of the step at which the action is suspended.
                     A value of C{None} indicates that the action should
                     be applied indefinitely.
        @type last: C{int}
        @param skip: the number of steps to skip between two action runs
        @type skip: C{int}
        """
        TrajectoryAction.__init__(self, first, last, skip)
        self.destination = trajectory
        self.categories = data
        self.must_be_closed = None

    spec_type = 'trajectory'

    def getSpecificationList(self, trajectory_generator, steps):
        if type(self.destination) == type(''):
            destination = self._setupDestination(self.destination,
                                                 trajectory_generator.universe)
        else:
            destination = self.destination
        if self.categories is None:
            categories = self._defaultCategories(trajectory_generator)
        else:
            if self.categories == 'all' or self.categories == ['all']:
                categories = trajectory_generator.available_data
            else:
                categories = self.categories
                for item in categories:
                    if item not in trajectory_generator.available_data:
                        raise ValueError('data item %s is not available' % item)
        return self._getSpecificationList(trajectory_generator, steps) \
               + (destination, categories)

    def _setupDestination(self, destination, universe):
        self.must_be_closed = Trajectory(universe, destination, 'a')
        return self.must_be_closed
        
    def cleanup(self):
        if self.must_be_closed is not None:
            self.must_be_closed.close()

    def _defaultCategories(self, trajectory_generator):
        available = trajectory_generator.available_data
        return tuple(filter(lambda x, a=available: x in a, self.default_data))

    default_data = ['configuration', 'energy', 'thermodynamic', 'time']

class RestartTrajectoryOutput(TrajectoryOutput):

    """
    Restart trajectory output action

    A RestartTrajectoryOutput object is used in the action list of any
    trajectory-generating operation. It writes those variables to a
    trajectory that the trajectory generator declares as necessary
    for restarting.
    """

    def __init__(self, trajectory, skip=100, length=3):
        """
        @param trajectory: a trajectory object or a string, which is interpreted
                           as the name of a file that is opened as a trajectory
                           in append mode with a cycle length of C{length} and
                           double-precision variables
        @param skip: the number of steps between two write operations to the
                     restart trajectory
        @type skip: C{int}
        @param length: the number of steps stored in the restart trajectory;
                       used only if C{trajectory} is a string
        """
        TrajectoryAction.__init__(self, 0, None, skip)
        self.destination = trajectory
        self.categories = None
        self.length = length

    def _setupDestination(self, destination, universe):
        self.must_be_closed = Trajectory(universe, destination, 'a',
                                         'Restart trajectory', 1, self.length)
        return self.must_be_closed
        
    def _defaultCategories(self, trajectory_generator):
        if trajectory_generator.restart_data is None:
            raise ValueError("Trajectory generator does not permit restart")
        return trajectory_generator.restart_data

class LogOutput(TrajectoryOutput):

    """
    Protocol file output action

    A LogOutput object can be used in the action list of any
    trajectory-generating operation. It writes any of the available
    data to a text file.
    """

    def __init__(self, file, data = None, first=0, last=None, skip=1):
        """
        @param file: a file object or a string, which is interpreted as the
                     name of a file that is opened in write mode
        @param data: a list of data categories. All variables provided by the
                     trajectory generator that fall in any of the listed
                     categories are written to the trajectory file. See the
                     descriptions of the trajectory generators for a list
                     of variables and categories. By default (C{data = None})
                     the categories "configuration", "energy",
                     "thermodynamic", and "time" are written.
        @param first: the number of the first step at which the action is run
        @type first: C{int}
        @param last: the number of the step at which the action is suspended.
                     A value of C{None} indicates that the action should
                     be applied indefinitely.
        @type last: C{int}
        @param skip: the number of steps to skip between two action runs
        @type skip: C{int}
        """
        TrajectoryOutput.__init__(self, file, data, first, last, skip)

    def _setupDestination(self, destination, universe):
        self.must_be_closed = open(destination, 'w')
        return self.must_be_closed

    spec_type = 'print'

    default_data = ['energy', 'time']

class StandardLogOutput(LogOutput):

    """
    Standard protocol output action

    A StandardLogOutput object can be used in the action list of any
    trajectory-generating operation. It is a specialization of
    LogOutput to the most common case and writes data in the categories
    "time" and "energy" to the standard output stream.
    """

    def __init__(self, skip=50):
        """
        @param skip: the number of steps to skip between two action runs
        @type skip: C{int}
        """
        LogOutput.__init__(self, sys.stdout, None, 0, None, skip)

