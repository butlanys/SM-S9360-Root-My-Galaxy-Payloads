# pa2q-S9360ZHSDCZH1 artifacts

Built 2026-09-26 for `SM-S9360` / `S9360ZHSDCZH1` (Hong Kong `OZS`).

**Offline-verified only: not yet executed on a device.** Run
`tools/reroot.sh --target pa2q-S9360ZHSDCZH1` (or `--force` after confirming
the fingerprint) and record the log here before treating this profile as
device-tested.

| file | size | SHA-256 | use |
| --- | ---: | --- | --- |
| `cve-2026-43499-app.so` | 126624 | `8f5aa2807f1bf0e736f23f28cc54220b27d329c85d395935dc504dcf5bcf9c80` | app payload (`--run-payload` / LD_PRELOAD); this is the feed artifact |
| `cve-2026-43499-root` | 26896 | `1acf40b8658a7971401d8d3d315bacf2d2bd00b1dea7cb9c0103e34f9907b17b` | root helper / su client |
| `cve-2026-43499` | 105872 | `315eb7c31058cc8f494987bb9db0d7a0aa903589e38e44c5e0a4f565e8890ae6` | root-umh LD_PRELOAD variant |

`cve-2026-43499-root` is byte-for-byte identical to the
`pa2q-S9360ZHSCCZG1` helper: it is compiled from `src/su_daemon.c` alone and
contains no firmware-dependent constant. The other two differ from the CZG1
artifacts by exactly one immediate (the `SLIDE_NFULNL_LOGGER_NAME_OFF`
`+0x33` shift) plus the rodata re-layout that the changed
`BUILD_VARIANT_LABEL` string causes; the disassembly diff is 311 `add`/10
`adr`/2 `adrp` string-address fixes and 2 `mov` immediates
(`#-7578` -> `#-7527`).

Firmware identity, offset derivation and the CZG1-versus-CZH1 comparison:
[`../../docs/SM-S9360-S9360ZHSDCZH1.md`](../../docs/SM-S9360-S9360ZHSDCZH1.md).

KernelSU uses the published `kernelsu/ksud-s25u-kdp` (`android15-6.6` KMI),
the same module the CZG1 profile uses. The KMI string
(`6.6.98-android15-8`) is unchanged by this build; only the
`pd6ff1cd-abogki<S9360ZHSDCZH1>-4k` local suffix changed, and the late-load
path loads with `MODULE_INIT_IGNORE_VERMAGIC`, so no module rebuild is
required. Not yet confirmed on hardware.
