# Contributing

Contributions are welcome through issues and pull requests.

## Development flow

1. Fork the repository and create a focused branch.
2. Keep changes scoped and preserve third-party license files.
3. Run `python3 dist/verify/validate_dist.py` and `bash dist/verify/doctor.sh`.
4. Run `bash release/build_release.sh` when changing packaging.
5. Explain behavior changes, safety implications, and license provenance in the pull request.

## Licensing requirement

Do not add a third-party skill unless its redistribution license and required notices are included in the skill directory. Unlicensed or ambiguous material will not be accepted into public packages.
