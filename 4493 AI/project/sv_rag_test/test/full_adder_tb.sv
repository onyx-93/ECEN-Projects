`timescale 1ns / 1ps
module tb ();

   logic    a;
   logic 	b;
   logic 	cin;
   logic 	cout;
   logic 	s;
   logic    clk;   
   
  // instantiate device under test
   fulladder dut (a, b, cin, s, cout);
 
   // 2 ns clock
   initial 
     begin	
	clk = 1'b1;
	forever #10 clk = ~clk;
     end


   initial
     begin
    
	#0   a = 0;	
	#0   b = 0;	
	#0   cin = 0;

	#20  a = 0;	
	#0   b = 0;	
	#0   cin = 1;

	#20  a = 0;	
	#0   b = 1;	
	#0   cin = 0;	

	#20  a = 0;	
	#0   b = 1;	
	#0   cin = 1;	

	#20  a = 1;	
	#0   b = 0;	
	#0   cin = 0;	

	#20  a = 1;	
	#0   b = 0;	
	#0   cin = 1;	

	#20  a = 1;	
	#0   b = 1;	
	#0   cin = 0;	

	#20  a = 1;	
	#0   b = 1;	
	#0   cin = 1;	

	#20  a = 1;	
	#0   b = 1;	
	#0   cin = 1;	
	
     end

   
endmodule

// ***** Provided by llm *****

// module test_full_adder;

//     // Inputs
//     logic [2:0] a, b, cin;
//     logic sum, cout;

//     // Instantiate the full adder
//     full_adder fa (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

//     // Test vectors
//     initial begin
//         // Test case 1: a=0, b=0, cin=0
//         a = 0; b = 0; cin = 0;
//         #1;
//         assert(sum == 0) $display("Test case 1: Pass");
//         assert(cout == 0) $display("Test case 1: Pass");

//         // Test case 2: a=0, b=0, cin=1
//         a = 0; b = 0; cin = 1;
//         #1;
//         assert(sum == 1) $display("Test case 2: Pass");
//         assert(cout == 1) $display("Test case 2: Pass");

//         // Test case 3: a=0, b=1, cin=0
//         a = 0; b = 1; cin = 0;
//         #1;
//         assert(sum == 1) $display("Test case 3: Pass");
//         assert(cout == 0) $display("Test case 3: Pass");

//         // Test case 4: a=0, b=1, cin=1
//         a = 0; b = 1; cin = 1;
//         #1;
//         assert(sum == 0) $display("Test case 4: Pass");
//         assert(cout == 1) $display("Test case 4: Pass");

//         // Test case 5: a=1, b=0, cin=0
//         a = 1; b = 0; cin = 0;
//         #1;
//         assert(sum == 1) $display("Test case 5: Pass");
//         assert(cout == 0) $display("Test case 5: Pass");

//         // Test case 6: a=1, b=0, cin=1
//         a = 1; b = 0; cin = 1;
//         #1;
//         assert(sum == 0) $display("Test case 6: Pass");
//         assert(cout == 1) $display("Test case 6: Pass");

//         // Test case 7: a=1, b=1, cin=0
//         a = 1; b = 1; cin = 0;
//         #1;
//         assert(sum == 1) $display("Test case 7: Pass");
//         assert(cout == 1) $display("Test case 7: Pass");

//         // Test case 8: a=1, b=1, cin=1
//         a = 1; b = 1; cin = 1;
//         #1;
//         assert(sum == 1) $display("Test case 8: Pass");
//         assert(cout == 1) $display("Test case 8: Pass");
//     end

// endmodule





// module FullAdder(
//     input  logic                 a,         // input a
//     input  logic                 b,         // input b
//     input  logic                 cin,       // carry in
//     output logic                 cout,      // carry out
//     output logic                 s          // sum
// );

// assign cout = (a & b & cin) | (a & cin & ~b) | (b & cin & ~a);
// assign s = (a ^ b ^ cin);

// endmodule