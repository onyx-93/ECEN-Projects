module top (input logic clk, reset, 
	    output logic [255:0] ff_out);

   logic 	 y;
   logic 	 z;   

   game dp (clk, z, y, ff_out);
   game_fsm control (clk, reset, y, z);

endmodule // top

   