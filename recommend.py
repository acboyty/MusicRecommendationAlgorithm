import pandas as pd 

df = pd.read_csv('./datasets/music-list/data_5950.csv', encoding='GB18030')  # wrong with GB2312, GB2312 < GBK < GB18030
# print(f'df.shape: {df.shape}')
# print(df.head())
# print(df.tail())

lst2music = {}  # music list to musics
music2lst = {}  # music to music lists
for i in range(len(df)):
    music = df.iloc[i]['歌名']
    lst = df.iloc[i]['歌单名称']
    if lst not in lst2music:
        lst2music[lst] = {music}
    else:
        lst2music[lst].add(music)
    if music not in music2lst:
        music2lst[music] = {lst}
    else:
        music2lst[music].add(lst)
# print('刷题 看书 学习 工作 冥想:', lst2music['刷题 看书 学习 工作 冥想'])
# print('无人之岛（翻自 任然）:', music2lst['无人之岛（翻自 任然）'])
# print(f'length of lst2music: {len(lst2music)}, length of music2lst: {len(music2lst)}')


def lst_dist(lst1, lst2):
    '''
    calculate distance between 2 music lists
    '''
    cnt = len(lst1 & lst2)
    return 10 / (1 + cnt)  # the smaller, the similar

# print(lst_dist(lst2music['伤感翻唱版集合'], lst2music['又是一个睡不着的夜晚']))

def music_dist(music1, music2):
    '''
    calculate the distance between 2 musics
    '''
    cnt = len(music2lst[music1] & music2lst[music2])
    return 10 / (1 + cnt)  # the smaller, the similar

# print(music_dist('星河清梦', '繚 星'))

def most_similar_lst(lst):
    '''
    get the most similar music list
    '''
    cur_lst, cur_dist = [], 15
    for lst_ in lst2music.keys():
        temp_dist = lst_dist(lst, lst2music[lst_])
        if lst_ != lst and temp_dist < cur_dist:
            cur_lst = lst2music[lst_]
            cur_dist = temp_dist
    return cur_lst, cur_dist

# print(most_similar_lst(lst2music['刷题 看书 学习 工作 冥想']))

def most_similar_music(music):
    '''
    get the most similar music
    '''
    cur_music, cur_dist = '', 15
    for music_ in music2lst.keys():
        temp_dist = music_dist(music, music_)
        if music_ != music and temp_dist < cur_dist:
            cur_music = music_
            cur_dist = temp_dist
    return cur_music, cur_dist

# print(most_similar_music('无人之岛（翻自 任然）'))

def recommend(lst):
    '''
    recommend according to music list
    '''
    # User-based Collaborative Filtering
    UserCF = most_similar_lst(lst)[0] - lst

    # Item-based Collaborative Filtering
    ItemCF = []
    for music in lst:
        ItemCF.append(most_similar_music(music)[0])
    ItemCF = set(ItemCF) - lst
    
    return UserCF | ItemCF

print(recommend({'呼吸', '无人之岛（翻自 任然）', '水星记', '像鱼', '大鱼 - (动画电影《大鱼海棠》印象曲)', '千千阙歌(Live)', '心はいつもあなたのそばに Piano'}))
