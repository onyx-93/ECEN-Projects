module color_fsm (clk, reset, y,z);

input logic clk;
input logic reset;
output logic [23:0] y;// alive
output logic [23:0] z;// dead



 typedef enum 	logic   {s0, s1} statetype;
   statetype state, nextstate;
   
   // state register
   always_ff @(posedge clk, posedge reset)
     if (reset) state <= s0;
     else  state <= nextstate;

   
   // next state logic
   always_comb
     case (state)

       s0: begin	  
       y <= 24'h008000; //GREEN
       z <= 24'hFFFFFF; //WHITE
       nextstate <= s1;
       end

      s1: begin	  
       y <= 24'hFF0000; //RED
       z <= 24'hFFFFFF; //WHITE
       nextstate <= s0;
       end

     endcase
endmodule
