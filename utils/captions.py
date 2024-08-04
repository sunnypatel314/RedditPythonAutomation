def condense_captions(segment, threshold):
    words_dictionary = {}
    words = segment["text"].strip().split(" ")

    phrase, current_count = "", 0
    counter_array = []
    phrase_array = []
    # print(words)

    for word in words:
        if phrase.endswith(". "):
            phrase_array.append(phrase)
            counter_array.append(current_count)
            phrase, current_count = "", 1
        if len(word) > threshold and phrase == "":
            counter_array.append(1)
            phrase_array.append(word + " ")
        elif len(word) + len(phrase) > threshold:
            counter_array.append(current_count)
            phrase_array.append(phrase)
            current_count = 1
            phrase = word + " "
        else:
            phrase += word + " "
            current_count += 1
            
    
    if phrase != "":
        phrase_array.append(phrase)
        counter_array.append(current_count)
    
    # print(phrase_array, counter_array)
    
    words_index, phrase_array_index = 0, 0
    while words_index <= len(words) - 1:
        words_dictionary[phrase_array[phrase_array_index]] = [segment["words"][words_index]["start"]]
        words_dictionary[phrase_array[phrase_array_index]].append(segment["words"][words_index + counter_array[phrase_array_index] - 1]["end"])
        words_index += counter_array[phrase_array_index]
        phrase_array_index += 1

    return words_dictionary


# for testing

my_d = {'id': 0, 'seek': 0, 'start': 0.0, 'end': 2.02, 
        'text': ' I secretly married a Muslim woman.', 
        'tokens': [50364, 286, 22611, 5259, 257, 8178, 3059, 13, 50514], 
        'temperature': 0.0, 'avg_logprob': -0.13443006896972656, 
        'compression_ratio': 1.5627240143369177, 'no_speech_prob': 0.021604226902127266, 
        'confidence': 0.941, 
        'words': [
            {'text': 'I', 'start': 0.0, 'end': 0.56, 'confidence': 0.847}, 
            {'text': 'secretly', 'start': 0.56, 'end': 0.92, 'confidence': 0.986}, 
            {'text': 'married', 'start': 0.92, 'end': 1.22, 'confidence': 0.995}, 
            {'text': 'a', 'start': 1.22, 'end': 1.36, 'confidence': 0.998}, 
            {'text': 'Muslim', 'start': 1.36, 'end': 1.56, 'confidence': 0.865}, 
            {'text': 'woman.', 'start': 1.56, 'end': 2.02, 'confidence': 0.971}
                ]
        }       


# print(condense_captions(my_d, 10))