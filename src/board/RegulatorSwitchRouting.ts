// TPS63802 SLVSEU9D: boost peak-current upper limit 5.75 A (electrical table),
// and short, wide power paths (section 12). These are local pad escapes, followed
// by 1 mm trunks in the unchanged genuine saved paths, not board-wide minima.
export const regulatorSwitchRouting = {
  padEscapeMinimumWidthMm: 0.275,
  padEscapeMaximumLengthMm: 0.751,
  trunkMinimumWidthMm: 1,
  trunkMinimumLengthMm: 1,
  maximumPeakCurrentAmps: 5.75,
  requiredOuterCopperThicknessMm: 0.035,
} as const
