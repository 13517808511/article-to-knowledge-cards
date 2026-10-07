# Knowledge Cards: HTTP Caching Basics

### 1. What HTTP Caching Is For
- **Core Knowledge:** HTTP caching stores responses so clients and intermediary caches can reuse them, which reduces latency and origin-server load.
- **Explanation:** Reuse avoids repeating an identical request-response round trip; the cached copy is served instead of regenerating the response at the origin.
- **Example or Self-Test:** A CDN is one example of an intermediary cache that holds reusable responses.

### 2. Freshness Windows and max-age
- **Core Knowledge:** For a cacheable response, the server states how long it stays fresh with `Cache-Control: max-age=<seconds>`, counted from the moment the response is generated.
- **Explanation:** Within the window the response is fresh and may be served without contacting the origin; once it expires it is stale and normally must be revalidated before reuse.
- **Example or Self-Test:** `max-age=60` means the response can be served for 60 seconds without contacting the origin.

### 3. public versus private Caches
- **Core Knowledge:** `public` allows a response to be stored by shared caches as well as the browser, while `private` restricts storage to the browser's private cache.
- **Explanation:** Shared caches such as CDNs must not store responses marked private, which keeps user-specific responses out of caches shared across users.
- **Example or Self-Test:** A response contains user-specific data — should it be marked `public` or `private`?

### 4. no-store Is Not no-cache
- **Core Knowledge:** `no-store` forbids storing anything at all, whereas `no-cache` allows storage but requires revalidation with the origin on every use.
- **Explanation:** The directive's name is misleading: choosing `no-cache` does not prevent caching, only serving without checking the origin first.
- **Example or Self-Test:** For truly sensitive data that must not be stored even temporarily, use `no-store`.

### 5. ETag Conditional Revalidation
- **Core Knowledge:** With `ETag`, the client echoes the server's validator in `If-None-Match`, and the origin confirms whether the stored representation is still current.
- **Explanation:** When unchanged, the origin returns `304 Not Modified` with no body; when the representation changed, it sends a fresh `200` response.
- **Example or Self-Test:** A stale stored response is revalidated and the representation has not changed — what status code does the origin return?

### 6. Last-Modified: the Weaker Validator
- **Core Knowledge:** `Last-Modified` offers validation similar to ETag via `If-Modified-Since`, but it is timestamp-based and therefore weaker.
- **Explanation:** HTTP dates carry only one-second resolution, so timestamp validation is less precise than ETag; ETag is preferred when exactness matters.
- **Example or Self-Test:** Why can two changes within the same second be indistinguishable to `Last-Modified` validation?
