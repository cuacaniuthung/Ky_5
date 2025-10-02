import re, requests, unicodedata
from bs4 import BeautifulSoup
from collections import Counter

URLS = [
    "https://en.wikipedia.org/wiki/Information_retrieval",
    "https://en.wikipedia.org/wiki/PageRank",
    "https://en.wikipedia.org/wiki/Hidden_Markov_model",
]

word_re = re.compile(r"[A-Za-z]+")  # chỉ chữ cái tiếng Anh
def ascii_only(text: str) -> str:
    # chuẩn hoá + loại ký tự non-ASCII
    norm = unicodedata.normalize("NFKD", text)
    return norm.encode("ascii", "ignore").decode("ascii")

tokens = []
for url in URLS:
    html = requests.get(url, timeout=20).text
    text = BeautifulSoup(html, "html.parser").get_text(" ")
    text = ascii_only(text).lower()
    tokens += word_re.findall(text)

# chỉ giữ token thuần alphabet (regex đã bảo đảm), bỏ rỗng nếu có
tokens = [t for t in tokens if t]

# Thống kê nhanh
N = len(tokens)
vocab = set(tokens)
V = len(vocab)
freq = Counter(tokens).most_common(20)

print(f"Total tokens (N) = {N}")
print(f"Vocabulary size (V) = {V}")
print("Top-20 words:", freq[:20])
