import pandas as pd

def get_music_lists():
    """
    Build connection with MySQL database and get data
    """

    # DbHandle = DataBaseHandle('127.0.0.1','root','68691102','recommend',3306)  # initialization
    # music_lists = DbHandle.selectDb('select * from allsong')
    # DbHandle.closeDb()

    df = pd.read_csv('./datasets/music-list/data_5950.csv', encoding='GB18030')
    music_lists = []
    for i in range(len(df)):
        music_lists.append(tuple(df.iloc[i]))
    music_lists = tuple(music_lists)

    # Data format:
    # (('music','','','','list'),('','','','',''),...,('','','','',''))

    lst2music = {}  # music list to musics
    music2lst = {}  # music to music lists
    for x in music_lists:
        music = x[0]
        lst = x[4]
        if lst not in lst2music:
            lst2music[lst] = {music}
        else:
            lst2music[lst].add(music)
        if music not in music2lst:
            music2lst[music] = {lst}
        else:
            music2lst[music].add(lst)

    return lst2music, music2lst
