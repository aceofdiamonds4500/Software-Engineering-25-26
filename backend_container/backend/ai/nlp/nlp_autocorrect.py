import re
from collections import Counter
from pathlib import Path
import pandas as pd
from transformers import pipeline

MODEL_NAME = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
TOP_K = 5

STOPWORDS = {
    "the","and","was","with","for","that","this","has","have","are",
    "were","been","his","her","she","him","they","their","from","not",
    "but","all","had","also","who","which","will","would","could",
}

def find_project_file(start: Path, target: str) -> Path:
    for parent in [start] + list(start.parents):
        candidate = parent / target
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"{target} not found in parent directories")

# Build vocab from MTSamples
def build_vocab(csv_path, min_freq=5):
    df = pd.read_csv(csv_path, index_col=0)

    vocab = set()

    # Keywords
    for kw in df["keywords"].dropna():
        for term in kw.split(","):
            t = term.strip().lower()
            if t:
                vocab.add(t)
                vocab.update(t.split())

    # Frequency-based vocab
    counts = Counter()
    for text in df["transcription"].dropna():
        for w in re.findall(r"[a-zA-Z]{3,}", text):
            counts[w.lower()] += 1

    for word, freq in counts.items():
        if freq >= min_freq and word not in STOPWORDS:
            vocab.add(word)

    return vocab


# Load BioBERT
_fill_mask = None

def load_model():
    global _fill_mask
    if _fill_mask is None:
        _fill_mask = pipeline(
            "fill-mask",
            model=MODEL_NAME,
            top_k=TOP_K
        )
    return _fill_mask

def suggest_corrections(text, vocab):
    fill_mask = load_model()

    # Split into sentences while preserving punctuation
    sentences = re.split(r"(?<=[.!?])\s+", text)

    all_suggestions = []

    for sent_idx, sentence in enumerate(sentences):
        tokens = sentence.split()

        for i, tok in enumerate(tokens):
            clean = re.sub(r"[^\w\-]", "", tok).lower()

            if clean in vocab or len(clean) <= 2:
                continue

            masked = tokens.copy()
            masked[i] = fill_mask.tokenizer.mask_token

            try:
                preds = fill_mask(" ".join(masked))

                valid_preds = [
                    p["token_str"].strip()
                    for p in preds
                    if p["token_str"].strip().lower() in vocab
                ]

                if valid_preds:
                    all_suggestions.append({
                        "sentence_index": sent_idx,
                        "sentence": sentence,
                        "word": tok,
                        "suggestions": valid_preds[:3]
                    })

            except Exception:
                continue

    return all_suggestions


if __name__ == "__main__":

    base_dir = Path(__file__).resolve()

    try:
        csv_path = find_project_file(base_dir, "mtsamples.csv")
    except FileNotFoundError:
        csv_path = Path.cwd() / "mtsamples.csv"

    print(f"Using dataset: {csv_path}")

    vocab = build_vocab(csv_path, min_freq=5)

    test_sentence = "The pacient has sever chest pane and difculty brething. The pacent ned chest surgry."

    results = suggest_corrections(test_sentence, vocab)

    print("\nInput:", test_sentence)
    print("\nSuggestions:")

    for r in results:
        print(f"{r['word']} -> {r['suggestions']}")