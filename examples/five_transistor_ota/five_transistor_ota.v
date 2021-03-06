//Verilog block level netlist file for five_transistor_ota
//Generated by UMN for ALIGN project 


module five_transistor_ota ( vinn, vdd, vss, id, vout, vinp ); 
input vinn, vdd, vss, id, vout, vinp;

DCL_PMOS_n10_X1_Y1 m1 ( .D(net8), .S(vdd) ); 
Switch_PMOS_n10_X1_Y1 m2 ( .D(vout), .G(net8), .S(vdd) ); 
SCM_NMOS_n10_X1_Y1 m5_m4 ( .DA(id), .DB(net10), .S(vss) ); 
DP_NMOS_n10_X1_Y1 m0_m3 ( .DA(net8), .GA(vinp), .S(net10), .DB(vout), .GB(vinn) ); 

endmodule
