# pa2q-S9360ZHSEDZJ1 artifacts

Built 2026-11-01 for `SM-S9360` / `S9360ZHSEDZJ1` — Android 17, Hong Kong
`OZS`/`TGY`, kernel `6.6.127-android15-8-p87b1ce1-abogkiS9360ZHSEDZJ1-4k`
(PDA released 2026-10-26, kernel built 2026-10-12).

**Offline-verified only: not yet executed on a device.**

| file | size | SHA-256 | use |
| --- | ---: | --- | --- |
| `cve-2026-43499-app.so` | 126624 | `15904bddcf8e24208da58015943bf941161d78c849200c4b9d22a192e4d926f8` | app payload (`--run-payload` / LD_PRELOAD); this is the feed artifact |
| `cve-2026-43499-root` | 26896 | `1acf40b8658a7971401d8d3d315bacf2d2bd00b1dea7cb9c0103e34f9907b17b` | root helper / su client |
| `cve-2026-43499` | 105872 | `69c0332bbfd01c0a9d16d4c4ec6a21d4b511dbf4e9122d7b4ed25517573b2e7f` | root-umh LD_PRELOAD variant |

This is the October wave on top of the pre-release September build: the GKI
commit moved (`p33f4ffe` → `p87b1ce1`) and about 5% of the Image bytes differ,
but **every symbol offset is identical** to `pa2q-S9360ZHUDDZIF`, the BTF blob
is byte-identical, and only the `nfnetlink_log` string moved
(`0x0175e238`…→`0x017916ae`). So exactly one macro changed, plus the p0 table
(7 of 32 rows, 14 qwords). Derivation and comparison:
[`../../docs/SM-S9360-S9360ZHSEDZJ1.md`](../../docs/SM-S9360-S9360ZHSEDZJ1.md).

KernelSU: same `kernelsu/ksud-s25u-kdp` (`android15-6.6`); the KMI generation
`6.6.127-android15-8` is unchanged, late-load uses
`MODULE_INIT_IGNORE_VERMAGIC`. Not yet confirmed on hardware.

`BUILD_FINGERPRINT` carries `UNKNOWN-BUILD-ID` until read from a device
(`adbd shell getprop ro.build.fingerprint`); only `tools/reroot.sh`'s guard
reads it and no artifact embeds it.
