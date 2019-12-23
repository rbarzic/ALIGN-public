************************************************************************
* auCdl Netlist:
* 
* Library Name:  OTA_class
* Top Cell Name: single_ended_low_voltage_cascode_pmos
* View Name:     schematic
* Netlisted on:  Sep 11 21:08:22 2019
************************************************************************

*.BIPOLAR
*.RESI = 2000 
*.RESVAL
*.CAPVAL
*.DIOPERI
*.DIOAREA
*.EQUATION
*.SCALE METER
*.MEGA
.PARAM

*.GLOBAL vdd!
+        gnd!

*.PIN vdd!
*+    gnd!

************************************************************************
* Library Name: OTA_class
* Cell Name:    single_ended_low_voltage_cascode_pmos
* View Name:    schematic
************************************************************************

.SUBCKT single_ended_low_voltage_cascode_pmos Vbiasp Vinn Vinp Voutp
*.PININFO Vbiasp:I Vinn:I Vinp:I Voutp:O
MM7 Voutp Vinn net11 net18 pmos_rvt w=WA l=LA nfin=nA
MM6 net13 Vinp net11 net18 pmos_rvt w=WA l=LA nfin=nA
MM5 net11 Vbiasp vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
MM1 Voutp net17 net20 gnd! nmos_rvt w=WA l=LA nfin=nA
MM0 net13 net17 net19 gnd! nmos_rvt w=WA l=LA nfin=nA
MM9 net20 net13 gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM8 net19 net13 gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
.ENDS


.SUBCKT LG_npmos Biasn Vbiasn Vbiasp
*.PININFO Biasn:I Vbiasn:O Vbiasp:O
MM4 Vbiasp Vbiasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM2 Vbiasn Vbiasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM10 neta Biasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM3 Vbiasp Vbiasp vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
MM1 Vbiasn neta vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
MM0 neta neta vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
.ENDS

.SUBCKT CR3_2 Vbiasn Vbiasp
*.PININFO Vbiasn:O Vbiasp:O
MM3 Vbiasp Vbiasp vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
MM1 Vbiasn Vbiasp vdd! vdd! pmos_rvt w=WA l=LA nfin=nA
RR0 net15 gnd! res=rK
MM0 Vbiasn Vbiasn gnd! gnd! nmos_rvt w=WA l=LA nfin=nA
MM2 Vbiasp Vbiasn net15 gnd! nmos_rvt w=WA l=LA nfin=nA
.ENDS


xiota LG_Vbiasp Vinn Vinp Voutp single_ended_low_voltage_cascode_pmos
xiLG_npmos Biasn LG_Vbiasn LG_Vbiasp LG_npmos
xibCR3_2 Biasn Vbiasp CR3_2
.END