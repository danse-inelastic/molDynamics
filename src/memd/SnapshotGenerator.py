#
# Snapshot generator
#
class SnapshotGenerator(TrajectoryGenerator):

    """
    Trajectory generator for single steps

    A SnapshotGenerator is used for manual assembly of trajectory
    files. At each call it writes one step to the trajectory,
    using the current state of the universe (configuration, velocities, etc.)
    and data provided explicitly with the call.

    Each call to the SnapshotGenerator object produces one step.
    All the keyword options can be specified either when
    creating the generator or when calling it.
    """

    def __init__(self, universe, **options):
        """
        @param universe: the universe on which the generator acts
        @keyword data: a dictionary that supplies values for variables
                       that are not part of the universe state
                       (e.g. potential energy)
        @keyword actions: a list of actions to be executed periodically
                          (default is none)
        """
        TrajectoryGenerator.__init__(self, universe, options)
        self.available_data = []
        try:
            e, g = self.universe.energyAndGradients()
        except: pass
        else:
            self.available_data.append('energy')
            self.available_data.append('gradients')
        try:
            self.universe.configuration()
            self.available_data.append('configuration')
        except: pass
        if self.universe.cellVolume() is not None:
            self.available_data.append('thermodynamic')
        if self.universe.velocities() is not None:
            self.available_data.append('velocities')
            self.available_data.append('energy')
            self.available_data.append('thermodynamic')

    default_options = {'steps': 0, 'actions': []}

    def __call__(self, **options):
        self.setCallOptions(options)
        from MMTK_trajectory import snapshot
        data = copy.copy(options.get('data', {}))
        energy_terms = 0
        for name in data.keys():
            if name == 'time' and 'time' not in self.available_data:
                self.available_data.append('time')
            if  name[-7:] == '_energy':
                energy_terms = energy_terms + 1
                if 'energy' not in self.available_data:
                    self.available_data.append('energy')
            if (name == 'temperature' or name == 'pressure') \
               and 'thermodynamic' not in self.available_data:
                self.available_data.append('thermodynamic')
            if name == 'gradients' and 'gradients' not in self.available_data:
                self.available_data.append('gradients')
        actions = self.getActions()
        for action in actions:
            categories = action[-1]
            for c in categories:
                if c == 'energy' and not data.has_key('kinetic_energy'):
                    v = self.universe.velocities()
                    if v is not None:
                        m = self.universe.masses()
                        e = (v*v*m*0.5).sumOverParticles()
                        data['kinetic_energy'] = e
                        df = self.universe.degreesOfFreedom()
                        data['temperature'] = 2.*e/df/Units.k_B/Units.K
                if c == 'configuration':
                    if  data.has_key('configuration'):
                        data['configuration'] = data['configuration'].array
                    else:
                        data['configuration'] = \
                                         self.universe.configuration().array
                if c == 'velocities':
                    if  data.has_key('velocities'):
                        data['velocities'] = data['velocities'].array
                    else:
                        data['velocities'] = self.universe.velocities().array
                if c == 'gradients':
                    if  data.has_key('gradients'):
                        data['gradients'] = data['gradients'].array
                p = self.universe.cellParameters()
                if p is not None:
                    data['box_size'] = p
                volume = self.universe.cellVolume()
                if volume is not None:
                    data['volume'] = volume
                try:
                    m = self.universe.masses()
                    data['masses'] = m.array
                except: pass
        snapshot(self.universe, data, actions, energy_terms)
