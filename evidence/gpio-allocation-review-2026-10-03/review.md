# GPIO allocation candidate — independent read-only review

This proposal starts from0573bf4492817ea0263827b6f0431fb7905d4959. It changes no native circuit, imported definition, dependency, firmware or PCB routing. It is not a complete pinout or a new board version. Source-label checks are separate from the unpassed native schematic, schema, placement and fabrication gates.

## Candidate assignments

| Function/net | GPIO | Module contact | Direction |
| --- | ---: | ---: | --- |
| Buffered HOLD readback | 21 | 23 | Input |
| Microphone BCLK / WS / SD | 15 / 16 / 17 | 8 / 9 / 10 | Output / output / input |
| Amplifier BCLK / LRCLK / DIN | 9 / 8 / 7 | 17 / 12 / 7 | Outputs |
| Amplifier enable | 4 | 4 | Output |
| Haptic enable | 5 | 5 | Output |
| LCD supply enable | 6 | 6 | Output |
| LCD CS / clock / MOSI | 10 / 12 / 11 | 18 / 20 / 19 | Outputs |
| LCD DC / reset | 13 / 14 | 21 / 22 | Outputs |

The existing genuine C2913201 import has all15 corresponding labels, with no duplicate GPIO, contact or net and no excluded-pin collision. Manufacturer modulev1.8 table3-1 agrees with these physical contact numbers. GPIO35/36/37 remain reserved for N8R8 octal PSRAM; USB19/20, service UART43/44 and boot0 retain their existing roles. Straps3/45/46 and pad-JTAG39–42 are excluded from new assignments. [Module datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf), saved unchanged as references/esp32-s3-module.pdf.

## Reset and boot review

Espressif lists GPIO21 with no default input/pull configuration, and as an input during USB-OTG download initialization. Firmware must explicitly enable its input and disable pulls. The GPIO power-up table identifies typical60µs low transients on the proposed output pins; GPIO18 can also go high and stays unassigned. GPIO38 is driven low during USB-OTG download; GPIO40 goes high, reinforcing the JTAG reservation. These tables do not guarantee all ramp, reset or fault waveforms. No eFuse change is proposed. [Current manufacturer checklist](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/schematic-checklist.html#gpio), reviewed2026-10-03.

Our active-high enable candidates4/5/6 retain the already reviewed external pull-down paths. Their boot behavior still needs native integration and measured power/ramp/boot tests. The proposed HOLD contact reaches only MCU_HOLD_READ behind U26's output and1kohm R100; it must never connect directly to HOLD_HARDWARE. The earlier conditional static readback/leakage bounds remain limited to their stated voltage, temperature and pull conditions. This proposal does not close partial-power injection, firmware-driven-output contention, contact bounce or the microphone off-deadline qualification.

## Peripheral allocation

Propose I2S0 RX for the microphone pair and I2S1 TX for the amplifier, each with its own clock pins and distinct data direction. Espressif supports two standard I2S controllers; this separates the external microphone clock isolation from speaker playback. No external MCLK pin is allocated in these current application interfaces. Actual clock frequencies, duty cycle, jitter, comparator delay, channel-slot wiring and privacy behavior remain pending. Firmware implementation is outside this task. [Current ESP-IDF I2S guide, stablev6.1](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/i2s.html).

Propose write-only SPI2 with dedicated CS10/SCLK12/MOSI11. Current LCD FPC has no separate MISO; DC13/reset14 use GPIO control, not quad-SPI signals. SPI2 IO_MUX mapping supports those three pins; matrix routing is also supported. Driver/buffer/LCD timing and actual trace loads must set the final clock limit; this review does not approve a speed. [Current ESP-IDF SPI guide, stablev6.1](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/spi_master.html#gpio-matrix-and-io-mux).

GPIO1/2/18/38/47/48 remain unassigned, including candidates for future battery sensing, backlight and status functions. Exact sensing networks, external driver/control polarity, physical boot behavior and final routing may change allocation. No raw battery/USB voltage is assigned directly to a GPIO. Existing backlight, protected pack, speaker, component, native-schema and publication blockers remain unchanged.

Evidence: proposal.json and static-source-check.json include the genuine import hash and precise limits of the15-label check. This is analysis of possible connectivity, not a substituted native netlist test or a completed schematic. No source-dependent checks were rerun because source/dependencies are unchanged. No new confirmed supplier/tooling defect arose, so no duplicate issue message was sent.
