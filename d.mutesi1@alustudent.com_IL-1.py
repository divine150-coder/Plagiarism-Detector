"""
Plagiarism Detector

Compares two essays for common words, word frequency, and plagiarism percentage.
"""

import string
import sys

def load_and_preprocess(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()
            if not text.strip():
                print(f"Error: '{filename}' is empty.")
                return []
            translator = str.maketrans('', '', string.punctuation)
            text = text.translate(translator).lower()
            words = [w for w in text.split() if w.strip()]
            return words
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{filename}': {e}")
        return []

def count_word_frequency(words):
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

def print_essay_stats(words, label):
    print(f"\n{label} Statistics:")
    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(set(words))}")

def find_common_words(freq1, freq2):
    common = set(freq1) & set(freq2)
    if not common:
        print("No common words found.")
        return
    print("\nCommon Words:")
    print(f"{'Word':<15}{'Essay 1':<10}{'Essay 2':<10}")
    print("-"*35)
    for word in sorted(common):
        print(f"{word:<15}{freq1[word]:<10}{freq2[word]:<10}")

def search_word(word, freq1, freq2):
    if not word:
        print("Error: Empty input.")
        return False
    w = word.lower()
    c1 = freq1.get(w, 0)
    c2 = freq2.get(w, 0)
    if c1 == 0 and c2 == 0:
        print(f"'{word}' not found in either essay.")
        return False
    print(f"'{word}' appears {c1} time(s) in Essay 1 and {c2} time(s) in Essay 2.")
    return True

def calculate_plagiarism_percentage(freq1, freq2):
    set1 = set(freq1)
    set2 = set(freq2)
    union = set1 | set2
    if not union:
        print("Cannot calculate plagiarism: essays are empty.")
        return
    intersection = set1 & set2
    percentage = (len(intersection) / len(union)) * 100
    print(f"\nPlagiarism Percentage: {percentage:.2f}%")
    if percentage >= 50:
        print("Plagiarism Detected!")
    else:
        print("No Plagiarism Detected.")

def main():
    print("\nPlagiarism Detector\n")

    essay1_file = 'essay-1.txt' # First essay filename
    essay2_file = 'essay-2.txt' # Second essay filename

    words1 = load_and_preprocess(essay1_file)
    words2 = load_and_preprocess(essay2_file)
    if not words1 or not words2:
        print("Both essays are required to proceed.")
        return

    freq1 = count_word_frequency(words1)
    freq2 = count_word_frequency(words2)

    print_essay_stats(words1, 'Essay 1')
    print_essay_stats(words2, 'Essay 2')

    find_common_words(freq1, freq2)

    print("\nChecking for plagiarism...")
    calculate_plagiarism_percentage(freq1, freq2)

    print("\n--- Word Search ---")
    print("Type a word to search for its count, or 'q' to quit.")

    while True:
        user_word = input("Enter word to search: ").strip()
        if user_word.lower() == 'q':
            print("Exiting.")
            break
        search_word(user_word, freq1, freq2)

    print("\nThank you!")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Unexpected error: {e}")
