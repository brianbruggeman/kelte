def echo(*messages, verbose=None):
    verbose = True if verbose is None else verbose
    msg = ' '.join(str(m) for m in messages)
    if verbose:
        print(msg)
