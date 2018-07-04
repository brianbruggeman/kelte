try:
    import line_profiler
    import atexit

    profile = line_profiler.LineProfiler()
    atexit.register(profile.print_stats)

except ImportError:
    import functools

    def profile(f):

        @functools.wraps(f)
        def wrapper(*args, **kwds):
            return f(*args, **kwds)

        return wrapper
