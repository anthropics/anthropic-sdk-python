fix(tools): stop EnvironmentWorker from running tools for a terminated session

For a terminated session, the worker now force-stops the work item right after it retrieves the session, before it downloads skills or memory stores. It no longer raises `SessionMemoryError` for such a session. The API reports an archived session as `terminated`.
