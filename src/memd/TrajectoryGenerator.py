#
# Base class for all objects that generate trajectories
#
class TrajectoryGenerator(object):

    """
    Trajectory generator base class

    This base class implements the common aspects of everything that
    generates trajectories: integrators, minimizers, etc.
    """

    def __init__(self, universe, options):
        self.universe = universe
        self.options = options

    def setCallOptions(self, options):
        self.call_options = options

    def getActions(self):
        try:
            self.actions = self.getOption('actions')
        except ValueError:
            self.actions = []
        try:
            steps = self.getOption('steps')
        except ValueError:
            steps = None
        return map(lambda a, t=self, s=steps: a.getSpecificationList(t, s),
                   self.actions)

    def cleanupActions(self):
        for a in self.actions:
            a.cleanup()

    def getOption(self, option):
        try:
            value = self.call_options[option]
        except KeyError:
            try:
                value = self.options[option]
            except KeyError:
                try:
                    value = self.default_options[option]
                except KeyError:
                    raise ValueError('undefined option: ' + option)
        return value

    def optionString(self, options):
        s = ''
        for o in options:
            s = s + o + '=' + `self.getOption(o)` + ', '
        return s[:-2]


#
# Trajectory reader (not yet functional...)
#
if False:

    class TrajectoryReader(TrajectoryGenerator):

        def __init__(self, trajectory, options):
            TrajectoryGenerator.__init__(self, trajectory.universe, options)
            self.input = trajectory
            self.available_data = trajectory.variables()

        default_options = {'trajectory': None, 'log': None, 'options': []}

        def __call__(self, **options):
            self.setCallOptions(options)
            from MMTK_trajectory import readTrajectory
            readTrajectory(self.universe, self.input.trajectory,
                           [self.getOption('trajectory'),
                            self.getOption('log')] +
                           self.getOption('options'))
