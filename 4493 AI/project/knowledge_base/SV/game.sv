   module game (clk, en, select, ff_out);
   output logic [255:0] ff_out;
   input logic 		clk;
   input logic 		en;
   input logic 		select;
   logic [255:0] 	seed;
   logic [255:0] 	grid_input;
   logic [255:0] 	ff_input;
   logic 		reset;
   assign seed = 256'h04121454_64247965_00341346_3C286478_04121454_64247965_00341346_3C286478;
   assign reset = 1'b0;

   mux2 #(256)mux (ff_out, seed, select, grid_input);
   datapath #(256)path (grid_input, ff_input);
   flopenr #(256)flip_flop (clk, reset, en, ff_input, ff_out);

endmodule

