# Performance

- Keep CPU-heavy work off the request event loop; use workers or bounded background jobs.
- Define response schemas to enable fast serialization and prevent accidental data leakage.
- Reuse database pools, compiled schemas, and stable service instances.
- Measure before optimizing; add backpressure and payload limits.
