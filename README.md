# What Swift Concurrency Repairs Actually Guarantee

Practitioner technical report by Ehsan Azish, 6 November 2026. Two completed local regression comparisons and a targeted source review of 29 production defect families. Not peer reviewed; classifications are provisional AI-assisted first-pass coding without independent human agreement scores.

[Read the report (PDF)](report/swift-concurrency-repairs-v1.0.pdf) | [Download the PDF](https://raw.githubusercontent.com/EhsanAzish80/swift-concurrency-repairs/main/report/swift-concurrency-repairs-v1.0.pdf)

The readable 3nsofts HTML edition is awaiting deployment; it is not linked as an available copy.

[Archived report and artifacts on Zenodo](https://doi.org/10.5281/zenodo.24005436) | [Swift Forums discussion](https://forums.swift.org/t/pitch-split-continuation/90096/15)

arXiv submission remains pending. The Zenodo v1.0 archive preserves the initial files, whose README and publication metadata predate the live-link correction; use the links above for current access. The report, original data and logs are licensed under [CC BY 4.0](LICENSES/CC-BY-4.0.txt); original scripts and research fixtures are [MIT licensed](LICENSES/MIT.txt). See [LICENSE](LICENSE) for exact scopes and third-party exceptions.

## Results and scope

- Kingfisher #2526 internal cancellation bridge: 100/100 selected early-cancellation failures on the parent, 0/100 on the repair, including Swift 5 with complete checking explicitly enabled. Matched controls passed. This is a real internal component with a local Task, not a full manager/view/URLSession or application reproduction.
- Nuke #916 real pipeline/memory-cache path: 20/20 immediate-subscription terminal-event losses on the parent, 0/20 on the repair under Swift 6. Late-subscriber replay is a separate contract check.
- NIO #3453 remains disputed and excluded from the 29-family denominator. The later interrupted executor experiment is not included as paired evidence.

The fixes passed these fixtures; no claim covers every schedule. The corpus is targeted, not prevalence data. No local TSan campaign or implemented split-continuation comparison was performed. `data/detection-triage.json` separates observations, reporter evidence, predictions and unknowns.

## Files

- `report/`: PDF, editable report content and PDF renderer.
- `data/`: source-case ledger, completed reproduction summary and source-only tool triage.
- `reproduction/fixtures/`: original completed research fixtures and manifest snapshots.
- `reproduction/`: fixture installer, bounded runner, manifest diffs, completed run records and sanitized build/test logs.
- `reproduction/log-provenance.json`: raw-log and sanitized-log hashes plus the exact redaction policy. Published log bytes have different hashes from raw local logs by design.
- `THIRD_PARTY_LICENSES/`: notices for the upstream source/manifests. Upstream projects retain their respective licenses; no ownership of upstream code is claimed.

AI assistance was used for retrieval, provisional coding, fixture construction and drafting; no reviewer endorsement is implied. No original maintainer is claimed as a co-author or endorser.

## Reproduction instructions (not run during publication)

Use clean, disposable source checkouts named `nio`, `nuke`, and `kingfisher` under one research root. The recorded source pairs are in `reproduction/results.json`; use the parent/repair exactly. The original environment was an M1 Max Mac Studio, 32 GB, macOS 27.2, Swift 6.4.2/Xcode 27.2. This was not a source-era toolchain comparison. Package dependency setup may need network access; the fixtures are offline.

Read `reproduction/install_fixtures.py` before using it; it edits research manifests and adds a test target. Keep unrelated work out of the disposable root. Create `logs` under that root. From `reproduction/`, install one case and invoke the saved runner with `REPRO_ROOT` pointing to the absolute research root. On the faulty Kingfisher parent the test adapter needs `-DREPRO_FAULTY`; an added complete-checking context uses `-strict-concurrency=complete`. Exact commands with placeholder roots are retained in `results.json`.

The runner's 300-second limit is a timeout, not success. Its process exit status is not a reliable summary of test outcome: inspect each generated metadata JSON `exit_code`, `timed_out`, and the test log. Do not infer that a passing shell wrapper means the test passed. Existing historical behavior of the runner is preserved for provenance.

No current Swift test is launched by the report renderer. Current work on executable reproductions is paused; these files document completed earlier observations for readers who choose to replicate them.

## Citation and related copies

The report and artifact publication locations are tracked in `publication.json`. An arXiv identifier or Zenodo DOI is only listed once actually assigned and verified. Until then the repository and hosted report provide source access, without pretending a canonical preprint or DOI exists.
