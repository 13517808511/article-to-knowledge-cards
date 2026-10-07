# HTTP Caching Basics

HTTP caching lets clients and intermediary caches store responses so they can be
reused, which cuts latency and reduces load on the origin server. A CDN is one
example of an intermediary cache.

## Freshness

When a response is cacheable, the server states how long it stays **fresh**
using the `Cache-Control: max-age=<seconds>` header. The age is counted from
the moment the response is generated, so `max-age=60` means the response can be
served without contacting the origin for the next 60 seconds. Note that the
max-age window is measured relative to response generation time, not the time
the document was last edited.

After the freshness window expires, the response is **stale**. A stale
response normally must be revalidated with the origin before reuse.

## Common Directives

- `Cache-Control: public` — the response may be stored by shared caches (such
  as CDNs) as well as the browser cache.
- `Cache-Control: private` — only the browser's private cache may store it;
  shared caches must not.
- `Cache-Control: no-store` — nothing may be stored at all, not even
  temporarily. Use it for truly sensitive data.
- `Cache-Control: no-cache` — despite the name, the response *can* be stored;
  it just must be revalidated with the origin on every use.

## Revalidation

To revalidate cheaply, validators are used. With `ETag`, the server assigns an
opaque validator to a representation; the client echoes it in
`If-None-Match`, and the server replies `304 Not Modified` (no body) when the
representation is unchanged, or sends a fresh `200` response when it is not.

`Last-Modified` provides similar but weaker validation based on a timestamp,
sent back through `If-Modified-Since`. It is less precise because HTTP dates
only carry one-second resolution, so ETag is preferred when exactness matters.

A typical caching mistake is assuming `no-cache` means "do not store it"; in
reality "do not store anything" is `no-store`.
