def fibonacci_memo(n, memo=None):
    if memo is None:
        memo = {}

    # Base cases
    if n <= 1:
        return n

    # Already calculated?
    if n in memo:
        return memo[n]

    # Calculate and store
    memo[n] = (
        fibonacci_memo(n - 1, memo)
        + fibonacci_memo(n - 2, memo)
    )

    return memo[n]


# Example
n = 10
print(f"Fibonacci({n}) =", fibonacci_memo(n))
