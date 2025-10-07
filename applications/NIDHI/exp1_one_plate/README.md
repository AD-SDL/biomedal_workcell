# Experiment 1

Adaptive Lab Evolution Experimental Application

Science leads: Nidhi Gupta, Paul Hanke, Chris Henry
Robotics lead: Casey Stone

## Experiment Abstract

This project combines AI hypothesis generation with high-throughput experimental biology to accelerate rational microbial engineering. AI is used to design gene variants for vanillate/vertarate demethylase enzymes in Acinetobacter baylyi. These designs are then tested using automated lab systems and evolving bacterial cultures. Experimental results are fed back into AI models for iterative refinement.

## General Application Description

In this experimental application, the 6 identical 96-well microplates will be created in an Opentrons OT-2 that contain a specific substrate. 5 of those substrate plates will be removed by hand and placed into a plate hotel. Cells will then be dispersed from a stock deepwell plate to 3 columns of the remaining substrate plate, then the plate will be transferred to the BMG microplate reader and incubated for 12 hours with OD(590) readings every 30 min. After the 12 hours, the microplate will be transferred back to the Opentrons OT-2 where 3 more columns of the microplate will be inoculated with cells form the previously inoculated columns and placed back into the BMG plate reader for another 12 hour cycle. This cycle will repeat until all columns of all 6 substrate plates are used, approximately 12 days.
