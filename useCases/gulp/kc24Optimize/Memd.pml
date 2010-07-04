<?xml version="1.0"?>
<!DOCTYPE inventory>
<inventory>

    <component name="Memd">
        <property name="engine">gulp</property>

        <component name="gulp">
            <property name="Engine Executable Path">/home/jbk/officialGulp3.4/Src/gulp</property>
            <property name="Log Filename">molDynamics.log</property>
            <facility name="Sample">Sample</facility>
            <property name="Potential">potential</property>
            <property name="runType">optimize</property>
            <property name="Compute Material Properties">False</property>
            <property name="outputDir">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Optimize</property>
            <property name="Input Filename">molDynamics.in</property>

            <component name="Sample">
                <property name="Pressure (GPa)">0</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="Temperature or Initial Energy (K)">0</property>

                <component name="xyzFile">
                    <property name="inputFile">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Optimize/kc24Relaxed.xyz</property>
                </component>

            </component>
            
            <component name="potential">
                <property name="Try to Identify Molecules">identify molecules; retain intramolecular Coulomb forces</property>
                <property name="Assign Bonding Based on Initial Geometry Only">True</property>
                <property name="Calculate Dispersion in Reciprocal Space">False</property>
                <property name="forcefield">gulpLibrary</property>

                <component name="gulpLibrary">
                    <property name="inputFile">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Optimize/graphite.lib</property>
                </component>

            </component>

            <component name="optimize">
                <property name="Optimize Coordinates">True</property>
                <property name="Optimize Cell">False</property>
                <property name="Constraints">constant volume</property>
            </component>

        </component>

    </component>

</inventory>
