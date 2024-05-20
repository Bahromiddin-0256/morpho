from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

def load_words_db(file_path):
    words_db = {}
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            word, tag, category = row
            words_db[word] = (tag, category)
    return words_db

words_db = load_words_db('words_db_large.csv')

suffixes = {
    'egalik': ['im', 'ing', 'i', 'imiz', 'ingiz', 'lari'],
    'kelishik': ['ning', 'ga', 'ni', 'da', 'dan', 'bilan'],
    'ko‘plik': ['lar'],
    'zamon': ['yapti', 'di', 'moqchi']
}

def morfoanalyze(word):
    result = []
    base_word = word
    for suf_type, suf_list in suffixes.items():
        for suf in suf_list:
            if word.endswith(suf):
                result.append(f"{suf} ({suf_type} qo‘shimchasi)")
                base_word = word[:-len(suf)]
                break

    if base_word in words_db:
        result.append(f"{base_word} ({words_db[base_word][0]}; {words_db[base_word][1]})")
    else:
        result.append(f"{base_word} (noma'lum)")

    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    input_text = request.form['input_text']
    words = input_text.split()
    analysis = {word: morfoanalyze(word) for word in words}
    return jsonify(analysis)

if __name__ == "__main__":
    app.run(debug=True)
