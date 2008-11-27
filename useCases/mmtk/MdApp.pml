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
        <property name="dumpconfiguration">False</property>
        <property name="help">False</property>
        <property name="help-properties">False</property>
        <property name="help-components">False</property>
        <property name="mdEngine">mmtk</property>

        <component name="mmtk">
            <property name="help-persistence">False</property>
            <property name="help">False</property>
            <property name="Integrator">velocity-verlet</property>
            <property name="Engine Executable Path"></property>
            <property name="Log Filename">molDynamics.log</property>
            <facility name="Sample">Sample</facility>
            <property name="help-properties">False</property>
            <property name="help-components">False</property>
            <property name="runType">md</property>
            <property name="outputDir">/home/jbk/DANSE/MolDyn/molDynamics/useCases/mmtk</property>

            <component name="Sample">
                <property name="Pressure (GPa)">0</property>
                <property name="atomicStructure">xyzFile</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="Temperature or Initial Energy (K)">100</property>
                <property name="help-components">False</property>

                <component name="xyzFile">
                    <property name="help-components">False</property>
                    <property name="help-properties">False</property>
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="inputFile">/home/jbk/DANSE/MolDyn/molDynamics/useCases/mmtk/argon.xyz</property>
                </component>

            </component>


            <component name="md">
                <property name="Trajectory Filename">molDynamics</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="Equilibration Time (ps)">0.0</property>
                <property name="Thermodynamic Ensemble">nve</property>
                <property name="Properties Calculation Frequency (fs)">5.0</property>
                <property name="Time step (fs)">0.5</property>
                <property name="Trajectory Type">xyz</property>
                <property name="help-properties">False</property>
                <property name="Barostat Parameter">0.005</property>
                <property name="Production Time (ps)">5.0</property>
                <property name="help-components">False</property>
                <property name="Thermostat Parameter">0.005</property>
                <property name="Restart Filename">molDynamics.res</property>
                <property name="Dump Frequency (ps)">0.0</property>
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

<!-- Generated automatically by Renderer on Thu Nov 27 05:07:37 2008-->

<!-- End of file -->
