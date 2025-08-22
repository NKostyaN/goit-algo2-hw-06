import requests
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def map_reduce(text):
    words = text.split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return None


def visualize_top_words(data):
    words, counts = zip(*data)

    plt.style.use("_mpl-gallery")
    plt.figure(figsize=(10, 6))
    plt.stem(words, counts)
    plt.title("Топ 10 найчастіше вживаних слів")
    plt.xlabel("Слова")
    plt.ylabel("Кількість")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    target_url = "https://www.gutenberg.org/cache/epub/164/pg164.txt"  # Twenty Thousand Leagues under the Sea by Jules Verne
    data = get_text(target_url)

    if data:
        result = map_reduce(data)
        sorted_words = sorted(result.items(), key=lambda x: x[1], reverse=True)[:10]
        visualize_top_words(sorted_words)
