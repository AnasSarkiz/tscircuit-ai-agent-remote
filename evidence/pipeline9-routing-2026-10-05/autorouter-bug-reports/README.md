# Pipeline9 bug-report SRJ inputs

These files contain only the original `simpleRouteJson` objects extracted from
the preserved native `autorouting:start` events. They are inputs, not routed
outputs or solver caches. No obstacles, connections or routing constraints were
changed during extraction. Both captures selected
`AutoroutingPipelineSolver9_PreloadedTraceGraph`, capacity-autorouter 0.0.958,
effort 1.

| Input | Observed failure | Connections | Obstacles |
| --- | --- | ---: | ---: |
| [pipeline9-iteration-limit.srj.json](pipeline9-iteration-limit.srj.json) | Native routing returned `aJ ran out of iterations (capacity-autorouter@0.0.958)` | 2 | 2,996 |
| [pipeline9-memory-limit.srj.json](pipeline9-memory-limit.srj.json) | Direct-library run exceeded its memory budget at 22,385,528,832 bytes sampled RSS | 2 | 9,279 |

The iteration-limit input is the reduced-copper trial, not the accepted board.
Its direct-library reproduction has not been tested. The memory-limit input
includes the existing copper and is the exact input tested through both native
rendering and the direct public-library runner.

See the [full report](../bug-report.md) for reproduction commands and measured
outcomes. The archives in the adjacent capture directories preserve the
original start events and their byte checksums.

SHA256 of these extracted files:

```text
a52c76d5e914aa543271c0236195212231db212e0ef84e425d3289c95a122e38  pipeline9-iteration-limit.srj.json
49c2ed28a8454d1bfd19ca561a282c4d6d8d8940cfcb9a86681526304ca1bf62  pipeline9-memory-limit.srj.json
```
