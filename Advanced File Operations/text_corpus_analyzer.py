import os
import re
import math
from collections import defaultdict, Counter

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text.split()

def build_graph(corpus):
    graph = defaultdict(lambda: defaultdict(int))
    for tokens in corpus:
        for i in range(len(tokens) - 1):
            w1, w2 = tokens[i], tokens[i+1]
            graph[w1][w2] += 1
            graph[w2][w1] += 1
    return graph

def compute_pagerank(graph, iterations=20, d=0.85):
    N = len(graph)
    ranks = {node: 1 / N for node in graph}

    for _ in range(iterations):
        new_ranks = {}
        for node in graph:
            rank_sum = sum(ranks[neighbor] / len(graph[neighbor]) for neighbor in graph[node])
            new_ranks[node] = (1 - d) / N + d * rank_sum
        ranks = new_ranks
    return ranks

def process_corpus(directory):
    file_count = 0
    total_words = 0
    word_docs = defaultdict(set)
    all_tokens = []
    bigram_counter = Counter()

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_count += 1
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                text = f.read()
                tokens = clean_text(text)
                total_words += len(tokens)
                all_tokens.append(tokens)
                for word in set(tokens):
                    word_docs[word].add(filename)
                for i in range(len(tokens) - 1):
                    bigram_counter[(tokens[i], tokens[i+1])] += 1

    unique_terms = len(word_docs)
    avg_length = total_words / file_count
    return all_tokens, word_docs, bigram_counter, file_count, total_words, unique_terms, avg_length

def analyze_text_corpus(directory):
    tokens_list, word_docs, bigrams, doc_count, total_words, unique_terms, avg_len = process_corpus(directory)
    graph = build_graph(tokens_list)
    pagerank = compute_pagerank(graph)

    print("\nText Corpus Analysis Results")
    print("Corpus Statistics:")
    print(f"- Documents processed: {doc_count}")
    print(f"- Total words: {total_words}")
    print(f"- Unique terms: {unique_terms}")
    print(f"- Average document length: {avg_len:.2f}")

    print("\nGraph Analysis:")
    node_degrees = [len(neighbors) for neighbors in graph.values()]
    edges = sum(node_degrees) // 2
    avg_degree = sum(node_degrees) / len(node_degrees)
    density = edges / (unique_terms * (unique_terms - 1) / 2)
    print(f"- Nodes (unique terms): {unique_terms}")
    print(f"- Edges (co-occurrences): {edges}")
    print(f"- Average node degree: {avg_degree:.2f}")
    print(f"- Graph density: {density:.4f}")

    print("\nPageRank Results - Top 10 Key Terms:")
    for term, score in sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{term} ({score:.4f}) - appears in {len(word_docs[term])} documents")

    print("\nMost Significant Bigrams:")
    for (w1, w2), count in bigrams.most_common(10):
        print(f"{w1} {w2} ({count} occurrences)")

if __name__ == "__main__":
    analyze_text_corpus("text_papers")
