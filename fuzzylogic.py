from itertools import permutations
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re

def word_comb(l):
  l2=list(permutations(l))
  words = [' '.join(i) for i in l2[1:]]
  return words


def address_extract(addr,parag):
  add_tokens=[i.strip(',') for i in addr.split(' ') if len(i)>0]
  idx_list = []
  for i in add_tokens:
    try:
      idx_list.extend(list(re.search(i, parag, re.I).span()))
      # print(re.search(i, parag, re.I))
    except Exception as e:
      print('Given word/token not present in address/data -------- Spelling mistake')
      para_tokesn = [i.strip(',') for i in parag.split(' ') if len(i)>0]
      word = process.extractOne(i,para_tokesn)[0]
      # print(word)
      idx_list.extend(list(re.search(word, parag, re.I).span()))
  mn,mx=min(idx_list), max(idx_list)
  return parag[mn:mx]


def fuzzyscore(comb, second_match, addr):
  df_dict={}
  for i in comb:
    score = fuzz.WRatio(i, second_match)
    df_dict['First Word'] = i
    df_dict['Score'] = score
    df_dict['Address'] = addr
    yield df_dict.copy()

def main():
  a='Blenheim House, Fountainhall Road, Aberdeen AB15 4DT'
  b='EY referes to the global organization, and may refer to one or more, of the member firms of Ernst & Young Global ' \
    'Limited, each of which is separate legal entity. Ernst & Young Global Limited, a UK company ' \
    'Blenheim House, Fountainhall Road, Aberdeen AB15 4DT limited by guarantee, does not provide services to clients.'

  l1=a.split(',')
  l1=[i.strip() for i in l1]
  # print(l1)

  plist=permutations(l1)

  combinations = [list(i) for i in plist]

  wcheck1 = combinations[0].copy()
  backup=wcheck1.copy()
  for i in combinations[0]:
    s=i.strip().split(' ')
    if len(s)>1:
      words=word_comb(s)
      id=combinations[0].index(i)
      for r in words:
        ''' wcheck2 have recent modified word like 'Blenheim House' to 'House Blenheim' and remaining all words same.
        wcheck1 have modified word along with previous modified word. Like 'Blenheim House' to 'House Blenheim' and 
        'Fountainhall Road' to 'Road Fountainhall' '''

        wcheck1.pop(id)
        wcheck1.insert(id, r)
        wlist = permutations(wcheck1)
        more_comb = [list(k) for k in wlist]
        combinations.extend(more_comb)

        wcheck2 = backup.copy()
        wcheck2.pop(id)
        wcheck2.insert(id, r)
        wlist = permutations(wcheck2)
        more_comb = [list(k) for k in wlist]
        combinations.extend(more_comb)

  # print(combinations)
  final_param_1=[', '.join(i) for i in combinations]
  addr = address_extract(final_param_1[0], b)

  df_data=list(fuzzyscore(final_param_1, b, addr))
  df=pd.DataFrame(df_data)
  # print(df)
  writer = pd.ExcelWriter('score_sheet_token_set.xlsx', engine='xlsxwriter')
  df.to_excel(writer, sheet_name='fuzzyscores', index=False)
  writer.save()


if __name__=='__main__':
  main()