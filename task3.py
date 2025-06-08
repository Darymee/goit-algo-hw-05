import timeit
import pandas as pd

# Import files
with open("article1.txt", encoding="utf-8") as f:
    text1 = f.read()
with open("article2.txt", encoding="utf-8") as f:
    text2 = f.read()

# Substrings 
existing_substring = "структури даних"
nonexistent_substring = "підрядок, що не існує"

# KMP algorithm
def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# Rabin-Karp algorithm
def rabin_karp(text, pattern):
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)
    h = pow(d, m - 1, q)
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for s in range(n - m + 1):
        if p == t and text[s : s + m] == pattern:
            return s
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            if t < 0:
                t += q
    return -1

# Boyer-Moore algorithm
def boyer_moore(text, pattern):
    def bad_character_table(pattern):
        return {char: idx for idx, char in enumerate(pattern)}

    bad_char = bad_character_table(pattern)
    m = len(pattern)
    n = len(text)
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
    return -1

# Measure execution time
def measure_time(func, text, pattern):
    return timeit.timeit(lambda: func(text, pattern), number=10)

# Saving results
results = {
    "стаття 1": {
        "існуючий": {
            "Боєр-Мур": measure_time(boyer_moore, text1, existing_substring),
            "КМП": measure_time(kmp_search, text1, existing_substring),
            "Рабін-Карп": measure_time(rabin_karp, text1, existing_substring),
        },
        "неіснуючий": {
            "Боєр-Мур": measure_time(boyer_moore, text1, nonexistent_substring),
            "КМП": measure_time(kmp_search, text1, nonexistent_substring),
            "Рабін-Карп": measure_time(rabin_karp, text1, nonexistent_substring),
        },
    },
    "стаття 2": {
        "існуючий": {
            "Боєр-Мур": measure_time(boyer_moore, text2, existing_substring),
            "КМП": measure_time(kmp_search, text2, existing_substring),
            "Рабін-Карп": measure_time(rabin_karp, text2, existing_substring),
        },
        "неіснуючий": {
            "Боєр-Мур": measure_time(boyer_moore, text2, nonexistent_substring),
            "КМП": measure_time(kmp_search, text2, nonexistent_substring),
            "Рабін-Карп": measure_time(rabin_karp, text2, nonexistent_substring),
        },
    },
}

# Results visualization
df = pd.DataFrame.from_dict(
    {
        (article, case): timings
        for article, cases in results.items()
        for case, timings in cases.items()
    },
    orient="index",
)
df.index.names = ["Стаття", "Підрядок"]


print(df)
