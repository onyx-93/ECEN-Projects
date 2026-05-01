`timescale 1ns / 1ps
module stimulus ();

   logic  clk;
   logic  a;
   logic  reset;
   logic b;
   logic  [3:0]y;
   
   // Instantiate DUT
   FSM dut (clk, reset, a, b, y);   
   
   // Setup the clock to toggle every 1 time units 
   initial 
     begin	
	clk = 1'b1;
	forever #5 clk = ~clk;
     end

   initial 
     begin      

     
	#0  reset = 1'b1;
   #40 reset = 1'b0;
	
   // Right Turn
   #20  b = 1'b1;
	#0   a = 1'b0;
   
   // Left Turn
   #20  b = 1'b0;
	#0  a = 1'b1;

   // Hazards
   #20  b = 1'b1;
   #0  a =1'b1;
  
     end

endmodule