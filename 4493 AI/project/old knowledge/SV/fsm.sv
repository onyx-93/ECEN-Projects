module game_fsm (clk, reset, y, z);

   input logic  clk;
   input logic  reset;
   
   output logic y; // y equals select
   output logic z; // z equals enable

   typedef enum 	logic  {s0, s1} statetype;
   statetype state, nextstate;
   
   // state register
   always_ff @(posedge clk, posedge reset)
     if (reset) state <= s0;
     else       state <= nextstate;
   
   // next state logic
   always_comb
     case (state)

       s0: begin	  
       y <= 1'b1; 
       z <= 1'b1;
       nextstate <= s1;
       end

      s1: begin	  
       y <= 1'b0; 
       z <= 1'b1;
       nextstate <= s1;
       end
     endcase
   endmodule 
   
