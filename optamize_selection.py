
# 0/1 Knapsack using Dynamic Programming

def knapsack_bottom_up(wt, val, W):
    n = len(wt)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if wt[i-1] <= w:
                dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]],
                               dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][W]


def knapsack_top_down(wt, val, W):
    from functools import lru_cache

    @lru_cache(None)
    def solve(i, w):
        if i == len(wt) or w == 0:
            return 0

        if wt[i] > w:
            return solve(i+1, w)

        return max(val[i] + solve(i+1, w-wt[i]),
                   solve(i+1, w))

    return solve(0, W)


# Input
wt = [2, 3, 4, 5]
val = [3, 4, 5, 6]
W = 5

print("Bottom-Up Result:", knapsack_bottom_up(wt, val, W))
print("Top-Down Result:", knapsack_top_down(wt, val, W))
