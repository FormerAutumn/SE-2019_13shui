#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from simple import *


# In[2]:


hyper_n = 5
# #方块 *草花 &红心 $黑桃
suit = ['#','*','&','$']
suit_sa = { '#':0, '*':1 , '&':2, '$':3 }
number_sa = { 'A':14, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13 }


# In[3]:


junk = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   JUNK
    [  0,  0,  0,  0,  0,  0,  1,  1,  2,  2,  4,  7, 14, 33 ],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1 ],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ]
]

one_pair = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   PAIR
    [  0, 46, 48, 50, 51, 54, 56, 60, 63, 68, 74, 81, 89, 97 ],
    [  0,  2,  3,  4,  4,  5,  7,  8, 10, 12, 15, 19, 24, 33 ],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  2,  3 ]
]

two_pair = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   TWO_PAIRS
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [  0,  0, 36, 37, 38, 40, 44, 46, 49, 54, 57, 62, 64,  0 ],
    [  0,  0,  2,  3,  4,  4,  6,  7,  8, 10, 11, 13, 13,  0 ]
]

triple = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   TRIPLE
    [  0, 99, 99,100,100,100,100,100,100,100,100,100,100,100 ],
    [  0, 63, 65, 69, 71, 72, 73, 73, 73, 74, 74, 75, 75, 75 ],
    [  0, 11, 12, 14, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15 ]
]

straight = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   STRAIGHT
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [  0,  0,  0,  0, 77, 78, 81, 83, 85, 87, 88, 90, 91, 92 ],
    [  0,  0,  0,  0, 16, 17, 20, 22, 24, 26, 28, 32, 33, 36 ]
]

flush = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   FLUSH
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [  0,  0,  0,  0,  0,  0, 93, 93, 93, 93, 94, 95, 97, 98 ],
    [  0,  0,  0,  0,  0,  0, 36, 36, 37, 38, 40, 44, 49, 61 ]
]

full_house = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   FULL_HOUSE
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [  0, 98, 98, 99, 99, 99,100,100,100,100,100,100,100,100 ],
    [  0, 64, 67, 70, 71, 73, 75, 77, 80, 82, 85, 88, 91, 94 ]
]

four_of_a_kind = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   FOUR_OF_A_KIND
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [  0,100,100,100,100,100,100,100,100,100,100,100,100,100 ],
    [  0, 93, 94, 95, 95, 96, 96, 96, 97, 97, 98, 98, 98, 98 ]
]

straight_flush = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   STRAIGHT_FLUSH
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [  0,  0,  0,  0,100,100,100,100,100,100,100,100,100,  0 ],
    [  0,  0,  0,  0, 98, 98, 99, 99, 99, 99, 99, 99,100,  0 ]
]

royal_flush = [
    #  1   2   3   4   5   6   7   8   9   T   J   Q   K   A   ROYAL_FLUSH
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0 ],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,100 ],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,100 ]
]


# In[9]:


#mode = 0(header) 1(middle) 2(last)
def get_weight( card_list, mode ):
    nw_cards = card_list.copy()
    sz = len(card_list)
    #straight_flush
    ret = jdg_straight(nw_cards) #(flush, straight, first_number)
    if ( ret[0] and ret[1] ):
        sm = 0.0
        for i in range(len(straight_flush[mode])):
            for j in card_list:
                if j[1]-1 == i:
                    sm += straight_flush[mode][i]
                    break
        return sm/sz
    
    #boom
    ret = jdg_boom(nw_cards)
    if ( ret != -1 ):
        return four_of_a_kind[mode][ret[0][1]-1]
    
    #hulu
    ret = jdg_fullhouse(nw_cards)
    if ( ret != -1 ):
        return (full_house[mode][ret[0]-1] + full_house[mode][ret[1]-1])/sz

    #flush
    ret = jdg_flush(nw_cards)
    if ( ret != -1 ):
        return flush[mode][ret[0][1]-1]
    
    #straight
    ret = jdg_straight(nw_cards)
    if ( ret[1] != 0 ):
        return np.array(straight[mode][ret[2]-1:ret[2]-1+sz]).sum()/sz

    #triple
    ret = jdg_triple(nw_cards)
    if ( ret != -1 ):
        sm = triple[mode][ret-1]*3
        for i in nw_cards:
            if ( i[1] != ret ):
                sm += junk[mode][i[1]-1]
        return sm/sz
    
    #2 pairs
    ret = jdg_2pairs(nw_cards)
    if ( ret != -1 ):
        sm = two_pair[mode][ret[0]-1]*2 + two_pair[mode][ret[1]-1]*2
        for i in nw_cards:
            if ( i[1] != ret[0] and i[1] != ret[1] ):
                sm += junk[mode][i[1]-1]
                break
        return sm/sz 
    #pair
    ret = jdg_pair(nw_cards)
    if ( ret != -1 ):
        sm = one_pair[mode][ret-1]*2
        for i in nw_cards:
            if ( i[1] != ret ):
                sm += junk[mode][i[1]-1]
        return sm/sz

    #junk
    sm = 0.0
    for i in nw_cards:
        sm += junk[mode][i[1]-1]
    return sm/sz


# In[5]:

"""
system_cards =  "*2 *3 *4 *5 *6 *7 *8 *9 *10 *J *Q *K *A"
system_cards = system_cards.split()
print(system_cards)
_cards = []
for i in system_cards:
    x, y = suit_sa[i[0]], number_sa[i[1:len(i)]]
    _cards.append((x,y))
print(_cards)
"""

# In[6]:

"""
header = _cards[:3]
middle = _cards[3:8]
last = _cards[8:13]
print(header); print(middle); print(last)


# In[7]:


#同花顺 > 炸弹 > 葫芦 > 同花 > 顺子 > 三条 > 二对 > 一对 > 散牌


# In[10]:


print(get_weight(header,0))
print(get_weight(middle,1))
print(get_weight(last,2))
"""

# In[ ]:




