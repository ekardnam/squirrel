
def check_n_args(args, n):
    if not (m := len(args)) == n:
        raise RuntimeError(f'Expecting exactly {n} arguments. {m} given')
