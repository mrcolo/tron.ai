`timescale 1ns / 1ps

module model_uart(/*AUTOARG*/
   // Outputs
   TX,
   // Inputs
   RX
   );

   output TX;
   input  RX;

   parameter baud    = 115200;
   parameter bittime = 1000000000/baud;
   parameter name    = "UART0";
   
   reg [7:0] rxData;
   event     evBit;
   event     evByte;
   event     evTxBit;
   event     evTxByte;
   reg       TX;

   initial
     begin
        TX = 1'b1;
     end
   
   always @ (negedge RX)
     begin
     $dumpfile("uart.vcd");
      $dumpvars(0, model_uart);
        rxData[7:0] = 8'h1;
        #(0.5*bittime);
        repeat (8)
          begin
             #bittime ->evBit;
             rxData[7:0] = {RX,rxData[7:1]};
          end
        ->evByte;
        $display ("%d %s Received byte %02x (%s)", $stime, name, rxData, rxData);
     end
endmodule // model_uart
