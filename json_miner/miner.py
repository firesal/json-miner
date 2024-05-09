from .indexedList import IndexedSubsetList
import json

def try_json_load(text, indexes):
    '''
    Try loading the indexes as a json from the text content.
    Returns boolean
    '''
    try:
        obj = json.loads(text[i:j+1])

    except ValueError:
        try:
            # obj = json.loads(text[i:j+1].replace('\\"', '"'))
            obj = json.loads(text[i:j+1].encode("utf-8").decode("unicode_escape"))
        except ValueError:
            return False

    return True

# def try_json_load_with_return(text):
#     try:
#         obj = json.loads(text)

#     except ValueError:
#         try:
#             # obj = json.loads(text[i:j+1].replace('\\"', '"'))
#             obj = json.loads(text.encode("utf-8").decode("unicode_escape"))
#         except ValueError:
#             return False

#     return obj

def json_load_wrap(text):
    '''
    A wrapper of json loading text with preloaded indexes to see if the
    indexes returns a valid json.
    '''

    def try_json_load2(indexes):
        i,j = indexes
        try:
            obj = json.loads(text[i:j+1])

        except ValueError:
            try:
                # To see if the json loads with a utf-8 encode and unicode escape decode
                # obj = json.loads(text[i:j+1].replace('\\"', '"'))
                obj = json.loads(text[i:j+1].encode("utf-8").decode("unicode_escape"))
            except ValueError:
                return False

        return True
    return try_json_load2


def get_slashes(text,index):
    '''
    Function to get all the double slashes
    '''
    result = ''
    for i in range(index,-1,-1):
        char = text[i]
        if char == '\\':
            result += '\\'
        else:
            break
    return result

def not_escaped(text,index):
    if index !=0:
        # counting double slashes uses get double slashes function     
        slash_count = len(get_slashes(text,index-1))

        # remainder theorem to see whether the character was actually escaped
        if slash_count%2 == 0:
            return True
        else:
            return False
    return True

def validate_pair(selected_pairs):
    def pair_validate(skipped_pair):
        for pair in selected_pairs:
            x,y = 0,1
            if (pair[x] <= skipped_pair[x] <= pair[y]) or \
                (pair[x] <= skipped_pair[y]<= pair[y]) or \
                (skipped_pair[x] <= pair[x] <= skipped_pair[y]) or \
                (skipped_pair[x] <= pair[y]<= skipped_pair[y]):
                return False
        return True
    return pair_validate

def generate_alertnate_pairs(pairs):
    result = []
    for i in range(1,len(pairs)):
        result.append((pairs[i-1][1]+1, pairs[i][0]-1))
    return result

def character_select(text, selected_characters, skip_characters, debug_flag= False):
    """
    Inputs:
        text - The actual text to mined
        selected_characters - character for a valid opening and closing character of a json to 
                   checked for, usually curl braces and square brackets
        skip_characters - 
    """
    if selected_characters[0] in text:
        i = text.index(selected_characters[0]) or 0
    else:
        i = 0
    skip = False
    last_skip_start = None
    skipped_pairs = []
    flag = debug_flag
    while i < len(text):
        char = text[i]
        if skip  and not_escaped(text,i):
            if char == skip:
                skip = False
                if last_skip_start:
                    skipped_pairs.append([last_skip_start,i])
                    last_skip_start = None
            else:
                i+=1
                continue
        elif char in ["'",'"',"`"] and not_escaped(text,i):
            if not skip:
                if i != 0 and text[i-1] in selected_characters[-1]:
                    i +=1
                    continue
                skip = char
                last_skip_start = i

        elif char in selected_characters:
            if i != 0:
                if not not_escaped(text,i):
                    i+=1
                    continue
            text.turn_on(i)
        i += 1
    if skip:
        skipped_pairs.append([last_skip_start,i])
    return skipped_pairs

def get_block_pairs(json_lists, start_char, end_char):
    i = 0
    pairs = []
    while i < len(json_lists):
        b_count = 0
        for j in range(i,len(json_lists)):
            if json_lists[j] == start_char:
                b_count += 1
            elif json_lists[j] == end_char:
                # if flag:
                #     print(b_count)
                b_count -= 1
                if b_count < 0 :
                    break
                if b_count == 0:
                    pairs.append([i,j])
                    i = j
                    break
        i += 1
    return pairs

def mine_json(text2,selected_characters = ['[',']']):
    text = IndexedSubsetList(text2)
    skip_characters = ["'",'"',"`"]
    opening_char, closing_char = selected_characters

    character_select(text, selected_characters, skip_characters)
    if text2.startswith(''''\n[null'''):
        # print('###',text2[:100])
        flag = True

    json_lists = text.get_subset()

    pairs = get_block_pairs(json_lists, opening_char,closing_char)
    
    load_test = json_load_wrap(text2)
    orginal_pairs = [json_lists.get_original_indexes(x,y) for x,y in pairs]

    alternate_pairs = generate_alertnate_pairs([[0,0]]+orginal_pairs+[[len(text2),len(text2)]])
    possible_valid_skipped = list(filter(lambda x:(x[1]-x[0])>100,alternate_pairs))
    newly_found_pairs = []
    for  start,end in possible_valid_skipped:


        temp_text = IndexedSubsetList(text2)
        for i in range(start,end+1):
            temp_text.turn_on(i)
        subset = temp_text.get_subset()
        if all([x in subset for x in selected_characters]):
            character_select(subset, selected_characters, skip_characters, True)
            new_json_lists = subset.get_subset()
            if new_json_lists:
                new_pairs = get_block_pairs(new_json_lists, opening_char, closing_char)
                mapped_pairs = [temp_text.get_original_indexes(x,y) for x,y in new_pairs]
                newly_found_pairs.extend(mapped_pairs)
                # print('@%&%#$', list(map(lambda x,y:y-x, new_pairs)))

    orginal_pairs.extend(newly_found_pairs)
    valid_pairs = list(filter(load_test, orginal_pairs))
    return valid_pairs

def wrap_get_text(text):
    def get_text(t):
        return text[t[0]:t[1]+1]
    return get_text



def remove_overlap(pairs1, pairs2):
    def overlap_check(main_pair,overlap_pair):
        return main_pair[0]<overlap_pair[0] < overlap_pair[1] < main_pair[1]
    def check_overlap(main_pairs,secondary_pairs):
        for m_pair in main_pairs:
            k = 0
            while k < len(secondary_pairs):
                if overlap_check(m_pair,secondary_pairs[k]):
                    # secondary_pairs.pop(k)
                    secondary_pairs.pop(k)
                    k -= 1
                k+=1
    check_overlap(pairs1, pairs2) 
    check_overlap(pairs2, pairs1)
    return pairs1 + pairs2

def json_miner(text):
    pairs1 = mine_json(text,['{','}'])
    pairs2 = mine_json(text,['[',']'])
    return remove_overlap(pairs1, pairs2)

class JsonMiner:
    '''
    Miner Class to mine json blocks from any kind of text(could be raw html)
    '''
    def __init__(self, text):
        self.m_text = text 
        pairs1 = mine_json(text,['{','}'])
        pairs2 = mine_json(text,['[',']'])
        self.mined_pairs = remove_overlap(pairs1, pairs2)

    def get_pairs(self):
        return self.mined_pairs

    def get_blocks(self):
        for i,j in self.mined_pairs:
            yield self.m_text[i:j+1]

