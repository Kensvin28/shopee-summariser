import re
import emoji
from deep_translator import GoogleTranslator
import unicodedata as uni
import time
from tqdm import tqdm # progress bar
tqdm.pandas()

from malaya import stem
from malaya import normalizer
from malaya import segmentation
from malaya import language_model
# from malaya import spelling_correction
# corrector = spelling_correction.probability.load(language_model = lm)
lm = language_model.kenlm()
stemmer = stem.deep_model('noisy')
normalizer = normalizer.rules.load(None, stemmer)
text_scorer = lambda x: lm.score(x)
segmenter = segmentation.transformer(model = 'small')
segmenter_func = lambda x: segmenter.greedy_decoder([x])[0]

spam_list = [
    r"RM0", 
    r"Gboard", 
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
]

def clean(df):
    time_start = time.perf_counter()
    
    df = df.dropna(subset=['comment']).copy().reset_index(drop=True) # drop reviews with empty comments
    df['comment'] = df['comment'].astype(str) # ensure input review is string
    df = filter_df(df) # filter spam and short reviews
    df = df[~df['comment'].apply(contains_cjk_characters)] # remove reviews with CJK characters
    df = df.head(300) # take up to first 300 reviews only
    df['cleaned_text'] = df['comment'].apply(lambda x: clean_text(x)) # clean text
    df = df[df['cleaned_text'] != ""].reset_index(drop=True) # remove empty reviews
    df['cleaned_text'] = df['cleaned_text'].progress_apply(lambda x: normalise_df(x)) # normalise text
    df['cleaned_text'] = translate(df['cleaned_text']) # translate to english
    df['cleaned_text'] = df['cleaned_text'].apply(lambda x: post_cleaning(str(x))) # post cleaning
    df['cleaned_text'] = df['cleaned_text'].apply(lambda x: add_padding(str(x))) # add padding for lemmatisation
    
    time_elapsed = (time.perf_counter() - time_start)
    print("Preprocessing: %3.1f secs" % time_elapsed)
    return df

# filter df
def filter_df(df):
    print("Before:", df.shape)
    df = filter_spam(df)
    df = filter_short_rev(df)
    print("After:", df.shape)
    return df

# remove spam
def filter_spam(df):
    df = df[~df.comment.str.contains('|'.join(spam_list))].reset_index(drop=True)
    return df

# remove short reviews with 1 word
def filter_short_rev(df):
    # handle colons that do not have space after 
    df['comment'] = df['comment'].str.replace(':', ': ')
    df = df[df.comment.apply(lambda x: len(x.split())) > 1].reset_index(drop=True)
    return df

# check if text contains CJK characters
def contains_cjk_characters(text):
    cjk_ranges = [
        (u'\u4E00', u'\u9FFF'),  # Chinese
        (u'\u1100', u'\u11FF'),  # Korean
        (u'\u3040', u'\u309F'),  # Hiragana (Japanese)
        (u'\u30A0', u'\u30FF')   # Katakana (Japanese)
    ]

    cjk_pattern = '[' + ''.join([f'{start}-{end}' for start, end in cjk_ranges]) + ']'

    # Check if the text contains CJK characters
    if re.search(cjk_pattern, text):
        return True
    else:
        return False

# clean text
def clean_text(string):
    string = uni.normalize('NFKD', string) # normalise characters
    string = emoji.replace_emoji(string, '') # remove emoji
    string = re.sub(r'(\n+|\.+)', '. ', string) # remove newlines and multiple dots
    string = re.sub(r'(\w)\1{2,}', r'\1', string) # repeated chars
    string = re.sub(r'[ ]+', ' ', string).strip() # remove extra spaces
    string = re.sub(r'\s+([.,!?])', r'\1', string) # remove space before punctuation
    string = re.sub(r'(?<=[.,!?])(?=[^\s])', ' ', string) # add space after punctuation
    return string

# normalise malay texts
def normalise_df(text):
    text = normalizer.normalize(text, normalize_entity = False, normalize_emoji=False, normalize_percent=False, normalize_ic=False, text_scorer = text_scorer, segmenter=segmenter_func)['normalize']
    text = re.sub(r'\s*([^\w\s])\s*', r'\1', text) # Remove spaces before and after punctuation marks
    text = re.sub(r'([.,:?!;%])', r'\1 ', text) # add space after certain punctuation
    text = re.sub(r'\s*\u200b\s\u200b', '', text)
    return text

# translate reviews to english
def translate(text_list):
    print("Translating...")
    try:
        translation = GoogleTranslator('ms', 'en').translate_batch(list(text_list))
    except:
        print("Error translating with Google Translate")
        return list(text_list)
    return translation

# post cleaning
def post_cleaning(string):
    string = uni.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8') # remove unwanted characters from normalization
    string = re.sub(r'\s+', ' ', string) # remove extra spaces
    return string

# add padding for lemmatisation
def add_padding(string):
    string = re.sub(r'([^\w\s])', r' \1 ', string) # space padding for punctuation
    string = re.sub(r'[ ]+', ' ', string).strip() # remove extra spaces
    return string