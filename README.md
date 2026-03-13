# antenna-switcher
Control code for the antenna switches connected to OpenWebRX Raspberry Pi

Antenna Switcher table mapping.
SW1, SW2 and SW3 are single input to 4 ouput antenna switchers controlled by two inputs; A and B. These six control inputs are connected to raspberry pi GPIOs as indicated in the table below. Thes switches are connected such that the antenna input for each selected SDR is connected either to a VHF or HF antenna depending on what OpenWebRX profile is selected.
 The LED Indicator GPIOs are connected to green LEDs that shine aon the selected SDR to show which is activated.

GPIO mapping:

|                    | SW1 selects antenna, SW2&3 are ganged to connedt antenn to SDR                     | SDR Green LED inicators                                               |
|             |      | SW1 | A        | B        | SW2 | A        | B         | SW3 | A        | B        |          |
| ----------- | ---- | --- | -------- | -------- | --- | -------- | --------- | --- | -------- | -------- | -------- |
|             |      |     | GPIO11   | GPIO13   |     | GPIO15   | GPIO16    |     | GPIO18   | GPIO22   | GPIO40   | GPIO38   | GPIO36   | GPIO32   | GPIO26   | GPIO24   |
| SDR         | Band |     | (GPIO17) | (GPIO27) |     | (GPIO22) | (GPIO 23) |     | (GPIO24) | (GPIO25) | (GPIO21) | (GPIO20) | (GPIO16) | (GPIO12) | (GPIO07) | (GPIO08) |
| RTL-SDR     | HF   | RF2 | High     | Low      | RF2 | High     | Low       | \-  |          |          | High     |          |          |          |          |          |
|             | VHF  | RF1 | Low      | Low      | RF2 | High     | Low       | \-  |          |          | High     |          |          |          |          |          |
| AirspHF+    | HF   | RF2 | High     | Low      | RF4 | High     | High      | \-  |          |          |          | High     |          |          |          |          |
|             | VHF  | RF1 | Low      | Low      | RF3 | Low      | High      | \-  |          |          |          | High     |          |          |          |          |
| LimeSDR     | HF   | RF2 | High     | Low      | RF1 | Low      | Low       | RF1 | Low      | Low      |          |          | High     |          |          |          |
|             | VHF  | RF1 | Low      | Low      | RF1 | Low      | Low       | RF1 | Low      | Low      |          |          | High     |          |          |          |
| B205mini    | HF   | RF2 | High     | Low      | RF1 | Low      | Low       | RF2 | High     | Low      |          |          |          | High     |          |          |
|             | VHF  | RF1 | Low      | Low      | RF1 | Low      | Low       | RF2 | High     | Low      |          |          |          | High     |          |          |
| ADALM-Pluto | HF   | RF2 | High     | Low      | RF1 | Low      | Low       | RF3 | Low      | High     |          |          |          |          | High     |          |
|             | VHF  | RF1 | Low      | Low      | RF1 | Low      | Low       | RF3 | Low      | High     |          |          |          |          | High     |          |
| HackRF      | HF   | RF2 | High     | Low      | RF1 | Low      | Low       | RF4 | High     | High     |          |          |          |          |          | High     |
|             | VHF  | RF1 | Low      | Low      | RF1 | Low      | Low       | RF4 | High     | High     |          |          |          |          |          | High     |

SW1,2&3 input truth table:

| Truth Table | A    | B    | Signal |
| ----------- | ---- | ---- | ------ |
|             | Low  | Low  | RF1    |
|             | High | Low  | RF2    |
|             | Low  | High | RF3    |
|             | High | High | RF4    |


