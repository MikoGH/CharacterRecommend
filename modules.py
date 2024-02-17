import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

def count_cosine(df: pd.DataFrame, character):
    top = 20
    df_similarity = pd.DataFrame(columns=['#', 'Name', 'Similarity'], index=df.index)
    for i, elm in df.iterrows():
        df_similarity.loc[i, 'Name'] = df.loc[i,'Name']
        df_similarity.loc[i, 'Similarity'] = round(1 - cosine(df.loc[i, df.columns != 'Name'].values[1:], character[df.columns != 'Name'].values[1:]),4)
    df_similarity = df_similarity.sort_values(by='Similarity', ascending=False).iloc[1:top+1]
    df_similarity['#'] = [i for i in range(1,top+1)]
    return df_similarity

# df = pd.read_csv('Anime_Traits_Wide.csv')[:500]
# character = df.loc[2]
# df_similarity = count_cosine(df, character)
# print(df_similarity)

# place = 0
# for i, elm in df_similarity.iterrows():
#     place += 1
#     same_traits = []
#     chr1_traits = []
#     chr2_traits = []
#     for trait in df.columns:
#         if character[trait] == df[trait][i] == 1:
#             same_traits.append(trait)
#         if character[trait] == 1 and df[trait][i] == 0:
#             chr1_traits.append(trait)
#         if character[trait] == 0 and df[trait][i] == 1:
#             chr2_traits.append(trait)
#     print(str(place)+' '+df.loc[i,'Name']+':',*same_traits,'- - - - -\n',sep='\n')