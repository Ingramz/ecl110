# MODBUS protocol for Danfoss ECL Comfort 110

## Physical

The device has a RS-485 transceiver (SN75LBC184P), for which connections are brought out on the display/buttons daughterboard.

Front view of the pinout:

| 1   | 2      | 3      | 4            |
|-----|--------|--------|--------------|
| GND | D- / B | D+ / A | +5V DC ?? mA |

The connector is Wieland DST85 / 4 (Art. No. [25.002.0453.0](https://eshop.wieland-electric.com/products/de/leiterplattendirektsteckklemme-dst85--4/25.002.0453.0?vendorProductId=25.002.0453.0&navigate=0) and [25.003.0453.0](https://eshop.wieland-electric.com/products/de/leiterplattendirektsteckklemme-dst85--4-ob/25.003.0453.0?vendorProductId=25.003.0453.0&navigate=0)). The best image of the connector from Danfoss can be seen from their [Danfoss Link installation video](https://youtu.be/icmg9PiaHfs?t=4) or the picture in [https://github.com/Ingramz/ecl110/issues/2]. The connector is only sold in larger quantities, however the plastic part of the connector can be 3D-printed using the step-file at https://eshop.wieland-electric.com/download/25.003.0453.0/DC0017610.STP. The plastic whiskers can be removed and replaced with bare wires bent into an "N"-shape.

The main microcontroller is Renesas R5F21258SN.

There are also six 0.1" headers on the main PCB that are probably used for servicing the device (flashing firmwares, debugging, ...). It uses 3.3V logic.

| 2   | 4      | 6    |
|-----|--------|------|
| TXD | VCC    | GND  |
| RXD | nRESET | MODE |
| 1   | 3      | 5    |

## Serial settings

* Baud rate: 19200
* Data bits: 8
* Parity: Even
* Stop bits: 1

## Communication

Communication is done using MODBUS RTU. The following values have been gathered from application 116/130, software version 1.06

|   | Read/Write | MODBUS register (PNU) | Line | Notes |
|  ------ | ------ | ------ | ------ | ------ |
|  Monday Start1 | RW | 1109 | N/A | Format: XXYY decimal where XX = 00..23 and YY = 00 or 30, XXYY = 2400 is also accepted. Value means time XX:YY. |
|  Monday Stop1 | RW | 1110 | N/A |  |
|  Monday Start2 | RW | 1111 | N/A |  |
|  Monday Stop2 | RW | 1112 | N/A |  |
|  Tuesday Start1 | RW | 1119 | N/A |  |
|  Tuesday Stop1 | RW | 1120 | N/A |  |
|  Tuesday Start2 | RW | 1121 | N/A |  |
|  Tuesday Stop2 | RW | 1122 | N/A |  |
|  Wednesday Start1 | RW | 1129 | N/A |  |
|  Wednesday Stop1 | RW | 1130 | N/A |  |
|  Wednesday Start2 | RW | 1131 | N/A |  |
|  Wednesday Stop2 | RW | 1132 | N/A |  |
|  Thursday Start1 | RW | 1139 | N/A |  |
|  Thursday Stop1 | RW | 1140 | N/A |  |
|  Thursday Start2 | RW | 1141 | N/A |  |
|  Thursday Stop2 | RW | 1142 | N/A |  |
|  Friday Start1 | RW | 1149 | N/A |  |
|  Friday Stop1 | RW | 1150 | N/A |  |
|  Friday Start2 | RW | 1151 | N/A |  |
|  Friday Stop2 | RW | 1152 | N/A |  |
|  Saturday Start1 | RW | 1159 | N/A |  |
|  Saturday Stop1 | RW | 1160 | N/A |  |
|  Saturday Start2 | RW | 1161 | N/A |  |
|  Saturday Stop2 | RW | 1162 | N/A |  |
|  Sunday Start1 | RW | 1169 | N/A |  |
|  Sunday Stop1 | RW | 1170 | N/A |  |
|  Sunday Start2 | RW | 1171 | N/A |  |
|  Sunday Stop2 | RW | 1172 | N/A |  |
|  ??? | R? | 2002 | N/A |  |
|  MOD address (MODBUS address) | R/W | 2007 | 8320 | Valid values: 0...247 |
|  ??? | R? | 2010 | N/A |  |
|  ??? | R? | 2014 | N/A |  |
|  Language | RW | 2027 | 8315 | 0 = English<br/>1 = Swedish<br/>2 = Danish<br/>3 = Finnish<br/>4 = German<br/>5 = Estonian<br/>6 = Lithuanian<br/>7 = Latvian<br/>8 = Polish |
|  ??? | R? | 2102 | N/A |  |
|  ??? | R? | 2103 | N/A |  |
|  ??? | R? | 2104 | N/A |  |
|  ??? | R? | 2105 | N/A |  |
|  ??? | R? | 2106 | N/A |  |
|  ??? | R? | 2107 | N/A |  |
|  ??? | R? | 2108 | N/A |  |
|  ??? | R? | 2109 | N/A |  |
|  ??? | R? | 2110 | N/A |  |
|   | R? | 4001 | N/A | **Pump on/off** |
|   | R? | 4100 | N/A | **Valve open?** |
|   | R? | 4101 | N/A | **Valve shut?** |
|   | RW | 4200 | N/A | **Desired Mode (1=AUTO/2=COMFORT/3=SETBACK/4=STANDBY)** |
|   | R? | 4210 | N/A | **Actual mode ?** |
|  ??? | R? | 4614 | N/A |  |
|  ECA address (choice of room panel / remote control) | RW | 11009 | 7010 | Application 130 only.<br/>0 = OFF<br/>1 = A<br/>2 = B |
|  Auto-reduct (setback temp. dependent on outdoor temp.) | RW | 11010 | 5011 | Application 130 only. TODO: FORMAT |
|  Boost | RW | 11011 | 5012 | Application 130 only. TODO: FORMAT |
|  Ramp (reference ramping) | RW | 11012 | 5013 | Application 130 only. TODO: FORMAT |
|  Optimizer (optimizing time constant) | RW | 11013 | 5014 | Application 130 only. TODO: FORMAT |
|  Intgr. time (time constant for room temp.) | RW | 11014 | 3015 | Application 130 only. TODO: FORMAT |
|  Based on (optimization based on room / outdoor temp.) | RW | 11019 | 5020 | Application 130 only. TODO: FORMAT |
|  Total stop | RW | 11020 | 5021 | Application 130 only. TODO: FORMAT |
|  P1 exercise (pump exercise) | RW | 11021 | 7022 | TODO: FORMAT |
|  M1 exercise (valve exercise) | RW | 11022 | 7023 | TODO: FORMAT |
|  Actuator (gear motor / thermo actuator) | RW | 11023 | 7024 | Application 130 only. TODO: FORMAT |
|  Limit (return temp. limitation) | RW | 11029 | 4030 | TODO: FORMAT |
|  Gain - max. (return temp. limitation - max. influence) | RW | 11034 | 4035 | TODO: FORMAT |
|  Gain - min. (return temp. limitation - min. influence) | RW | 11035 | 4036 | TODO: FORMAT |
|  Intgr. time (time constant for return temp. limitation) | RW | 11036 | 4037 | TODO: FORMAT |
|  DHW prior. (closed valve / normal operation) | RW | 11051 | 7052 | Application 130 only. TODO: FORMAT |
|  P1 frost T (frost protection) | RW | 11076 | 7077 | TODO: FORMAT |
|  P1 heat T (heat demand) | RW | 11077 | 7078 | TODO: FORMAT |
|  Priority (priority for return temp. limitation) | RW | 11084 | 4085 | Application 130 only. TODO: FORMAT |
|  Standby T (standby temperature) | RW | 11092 | 7093 | TODO: FORMAT |
|  ??? | R? | 11099 | N/A | Application 130 only. Accumulated Outside Temperature? |
|  Ext. (external override) | RW | 11140 | 7141 | TODO: FORMAT |
|  Knee point | RW | 11161 | 7162 | TODO: FORMAT |
|  ??? | R? | 11173 | N/A | Application 116 only. |
|  Motor prot. (motor protection) | RW | 11173 | 6174 | Application 130 only. TODO: FORMAT |
|  Slope | RW | 11174 | 2175 | Application 130 only. TODO: FORMAT |
|  Displace (parallel displacement) | RW | 11175 | 2176 | Application 130 only. TODO: FORMAT |
|  Temp. min. (flow temp. limit, min.) | RW | 11176 | 2177 | TODO: FORMAT |
|  Temp. max. (flow temp. limit, max.) | RW | 11177 | 2178 | TODO: FORMAT |
|  Cut-out (limit for heating cut-out) | RW | 11178 | 5179 | Application 130 only. TODO: FORMAT |
|  ??? | R? | 11179 | N/A | Application 130 only. Desired room temperature? |
|  ??? | R? | 11180 | N/A | Application 130 only. Manual temperature? |
|  Gain - max. (room temp. limitation, max.) | RW | 11181 | 3182 | Application 130 only. TODO: FORMAT |
|  Gain - min. (room temp. limitation, min.) | RW | 11182 | 3183 | Application 130 only. TODO: FORMAT |
|  Xp (proportional band) | RW | 11183 | 6184 | TODO: FORMAT |
|  Tn (integration time constant) | RW | 11184 | 6185 | TODO: FORMAT |
|  M1 run (running time of the motorized control valve) | RW | 11185 | 6186 | TODO: FORMAT |
|  Nz (neutral zone) | RW | 11186 | 6187 | TODO: FORMAT |
|  Min. on time (min. activation time gear motor) | RW | 11188 | 7189 | TODO: FORMAT |
|  ??? | R? | 11189 | N/A | Application 116 only. |
|  ??? | R? | 11190 | N/A | Application 116 only. |
|  Daylight (daylight saving time changeover) | RW | 11197 | 7198 | TODO: FORMAT |
|  ECL address (master / slave address) | RW | 11198 | 7199 | TODO: FORMAT |
|  ??? | R? | 11200 | N/A | S1 actual readout in 0.1°C, 192°C = not connected |
|  ??? | R? | 11201 | N/A | S2 actual readout in 0.1°C, 192°C = not connected |
|  ??? | R? | 11202 | N/A | S3 actual readout in 0.1°C, 192°C = not connected |
|  ??? | R? | 11203 | N/A | S4 actual readout in 0.1°C, 192°C = not connected |
|  ??? | R? | 11220 | N/A |  |
|  ??? | R? | 11221 | N/A |  |
|  ??? | R? | 11222 | N/A |  |
|  ??? | R? | 11223 | N/A |  |
|  ??? | R? | 11228 | N/A | Application 130 only. S2 desired readout |
|  ??? | R? | 11229 | N/A | S3 desired readout |
|  ??? | R? | 60007 | N/A |  |
|  ??? | RW | 60020 | N/A |  |
|  ??? | R? | 60025 | N/A |  |
|  Backlight (display brightness) | RW | 60057 | 8310 | TODO: FORMAT |
|  Contrast (display contrast) | RW | 60058 | 8311 | TODO: FORMAT |
|  Hours | RW | 64044 | 1000 | Valid range 0...23 |
|  Minutes | RW | 64045 | 1000 | Valid range 0...59 |
|  Day | RW | 64046 | 1000 | Valid range 1...31 depending on month |
|  Month | RW | 64047 | 1000 | Valid range 1...12, cannot be set if currently set day is greater than number of days in given month |
|  Year | RW | 64048 | 1000 | Year number since 2000, valid range 1..40 |
|  ??? | R? | 65534 | N/A |  |
|  ??? | R? | 65535 | N/A |  |
