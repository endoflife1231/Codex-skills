# Release tooling

Run:

```bash
bash release/build_release.sh
```

Outputs for version 0.2.2:

- `release/out/codex-powerpack-v0.2.2-user.zip`
- `release/out/codex-powerpack-v0.2.2-repository.zip`
- `release/out/user-manifest.json`
- `release/out/repository-manifest.json`
- `release/out/SHA256SUMS`

The user archive is installation-focused. The repository archive contains the full maintainership structure and a copy of the user archive under `release/out/`.
