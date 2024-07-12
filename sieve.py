class Letter():
    
    TYPES_LIST = ['white','yellow','green']
        
    def __init__(self,char:str,type:str):
        self.char = char
        self.type = type
    
    def change_type(self,new_type:int):
        self.type = self.TYPES_LIST[new_type]
        return self
    
    def get_type_index(self):
        return self.TYPES_LIST.index(self.type)


class Filter():
    
    DICT_CHARS = {
        "white":{},
        "green":{},
        "yellow":{}
    }
    
    actual_dict_chars = {
        "white":{},
        "green":{},
        "yellow":{}
    }
    sieve_list = []
    all_words = []
    
    def __init__(self,all_words:list):
        self.all_words = all_words.copy()
        self.sieve_list = all_words.copy()
    
    def process_word(self,list_of_chars):
        self.actual_dict_chars = {
            "white":{},
            "green":{},
            "yellow":{}
        }
        for index,char in enumerate(list_of_chars):
            try:
                self.actual_dict_chars[char.type][char.char.upper()].update(set([index]))
            except:
                self.actual_dict_chars[char.type][char.char.upper()] = set([index])
        
        for key,values in self.actual_dict_chars.items():
            self.DICT_CHARS[key].update(values)
        
        return self
    
    
    def process_whites(self,sieve:list,whites:dict):
        words_to_remove = []
        new_sieve = sieve
        two_lists_keys = set(self.DICT_CHARS['green'].keys())
        two_lists_keys.update(set(self.DICT_CHARS['yellow']))
        not_have_100 = set(whites.keys()).difference(set(two_lists_keys))
        new_sieve = [x for x in new_sieve if not any(letter in x for letter in not_have_100)]
        for word in new_sieve:
            dict_word = self.get_all_chars_indexes(word)
            all_keys = set(dict_word.keys()).intersection(set(whites.keys()))
            for key in all_keys:
                indexes = dict_word[key]
                intersec = set(indexes).intersection(set(whites[key]))
                if len(intersec) != 0:
                    words_to_remove.append(word)
                    break
                
        for word in words_to_remove:
            new_sieve.remove(word)
        return new_sieve
    
    def process_yellows(self,sieve:list,yellows:dict):
        new_sieve = sieve
        words_to_remove = []
        for word in new_sieve:
            dict_word = self.get_all_chars_indexes(word)
            all_keys = set(dict_word.keys()).intersection(set(yellows.keys()))
            if all_keys != yellows.keys():
                words_to_remove.append(word)
            else:
                for key in all_keys:
                    values = dict_word[key]
                    intersec = set(values).intersection(set(yellows[key]))
                    if len(intersec) != 0:
                        words_to_remove.append(word)
                        break
        
        for word in words_to_remove:
            new_sieve.remove(word)
        return new_sieve
        
    def process_greens(self,sieve:list,greens:dict):
        new_sieve = sieve
        words_to_remove = []
        for word in sieve:
            dict_word = self.get_all_chars_indexes(word)
            all_keys = set(dict_word.keys()).intersection(set(greens.keys()))
            if all_keys != greens.keys():
                words_to_remove.append(word)
            else:
                for key in all_keys:
                    values = dict_word[key]
                    intersec = set(values).intersection(greens[key])
                    if len(intersec) == 0:
                        words_to_remove.append(word)
                        break
            
        for word in words_to_remove:
            new_sieve.remove(word)
        return new_sieve
    
    def process_repeated_letters(self,sieve:list):
        new_sieve = sieve
        words_to_remove = []
        repeated_letters = set(self.actual_dict_chars['green'].keys()).intersection(self.actual_dict_chars['yellow'].keys())
        for word in new_sieve:
            dict_word = self.get_all_chars_indexes(word)
            for key in repeated_letters:
                if len(dict_word[key]) < 2:
                    words_to_remove.append(word)
                    break
        
        for word in words_to_remove:
            new_sieve.remove(word)
        return new_sieve
            
            
    
    def get_all_chars_indexes(self,word:str):
        char_dicts = {}
        for index,char in enumerate(word):
            try:
                char_dicts[char].append(index)
            except:
                char_dicts[char] = [index]
        return char_dicts
    
    def sieve(self):
        #remove words which have white chars
        sieve = self.process_whites(self.sieve_list,self.DICT_CHARS['white'])
        #end
        
        #remove words which have yellows chars in some indexes
        sieve = self.process_yellows(sieve,self.DICT_CHARS['yellow']) if len(self.DICT_CHARS['yellow'].keys()) > 0 else sieve
        #end    
        
        #remove words which DO NOT have green chars in some indexes
        sieve = self.process_greens(sieve,self.DICT_CHARS['green']) if len(self.DICT_CHARS['green'].keys()) > 0 else sieve
        #end
        
        #verify if the word has repeated letters, if has, remove the words which does not have repeated letters
        sieve = self.process_repeated_letters(sieve)
        #end
        self.sieve_list = sieve.copy()
        self.sieve_list.sort()
        
        return self.sieve_list
    
    def reset_values(self):
        self.DICT_CHARS = {
            "white":{},
            "green":{},
            "yellow":{}
        }
        self.sieve_list = self.all_words.copy()