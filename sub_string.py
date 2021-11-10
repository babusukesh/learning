import difflib

from fuzzysearch import find_near_matches
from fuzzywuzzy import process

def fuzzy_extract(qs, ls, threshold):
    '''fuzzy matches 'qs' in 'ls' and returns list of
    tuples of (word,index)
    '''
    for word, _ in process.extractBests(qs, (ls,), score_cutoff=threshold):
        # print('word {}'.format(word))
        for match in find_near_matches(qs, word, max_l_dist=1):
            match = word[match.start:match.end]
            # print('match {}'.format(match))
            index = ls.find(match)
            yield (match, index)


large_string = 'EY referes to the global organization, and may refer to one or more, of the member firms of Ernst & Young Global' \
    'Limited, each of which is separate legal entity. Ernst & Young Global Limited, a UK company' \
    'Blenheim House, Fountainhall Road, Aberdeen AB15 4DT limited by guarantee, does not provide services to clients.'
query_string = 'House Blenheim, Aberdeen AB15 4DT, Fountainhall Road'


# print('query: {}\nstring: {}'.format(query_string, large_string))
for match,index in fuzzy_extract(query_string, large_string, 50):
    print('match: {}\nindex: {}'.format(match, index))