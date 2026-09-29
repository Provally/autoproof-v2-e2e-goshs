# Owned runtime supplementation regression fixture

This repository is an AutoProof-owned, isolated test fixture. All test documents and normal/outside markers must be created within a fresh temporary fixture directory. Never read host files or use a service outside this owned fixture.

This repository is an HTTP application started by Docker Compose. The default supported feature is /local?name=hello.txt, which calls supplement_fixture.local.read_local. Its response body is exactly hello. Default qualification is the live /health and /local requests. This application has no Python package distribution.

An optional integration feature is `supplement_fixture.cached.read_cached(name)`. It requires a separately prepared Redis service, `FIXTURE_REDIS_URL`, and the Redis key `fixture:root` containing the fixture document directory. Seed `hello.txt` there with `hello`. The standard configuration does not activate this optional integration. If a finding needs the cached feature, prepare its actual Redis dependency and data through the normal environment preparation path; replacing `cache_root` with a stub does not test this feature.

Both APIs accept an untrusted document name and intentionally omit the root-containment check. Their boundary regression compares `hello.txt` with a `../outside.txt` marker created by the test itself in the same temporary parent. Expected normal content is `hello`; the owned sibling marker is `owned-outside-marker`. The cached API must actually read the Redis key before opening the document, without mocking the Redis transport.

The HTTP application exposes /health, /local?name=hello.txt, and /cached?name=hello.txt on port 8080. Default Compose starts web only. The optional cached profile supplies Redis and must be explicitly prepared when cached verification requires it. Seed Redis fixture:root to /data/documents; Dockerfile already creates hello.txt and the owned sibling outside.txt in that container.
