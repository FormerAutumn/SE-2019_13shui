#!/usr/bin/env python
# coding: utf-8

# In[14]:


import heapq
from simple import *
from special import *
from GetWeight import *
import json


# In[15]:


hyper_n = 5
# #方块 *草花 &红心 $黑桃
suit = ['#','*','&','$']
suit_sa = { '#':0, '*':1 , '&':2, '$':3 }
number_sa = { 'A':14, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13 }


# In[16]:


def chg(x):
    nw = ['A', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return nw[x]


# In[17]:


class Hands():
    def __init__(self, card_sublist, weight):
        self.list = card_sublist.copy()
        self.weight = weight
    
    def __lt__(self, b):
        return self.weight <= b.weight


# In[18]:


def RecommendHands( card_list ):
    sz = len(card_list)
    q = []
    heapq.heapify(q)
    nw_hands = []
    #last O(n^5) using the brute force to enumerate the combination of the last hands
    for i in range(0,sz,1):
        nw_hands.append(card_list[i])
        for j in range(i+1,sz,1):
            nw_hands.append(card_list[j])
            for k in range(j+1,sz,1):
                nw_hands.append(card_list[k])
                for g in range(k+1,sz,1):
                    nw_hands.append(card_list[g])
                    for t in range(g+1,sz,1):
                        nw_hands.append(card_list[t])
                        _c = nw_hands; _w = get_weight(_c, 2)
                        heapq.heappush(q, Hands(_c, -_w))
                        if len(q) > hyper_n:
                            _ = heapq.heappop(q)
                        nw_hands.pop()
                    nw_hands.pop()
                nw_hands.pop()
            nw_hands.pop()
        nw_hands.pop()
    
    last_hands = []; middle_hands = []; header_hands = []
    while len(q)>0:
        last_hands.append(heapq.heappop(q))

    #last_hands = [ ([(1,1),(1,2),(1,3),(1,4),(1,5)],weight), (), (), ... () ].dtype = Hands([(),()],w)
    for _ in last_hands:
        #fir every last_hands choose the middle_hands and header_hands
        tp_card_list = card_list.copy()
        for i in _.list:
            for j in range(len(tp_card_list)):
                if tp_card_list[j] == i:
                    tp_card_list.pop(j)
                    break
        
        #now tp_card_list contain only 8 cards for middle and header
        sz = len(tp_card_list)
        for i in range(0,sz,1):
            nw_hands.append(tp_card_list[i])
            for j in range(i+1,sz,1):
                nw_hands.append(tp_card_list[j])
                for k in range(j+1,sz,1):
                    nw_hands.append(tp_card_list[k])
                    for g in range(k+1,sz,1):
                        nw_hands.append(tp_card_list[g])
                        for t in range(g+1,sz,1):
                            nw_hands.append(tp_card_list[t])
                            _c = nw_hands; _w = get_weight(_c, 1)
                            heapq.heappush(q, Hands(_c, -_w))
                            if len(q) > hyper_n:
                                _ = heapq.heappop(q)
                            nw_hands.pop()
                        nw_hands.pop()
                    nw_hands.pop()
                nw_hands.pop()
            nw_hands.pop()
        
        while len(q)>0:
            X = heapq.heappop(q)
            middle_hands.append(X)
            tp2_card_list = tp_card_list.copy()
            szz = len(middle_hands)
            for i in middle_hands[szz-1].list:
                for j in range(len(tp2_card_list)):
                    if i == tp2_card_list[j]:
                        tp2_card_list.pop(j)
                        break
            _c = tp2_card_list; _w = get_weight(tp2_card_list, 0)
            header_hands.append(Hands(_c, -_w))
    
    my_hands = []
    for lst in last_hands:
        for j in range(hyper_n):
            my_hands.append(  [(header_hands[j].list, header_hands[j].weight),
                               (middle_hands[j].list, middle_hands[j].weight),
                               (lst.list, lst.weight)] ) 
    return my_hands
    #middle O(n^5) using the brute force to enumrate the combination of the middle hands 
    #first the rest, no choise to choose


def get_battle():
    import http.client
    conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")
    headers = { 'x-auth-token': "c321f1b9-1a2c-43fd-b0f7-4c5af34eb605" }
    conn.request("POST", "/game/open", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data


# In[28]:


def decode_data(data):
    data_dict = json.loads(get_battle().decode('utf-8'))
    #print(data_dict)
    system_cards = data_dict["data"]["card"]
    nw_id = data_dict["data"]["id"]
    #print(system_cards)
    #print(nw_id)
    return (nw_id, system_cards)


# In[21]:


def my_choose(nw_id, _cards):
    chupai = RecommendHands(_cards)
    #print(len(chupai))
    _my_cards = []
    hyper_weight = [0.2, 0.3, 0.5]
    for i in chupai:
        tp_list = []
        tp_weight = 0.0
        for j in range(len(i)):
            tp_list += i[j][0]
            tp_weight += hyper_weight[j]*i[j][1]
        _my_cards.append((tp_list,-tp_weight))
    _my_cards.sort( key = lambda x : -x[1] )
    best_choose = _my_cards[0]
    #print(best_choose)
    my_header = best_choose[0][:3]
    my_middle = best_choose[0][3:8]
    my_last = best_choose[0][8:13]
    _my_hands_1 = []
    _my_hands_2 = []
    _my_hands_3 = []
    for i in my_header:
        _my_hands_1.append( suit[i[0]] + ''.join(chg(i[1])) )
    for i in my_middle:
        _my_hands_2.append( suit[i[0]] + ''.join(chg(i[1])) )
    for i in my_last:
        _my_hands_3.append( suit[i[0]] + ''.join(chg(i[1])) )
    #print(_my_hands_1); print(_my_hands_2); print(_my_hands_3)
    cards_set = {"id": nw_id, "card": [' '.join(_my_hands_1), ' '.join(_my_hands_2), ' '.join(_my_hands_3)]}
    #print(cards_set)
    return cards_set


# In[38]:


def send_2_system( card_set ):
    import http.client
    conn = http.client.HTTPSConnection("api.shisanshui.rtxux.xyz")
    payload = json.dumps(card_set)#"{\"id\":1000,\"card\":[\"*2 *3 *4\",\"*5 *6 *7 *8 *9\",\"*10 *J *Q *K *A\"]}"
    headers = {
        'content-type': "application/json",
        'x-auth-token': "c321f1b9-1a2c-43fd-b0f7-4c5af34eb605"
    }
    conn.request("POST", "/game/submit", payload, headers)
    res = conn.getresponse()
    #print(data.decode("utf-8"))


# In[35]:


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
    cards_set = my_choose(nw_id, _cards)
    send_2_system(cards_set)


# In[36]:


def main():
    T = 32
    while (T):
        T -= 1
        _start()


# In[37]:


main()


# In[ ]:




