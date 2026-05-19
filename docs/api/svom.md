# SVOM

SVOM parsers cover GRM, ECLAIRs, MXT, and generic retraction VOEvent notices.
Retractions are detected from the notice payload and parsed into their own
model.

The exact GCN topics covered by the parsers are:

* `gcn.notices.svom.voevent.grm`
* `gcn.notices.svom.voevent.eclairs`
* `gcn.notices.svom.voevent.mxt`

## Classes

::: gcn_parser.svom.SvomEclairs
::: gcn_parser.svom.SvomGrm
::: gcn_parser.svom.SvomMxt
::: gcn_parser.svom.SvomRetraction
::: gcn_parser.svom.SvomPacket

## Functions

::: gcn_parser.svom.parse_svom_eclairs
::: gcn_parser.svom.parse_svom_grm_trigger
::: gcn_parser.svom.parse_svom_mxt
::: gcn_parser.svom.parse_svom_retraction
::: gcn_parser.svom.is_svom_retraction

## References

- [French Science Ground Segment](https://fsc.svom.org/readthedocs/svom/notices_and_circulars/index.html)
