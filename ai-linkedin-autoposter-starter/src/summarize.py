from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


def summarize(text: str, sentences: int = 2) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary_sents = summarizer(parser.document, sentences)
    return " ".join(str(s) for s in summary_sents)
