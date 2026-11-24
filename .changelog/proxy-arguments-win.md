fix(client): honor proxy and trust_env when proxy variables are set

`DefaultHttpxClient` and `DefaultAsyncHttpxClient` read `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` and `NO_PROXY` even when the caller passed `proxy=` or `trust_env=False`, and the variables won. Now `proxy=` is used for every request and the variables are not read, and `trust_env=False` ignores them, as in plain `httpx2`.

What you may notice: with `proxy=` set, a host listed in `NO_PROXY` used to be reached directly and now goes through your proxy. To keep a host off the proxy, pass `mounts={"all://that.host": None}`.
