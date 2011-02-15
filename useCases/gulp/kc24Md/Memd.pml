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
            <property name="runType">md</property>
            <property name="Compute Material Properties">False</property>
            <property name="outputDir">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Md</property>
            <property name="Input Filename">kc24-70K.gin</property>

            <component name="Sample">
                <property name="Pressure (GPa)">0</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="Temperature or Initial Energy (K)">70</property>

                <component name="xyzFile">
                    <property name="inputFile">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Md/kc24Relaxed.xyz</property>
                </component>

            </component>

            <component name="md">
                <property name="trajectoryFilename">kc24-70K</property>
                <property name="equilibrationTime (ps)">0.0</property>
                <property name="ensemble">nvt</property>
                <property name="propCalcInterval">5.0</property>
                <property name="timeStep">1.0</property>
                <property name="trajectoryType">xyz and history</property>
                <property name="barostatParameter">0.005</property>
                <property name="productionTime">1.0</property>
                <property name="thermostatParameter">0.05</property>
                <property name="restartFilename">molDynamics.res</property>
                <property name="dumpInterval">0.25</property>
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

