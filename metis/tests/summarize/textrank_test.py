from src.summarize.textrank.textrank_keyword import TextRankKeyword
from src.summarize.textrank.textrank_sentence import TextRankSentence


def test_textrank():
    with open('../Readme.md', 'r', encoding='utf-8') as f:
        text = f.read()

        trkw = TextRankKeyword()
        trkw.analyze(text=text, lower=True, window=2)

        print('关键词：')
        for item in trkw.get_keywords(3, word_min_len=1):
            print(item.word, item.weight)

        print('关键短语：')
        for phrase in trkw.get_keyphrases(keywords_num=3, min_occur_num=2):
            print(phrase)

        trs = TextRankSentence()
        trs.analyze(text=text, lower=True, source='all_filters')

        print('摘要：')
        for item in trs.get_key_sentences(num=3):
            print(item.index, item.weight, item.sentence)
