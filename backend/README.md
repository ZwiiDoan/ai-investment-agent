# Async & Logging Implementation Notes

## Async Endpoint

The `/ai-response` endpoint is implemented as an async FastAPI route, simulating I/O with `await asyncio.sleep(0.1)`. This allows the server to handle many concurrent requests efficiently.

## Synchronous Endpoint

For comparison, `/ai-response-sync` is implemented as a synchronous route using `time.sleep(0.1)`. This blocks the server process, reducing concurrency and throughput under load.

## Structured Logging

Structured logging is implemented using [Loguru](https://loguru.readthedocs.io/). Logs are written to `logs/app.log` with weekly rotation. All HTTP requests and responses are logged via FastAPI middleware.

## Performance Findings

- Async endpoint (`/ai-response`) handled significantly more concurrent requests with lower latency compared to the sync endpoint (`/ai-response-sync`).
- Synchronous endpoint caused blocking and higher response times under load.
- See `reports/` for detailed Locust performance reports.

## References

- See `plans/month1_week1_day4.md` for the original task breakdown.
- ADR #1 (Language & Framework Choice): See `../adr/adr-1-Language and Framework Choice - Python and FastAPI.md`
