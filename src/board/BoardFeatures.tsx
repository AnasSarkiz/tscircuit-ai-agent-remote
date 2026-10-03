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
      <keepout
        shape="rect"
        pcbX={-12}
        pcbY={33}
        width={20}
        height={5}
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
        pcbX={0}
        pcbY={-3}
        width={33.7}
        height={42.94}
        strokeWidth={0.15}
        isStrokeDashed
        color="#33b5e5"
      />
      <pcbnoterect
        pcbX={0}
        pcbY={-3}
        width={28.03}
        height={35.04}
        strokeWidth={0.1}
        isStrokeDashed
        color="#33b5e5"
      />
      <pcbnotetext pcbX={0} pcbY={6.5} text="DISPLAY - PROVISIONAL" fontSize={1} color="#33b5e5" />
      <pcbnotetext
        pcbX={0}
        pcbY={-2}
        text="Raised above top assembly; Z fit unqualified"
        fontSize={0.7}
        color="#33b5e5"
      />
      <pcbnotetext pcbX={19} pcbY={32} text="TALK" fontSize={1} />
      <pcbnotetext pcbX={-24} pcbY={5.5} text="PRIVACY" fontSize={0.8} />
      <pcbnotetext pcbX={0} pcbY={-32} text="USB-C 5V / PROGRAM" fontSize={0.8} />
      <pcbnotetext pcbX={0} pcbY={-31} text="A1 UNROUTED - NOT FOR FABRICATION" fontSize={0.7} />
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
              pcbX={index === 7 ? -1 : -18 + index * 2.2}
              pcbY={6.5}
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
