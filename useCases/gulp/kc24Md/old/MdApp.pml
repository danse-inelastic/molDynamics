<?xml version="1.0"?>
<!DOCTYPE inventory>
<inventory>
    <component name="MdApp">
        <property name="engine">gulp</property>
        
        <component name="gulp">
            <property name="Engine Executable Path">/home/jbk/officialGulp3.4/Src/gulp</property>
            <property name="Log Filename">molDynamics.log</property>
            <facility name="sample">Sample</facility>
            <property name="potential">potential</property>
            <property name="runType">md</property>
            <property name="Compute Material Properties">False</property>
            <property name="outputDir">/home/jbk/DANSE/MolDyn/molDynamics/useCases/gulp/kc24Md</property>
            <property name="Input Filename">kc24-70K.gin</property>

            <component name="Sample">
                <property name="Pressure (GPa)">0</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="Temperature or Initial Energy (K)">70</property>

                <component name="xyzFile">
                    <property name="inputFile">/home/jbk/DANSE/MolDyn/molDynamics/useCases/gulp/kc24Md/kc24Relaxed.xyz</property>
                </component>

            </component>

            <component name="md">
                <property name="Trajectory Filename">kc24-70K</property>
                <property name="Equilibration Time (ps)">0.0</property>
                <property name="Thermodynamic Ensemble">nvt</property>
                <property name="Properties Calculation Frequency (fs)">5.0</property>
                <property name="Time step (fs)">1.0</property>
                <property name="Trajectory Type">xyz and history</property>
                <property name="Barostat Parameter">0.005</property>
                <property name="Production Time (ps)">1.0</property>
                <property name="Thermostat Parameter">0.05</property>
                <property name="Restart Filename">molDynamics.res</property>
                <property name="Dump Frequency (ps)">0.25</property>
            </component>

            <component name="potential">
                <property name="Try to Identify Molecules">identify molecules; retain intramolecular Coulomb forces</property>
                <property name="Assign Bonding Based on Initial Geometry Only">False</property>
                <property name="Calculate Dispersion in Reciprocal Space">False</property>
                <property name="forcefield">gulpLibrary</property>

                <component name="gulpLibrary">
                    <property name="inputFile">graphite.lib</property>
                </component>

            </component>

        </component>

    </component>

</inventory>

