def longest_common_subsequence(seq1, seq2):
    m = len(seq1)
    n = len(seq2)

    # DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if seq1[i - 1] == seq2[j - 1]:
                # Characters/elements match
                dp[i][j] = dp[i - 1][j - 1] + 1

            else:
                # Take the better of the two possibilities
                dp[i][j] = max(
                    dp[i - 1][j],
                    dp[i][j - 1]
                )

    # Reconstruct the actual LCS
    i = m
    j = n
    lcs = []

    while i > 0 and j > 0:

        if seq1[i - 1] == seq2[j - 1]:
            lcs.append(seq1[i - 1])
            i -= 1
            j -= 1

        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1

        else:
            j -= 1

    # We reconstructed it backwards
    lcs.reverse()

    return lcs, dp[m][n]


# Example
sequence1 = "AGGTAB"
sequence2 = "GXTXAYB"

lcs, length = longest_common_subsequence(
    sequence1,
    sequence2
)

print("LCS:", "".join(lcs))
print("Length:", length)
