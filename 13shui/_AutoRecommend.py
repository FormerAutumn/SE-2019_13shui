#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import time
import json
import heapq
from simple import *
from GetWeight import *


# In[2]:


# #方块 *草花 &红心 $黑桃
suit = ['#','*','&','$']
suit_sa = { '#':0, '*':1 , '&':2, '$':3 }
number_sa = { 'A':14, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13 }

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

def chg(x):
    nw = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return nw[x]


# In[3]:


class HandCard():
    def __init__(self, sublist, weight):
        self.list = sublist
        self.weight = weight
    def __lt__(self, a):
        return self.weight <= a.weight


# In[4]:


def jdg_ordered(card_list, mode):
    ned = [1]
    for i in range(1,20):
        ned.append(2*ned[i-1])
        
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
        return (ned[18], ret[2], sm/sz)
    
    #boom
    ret = jdg_boom(nw_cards)
    if ( ret != -1 ):
        return (ned[17], ret[0][1], four_of_a_kind[mode][ret[0][1]-1])
    
    #hulu
    ret = jdg_fullhouse(nw_cards)
    if ( ret != -1 ):
        return (ned[16], ret[0], full_house[mode][ret[0]-1] + full_house[mode][ret[1]-1]/sz)

    #flush
    ret = jdg_flush(nw_cards)
    if ( ret != -1 ):
        return (ned[15], np.array(ret).max(), flush[mode][np.array(ret).max()-1])
    
    #straight
    ret = jdg_straight(nw_cards)
    if ( ret[1] != 0 ):
        return (ned[14], ret[2], np.array(straight[mode][ret[2]-1:ret[2]-1+sz]).sum()/sz)

    #triple
    ret = jdg_triple(nw_cards)
    if ( ret != -1 ):
        sm = triple[mode][ret-1]*3
        for i in nw_cards:
            if ( i[1] != ret ):
                sm += junk[mode][i[1]-1]
        return (ned[12], ret, sm/sz)
    
    #2 pairs
    ret = jdg_2pairs(nw_cards)
    if ( ret != -1 ):
        sm = two_pair[mode][ret[0]-1]*2 + two_pair[mode][ret[1]-1]*2
        for i in nw_cards:
            if ( i[1] != ret[0] and i[1] != ret[1] ):
                sm += junk[mode][i[1]-1]
                break
        return (ned[11], ret[1], sm/sz)
    
    #pair
    ret = jdg_pair(nw_cards)
    if ( ret != -1 ):
        sm = one_pair[mode][ret-1]*2
        for i in nw_cards:
            if ( i[1] != ret ):
                sm += junk[mode][i[1]-1]
        return (ned[10], ret, sm/sz)

    #junk
    sm = 0.0
    for i in nw_cards:
        sm += junk[mode][i[1]-1]
    return (ned[9], np.array(nw_cards).max(), sm/sz)


# In[5]:


##同花顺(18) > 炸弹(17) > 葫芦(16) > 同花(15) > 顺子(14) > 三条(12) > 二对(11) > 一对(10) > 散牌(9)
def chk_ordered(st, nd, rd):
    retst = jdg_ordered(st, 0)
    retnd = jdg_ordered(nd, 1)
    retrd = jdg_ordered(rd, 2)
    if ( (retst[0] > retnd[0]) or (retst[0] > retrd[0]) or (retnd[0] > retrd[0]) ):
        return (0,0)
    elif ( (retst[0]==retnd[0] and retst[1] > retnd[1]) ):
        return (0,0)
    elif ( (retst[0]==retrd[0] and retst[1] > retrd[1]) ):
        return (0,0)
    elif ( (retnd[0]==retrd[0] and retnd[1] > retrd[1]) ):
        return (0,0)
    else:
        return (1, (np.array([retst[2], retnd[2], retrd[2]])*np.array([0.2, 0.3, 0.5])).sum())


# In[102]:


def get_battle():
    import http.client
    conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")
    headers = { 'x-auth-token': "b1d7d1b0-0512-42c9-9c08-b718228fb5ec" }
    conn.request("POST", "/game/open", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data


# In[92]:


def decode_data(data):
    data_dict = json.loads(get_battle().decode('utf-8'))
    #print(data_dict)
    system_cards = data_dict["data"]["card"]
    nw_id = data_dict["data"]["id"]
    #print(system_cards, nw_id)
    return (nw_id, system_cards)


# In[103]:


def send_2_system( card_set ):
    import http.client
    conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")
    payload = json.dumps(card_set)#"{\"id\":1000,\"card\":[\"*2 *3 *4\",\"*5 *6 *7 *8 *9\",\"*10 *J *Q *K *A\"]}"
    headers = {
        'content-type': "application/json",
        'x-auth-token': "b1d7d1b0-0512-42c9-9c08-b718228fb5ec"
    }
    conn.request("POST", "/game/submit", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


# In[80]:


def pattern_search(cards):
    tp_cards = cards.copy()
    tp_cards.sort(key=lambda x:x[1])
    #print("original cards ", tp_cards)

    ct = np.zeros(15); ctf = np.zeros(4)
    for x, y in tp_cards:
        ctf[x] += 1
        ct[y] += 1

    _flushs = [ j for i in np.where(ctf==5) for j in i ]
    flushs = []
    for i in _flushs:
        tp = []
        for x, y in tp_cards:
            if ( x == i ):
                tp.append((x,y))
        flushs.append(tp)

    _junks = [ j for i in np.where(ct>=1) for j in i ]#; print(_junks)
    junks = []
    for i in _junks:
        for x, y in tp_cards:
            if ( y == i ):
                junks.append([(x,y)])
    junks.sort(key=lambda x:-x[0][1])

    _pairs = [ j for i in np.where(ct==2) for j in i ]#; print(_pairs)
    pairs = []
    for i in _pairs:
        tp = []
        for x, y in tp_cards:
            if ( y == i ):
                tp.append((x,y))
        pairs.append(tp)
    pairs.sort(key=lambda x:-x[0][1])
    #print(pairs)

    _triples = [ j for i in np.where(ct==3) for j in i ]#; print(_triples)
    triples = []
    for i in _triples:
        tp = []
        for x, y in tp_cards:
            if ( y == i ):
                tp.append((x,y))
        triples.append(tp)
    triples.sort(key=lambda x:-x[0][1])
    #print(triples)

    _booms = [ j for i in np.where(ct==4) for j in i ]#; print(_booms)
    booms = []
    for i in _booms:
        tp = []
        for x, y in tp_cards:
            if ( y == i ):
                tp.append((x,y))
        booms.append(tp)
    booms.sort(key=lambda x:-x[0][1])
    #print(booms)

    _straights = []; straights = []
    for i in range(len(ct)):
        ctt = ct.copy()
        while ( (ct[i] > 0) and (i < 11) ):
            flg = 1
            for j in range(2,6):
                if ( ctt[j] == 0 ):
                    flg = 0; break
                else:
                    ctt[j]
            if ( flg ):
                tp = []
                for j in range(i,i+5):
                    ct[j] -= 1
                    for k, t in tp_cards:
                        if ( t == j ):
                            tp.append((k,t))
                straights.append(tp)
            else:
                break
        ct = ctt.copy()
    straights.sort(key=lambda x:-x[0][1])
    #print(ct)

    #type [[(x,y),..,()],[(),..,()]]
    _2_pairs = []
    for i in range(len(pairs)):
        for j in range(i+1,len(pairs)):
            a, b, c, d = pairs[i][0], pairs[i][1], pairs[j][0], pairs[j][1]
            _2_pairs.append([a,b,c,d])

    _32_tps = []
    for i in range(len(triples)):
        for j in range(len(pairs)):
            a, b, c, d, e = triples[i][0], triples[i][1], triples[i][2], pairs[j][0], pairs[j][1]
            _32_tps.append([a,b,c,d,e])
        
    #junks pairs triples booms straights flush _2_pairs _32_tp
    #print("junks ", junks); print("pairs ", pairs); print("triples ", triples);
    #print("booms ", booms); print("straights ", straights);
    #print("flushs ", flush); print("_2_pairs ", _2_pairs); print("_32_tps ", _32_tps)
    return junks, pairs, triples, booms, straights, flushs, _2_pairs, _32_tps


# In[89]:


#同花顺 > 炸弹 > 葫芦 > 同花 > 顺子 > 三条 > 二对 > 一对 > 散牌
def AutoRecommend(tp_cards, junks, pairs, triples, booms, straights, flushs, _2_pairs, _32_tps):
    _third  = booms + _32_tps + flushs + straights + triples + _2_pairs + pairs + junks
    _second = booms + _32_tps + flushs + straights + triples + _2_pairs + pairs + junks
    _first  = triples + pairs + junks
    nw_cards = tp_cards.copy()
    nw_cards.sort(key=lambda x:-x[1])
    #print("nw_cards = ", nw_cards)
    q = []
    hyper_n = 20
    my_weight = [1/3, 1/3, 1/3]
    heapq.heapify(q)

    for i in _third:
    
        #print("i = ",i)
        nwcs = nw_cards.copy()
        #print("nwcs0 ", nwcs)
    
        tail = i.copy()
        for ii in tail:
            nwcs.remove(ii)
    
        tp_nwcs0 = nwcs.copy()
        #print("nwcs after ii ", nwcs)
        tp_tail = tail.copy()
        for j in _second:
            nwcs = tp_nwcs0.copy()
            #print("j = ",j)
            tail = tp_tail.copy()
            mid = j.copy()
            flg = 1
            for jj in mid:
                if ( jj in nwcs ):
                    nwcs.remove(jj)
                else:
                    flg = 0
                    break
            if ( flg == 0 ):
                continue
            
            tp_nwcs1 = nwcs.copy()
            #print("nwcs = ", nwcs)
            #print("nwcs after jj ", nwcs)
            tp_mid = mid.copy()
            for k in _first:
                nwcs = tp_nwcs1.copy()
                #print("k = ",k)
                tail = tp_tail.copy()
                mid = tp_mid.copy()
                head = k.copy()
                flg = 1
                for kk in head:
                    if ( kk in nwcs):
                        nwcs.remove(kk)
                    else:
                        flg = 0
                        break
                if ( flg == 0 ):
                    continue
                
                #print("nwcs the rest ", nwcs)
                #print("nw_cards_0 = ", head, mid, tail)
                #complete the head

                #print(head); print(mid); print(tail)
                
                tpp = nw_cards.copy()
                #print("tpp = ", tpp)
                for hd in head:
                    tpp.remove(hd)
                for mi in mid:
                    tpp.remove(mi)
                for tl in tail:
                    tpp.remove(tl)
                
                pos = 0
                while ( pos < len(tpp) ):
                    if ( len(head) < 3 and pos < len(tpp) ):
                        head.append(tpp[pos])
                        pos += 1
                    if ( len(mid) < 5 and pos < len(tpp) ):
                        mid.append(tpp[pos])
                        pos += 1
                    if ( len(tail) < 5 and pos < len(tpp) ):
                        tail.append(tpp[pos])
                        pos += 1
            
                w_h, w_m, w_t = get_weight(head,0), get_weight(mid,1), get_weight(tail,2)
                nw_w = (np.array([w_h,w_m,w_t])*np.array(my_weight)).sum()
                #print("nw_cards_1 = ", head, mid, tail)
                chk_val = chk_ordered(head, mid, tail)
                if ( chk_val[0] == 1 ):
                    if ( len(q) < hyper_n ):
                        heapq.heappush(q,HandCard(head+mid+tail, nw_w))
                    else:
                        if ( nw_w > q[0].weight ):
                            heapq.heappushpop(q, HandCard(head+mid+tail, nw_w))

    result_cards = []
    while ( len(q) > 0 ):
        result_cards.append(heapq.heappop(q))
    ret = result_cards[len(result_cards)-1].list
    return ret


# In[11]:


def _start():
    data = get_battle()
    decoded_data = decode_data(data)
    system_cards = decoded_data[1].split()
    nw_id = decoded_data[0]
    #print(system_cards)
    _cards = []
    for i in system_cards:
        x, y = suit_sa[i[0]], number_sa[i[1:len(i)]]
        _cards.append((x,y))
    #print(_cards)
    junks, pairs, triples, booms, straights, flushs, _2_pairs, _32_tps = pattern_search(_cards)
    cards_set = AutoRecommend( _cards,junks, pairs, triples, booms, straights, flushs, _2_pairs, _32_tps)
    encode_cards = []
    for x, y in cards_set:
        encode_cards.append(suit[x]+chg(y))
    send_cards_set = {"id":nw_id, "card":[' '.join(encode_cards[:3]), ' '.join(encode_cards[3:8]), ' '.join(encode_cards[8:13])]}
    print(send_cards_set)
    send_2_system(send_cards_set)


# In[104]:


import time
T = 10
while ( T ):
    start = time.time()
    _start()
    T -= 1
    print("time: %.2f secs" % (time.time()-start))


# In[ ]:




