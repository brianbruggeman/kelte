def echo(*messages, verbose=None):
    if verbose:
        for message in messages:
            print(message, end=" ")
        if messages:
            print()
