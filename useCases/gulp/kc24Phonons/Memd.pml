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
            <property name="runType">phonon</property>
            <property name="Compute Material Properties">False</property>
            <property name="outputDir">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Phonons</property>
            <property name="Input Filename">kc24-70K.gin</property>

            <component name="Sample">
                <property name="Pressure (GPa)">0</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="Temperature or Initial Energy (K)">0</property>

                <component name="xyzFile">
                    <property name="inputFile">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Phonons/kc24Relaxed.xyz</property>
                </component>

            </component>

            <component name="phonon">
                <property name="Monkhorst Pack mesh">1 1 4</property>
                <property name="Filename for DOS Output">phonon</property>
                <property name="Project the DOS onto certain species">H</property>
                <property name="Broaden the DOS">True</property>
            </component>

            <component name="potential">
                <property name="Try to Identify Molecules">identify molecules; retain intramolecular Coulomb forces</property>
                <property name="Assign Bonding Based on Initial Geometry Only">True</property>
                <property name="Calculate Dispersion in Reciprocal Space">False</property>
                <property name="forcefield">gulpLibrary</property>

                <component name="gulpLibrary">
                    <property name="inputFile">/home/jbk/workspace/molDynamics/useCases/gulp/kc24Phonons/graphite.lib</property>
                </component>

            </component>

        </component>

    </component>

</inventory>
