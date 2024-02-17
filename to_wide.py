import pandas as pd
import numpy as np


def remove_rare(dct):
    to_remove = []
    for elm in dct.keys():
        if dct[elm] < 30:
            to_remove.append(elm)
    for elm in to_remove:
        dct.pop(elm)
    return dct

def get_params(df):
    tags = dict()
    genders = dict()
    hair_colors = dict()

    for i, row in df.iterrows():
        # Genders
        if not(pd.isnull(row['Gender'])):
            if row['Gender'] in genders:
                genders[row['Gender']] += 1
            else:
                genders.update({row['Gender'] : 1})
        # Hair Colors  
        if not(pd.isnull(row['Hair_Color'])):
            if row['Hair_Color'] in hair_colors:
                hair_colors[row['Hair_Color']] += 1
            else:
                hair_colors.update({row['Hair_Color'] : 1})
        # Tags
        row_tags = str(row.loc['Tags'])[1:-1].split(",")
        for j in range(len(row_tags)):
            row_tags[j] = row_tags[j].strip("' ")   
            if not(pd.isnull(row_tags[j])): 
                if row_tags[j] in tags:
                    tags[row_tags[j]] += 1
                else:
                    tags.update({row_tags[j] : 1})


    genders = remove_rare(genders)
    hair_colors = remove_rare(hair_colors)
    tags = remove_rare(tags)

    return genders, hair_colors, tags

def to_wide_csv(df, genders, hair_colors, tags):
    columns = ['Name', 'Anime'] + list(genders.keys()) + list(hair_colors.keys()) + list(tags.keys())
    df_wide = pd.DataFrame(columns=columns)
    ind = 0

    for i, row in df.iterrows():
        row_tags = str(row.loc['Tags'])[1:-1].split(",")
        row_animes = str(row.loc['Anime'])[1:-1].split(",")
        # Tags
        row_tags.insert(0, str(df.loc[i, 'Hair_Color']))
        row_tags.insert(0, str(df.loc[i, 'Gender']))
        j = 0
        while j < len(row_tags):
            row_tags[j] = row_tags[j].strip("' ").replace('|','')
            if not(row_tags[j] in df_wide.columns):
                row_tags.pop(j)
            else:
                j += 1
        if len(row_tags) >= 4:
            ind += 1
            df_wide = pd.concat([df_wide, pd.DataFrame([[0]*df_wide.shape[1]], columns = df_wide.columns, index = [i])])
            # Name
            df_wide.loc[i, 'Name'] = df.loc[i, 'Names']
            # Anime
            if len(row_animes) > 0:
                df_wide.loc[i, 'Anime'] = sorted(row_animes, key=lambda x: len(x))[0].strip("'\" ")
            # Tags list
            # df_wide.loc[i, 'Tags'] = '|'.join(row_tags)
            # Tags wide
            for j in range(len(row_tags)):
                df_wide.loc[i, row_tags[j]] = 1 

            if ind*100//len(df) % 10 == 0 and (ind-1)*100//len(df) % 10 != 0:
                print(ind*100//len(df))
    # df_wide.to_csv('Anime_Traits_Wide.csv')
    df_wide.to_csv('Anime_Traits_Wide.csv', mode='a', header=False)


df = pd.read_csv('Anime_Traits.csv')[:]
df = df.dropna(subset=['Names','Tags','Anime'])
genders, hair_colors, tags = get_params(df)
# print(len(df), len(genders), len(hair_colors), len(tags))
# print(genders)
# print(hair_colors)
# print(tags)
df = df.loc[10001:25000]
to_wide_csv(df, genders, hair_colors, tags)

