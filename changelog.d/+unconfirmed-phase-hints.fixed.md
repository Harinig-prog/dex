**Phase hints on an unconfirmed command no longer cite a confirmed budget.**
When an unconfirmed `explore` command reaches a phase checkpoint (for example
`explore relationships --verify` with every profile fresh in the cache), the
hint now says the phase needs confirming, without "beyond what remains of the
confirmed budget" or "a re-run re-profiles first", and says the cached profiles
are reused. Hints on a confirmed command are unchanged.
