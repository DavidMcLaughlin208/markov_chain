import re
import pickle
import random
import math
from collections import defaultdict, deque



class MarkovChain:

    SENTENCE_END = "!sentence_end!"
    SENTENCE_START = "sentence_start"

    def __init__(self, depth=2):
        self.depth = depth
        self.lookup_dict = defaultdict(list)
        self._punctuation_regex = re.compile('[,;\?\:\-\[\]\n[0-9]]+')
        self._whitespace_regex = re.compile('\s+')
        self._abbreviations = ["mr", "dr"]


    def read_string(self, str):
        self.__add_data(str)


    def read_file(self, location):
        with open(location, 'r') as fh:
            self.__add_data(fh.read())


    def __add_data(self, str):
        sanitized_string = self._punctuation_regex.sub(' ', str).lower()
        sentences = sanitized_string.split(".")
        for i in range(len(sentences)):
            print(sentences[i])
            sanitized_sentence = self._whitespace_regex.sub(' ', sentences[i])
            words = sanitized_sentence.strip().split(" ")
            words_length = len(words)
            if words_length == 1:
                self.lookup_dict[self.SENTENCE_START].append(tuple(("", words[0])))
                self.lookup_dict[tuple(("", words[0]))].append(self.SENTENCE_END)
                continue
            for j in range(words_length - 1):
                print(j, words[j])
                if j == 0:
                    starting_two_word_tuple = tuple((words[j], words[j + 1]))
                    self.lookup_dict[self.SENTENCE_START].append(starting_two_word_tuple)
                two_word_tuple = tuple((words[j], words[j + 1]))
                followup_word = words[j + 2] if j < len(words) - 2 else self.SENTENCE_END
                self.lookup_dict[two_word_tuple].append(followup_word)

    def print_dict(self):
        print(self.lookup_dict)

    def generate_text(self, number_of_sentences=0):
        if len(self.lookup_dict[self.SENTENCE_START]) == 0:
            return
        if number_of_sentences == 0:
            number_of_sentences = math.ceil(random.random() * 10) + 5
        text = deque()
        for i in range(number_of_sentences):
            text.append(self.generate_sentence())
        print(" ".join(text))

    def generate_sentence(self):
        sentence = deque()
        tup = random.sample(self.lookup_dict[self.SENTENCE_START], 1)[0]
        sentence.extend(tup)
        print(tup)
        while self.lookup_dict[tup]:
            word = random.sample(self.lookup_dict[tup], 1)[0]
            print(word)
            if word == self.SENTENCE_END:
                break
            sentence.append(word)
            tup = (sentence[-2], sentence[-1])
        return " ".join(sentence).capitalize() + "."
