fix(tools): stop the session tool runner from running the tool calls of a terminated session thread

The runner also no longer yields these calls, including a denied call (`confirmation="deny"`) and a call to a tool that it does not own. The one exception is a call whose tool is already running when the thread terminates: the runner yields it with `posted=False` and posts no result.
