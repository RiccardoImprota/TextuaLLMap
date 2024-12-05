from emoatlas import EmoScores
import os
import json
import re
from pprint import pprint
from collections import defaultdict
from emoatlas.resources import _valences
import random
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats



emos=EmoScores()

base_output_dir = "localdb"
valence_dir = "Valence_Metrics"

# Folders of interest
folders_of_interest = ['climate', 'math', 'misinformation_health','gwarming']
folders_of_interest = ['misinformation_health']

def extract_model(filename):
    if filename.endswith('.jsonl'):
        return filename[:-6]  # Remove the last 6 characters
    else:
        return filename
    
def get_valence_sets(weighted_fmnt, language='english'):
    
    positive, negative, ambivalent = _valences(language)
    

    all_nodes = set(node for edge in weighted_fmnt for node in edge[:2])

    print('wtf:', all_nodes)



    positive_nodes = all_nodes.intersection(positive)
    print(positive_nodes)
    negative_nodes = all_nodes.intersection(negative)
    neutral_nodes = all_nodes - (positive_nodes | negative_nodes )

    return positive_nodes, negative_nodes, neutral_nodes

def swap_elements_in_sets(set1, set2, set3):
    # Calculate total number of elements
    total_elements = len(set1) + len(set2) + len(set3)
    
    # Convert sets to lists for easy manipulation
    lists = [list(set1), list(set2), list(set3)]
    
    # Perform swapping operations
    for _ in range(10 * total_elements):
        # Pick 2 random sets without repetition
        set_indices = random.sample(range(3), 2)
        
        # Pick a random word from each set
        word1 = random.choice(lists[set_indices[0]])
        word2 = random.choice(lists[set_indices[1]])
        
        # Only swap if the words don't already exist in the other list
        if word1 not in lists[set_indices[1]] and word2 not in lists[set_indices[0]]:
            lists[set_indices[0]].remove(word1)
            lists[set_indices[1]].remove(word2)
            lists[set_indices[0]].append(word2)
            lists[set_indices[1]].append(word1)
    
    # Convert lists back to sets
    return set(lists[0]), set(lists[1]), set(lists[2])

def export_loop_valences():
    for folder in folders_of_interest:
        input_folder_path = os.path.join(base_output_dir, folder)
        valence_output_path = os.path.join(valence_dir, folder)

        for filename in os.listdir(input_folder_path):
            print(filename.rstrip('.jsonl'))

            file_path = os.path.join(input_folder_path, filename)
            with open(file_path, 'r') as file:
                fmnts = []
                for line in file:
                    data = json.loads(line)
                    fmnts.append(data['fmnt']['syntactic'])
            
            weighted_fmnt = emos.combine_formamentis(fmnts, weights=True)
            if 'ITA' in filename:
                language = 'italian'
            else:
                language = 'english'

            positive, negative, neutral = get_valence_sets(weighted_fmnt, language=language)

            output_file_path = os.path.join(valence_output_path, f"{filename.rstrip('.jsonl')}_valence.jsonl")
            os.makedirs(valence_output_path, exist_ok=True)  # Assicurati che la directory esista

            with open(output_file_path, 'a') as out_file:
                for i in range(1000):
                    if i % 50 == 0:
                        print(i)
                    random_positive, random_negative, random_neutral = swap_elements_in_sets(positive, negative, neutral)
                    
                    def get_random_valence(word):
                        if word in random_positive:
                            return 'positive'
                        elif word in random_negative:
                            return 'negative'
                        else:
                            return 'neutral'
                    
                    # Weighted network analysis
                    random_weights = {
                        'pos_pos': 0, 'pos_neutral': 0, 'neg_neutral': 0,
                        'neg_neg': 0, 'neutral_neutral': 0, 'pos_neg': 0,
                        'weight_pos_pos': 0, 'weight_pos_neutral': 0, 'weight_neg_neutral': 0,
                        'weight_neg_neg': 0, 'weight_neutral_neutral': 0, 'weight_pos_neg': 0
                    }
        
                    for node1, node2, weight in weighted_fmnt:
                        random_valence1, random_valence2 = get_random_valence(node1), get_random_valence(node2)
            
                        # Random distribution
                        if random_valence1 == 'positive' and random_valence2 == 'positive':
                            random_weights['pos_pos'] += 1
                            random_weights['weight_pos_pos'] += weight
                        elif (random_valence1 == 'positive' and random_valence2 == 'neutral') or (random_valence1 == 'neutral' and random_valence2 == 'positive'):
                            random_weights['pos_neutral'] += 1
                            random_weights['weight_pos_neutral'] += weight
                        elif (random_valence1 == 'negative' and random_valence2 == 'neutral') or (random_valence1 == 'neutral' and random_valence2 == 'negative'):
                            random_weights['neg_neutral'] += 1
                            random_weights['weight_neg_neutral'] += weight
                        elif random_valence1 == 'negative' and random_valence2 == 'negative':
                            random_weights['neg_neg'] += 1
                            random_weights['weight_neg_neg'] += weight
                        elif random_valence1 == 'neutral' and random_valence2 == 'neutral':
                            random_weights['neutral_neutral'] += 1
                            random_weights['weight_neutral_neutral'] += weight
                        elif (random_valence1 == 'negative' and random_valence2 == 'positive') or (random_valence1 == 'positive' and random_valence2 == 'negative'):
                            random_weights['pos_neg'] += 1
                            random_weights['weight_pos_neg'] += weight
                        
                    json.dump(random_weights, out_file)
                    out_file.write('\n')
                    out_file.flush()
                    
export_loop_valences()