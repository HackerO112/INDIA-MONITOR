# Production readiness assessment

Status: **public-data dashboard prototype; production data-quality work required**.

## Verified from the current default branch
- Streamlit dashboard fetches public macroeconomic, market, weather, air-quality, and news data from external providers.
- Fetch helpers return empty or null values after broad exception handling, which can hide provider outages and stale data.
- No tests, CI workflow, dependency lockfile, or security policy was found.

## Release blockers
1. Show source, observation date, retrieval time, unit, and freshness for every displayed indicator.
2. Distinguish unavailable, stale, estimated, and live values; never render missing data as zero or a live status.
3. Add schema validation and contract tests for every external API; handle rate limits, malformed responses, and provider outages explicitly.
4. Review composite-score normalization, weighting, directionality, and missing-data behavior; publish methodology and uncertainty.
5. Add caching policy, retries with backoff, timeouts, observability, dependency pinning, and tests.
6. Audit HTML rendering and ensure all external text is escaped before interpolation.

## Release gate
Require data-source validation, score-methodology review, tests, dependency review, and a live deployment smoke test. This assessment does not certify the accuracy of the dashboard's indicators.
