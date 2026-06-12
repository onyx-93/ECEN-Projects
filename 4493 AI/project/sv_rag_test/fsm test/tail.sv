module FSM (
    input  logic       clk,
    input  logic       reset,
    input  logic       a,
    input  logic       b,
    output logic [3:0] y
);

    typedef enum logic [2:0] {
        S0, S1, S2, S3, S4, S5, S6
    } statetype;

    statetype state, nextstate;

    // State Register - only updates on slow clk_en
    always_ff @(posedge clk, posedge reset) begin
        if (reset)
            state <= S0;
        else        
            state <= nextstate;
    end

    // Next-state and Output logic (use blocking assignments in always_comb)
    always_comb

        case (state)
            S0: begin
                y <= 4'b0000;
                if (a && b)      nextstate <= S5;
                else if (b)      nextstate <= S3;
                else if (a)      nextstate <= S1;
                else             nextstate <= S0;
            end

            S1: begin y <= 4'b01_00; nextstate <= S2; end
            S2: begin y <= 4'b11_00; nextstate <= S0; end

            S3: begin y <= 4'b00_10; nextstate <= S4; end
            S4: begin y <= 4'b00_11; nextstate <= S0; end

            S5: begin y <= 4'b01_10; nextstate <= S6; end
            S6: begin y <= 4'b11_11; nextstate <= S0; end

            default: begin
                y <= 4'b0000;
                nextstate <= S0;
            end
        endcase

endmodule