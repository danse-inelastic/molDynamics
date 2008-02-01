<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!
! [u"['{LicenseText}']"]
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
            <property name="Engine Executable Path">/home/jbk/gulp3.0/Src/gulp</property>
            <property name="Log Filename">molDynamics.log</property>
            <facility name="Sample">Sample</facility>
            <property name="help-properties">False</property>
            <property name="Potential">potential</property>
            <property name="help-components">False</property>
            <property name="runType">optimize</property>
            <property name="Compute Material Properties">False</property>
            <property name="outputDir">/home/jbk/DANSE/molDynamics/tests/gulpTests/kc24Optimize</property>
            <property name="Input Filename">molDynamics.in</property>

            <component name="Sample">
                <property name="Pressure (GPa)">None</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="Temperature or Initial Energy (K)">None</property>
                <property name="help-components">False</property>
                <property name="Partial Charges">None</property>

                <component name="xyzFile">
                    <property name="help-components">False</property>
                    <property name="help-properties">False</property>
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="inputFile">/home/jbk/DANSE/molDynamics/tests/gulpTests/kc24Optimize/kc24Relaxed.xyz</property>
                </component>

            </component>


            <component name="potential">
                <property name="help-persistence">False</property>
                <property name="Try to Identify Molecules">identify molecules; retain intramolecular Coulomb forces</property>
                <property name="Assign Bonding Based on Initial Geometry Only">True</property>
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
                    <property name="inputFile">/home/jbk/DANSE/molDynamics/tests/gulpTests/kc24Optimize/graphite.lib</property>
                </component>

            </component>


            <component name="optimize">
                <property name="help-persistence">False</property>
                <property name="Optimize Coordinates">True</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="Optimize Cell">False</property>
                <property name="help-components">False</property>
                <property name="Constraints">constant volume</property>
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
            <property name="licenseText">[u'[u"[\'{LicenseText}\']"]']</property>
            <property name="copyrightLine">(C) %s  All Rights Reserved</property>
            <property name="organization"></property>
            <property name="bannerWidth">78</property>
        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by Renderer on Sat Dec  1 16:58:54 2007-->

<!-- End of file -->
