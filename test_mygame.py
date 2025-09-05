from mygame import rotate, merge_row

def test_rotate_cw90():
    map = [[1, 2, 3],[4, 5, 6],[7, 8, 9 ]]

    m = list(zip(*map[::-1])) # CW회전
    assert m[0] == (7, 4, 1)
    assert m[1] == (8, 5, 2)
    assert m[2] == (9, 6, 3)

def test_rotate_ccw90():
    map = [[1, 2, 3],[4, 5, 6],[7, 8, 9 ]]

    m = list(zip(*map))[::-1]
    assert m[0]  == (3, 6, 9)
    assert m[1]  == (2, 5, 8)
    assert m[2]  == (1, 4, 7)

def test_rotate_func():
    map = [[1, 2, 3],[4, 5, 6],[7, 8, 9 ]]

    # CW90 회전
    m = rotate(True,map) # CW회전
    assert m[0] == [7, 4, 1]
    assert m[1] == [8, 5, 2]
    assert m[2] == [9, 6, 3]

    # CCW90 회전
    m = rotate(False,map) 
    assert m[0]  == [3, 6, 9]
    assert m[1]  == [2, 5, 8]
    assert m[2]  == [1, 4, 7]

def test_merge_row():
    l = [1, 2, 3, 4]
    nl = merge_row(l) 
    assert nl == [1, 2, 3, 4]

    l = [2, 2, 4, 3]
    nl = merge_row(l) 
    assert nl == [4, 4, 3, 0]

    l = [0, 2, 2, 0]
    nl = merge_row(l) 
    assert nl == [4, 0, 0, 0]