
import pandas as pd
import fast_hangle_levenshtein
from fast_hangle_levenshtein import LevenshteinIndex
from fast_hangle_levenshtein import levenshtein
from fast_hangle_levenshtein import jamo_levenshtein


# load clean dataset 
default_word = pd.read_csv("data/clean_dataset.csv", names = ['num', 'words'])
default_word = list(default_word['words'])[1:]



def edit_distance(query, words = default_word):
    """
    input : 모해, words(비교할 대상이 담긴 word dataset)
    output : [{'못해': 0.3333333333333333}, {'오해': 0.3333333333333333}, {'묘해': 0.3333333333333333},
                {'뭐해': 0.3333333333333333}, {'모래': 0.3333333333333333}, {'토해': 0.3333333333333333}]
    input : 안녕
    output : [{'안녕': 0}]
    """
    #print("let's start with " + query)
    similars = [] # edit distance 및 유사한 단어 구하기
   # word dataset에 구하고자 하는 단어가 있는 경우
    similar = []
    distance = {word:jamo_levenshtein(word, query) for word in words}
    #print("distance: ")
    #print(distance)
    for key,value in distance.items():
      if value == 0:
        similars.append({query:0})
        break
      elif value<=0.4:
        similar.append({key:value})
        #print(key)
            
    if len(similar) == 0: # jamo_edit distance에서 유사한 단어를 구하지 못하면
      #print(words)
      distance = {word:levenshtein(word, query) for word in words} # edit_distance로 진행
      for key,value in distance.items():
        if value==1:
          similar.append({key:value})

    similars.append(similar)

    return similars[0]




def compare(edit_output, model_output, origin_word):
    """
    Compare outputs of model with edit_distance.
    input: edit_distance's output: [{'못해': 0.3333333333333333}, {'오해': 0.3333333333333333}, {'묘해': 0.3333333333333333},
            {'뭐해': 0.3333333333333333}, {'모래': 0.3333333333333333}, {'토해': 0.3333333333333333}]
            model's output: '뭐해'
    output: total output(model's output or edit_distance's output)
    """
    result=""
    if len(model_output)==0:
        result = edit_output
    elif len(edit_output) == 0:
        result = model
    else:
        for i in range(len(edit_output)):
            if edit_output[i].get(model_output): # model output이 edit_output에 존재하는 경우
                result += model_output
                break
        if result!=model_output:
            print("select mode: 1, 2, 3")
            a = input("")
            if a == "1":
                result = select_output_1(edit_output, model_output, origin_word)
            elif a == "2":
                result = select_output_2(edit_output, model_output, origin_word)
            else:
                result = select_output_3(edit_output, model_output, origin_word)
    return result


# 만약 model에서와 edit_distance에서의 output이 다르다면?
def select_output_1(edits, models, origin_word):
    """
    case 1) model의 것을 채택하기

    """
    # case 1
    return models

# 만약 model에서와 edit_distance에서의 output이 다르다면?
def select_output_2(edits, models, origin_word):
    """
    case 2) 모델에서 나온 output의 edit distance가 일정 수준 이하인 경우
    - edit distance와 모델 output간의 distance를 재차 구함 그래서 그 중 가장 좋은 걸로
        - 여기서 조차 같으면 그냥 다 보여주기…………….
        - {안녕, 앙뇽}

    """

    # case 2,3
    ## model의 edit distance 구하기
    edit_data = [k for i in range(len(edits)) for k in edits[i].keys()]

    # case 2
    ## step 1) model의 output과 original word의 edit distance 구하기
    jamo_levensht = []
    distance = {word:jamo_levenshtein(word, models) for word in edit_data}
    for key,value in distance.items():
      if value<=0.5:
        jamo_levensht.append({key:value})
    # 모델에서 나온 output의 edit distance가 일정 수준 이하인 경우
    if len(jamo_levenshtein)==0:
        output = edit_distance(models, edit_data)
        min_distance = 1
        min_index = 0
        for dis in [k for i in range(len(output)) for k in output[i].values()]:
            if min_distance > dis:
                min_distance = dis
                min_index = i
        if min_distance == 0:
            result = [k for i in range(len(output)) for k in output[i].values()][i]
        else:
            result = [k for i in range(len(output)) for k in output[i].values()]
    else:
        result = models

    return result
    
# 만약 model에서와 edit_distance에서의 output이 다르다면?
def select_output_3(edits, models, origin_word):
    """
    case 3) 모델에서 나온 output의 edit distance가 edit으로 구한 것보다 큰 경우
    - edit distance와 모델 output간의 distance를 재차 구함 그래서 그 중 가장 좋은 걸로
    - 같으면 모델로 따라가기
        - 여기서 조차 같으면 그냥 다 보여주기…………….
        - {안녕, 앙뇽}
    """
    # case 1
    result =  models

    # case 2,3
    ## model의 edit distance 구하기
    edit_data = [k for i in range(len(edits)) for k in edits[i].keys()]

    # case 3
    jamo_levensht = []
    distance = {word:jamo_levenshtein(word, models) for word in edit_data}
    for key,value in distance.items():
      if value<=0.5:
        jamo_levensht.append({key:value})
        
    models_min = min([jamo_levensht[i][1] for i in range(len(jamo_levensht))])
    edit_min = min([k for i in range(len(similars)) for k in similars[i].values()])
    # model에서 나온 output의 distance가 edit으로 나온 distance보다 크다면?
    if models_min > edit_min:
        #edit distance와 model output의 distance 구하기
        output = edit_distance(models, edit_data)
        if models in [k for i in range(len(output)) for k in output[i].keys()]:
            result = models
        else:
            result = [k for i in range(len(output)) for k in output[i].keys()]
    else:
        result = models


    return result