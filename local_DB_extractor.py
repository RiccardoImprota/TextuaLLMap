from emoatlas import EmoScores
import os
import json
import re
from pprint import pprint
from collections import defaultdict


emos = EmoScores()
emosita = EmoScores(language='italian')


# Define the base directory containing the folders of interest
base_dir = 'texts'
base_output_dir = "localdb"

# Folders of interest
folders_of_interest = ['climate', 'math', 'misinformation_health','gwarming']


def extract_model(filename):
    match = re.search(r'_(.*?)_', filename)
    if match:
        return match.group(1)
    return None

def get_output_file(base_output_dir, model, topic):
    # Create directory if it doesn't exist
    os.makedirs(base_output_dir, exist_ok=True)
    return os.path.join(base_output_dir, topic ,f"{model}.jsonl")



for folder in folders_of_interest:
    folder_path = os.path.join(base_dir, folder)
    

    for filename in os.listdir(folder_path):


        file_path = os.path.join(folder_path, filename)

        if '(ITA)' not in file_path:
            continue
        model = extract_model(filename)
        output_file = get_output_file(base_output_dir, model, folder)
        print(folder, filename)

        with open(file_path, 'r') as infile, open(output_file, 'a') as outfile:
            data = json.load(infile)

            for testo in data:
                output = {
                    'topic': folder,
                    'model': model,
                    'testo': testo
                }
##
                if '(ITA)' in file_path:
                    output['language'] = 'ITA'
                    #zscores_list = []
                    #for _ in range(10):
                    #    emosita.set_baseline()
                    #    emotion_scores = emosita.zscores(testo)
                    #    zscores_list.append(emotion_scores)
                    output['zscores'] = emosita.zscores(testo)
                    
                    fmnt = emosita.formamentis_network(testo,semantic_enrichment=['synonyms'],multiplex=True)
                    output['fmnt'] = fmnt.edges
                    output['lemmatized_test'] = emosita.lemmatize_text(testo)
                else:
                    output['language'] = 'ENG'
                    #zscores_list = []
                    #for _ in range(10):
                    #    emos.set_baseline()
                    #    emotion_scores = emos.zscores(testo)
                    #    zscores_list.append(emotion_scores)
                    output['zscores'] = emos.zscores(testo)
                    fmnt = emos.formamentis_network(testo,semantic_enrichment=['synonyms'],multiplex=True)
                    output['fmnt'] = fmnt.edges
                    output['lemmatized_test'] = emos.lemmatize_text(testo)
                    
                
##
                # Write the output to the file as a JSON line
                json.dump(output, outfile)
                outfile.write('\n')
                outfile.flush()
                