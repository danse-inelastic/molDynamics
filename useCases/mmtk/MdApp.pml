<?xml version="1.0"?>
<!--
! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!
!
! {LicenseText}
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
                <property name="Pressure (GPa)">None</property>
                <property name="atomicStructure">unitCellBuilder</property>
                <property name="help-persistence">False</property>
                <property name="help">False</property>
                <property name="help-properties">False</property>
                <property name="Temperature or Initial Energy (K)">None</property>
                <property name="help-components">False</property>

                <component name="unitCellBuilder">
                    <property name="help-persistence">False</property>
                    <property name="help">False</property>
                    <property name="Unit Cell">UnitCell a=[ 1.  0.  0.], b=[ 0.  1.  0.], c=[ 0.  0.  1.]
</property>
                    <property name="Atomic/Species information"></property>
                    <property name="help-properties">False</property>
                    <property name="help-components">False</property>

                    <component name="UnitCell">
                        <property name="c Vector">0.0 0.0 1.0</property>
                        <property name="help-persistence">False</property>
                        <property name="help">False</property>
                        <property name="a Vector">1.0 0.0 0.0</property>
                        <property name="b Vector">0.0 1.0 0.0</property>
                        <property name="help-properties">False</property>
                        <property name="help-components">False</property>
                        <property name="Space Group">1</property>
                    </component>

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
            <property name="licenseText">['{LicenseText}']</property>
            <property name="copyrightLine">(C) %s  All Rights Reserved</property>
            <property name="organization"></property>
            <property name="bannerWidth">78</property>
        </component>

    </component>

</inventory>

<!-- version-->
<!-- $Id$-->

<!-- Generated automatically by Renderer on Wed Nov 26 15:02:19 2008-->

<!-- End of file -->