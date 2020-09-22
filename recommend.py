from getMusicLists import get_music_lists
import CollaborativeFiltering
import MatrixDecomposition

lst2music, music2lst = get_music_lists()

def recommend(music_list):
    music_list = music_list & music2lst.keys()

    # CF
    CF = CollaborativeFiltering.recommend(music_list)
    # Matrix
    Matrix = MatrixDecomposition.recommend(music_list)
    
    print('CF:', CF, '\n')
    print('Matrix:', Matrix, '\n')
    ret = CF | Matrix
    return ret

print('Hybrid:', recommend({'呼吸', '无人之岛（翻自 任然）', '水星记', '像鱼', '大鱼 - (动画电影《大鱼海棠》印象曲)',
           '千千阙歌(Live)', '心はいつもあなたのそばに Piano'}))