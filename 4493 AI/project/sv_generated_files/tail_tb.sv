`timescale 1ns / 1ps
module stimulus ();

   logic  clk;
   logic  left;
   logic  reset;
   logic right;
   logic  [3:0] out;
   
   integer handle3;
   integer desc3;
   
   // Instantiate DUT
   taillight_fsm dut (clk, reset, left, right, out);   
   
   // Setup the clock to toggle every 1 time units 
   initial 
     begin	
	clk = 1'b1;
	forever #5 clk = ~clk;
     end

   // initial
   //   begin
	// // Gives output file name
	// handle3 = $fopen("fsm.out");
	// // Tells when to finish simulation
	// #6000 $finish;		
   //   end

   // always 
   //   begin
	// desc3 = handle3;
	// #10 $fdisplay(desc3, "%b || %b  %b || %b", 
	// 	     reset, a, b, y);
   //   end   
   
   initial 
     begin      

     
	#0  reset = 1'b1;
   #40 reset = 1'b0;
	
   // Right Turn
   #20  right = 1'b1;
	#0   left = 1'b0;
   
   // Left Turn
   #20  right = 1'b0;
	#0  left = 1'b1;

   // Hazards
   #20  right = 1'b1;
   #0  left =1'b1;
  
     end

endmodule