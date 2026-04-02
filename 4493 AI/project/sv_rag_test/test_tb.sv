

// *************Provided by my llm *************

// module and_gate_testbench;

//   // Input signals
//   logic clk;
//   logic a;
//   logic b;
//   logic c;

//   // Output signals
//   logic q;

//   // Instantiate the AND gate module
//   and_gate and_gate_inst (
//     .A(a),
//     .B(b),
//     .C(c),
//     .Q(q)
//   );

//   // Clock signal
//   always #5 clk = ~clk;

//   // Testbench logic
//   initial begin
//     // Initialize inputs
//     a = 0;
//     b = 0;
//     c = 0;

//     // Test the AND gate
//     #10 a = 1; b = 0; c = 0; // Test with A=1, B=0, C=0
//     #10 a = 1; b = 1; c = 0; // Test with A=1, B=1, C=0
//     #10 a = 1; b = 0; c = 1; // Test with A=1, B=0, C=1
//     #10 a = 1; b = 1; c = 1; // Test with A=1, B=1, C=1

//     // Test the AND gate with all inputs low
//     #10 a = 0; b = 0; c = 0; // Test with all inputs low

//     // Stop the simulation
//     #20 $stop;
//   end

// endmodule


// ************* Made by me *************
module and_gate_testbench;

  // Input signals
  logic clk;
  logic a;
  logic b;
  logic y;

  // Instantiate the AND gate module
  and_gate and_gate_inst (a, b, y);
    

   // 2 ns clock
   initial 
     begin	
	clk = 1'b1;
	forever #10 clk = ~clk;
     end

  // Testbench logic
  initial begin
    // Initialize inputs
    a = 0;
    b = 0;


    // Test the AND gate
    #10 a = 0; b = 0; // Test with A=0, B=0
    #10 a = 0; b = 1; // Test with A=0, B=1
    #10 a = 1; b = 0; // Test with A=1, B=0
    #10 a = 1; b = 1; // Test with A=1, B=1

  end

endmodule