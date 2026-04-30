`timescale 1ns / 1ps
module stimulus ();

   logic  clk;
   logic  reset;
   logic en;
   logic select;
   logic [255:0] ff_out;
   
   

   // Instantiate DUT
     game dut (clk,en, select, ff_out);  
   
   // Setup the clock to toggle every 1 time units 
   initial 
     begin	
	clk = 1'b1;
	forever #5 clk = ~clk;
     end

   initial 
     begin      
	#0   reset = 1'b1;
	#40  reset = 1'b0;	
	#0   en = 1'b1;
	#30  select= 1'b1;
	#80  select = 1'b0;
     end

endmodule // FSM_tb
