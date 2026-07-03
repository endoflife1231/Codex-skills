# Release Layer

This directory contains release artifacts and release tooling for the assembled Codex Powerpack distribution.

Expected flow:

1. validate the assembled `dist/`
2. build a release zip
3. emit checksums and a release manifest

Current outputs:

- `out/codex-powerpack.zip`
- `out/release-manifest.json`
- `out/SHA256SUMS`

The release build is local and filesystem-based. It does not publish anywhere automatically.
