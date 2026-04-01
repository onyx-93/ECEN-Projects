# Copyright 1991-2016 Mentor Graphics Corporation
# 
# Modification by Oklahoma State University
# Use with Testbench 
# James Stine, 2008
# Go Cowboys!!!!!!
#
# All Rights Reserved.

onbreak {resume}

# Create library
if [file exists work] {
    vdel -all
}
vlib work

# Compile source files
vlog test_1.sv test_tb.sv

# Start and run simulation 
# Changed work.tb to work.and_gate_testbench
vsim -voptargs=+acc work.and_gate_testbench

# Only useful if NOT running with -c (batch mode)
view list
view wave

# Display input and output signals as hexadecimal values
# Changed path to match your actual module name
add wave -hex -r /and_gate_testbench/*

# Add list and log
add list -hex -r /and_gate_testbench/*
add log -r /*

# Set Wave Output Items 
# Note: These commands mostly apply to the GUI environment
TreeUpdate [SetDefaultTree]
WaveRestoreZoom {0 ps} {75 ns}
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2

# Run the Simulation
run 250 ns
