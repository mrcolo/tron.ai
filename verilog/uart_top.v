module uart_top (
  output o_tx, 
  output o_tx_busy, 
  output [7:0] o_rx_data, 
  output o_rx_valid,
  input i_rx, 
  input [15:0] i_tx_data, 
  input i_tx_stb, 
  input [1:0] i_tx_meta, 
  input clk, 
  input rst);

  parameter uart_num_nib = 4; // number of nibbles to send

  parameter stIdle = 0;
  parameter stCR   = uart_num_nib+5;  //8

  /*AUTOWIRE*/
  // Beginning of automatic wires (for undeclared instantiated-module outputs)
  wire                 tfifo_empty;            // From tfifo_ of uart_fifo.v
  wire                 tfifo_full;             // From tfifo_ of uart_fifo.v
  wire [7:0]           tfifo_out;              // From tfifo_ of uart_fifo.v
  // End of automatics

  reg [7:0]               tfifo_in;
  wire                    tx_active;
  wire                    tfifo_rd;
  reg                     tfifo_rd_z;
  reg [15:0]              tx_data;
  reg [1:0]               tx_meta;
  reg [3:0]               state;

  // tells me if it's busy or not
  assign o_tx_busy = (state != stIdle);

  always @ (posedge clk)
    // if we reset, transmitter is idle
    if (rst)
      state <= stIdle;
    else
      case (state)
        // If I can send, increase state by 1
        stIdle:
          if (i_tx_stb) state <= state + 1;
        // If all is transmitted, reset
        stCR:
           if (~tfifo_full) state <= stIdle;
         default:
         // By default, if stack is not full, 
           if (~tfifo_full) begin
                state   <= state + 1;
                // shift four bits so that we can send it
                tx_data <= {tx_data,4'b0000};
           end
      endcase // case (state)

  always @*xw
    tfifo_in = tx_data[15:12];

  assign tfifo_rd = ~tfifo_empty & ~tx_active & ~tfifo_rd_z;

  assign tfifo_wr = ~tfifo_full & (state!=stIdle);

  uart_fifo tfifo_ (// Outputs
                    .fifo_cnt          (),
                    .fifo_out          (tfifo_out[7:0]),
                    .fifo_full         (tfifo_full),
                    .fifo_empty        (tfifo_empty),
                    // Inputs
                    .fifo_in           (tfifo_in[7:0]),
                    .fifo_rd           (tfifo_rd),
                    .fifo_wr           (tfifo_wr),
                    /*AUTOINST*/
                    // Inputs
                    .clk               (clk),
                    .rst               (rst));

  always @ (posedge clk)
    if (rst)
      tfifo_rd_z <= 1'b0;
    else
      tfifo_rd_z <= tfifo_rd;

  uart uart_ (// Outputs
              .received                (o_rx_valid),
              .rx_byte                 (o_rx_data[7:0]),
              .is_receiving            (),
              .is_transmitting         (tx_active),
              .recv_error              (),
              .tx                      (o_tx),
              // Inputs
              .rx                      (i_rx),
              .transmit                (tfifo_rd_z),
              .tx_byte                 (tfifo_out[7:0]),
              /*AUTOINST*/
              // Inputs
              .clk                     (clk),
              .rst                     (rst));

endmodule
