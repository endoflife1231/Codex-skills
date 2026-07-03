# Graphify Adapter

This directory contains the optional Graphify integration layer for the Codex Powerpack.

Design rules:

- Graphify is optional.
- The core distribution must work without it.
- No `curl | sh`.
- No silent hook installation.
- Every script performs a local preflight first.
- Commands are based on the inspected local Graphify source, not guessed from memory.
