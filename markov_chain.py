import os
import pickle
from collections import defaultdict
import json
import random
import numpy as np


def weighted_random_choice(next_words_dict):
    """Select a word based on weighted probabilities."""
    next_words = list(next_words_dict.keys())
    weights = list(next_words_dict.values())
    return np.random.choice(next_words, p=np.array(weights) / np.sum(weights))


class PoemGenerator:
    def __init__(self, json_file, model_filename, order=1, save_model=False, build_model=True):
        self.json_file = json_file
        self.markov_chain = {}
        self.order = order
        self.all_words = []
        self.load_poems()
        if build_model:
            self.build_markov_chain(model_filename, save_model)

    def save_markov_chain(self, filename, directory):
        """Save the Markov chain to a file using pickle."""
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, filename), 'wb') as f:
            pickle.dump(self.markov_chain, f)

    def load_markov_chain(self, filename, directory):
        """Load the Markov chain from a file using pickle."""
        print(f'Loading model from: {os.path.join(directory, filename)}')
        with open(os.path.join(directory, filename), 'rb') as f:
            self.markov_chain = pickle.load(f)

    def load_poems(self):
        """Load poems from a JSON file and prepare words."""
        with open(self.json_file, 'r') as f:
            poems_data = json.load(f)

        for poem in poems_data:
            poem_text = poem["text"].replace('\n\n', ' ')  # Replace with space
            words = poem_text.split()
            self.all_words.extend(words)

    def build_markov_chain(self, model_filename="markov_chain.pkl", save_model=False):
        """Build a weighted Markov chain from the loaded words."""
        for i in range(len(self.all_words) - self.order):
            current_ngram = tuple(self.all_words[i:i + self.order])
            next_word = self.all_words[i + self.order]
            if current_ngram not in self.markov_chain:
                self.markov_chain[current_ngram] = defaultdict(int)
            self.markov_chain[current_ngram][next_word] += 1

        # Save markov chain
        if save_model:
            self.save_markov_chain(model_filename, "MarkovChains")

    def generate_poem(self, max_words=50, start_word="<START>", load_markov_chain=False, model_name=None):
        """Generate a poem based on the Markov chain."""
        poem = []

        if load_markov_chain:
            try:
                self.load_markov_chain(model_name, "MarkovChains")
                print("Model loaded successfully. \n\n")
            except FileNotFoundError:
                print("Model file not found. Make sure the model exists.")
                return

        # Handle first-order case separately (no tuples, just words)
        if self.order == 1:
            # Find keys that match "<START>" (keys are words)
            start = [ngram for ngram in self.markov_chain.keys() if ngram[0] == "<START>"]
            print(f'First order - ngram amount: {len(start)}')

            if (start_word,) in self.markov_chain.keys():
                current_word = (start_word,)
            else:
                print("No valid start word found!")
                return

            poem.append(current_word)  # Add <START> word to the poem
        else:
            # Find an n-gram that starts with "<START>" (keys are tuples)
            start_ngrams = [ngram for ngram in self.markov_chain.keys() if ngram[0] == "<START>"]

            print(f"higher order - ngram amount: {len(start_ngrams)}")

            if not start_ngrams:
                print("No valid start n-grams found!")
                return

            # Randomly choose one of the start n-grams
            start_ngram = random.choice(start_ngrams)
            poem.extend(start_ngram[1:])  # Don't add <START> to the poem itself
            current_word = start_ngram

        # Continue generating the poem
        while len(poem) < max_words:
            next_words_dict = self.markov_chain.get(current_word, None)
            if not next_words_dict:
                break

            next_word = weighted_random_choice(next_words_dict)
            if next_word == "<END>":
                break

            poem.append(next_word)  # Add the next word

            if self.order == 1:
                # For first-order chain, just update the current word (as a tuple)
                current_word = (next_word,)  # Wrap next_word in a tuple
            else:
                # For higher-order chains, shift the n-gram window
                current_word = tuple(poem[-self.order:])  # Shift the n-gram window

        # Join the list into a poem, ensuring only individual words (not tuples) are joined
        return ' '.join(map(str, poem)).replace("('<START>',)", "")


# Example usage
if __name__ == "__main__":
    poems_file = "Dataset/Cleaned/cleaned_poems.json"  # Path to your .json file
    # Make sure to change the "order" to the order of the model if you do not decide to load the model in. Because the
    # code still relies on this parameter to check if it needs to use the higher order or first order start word selection
    generator = PoemGenerator(poems_file, "markov_chain_1st_order.pkl", order=1, save_model=True, build_model=False)
    generated_poem = generator.generate_poem(max_words=50, load_markov_chain=True, model_name="markov_chain_1st_order.pkl")
    print(generated_poem)