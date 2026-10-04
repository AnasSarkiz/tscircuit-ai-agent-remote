const testNets = [
  "GND",
  "VBUS",
  "PACK_BAT",
  "VSYS",
  "V3V3",
  "VMIC",
  "HOLD_HARDWARE",
  "CHARGE_STATUS_N",
] as const

export function BoardFeatures() {
  return (
    <>
      {/* M2 mounting trial: final enclosure, flex and hardware Z fit remain open. */}
      {[
        { x: 22, y: -23 },
        { x: -21.5, y: -29.5 },
      ].map((mount, index) => (
        <group key={index} name={`mount-${index + 1}`} pcbX={0} pcbY={0}>
          <hole diameter={2.2} pcbX={mount.x} pcbY={mount.y} />
          <keepout
            shape="circle"
            radius={3}
            pcbX={mount.x}
            pcbY={mount.y}
            layers={["top", "inner1", "inner2", "bottom"]}
          />
          <pcbnotetext
            pcbX={mount.x + 4}
            pcbY={mount.y}
            text={`M${index + 1}: M2 / NPTH 2.2 / KO 6`}
            fontSize={0.5}
          />
        </group>
      ))}
      <keepout
        shape="rect"
        pcbX={-12}
        pcbY={35.675}
        width={20}
        height={8}
        layers={["top", "inner1", "inner2", "bottom"]}
        excludeRefs={[".U1"]}
      />
      <pcbnotetext
        pcbX={-15}
        pcbY={-27}
        text="B-005 MIC PASTE: BLOCKED"
        fontSize={0.6}
        color="#ffb34d"
      />
      <pcbnoterect
        pcbX={-5.8}
        pcbY={-0.8}
        width={46}
        height={64}
        strokeWidth={0.15}
        isStrokeDashed
        color="#33b5e5"
      />
      <pcbnoterect
        pcbX={-5.8}
        pcbY={0}
        width={39.6}
        height={52.8}
        strokeWidth={0.1}
        isStrokeDashed
        color="#33b5e5"
      />
      <pcbnotetext
        pcbX={0}
        pcbY={6.5}
        text="PROVISIONAL ER-TFT026-1 / 82.7% BODY COVERAGE"
        fontSize={1}
        color="#33b5e5"
      />
      <pcbnotetext
        pcbX={0}
        pcbY={-2}
        text="A4: availability, portrait FPC and thickness qualification pending"
        fontSize={0.7}
        color="#33b5e5"
      />
      <pcbnotetext
        pcbX={19}
        pcbY={5}
        text="BAT: OUTER / NTC / OUTER; POLARITY PENDING"
        fontSize={0.4}
        color="#ffb34d"
      />
      <pcbnotetext pcbX={22.7} pcbY={32} text="TALK" fontSize={1} />
      <pcbnotetext pcbX={-24} pcbY={5.5} text="PRIVACY" fontSize={0.8} />
      <pcbnotetext pcbX={0} pcbY={-32} text="USB-C 5V / PROGRAM" fontSize={0.8} />
      <pcbnotetext pcbX={0} pcbY={-31} text="A4 PROTOTYPE - NOT FOR FABRICATION" fontSize={0.7} />
      <schematicsheet
        name="test-access"
        displayName="AI Remote A1 - Test access"
        sheetSize="A4"
        sheetIndex={13}
      >
        <group name="test-access-group" schLayout={{ layoutMode: "relative" }}>
          {testNets.map((net, index) => (
            <testpoint
              key={net}
              name={`TP${index + 1}`}
              footprintVariant="pad"
              padShape="circle"
              padDiameter={1}
              layer="top"
              pcbX={index === 0 ? -17 : index === 7 ? -1 : -18 + index * 2.2}
              pcbY={index === 7 ? -5 : 10.8}
              schX={-10 + index * 3}
              schY={0}
              connections={{ pin1: `net.${net}` }}
            />
          ))}
        </group>
      </schematicsheet>
    </>
  )
}
