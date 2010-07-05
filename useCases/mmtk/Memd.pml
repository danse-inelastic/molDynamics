<?xml version="1.0"?>
<!DOCTYPE inventory>
<inventory>

    <component name="Memd">
        <property name="engine">mmtk</property>

        <component name="mmtk">
            <property name="Trajectory Filename">molDynamics.nc</property>
            <property name="Equilibration Time (ps)">0.0</property>
            <property name="Thermodynamic Ensemble">nve</property>
            <property name="integrator">velocity-verlet</property>
            <property name="Time step (fs)">0.5</property>
            <property name="Trajectory Type">xyz</property>
            <property name="outputDir">/home/jbk/DANSE/MolDyn/molDynamics/useCases/mmtk</property>
            <facility name="Sample">Sample</facility>
            <property name="Barostat Parameter">0.005</property>
            <property name="Production Time (ps)">50.0</property>
            <property name="forcefield">lennardJones</property>
            <property name="Thermostat Parameter">0.005</property>
            <property name="Properties Calculation Frequency (fs)">5.0</property>
            <property name="runType">md</property>
            <property name="Dump Frequency (ps)">0.0</property>
            <property name="Restart Filename">molDynamics.res</property>
            <property name="Log Filename">molDynamics.log</property>

            <component name="Sample">
                <property name="Pressure (GPa)">0</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="Temperature or Initial Energy (K)">0</property>

                <component name="xyzFile">
                    <property name="inputFile">/home/jbk/workspace/molDynamics/useCases/mmtk/argon.xyz</property>
                </component>

            </component>

            <component name="lennardJones">
                <property name="Lennard-Jones Cutoff (nm)">None (minimum image convention for periodic systems)</property>
            </component>

        </component>

    </component>

</inventory>
