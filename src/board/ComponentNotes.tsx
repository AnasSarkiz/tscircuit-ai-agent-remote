import { Fragment } from "react"

// Native schematic annotations; references follow the components on each sheet.
export const componentExplanations = {
  "mcu-usb-review": [
    ["U1", "ESP32-S3: runs firmware, Wi-Fi and board interfaces."],
    ["J1", "USB-C: 5 V input, USB data and USB programming."],
    ["D2", "Protects both USB data lines against ESD."],
    ["U12", "Resets the MCU when its 3.3 V supply is too low."],
    ["J6", "Standard JST UART: RX/GND/TX; separate power, manual BOOT/RESET."],
    ["R31", "Series resistor on USB D+ to the MCU."],
    ["R32", "Series resistor on USB D- to the MCU."],
    ["R33", "USB CC1 pull-down identifies a power-consuming device."],
    ["R34", "USB CC2 pull-down supports either plug orientation."],
    ["R35", "Series resistor between reset supervisor and MCU EN."],
    ["R36", "Holds BOOT high during normal startup."],
    ["R37", "Pulls MCU EN low when its driver is inactive."],
    ["R38", "Series resistor in the backup UART transmit path."],
    ["C30", "22 uF bulk capacitor for the MCU 3.3 V supply."],
    ["C31", "100 nF local bypass at the MCU supply escape."],
    ["C32", "Additional 100 nF bypass on the 3.3 V rail."],
  ],
  ChargerSheet: [
    ["U16", "Battery charger and power path; USB100 startup mode."],
    ["J3", "Battery/NTC connector; outer polarity unverified."],
    ["C1", "Filters the USB 5 V input to the charger."],
    ["C2", "Stabilizes the charger's battery terminal."],
    ["C3", "Filters VSYS, the charger's system-power output."],
    ["R1", "Programs the battery charge-current setting."],
    ["R2", "Programs the adjustable input-current limit."],
    ["R3", "Pull-up for the active-low charger power-good output."],
    ["R4", "Pull-up for the active-low charging-status output."],
  ],
  "regulated-3v3-review": [
    ["U2", "Buck-boost converter: VSYS to regulated 3.3 V."],
    ["L1", "Stores energy between the converter's switch nodes."],
    ["C4", "Filters the converter's VSYS input."],
    ["C5", "Stabilizes the converter's 3.3 V output."],
    ["R5", "Upper feedback-divider resistor; senses 3.3 V."],
    ["R6", "Lower feedback-divider resistor; sets output with R5."],
    ["R7", "Pull-up for the converter's power-good output."],
  ],
  "display-logic-review": [
    ["U13", "Switchable 2.8 V regulator for the display circuitry."],
    ["U14", "Buffers MCU control signals onto the display rail."],
    ["J7", "Display FPC connector; contact orientation unverified."],
    ["C40", "Filters the display regulator's 3.3 V input."],
    ["C41", "Bulk capacitor on the 2.8 V display supply."],
    ["C42", "High-frequency bypass on the display supply."],
    ["C43", "Additional display-supply bypass for the logic buffer."],
    ["R40", "Keeps the display regulator disabled at startup."],
    ["R41", "Discharges the switched display supply."],
    ["R47", "Pull-down on the MCU chip-select buffer input."],
    ["R42", "Pull-up on the display chip-select output."],
    ["R48", "Pull-down on the MCU display-reset buffer input."],
    ["R43", "Pull-up on the display-reset output."],
    ["R49", "Pull-down on the MCU data/command buffer input."],
    ["R44", "Pull-up on the display data/command output."],
    ["R50", "Pull-down on the MCU display-clock buffer input."],
    ["R45", "Pull-up on the display-clock output."],
    ["R51", "Pull-down on the MCU display-data buffer input."],
    ["R46", "Pull-up on the display-data output."],
  ],
  "speaker-amplifier-review": [
    ["U3", "Converts digital I2S audio into speaker drive."],
    ["J4", "External speaker across two driven outputs; no GND."],
    ["Q1", "MCU-controlled transistor driving the enable switch."],
    ["Q2", "High-side transistor supplying amplifier enable."],
    ["C50", "Bulk filtering for the amplifier's VSYS supply."],
    ["C51", "High-frequency bypass for the amplifier supply."],
    ["R60", "Series resistor from MCU enable to Q1's gate."],
    ["R61", "Pulls Q1's gate low when MCU enable is inactive."],
    ["R62", "Pulls Q2's gate to VSYS to keep Q2 off by default."],
    ["R63", "Series resistor feeding amplifier shutdown/mode."],
    ["R64", "Pull-down on amplifier shutdown/mode."],
    ["R65", "Series damping resistor on amplifier I2S data."],
    ["R68", "Pull-down on the amplifier I2S data input."],
    ["R66", "Series damping resistor on amplifier bit clock."],
    ["R69", "Pull-down on the amplifier bit-clock input."],
    ["R67", "Series damping resistor on amplifier word clock."],
    ["R70", "Pull-down on the amplifier word-clock input."],
  ],
  "haptic-driver-review": [
    ["U22", "Switchable 3.0 V regulator for the vibration motor."],
    ["Q9", "Low-side transistor switching the motor return."],
    ["D3", "Flyback diode clamps the motor's turn-off transient."],
    ["C70", "Filters the motor regulator's VSYS input."],
    ["C71", "Bulk capacitor on the motor supply."],
    ["C72", "Noise-suppression capacitor across the motor."],
    ["R82", "Discharges the switched motor supply."],
    ["R83", "Series resistor from MCU enable to Q9's gate."],
    ["R84", "Pulls Q9's gate low to keep the motor off by default."],
    ["R85", "Keeps the motor regulator disabled at startup."],
  ],
  "mic-regulated-clock-review": [
    ["U23", "2.8 V microphone regulator enabled by TALK/HOLD."],
    ["U24", "Open-drain buffers for microphone bit/word clocks."],
    ["C73", "Filters the privacy-switched microphone input rail."],
    ["C74", "Bulk filtering on the 2.8 V microphone supply."],
    ["C75", "High-frequency bypass for the clock buffer."],
    ["R86", "Discharges the switched microphone supply."],
    ["R87", "Pulls TALK/HOLD low to disable microphone power."],
    ["R88", "Series resistor on MCU microphone bit clock."],
    ["R89", "Series resistor on MCU microphone word clock."],
    ["R90", "Pull-down on the bit-clock buffer input."],
    ["R91", "Pull-down on the word-clock buffer input."],
    ["R92", "Pull-up to 2.8 V for open-drain bit-clock output."],
    ["R93", "Pull-up to 2.8 V for open-drain word-clock output."],
    ["R94", "Pull-down on the microphone bit-clock output."],
    ["R95", "Pull-down on the microphone word-clock output."],
  ],
  "hold-readback-review": [
    ["U26", "Schmitt buffer cleans TALK/HOLD for MCU readback."],
    ["R99", "Pull-down on the physical TALK/HOLD signal."],
    ["R100", "Series resistor in the MCU TALK/HOLD readback path."],
    ["C78", "Supply bypass for the TALK/HOLD buffer."],
  ],
  "battery-ready-review": [
    ["U25", "Battery-voltage supervisor controls regulator enable."],
    ["R96", "Pull-up on the regulator-enable signal to VSYS."],
    ["R97", "Pull-down on regulator enable; forms bias with R96."],
    ["C76", "Supply bypass for the battery supervisor."],
    ["C77", "Filters the regulator-enable signal."],
  ],
  MicrophonesSheet: [
    ["U4", "Digital I2S microphone assigned to the left channel."],
    ["U5", "Digital I2S microphone assigned to the right channel."],
    ["C80", "100 nF supply bypass for microphone U4."],
    ["C81", "100 nF local U5 bypass; direct top supply and ground loop."],
    ["U7", "Comparator restores microphone data to 3.3 V logic."],
    ["R26", "Pull-down on the shared microphone data line."],
    ["R27", "Series resistor from buffered microphone data to MCU."],
    ["R29", "Upper divider resistor for data-comparator reference."],
    ["R30", "Lower divider resistor for data-comparator reference."],
    ["C25", "Supply bypass for the microphone data comparator."],
    ["C26", "Filters the data-comparator reference voltage."],
  ],
  ControlsSheet: [
    ["SW4", "Top TALK button powers microphones while held."],
    ["SW1", "BOOT button selects the MCU download mode."],
    ["SW2", "RESET button pulls MCU EN low."],
    ["SW5", "Privacy switch selects microphone supply or ground."],
    ["TP_MOTOR_P", "Motor positive solder pad: VMOTOR (M+)."],
    ["TP_MOTOR_N", "Motor switched-return pad: HAPTIC_N (M-), not GND."],
  ],
  BacklightSheet: [
    ["U27", "Charge-pump LED driver for four backlight channels."],
    ["R102", "Programs the backlight LED-current setting."],
    ["R103", "Series resistor on MCU backlight PWM/enable."],
    ["R104", "Pull-down keeps the backlight disabled at startup."],
    ["C82", "First flying capacitor for the LED charge pump."],
    ["C83", "Second flying capacitor for the LED charge pump."],
    ["C84", "Filters the backlight driver's 3.3 V input."],
    ["C85", "Stabilizes the charge-pump LED supply output."],
  ],
  "test-access": [
    ["TP1", "Ground reference for voltage measurements."],
    ["TP2", "Probe USB 5 V input (VBUS)."],
    ["TP3", "Probe battery positive rail (PACK_BAT)."],
    ["TP4", "Probe charger system-power output (VSYS)."],
    ["TP5", "Probe regulated 3.3 V supply (V3V3)."],
    ["TP6", "Probe switched 2.8 V microphone supply (VMIC)."],
    ["TP7", "Probe the physical TALK/HOLD signal."],
    ["TP8", "Probe the active-low charging-status signal."],
  ],
} as const

export const guideSheets = [
  {
    name: "mcu-usb-review",
    guideIndex: 14,
    footerY: -8.1,
    title: "MCU, USB and programming",
  },
  {
    name: "ChargerSheet",
    guideIndex: 15,
    footerY: -7.83,
    title: "USB100 charging - PACK PROVISIONAL",
  },
  {
    name: "regulated-3v3-review",
    guideIndex: 16,
    footerY: -8.8,
    title: "3.3 V buck boost",
  },
  {
    name: "display-logic-review",
    guideIndex: 17,
    footerY: -10.05,
    title: "PROVISIONAL BuyDisplay ER-TFT026-1 SPI II",
  },
  {
    name: "speaker-amplifier-review",
    guideIndex: 18,
    footerY: -12.8,
    title: "External 8 ohm speaker",
  },
  {
    name: "haptic-driver-review",
    guideIndex: 19,
    footerY: -7.83,
    title: "External motor and flyback",
  },
  {
    name: "mic-regulated-clock-review",
    guideIndex: 20,
    footerY: -3.3,
    title: "Microphone power and clocks",
  },
  {
    name: "hold-readback-review",
    guideIndex: 21,
    footerY: -4.8,
    title: "Top HOLD control",
  },
  {
    name: "battery-ready-review",
    guideIndex: 22,
    footerY: -3.8,
    title: "Battery readiness - PROVISIONAL",
  },
  {
    name: "MicrophonesSheet",
    guideIndex: 23,
    footerY: -10.5,
    title: "Dual microphones - prototype",
  },
  {
    name: "ControlsSheet",
    guideIndex: 24,
    footerY: -7.6,
    title: "Physical controls and motor solder pads",
  },
  {
    name: "BacklightSheet",
    guideIndex: 25,
    footerY: -7.83,
    title: "Four-channel provisional display backlight",
  },
  {
    name: "test-access",
    guideIndex: 26,
    footerY: -1.6,
    title: "Test access",
  },
] as const

export function ComponentNotes({ sheet }: { sheet: keyof typeof componentExplanations }) {
  const guide = guideSheets.find((entry) => entry.name === sheet)
  if (!guide) throw new Error(`Missing component guide for ${sheet}`)
  return (
    <schematictext
      schX={-9}
      schY={guide.footerY}
      text={`Component explanations: schematic sheet ${guide.guideIndex}.`}
      fontSize={0.25}
      anchor="left"
    />
  )
}

export function ComponentGuides() {
  return (
    <>
      {guideSheets.map((guide) => (
        <Fragment key={guide.name}>
          <schematicsheet
            name={`component-guide-${guide.name}`}
            displayName={`AI Remote - Component guide: ${guide.title}`}
            sheetIndex={guide.guideIndex}
            sheetSize="A4"
          >
            <schematicrect
              schX={0}
              schY={0}
              width={27}
              height={20}
              strokeWidth={0.03}
              color="#777777"
            />
            <schematictext
              schX={-11}
              schY={9}
              text="COMPONENT GUIDE"
              fontSize={0.7}
              anchor="left"
            />
            <schematictext
              schX={-11}
              schY={8.1}
              text={`${guide.title} - circuit sheet ${guide.guideIndex - 13}`}
              fontSize={0.25}
              anchor="left"
            />
            {componentExplanations[guide.name].map(([reference, explanation], index) => (
              <Fragment key={reference}>
                <schematictext
                  schX={-11}
                  schY={7.2 - index * 0.85}
                  text={`${reference}: ${explanation}`}
                  fontSize={0.45}
                  anchor="left"
                />
              </Fragment>
            ))}
          </schematicsheet>
        </Fragment>
      ))}
    </>
  )
}
