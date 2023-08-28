from pyabsa import AspectSentimentTripletExtraction as ASTE
from collections import defaultdict
import re
from tqdm import tqdm
import spacy

nlp = spacy.load('en_core_web_sm')

triplet_extractor = ASTE.AspectSentimentTripletExtractor(
    checkpoint="emcgcn",
)

def perform_aste_inference(df):
    print("Predicting...")

    document_results = defaultdict(list)
    document_dict = defaultdict() # id -> text dictionary
    for _, row in tqdm(df.iterrows()):
        # tokenise reviews into sentences
        doc = nlp(row['cleaned_text'])
        sentences = [sent.text for sent in doc.sents]
        sentence = row['cleaned_text']
        # remove spaces before and after punctuation marks
        sentence = re.sub(r'\s*([^\w\s])\s*', r'\1', sentence)
        # add space for certain punctuation
        sentence = re.sub(r'([.,:?!;%])', r'\1 ', sentence)

        document_dict[row.name] = sentence
        # predict triplets for each sentence
        for sent in sentences:
            result = triplet_extractor.predict(sent, print_result=False)
            document_results[row.name].append(result)

    aspect_list = process_aspects(dict(document_results), document_dict)
    return aspect_list

def process_aspects(document_results, document_dict):
    aspect_list = [] # list of aspect_dicts
    overall_sentiment = defaultdict(int) # percentage of each polarity
    opi_dict = defaultdict(dict) # frequency of each opinion for each aspect
    # for each review
    for document_id, results in document_results.items():
        # for each sentence in review
        for result in results:
            triplets = result['Triplets']
            # skip if Triplets is empty
            if len(triplets) == 0:
                continue
            # for each triplet prediction in sentence
            for triplet in triplets:
                try:
                    if triplets == '[]':
                        triplet = []
                        continue
                    # lowercase all terms
                    aspect_name = triplet['Aspect'].lower()
                    doc = nlp(aspect_name)
                    aspect_name = " ".join([token.lemma_ for token in doc]) # get lemma of aspect
                    opinion = triplet['Opinion'].lower()
                    polarity = triplet['Polarity'].lower()
                    
                    if aspect_name is None or opinion is None or polarity is None:
                        print("Error - Missing required keys in triplet:", triplet)
                        continue

                    # add aspect to aspect_list if it does not exist
                    aspect_dict = next((aspect for aspect in aspect_list if aspect['name'] == aspect_name), None)
                    # create new aspect dictionary if it does not exist
                    if aspect_dict is None:
                        aspect_dict = {
                            'name': aspect_name,
                            'reviews': defaultdict(list),
                            'opinions': set()
                        }
                        aspect_dict['reviews']['positive'] = set()
                        aspect_dict['reviews']['neutral'] = set()
                        aspect_dict['reviews']['negative'] = set()
                        aspect_list.append(aspect_dict)
                    
                    # add opinion count to opi_dict
                    if aspect_name in opi_dict:
                        if opinion in opi_dict[aspect_name]:
                            opi_dict[aspect_name][opinion] += 1
                        else:
                            opi_dict[aspect_name][opinion] = 1
                    else:
                        opi_dict[aspect_name] = {opinion: 1}

                    # add opinion to aspect
                    aspect_dict['opinions'].add(opinion)
                    # add sentence to its sentiment category
                    aspect_dict['reviews'][polarity].add(document_dict[document_id])
                except Exception as e:
                    print("Error:", e, result)

    for aspect in aspect_list:
        # sort opinions by frequency
        aspect['opinions'] = [opinion_freq[0] for opinion_freq in sorted(opi_dict[aspect['name']].items(),
                                                                        key=lambda item: item[1], reverse=True)]
        # get top 3 opinions
        aspect['opinions'] = aspect['opinions'][:3]
        
        # calculate sentiment percentages for each aspect
        sentiment_counts = defaultdict(int)
        for polarity, reviews in aspect['reviews'].items():
            sentiment_counts[polarity] = len(reviews)

        total_reviews = sum(sentiment_counts.values())

        sentiments = {
            polarity: format(round(count / total_reviews, 3) * 100, ".2f") if total_reviews > 0 else 0.0
            for polarity, count in sentiment_counts.items()
        }
        aspect['sentiments'] = sentiments

    # prepare data and filter out aspects with less than 3 reviews
    aspect_list = [
        {
            'name': aspect['name'],
            'reviews': {polarity: list(reviews) for polarity, reviews in aspect['reviews'].items()},
            'opinions': list(aspect['opinions']),
            'sentiments': aspect['sentiments'],
        }
        for aspect in aspect_list 
        if len(aspect['reviews']['positive']) > 2 or
            len(aspect['reviews']['neutral']) > 2
            or len(aspect['reviews']['negative']) > 2
    ]
    
    # calculate overall sentiment
    for aspect in aspect_list:
        for polarity, reviews in aspect['reviews'].items():
            overall_sentiment[polarity] += len(reviews)

    # construct the final JSON object
    json_data = {
        "aspect_sentiment": aspect_list,
        'overall_sentiment': {
            polarity: format(round(count / sum(overall_sentiment.values()), 3) * 100, ".2f") 
            if sum(overall_sentiment.values()) > 0 else 0.0
            for polarity, count in overall_sentiment.items()
        }
    }
    return json_data