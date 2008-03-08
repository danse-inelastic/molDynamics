<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!
! [u'[u"[\'{LicenseText}\']"]']
!
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-->

<!DOCTYPE inventory>

<inventory>

    <component name="MdApp">
        <property name="typos">strict</property>
        <property name="help-persistence">False</property>
        <property name="help">False</property>
        <property name="help-properties">False</property>
        <property name="help-components">False</property>
        <property name="mdEngine">gulp</property>

        <component name="gulp">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="Engine Executable Path">/home/jbk/gulp-3.4-dev--amw--17-2-08/Src/gulp</property>
            <property name="Log Filename">molDynamics.log</property>
            <facility name="Sample">Sample</facility>
            <property name="help-properties">False</property>
            <property name="Potential">potential</property>
            <property name="help-components">False</property>
            <property name="runType">md</property>
            <property name="Compute Material Properties">False</property>
            <property name="outputDir">/home/jbk/DANSE/MolDyn/molDynamics/useCases/gulp/kc24Md</property>
            <property name="Input Filename">kc24-70K.gin</property>

            <component name="Sample">
                <property name="Pressure (GPa)">0</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="Temperature or Initial Energy (K)">70</property>
                <property name="help-components">False</property>

                <component name="xyzFile">
                    <property name="help-components">False</property>
                    <property name="help-properties">False</property>
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="inputFile">/home/jbk/DANSE/MolDyn/molDynamics/useCases/gulp/kc24Md/kc24Relaxed.xyz</property>
                </component>

            </component>


            <component name="md">
                <property name="Trajectory Filename">kc24-70K</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="Equilibration Time (ps)">0.0</property>
                <property name="Thermodynamic Ensemble">nvt</property>
                <property name="Properties Calculation Frequency (fs)">5.0</property>
                <property name="Time step (fs)">1.0</property>
                <property name="Trajectory Type">xyz and history</property>
                <property name="help-properties">False</property>
                <property name="Barostat Parameter">0.005</property>
                <property name="Production Time (ps)">1.0</property>
                <property name="help-components">False</property>
                <property name="Thermostat Parameter">0.05</property>
                <property name="Restart Filename">molDynamics.res</property>
                <property name="Dump Frequency (ps)">0.25</property>
            </component>


            <component name="potential">
                <property name="help-persistence">False</property>
                <property name="Try to Identify Molecules">identify molecules; retain intramolecular Coulomb forces</property>
                <property name="Assign Bonding Based on Initial Geometry Only">False</property>
                <property name="Calculate Dispersion in Reciprocal Space">False</property>
                <property name="help-properties">False</property>
                <property name="forcefield">gulpLibrary</property>
                <property name="help-components">False</property>
                <property name="help">False</property>

                <component name="gulpLibrary">
                    <property name="help-components">False</property>
                    <property name="help-properties">False</property>
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="inputFile">/home/jbk/DANSE/MolDyn/molDynamics/useCases/gulp/kc24Md/graphite.lib</property>
                </component>

            </component>

        </component>


        <component name="weaver">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="copyright"></property>
            <property name="creator"></property>
            <property name="timestamp">True</property>
            <property name="author"></property>
            <property name="bannerCharacter">~</property>
            <property name="help-properties">False</property>
            <property name="versionId"> $Id$</property>
            <property name="timestampLine"> Generated automatically by %s on %s</property>
            <property name="help-components">False</property>
            <property name="lastLine"> End of file </property>
            <property name="licenseText">[u'[u\'[u"[\\\'{LicenseText}\\\']"]\']']</property>
            <property name="copyrightLine">(C) %s  All Rights Reserved</property>
            <property name="organization"></property>
            <property name="bannerWidth">78</property>
        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by Renderer on Thu Mar  6 16:10:42 2008-->

<!-- End of file -->
