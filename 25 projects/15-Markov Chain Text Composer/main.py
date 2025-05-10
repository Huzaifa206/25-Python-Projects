import os
import re
import string
import random
import sys
from graph import Graph, Vertex

def get_words_from_text(text_path):
    try:
        with open(text_path, 'rb') as file:
            text = file.read().decode("utf-8")
            text = re.sub(r'\[(.+)\]', ' ', text)  # Remove [verse 1: artist]
            text = ' '.join(text.split())
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        words = words[:1000]  # Limit to 1000 words
        if len(words) < 10:
            raise ValueError("Input text is too short. Provide a file with more content.")
        return words
    except FileNotFoundError:
        print(f"Error: File '{text_path}' not found.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Unable to decode '{text_path}'. Ensure it's a valid text file.")
        sys.exit(1)

def make_graph(words):
    g = Graph()
    prev_word = None
    for word in words:
        word_vertex = g.get_vertex(word)
        if prev_word:
            prev_word.increment_edge(word_vertex)
        prev_word = word_vertex
    g.generate_probability_mappings()
    return g

def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        # Add 10% chance to jump to a random word to increase variety
        if random.random() < 0.1:
            word = g.get_vertex(random.choice(words))
        else:
            word = g.get_next_word(word)
    return composition

def main(text_path='lyrics.txt'):
    words = get_words_from_text(text_path)
    print(f"Processed {len(words)} words from '{text_path}'")
    g = make_graph(words)
    composition = compose(g, words, 100)
    print('Generated Composition:')
    print(' '.join(composition))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()