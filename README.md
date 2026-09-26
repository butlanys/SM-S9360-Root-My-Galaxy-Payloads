# SM-S9360 — Root My Galaxy Payloads

Personal backup fork of
[Root My Galaxy Payloads](https://github.com/BuSung-dev/Root-My-Galaxy-Payloads)
for the Galaxy S25+ `SM-S9360` (`pa2q`); see
[Fork additions](#fork-additions-butlanys) below.

This repository contains the device-specific native side of
[Root My Galaxy](https://github.com/BuSung-dev/Root-My-Galaxy):

- exact firmware profiles and offsets;
- the app-domain CVE-2026-43499 exploit source and compiled payload;
- the app bootstrap helper source;
- the verified KernelSU late-load build artifacts;
- the support feed consumed by the application.

It intentionally does not contain Android application source code.

## Fork additions (`butlanys`)

This fork carries the Galaxy S25+ Hong Kong (`OZS`, `pd6ff1cd` GKI) port plus
the per-boot KernelSU tooling that came out of debugging it:

- **`pa2q-S9360ZHSCCZG1` profile** -- Galaxy S25+ `SM-S9360`,
  `6.6.98-android15-8-pd6ff1cd-abogkiS9360ZHSCCZG1-4k`, device-tested through
  temporary root and the KernelSU LKM late-load. Offsets, the physical-P0
  fingerprint and the validation log are in
  [`docs/SM-S9360-S9360ZHSCCZG1.md`](docs/SM-S9360-S9360ZHSCCZG1.md).
- **`pa2q-S9360ZHSDCZH1` profile** -- Galaxy S25+ `SM-S9360`,
  `6.6.98-android15-8-pd6ff1cd-abogkiS9360ZHSDCZH1-4k` (Hong Kong `OZS`,
  released 2026-09-03), built 2026-09-26. Offline-verified: the kernel keeps
  the CZG1 layout, so the profile differs only in
  `SLIDE_NFULNL_LOGGER_NAME_OFF` (`0x0175e299`) and one p0 fingerprint row.
  Hardware validation is still pending -- see
  [`docs/SM-S9360-S9360ZHSDCZH1.md`](docs/SM-S9360-S9360ZHSDCZH1.md).
- **Module rescue tooling** -- [`tools/module-rescue.sh`](tools/module-rescue.sh)
  with the device-side helpers in [`tools/device/`](tools/device/) inspect, back
  up, disable and remove KernelSU modules, and can load the kernel driver
  without running the late-load stage. It exists because one bad module (a
  `system/` overlay mounted through the `mountify` metamodule) turned the
  expected warm framework restart of the late-load into a cold reset, which
  drops the per-boot root before the module can be removed. Recovery ladder:
  [`tools/README.md`](tools/README.md#recovering-from-a-bad-module).
- **LAN / mock feed server** -- [`tools/feed_server.py`](tools/feed_server.py)
  serves `support/targets-v3.json` and every artifact from a local checkout, so
  the app can be built and tested without GitHub. The companion app fork
  (<https://github.com/butlanys/Root-My-Galaxy>) adds the matching
  `-PfeedCommitApi` / `-PfeedRawBase` Gradle flags.
- **Per-boot by design** -- no boot image is modified; KernelSU and `su` exist
  only for the current boot, and a reboot restores the stock system.

## Supported payloads

| Payload | Compatible models | Kernel version | Status |
| --- | --- | --- | --- |
| `galaxy-s25-series-2026-06-07` | Galaxy S25, S25+, S25 Edge, and S25 Ultra regional models | `6.6.98` | Device-tested |
| `pa2q-S9360ZHSCCZG1` | Galaxy S25+ `SM-S9360` (Hong Kong `OZS`, `pd6ff1cd` GKI) | `6.6.98` | Device-tested |
| `pa2q-S9360ZHSDCZH1` | Galaxy S25+ `SM-S9360` (Hong Kong `OZS`, `pd6ff1cd` GKI) | `6.6.98` | Built 2026-09-26: offline-verified, hardware validation pending |
| `e3q-S928USQS6DZF2` | Galaxy S24 Ultra `SM-S928U1` | `6.1.145` | Device-tested |
| `e3q-S9280ZCS6DZF2` | Galaxy S24 Ultra China `SM-S9280` | `6.1.145` | Device-tested |
| `e2s-S926BXXUEDZDR` | Galaxy S24+ `SM-S926B` | `6.1.157` | Device-tested |
| `essi-A566EXXSCCZG6` | Galaxy A56 5G `SM-A566E` | `6.6.102` | Device-tested |
| `a36xq-A366WVLS3AYG1` | Galaxy A36 5G `SM-A366W` | `6.6.46` | Device-tested |
| `a53x-A536EXXSNGZG3` | Galaxy A53 5G `SM-A536E` | `5.10.237` | Device-tested |
| `dm3q-S9180ZHS8FZF5` | Galaxy S23 Ultra `SM-S9180` | `5.15.189` | Test in progress |
| `q4q-F9360ZCSAIZF1` | Galaxy Z Fold4 `SM-F9360` | `5.10.236` | Device-tested |
| `dm2q-S916BXXSAFZG1` | Galaxy S23+ `SM-S916B` | `5.15.189` | Experimental: hardware root from ADB shell; not in app feed |
| `dm3q-S918BXXSAFZF5` | Galaxy S23 Ultra `SM-S918B` | `5.15.189` | Confirmed working: full chain through the app (Shizuku mode) incl. KernelSU late-load and granted `su` |

The S916B FZG1 profile is shell-only today. Its exact tracefs route works from `adb shell`, but direct app-domain execution is not supported. Root My Galaxy would need to delegate the native runner through an authorized shell bridge such as Shizuku. See [`artifacts/dm2q-S916BXXSAFZG1/README.md`](artifacts/dm2q-S916BXXSAFZG1/README.md).

The S918B FZF5 profile is hardware-verified through the app's Shizuku mode (exploit, KernelSU late-load, granted `su` under enforcing). Its physical-P0 fallback also engages in unprivileged app-domain execution, but rooting without Shizuku is not yet hardware-confirmed. See [`docs/SM-S918B-S918BXXSAFZF5.md`](docs/SM-S918B-S918BXXSAFZF5.md).

Schema version 3 keeps each exploit and KernelSU artifact once. Its flat
`models` and `kernelVersions` arrays define runtime compatibility. See
[`support/README.md`](support/README.md) for the matching rules.

The port is based on the exploit source published at
<https://github.com/NebuSec/CyberMeowfia/tree/main/IonStack/CVE-2026-43499/exploit>.

## Feed delivery

Root My Galaxy resolves the payload repository's current commit first and
fetches `support/targets-v3.json` and every artifact from that immutable
commit. Per-artifact SHA-256 fields and manifest signatures are not part of
schema version 3. `targets-v2.json` is retained for released 0.2.3 clients.

## Build

```sh
make TARGET=pa3q-S938NKSUACZF1 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=pa2q-S9360ZHSCCZG1 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=pa2q-S9360ZHSDCZH1 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=e3q-S928USQS6DZF2 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=e2s-S926BXXUEDZDR ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=essi-S721NKSSCDZF3 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=e1s-S921BXXSFDZF2 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=a15-A155NKSS6BYH1 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=essi-A566EXXSCCZG6 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=a36xq-A366WVLS3AYG1 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=a53x-A536EXXSNGZG3 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=dm3q-S9180ZHS8FZF5 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=q4q-F9360ZCSAIZF1 ANDROID_NDK_HOME=/path/to/android-ndk
make TARGET=dm2q-S916BXXSAFZG1 ANDROID_NDK_HOME=/path/to/android-ndk
```

Outputs:

```text
build/<profile>/cve-2026-43499
build/<profile>/cve-2026-43499-app.so
build/<profile>/cve-2026-43499-root
```

The release app payload is built with:

```sh
make TARGET=essi-S721NKSSCDZF3 ANDROID_NDK_HOME=/path/to/android-ndk release
```

The complete firmware-to-profile procedure is recorded in
[`docs/PORTING.md`](docs/PORTING.md). Samsung-specific KernelSU changes and
versioned artifacts are documented in [`kernelsu/README.md`](kernelsu/README.md).
The exact S921B DZF2 analysis is recorded separately in
[`docs/SM-S921B-S921BXXSFDZF2.md`](docs/SM-S921B-S921BXXSFDZF2.md), and the
S928U/S928U1 DZF2 analysis is in
[`docs/SM-S928U1-S928U1UES6DZF2.md`](docs/SM-S928U1-S928U1UES6DZF2.md). S921B
is an Exynos 2400 target and is not a Qualcomm/Snapdragon reference for E3Q.
The 5.10 A15 analysis is in
[`docs/SM-A155N-A155NKSS6BYH1.md`](docs/SM-A155N-A155NKSS6BYH1.md).
The SM-A566E CCZG6 analysis and validation record is in
[`docs/SM-A566E-A566EXXSCCZG6.md`](docs/SM-A566E-A566EXXSCCZG6.md).
The SM-S926B DZDR analysis and device-validation record is in
[`docs/SM-S926B-S926BXXUEDZDR.md`](docs/SM-S926B-S926BXXUEDZDR.md).
The SM-A366W AYG1 device validation is in
[`docs/SM-A366W-A366WVLS3AYG1.md`](docs/SM-A366W-A366WVLS3AYG1.md).
The SM-F9360 AIZF1 (5.10, locked-BL, no-LTO clang-12 module) validation is in
[`docs/SM-F9360-F9360ZCSAIZF1.md`](docs/SM-F9360-F9360ZCSAIZF1.md).
The experimental SM-S916B FZG1 shell port and its exact hardware evidence are in [`docs/SM-S916B-S916BXXSAFZG1.md`](docs/SM-S916B-S916BXXSAFZG1.md).
The SM-A536E GZG3 device validation is in
[`docs/SM-A536E-A536EXXSNGZG3.md`](docs/SM-A536E-A536EXXSNGZG3.md).
The SM-S9280 China (CHC) DZF2 port and validation record is in
[`docs/SM-S9280-S9280ZCS6DZF2.md`](docs/SM-S9280-S9280ZCS6DZF2.md).
The SM-S9360 Hong Kong (OZS) ZHS port, its build-specific offsets and the
module-rescue procedure are in
[`docs/SM-S9360-S9360ZHSCCZG1.md`](docs/SM-S9360-S9360ZHSCCZG1.md).

Use only on devices you own or are explicitly authorized to test.
