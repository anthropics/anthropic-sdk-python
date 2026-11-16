fix(tools): keep the session tool runner's max_idle countdown running when a session thread terminates

If the runner fails to read the session's event history after a reconnect, a termination that then arrives on the event stream still cancels the countdown, until the next idle or successful read.
