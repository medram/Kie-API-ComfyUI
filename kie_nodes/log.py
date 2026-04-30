def _log(*args):
    import inspect
    import os
    from datetime import datetime

    # Get the caller's frame
    caller_frame = inspect.stack()[1]

    # Get the caller's file name and line number
    caller_file = os.path.basename(caller_frame.filename)
    caller_line = caller_frame.lineno

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the log message from the arguments passed to the function
    log_message = " ".join(str(arg) for arg in args)

    # Format the log entry
    log_entry = f"[KIE] [{timestamp}] {caller_file}:{caller_line} - {log_message}"

    # Print the log entry to the console
    print(log_entry, flush=True)
