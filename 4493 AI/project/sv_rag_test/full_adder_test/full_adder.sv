module FullAdder(
    input  logic                 a,         // input a
    input  logic                 b,         // input b
    input  logic                 cin,       // carry in
    output logic                 cout,      // carry out
    output logic                 s          // sum
);

assign cout = (a & b & cin) | (a & cin & ~b) | (b & cin & ~a);
assign s = (a ^ b ^ cin);

endmodule