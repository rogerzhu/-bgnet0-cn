# Some common English words

WORDS = [
    "the", "be", "and", "a", "of", "to", "in", "you", "it", "have",
    "to", "that", "for", "do", "he", "with", "on", "this", "we", "that",
    "not", "but", "they", "say", "at", "what", "his", "from", "go",
    "or", "by", "get", "she", "my", "can", "as", "know", "if", "me",
    "your", "all", "who", "about", "their", "will", "so", "would",
    "make", "just", "up", "think", "time", "there", "see", "her", "as",
    "out", "one", "come", "people", "take", "year", "him", "them",
    "some", "want", "how", "when", "which", "now", "like", "other",
    "could", "our", "into", "here", "then", "than", "look", "way",
    "more", "these", "no", "thing", "well", "because", "also", "two",
    "use", "tell", "good", "first", "day", "find", "give", "more",
    "new", "one", "us", "any", "those", "very", "her", "need", "back",
    "there", "should", "even", "only", "many", "really", "work", "life",
    "why", "right", "down", "on", "try", "let", "something", "too",
    "call", "may", "still", "through", "mean", "after", "never", "no",
    "world", "in", "feel", "yeah", "great", "last", "child", "over",
    "ask", "when", "as", "school", "state", "much", "talk", "out",
    "keep", "leave", "put", "like", "help", "big", "where", "same",
    "all", "own", "while", "start", "three", "high", "every", "another",
    "become", "most", "between", "happen", "family", "over",
    "president", "old", "yes", "house", "show", "again", "student",
    "so", "seem", "might", "part", "hear", "its", "place", "problem",
    "where", "believe", "country", "always", "week", "point", "hand",
    "off", "play", "turn", "few", "group", "such"
]   

import sys
import socket
import random

# How many bytes is the word length?
WORD_LEN_SIZE = 2

def usage():
    print("usage: wordserver.py port", file=sys.stderr)

def build_word_packet(word_count):
    word_packet = b''
    word_list = []

    for _ in range(word_count):
        word = random.choice(WORDS)
        word_bytes = word.encode()
        word_len = len(word)
        word_len_bytes = word_len.to_bytes(WORD_LEN_SIZE, "big")

        word_packet += word_len_bytes + word_bytes
        word_list.append(word)

    return word_packet, word_list
        
def send_words(s):
    word_count = random.randrange(1, 10)

    word_packet, word_list = build_word_packet(word_count)

    s.sendall(word_packet)

    return word_list

def main(argv):

    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    s = socket.socket()
    s.bind(('', port))
    s.listen()

    while True:
        print("-----------------------")
        print("Waiting for connections")
        print("-----------------------")

        new_s, connection_info = s.accept()

        print(f"Got connection from {connection_info}")

        word_list = send_words(new_s)

        print(f"Sent words: {','.join(word_list)}")

        new_s.close()
        
if __name__ == "__main__":
    sys.exit(main(sys.argv))
