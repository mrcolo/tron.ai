module nexys3 (/*AUTOARG*/
   // Outputs
   RsTx,
   // Inputs
   RsRx, clk
   );

`include "seq_definitions.v"
   
   // USB-UART
   input        RsRx;
   output       RsTx;

   // Logic
   input        clk;                  // 100MHz
   
   /*AUTOWIRE*/
   // Beginning of automatic wires (for undeclared instantiated-module outputs)
   wire [seq_dp_width-1:0] seq_tx_data;         // From seq_ of seq.v
   wire                 seq_tx_valid;           // From seq_ of seq.v
   wire [7:0]           uart_rx_data;           // From uart_top_ of uart_top.v
   wire                 uart_rx_valid;          // From uart_top_ of uart_top.v
   wire                 uart_tx_busy;           // From uart_top_ of uart_top.v
   
   // ===========================================================================
   // UART controller
   // ===========================================================================

   // if its the agent's action, can_send is 1 and curr_byteseq 16 bits of the board
   wire [15:0] curr_byteseq = 16'b1010101010101010;
   wire can_send = 1

   uart_top uart_top_ (// Outputs
                       .o_tx            (RsTx),
                       .o_tx_busy       (uart_tx_busy),
                       .o_rx_data       (uart_rx_data[7:0]),
                       .o_rx_valid      (uart_rx_valid),
                       // Inputs
                       .i_rx            (RsRx),
                       .i_tx_data       (test),
                       .i_tx_stb        (can_send),
                       /*AUTOINST*/
                       // Inputs
                       .clk             (clk),
                       .rst             ());
endmodule // nexys3
