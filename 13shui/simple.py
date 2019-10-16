#!/usr/bin/env python
# coding: utf-8

# In[20]:


import numpy as np


# In[15]:
hyper_n = 20


class Card():
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
    
    def get_suit(self):
        return self.suit
    def get_number(self):
        return self.number
    def ToDict(self):
        return {'suit':self.suit, 'number':self.number}


# In[26]:


#first->suit second->number


# In[27]:


# In[5]:


def jdg_pair( card_list ):
    ct = np.zeros(hyper_n)
    for i in card_list:
        ct[i[1]] += 1
    _ = np.where(ct==2)
    indxs = [j for i in _ for j in i]
    if ( len(indxs) != 1 ):
        return -1
    else:
        return indxs[0]


def jdg_2pairs( card_list ):
    ct = np.zeros(hyper_n)
    for i in card_list:
        ct[i[1]] += 1
    _ = np.where(ct==2)
    indxs = [j for i in _ for j in i]
    if ( len(indxs)!=2 ):
        return -1
    else:
        return (indxs[0], indxs[1])
# In[4]:


def jdg_triple( card_list ):
    ct = np.zeros(hyper_n)
    for i in card_list:
        ct[i[1]] += 1
    _ = np.where(ct==3)
    indxs = [j for i in _ for j in i]
    if ( len(indxs) > 0 ):
        return indxs[0]
    else:
        return -1


# In[2]:


def jdg_boom( card_list ):
    ct = np.zeros(hyper_n)
    for i in card_list:
        ct[i[1]] += 1
    _ = np.where(ct==4)
    indxs = [j for i in _ for j in i]
    booms = []
    for i in indxs:
        for j in card_list:
            if j[1] == i:
                booms.append(j)
    if len(booms)>0:
        return booms
    else:
        return -1


# In[84]:


def jdg_straight( card_list ):
    ct = np.zeros(4)
    cards = []
    for i in card_list:
        ct[i[0]] += 1
        cards.append(i[1])
        if i == 1:
            return (0,0)
    th_flg = 0
    if ct[card_list[0][0]] == len(card_list):
        th_flg = 1
    cards.sort()
    for i in range(0,len(cards)-1,1):
        if (cards[i]+1 != cards[i+1]):
            return (th_flg,0,0)
    return (th_flg,1,cards[0])


# In[2]:


def jdg_flush( card_list ):
    ct = np.zeros(4)
    for i in card_list:
        ct[i[0]] += 1
    cards = []
    for i in range(len(ct)):
        if ct[i] == 5:
            for j in card_list:
                if j[1] == i:
                    cards.append(j)
    if len(cards)>0:
        return cards
    else:
        return -1


# In[1]:


def jdg_fullhouse( card_list ):
    pairs = jdg_pair(card_list)
    triples = jdg_triple(card_list)
    if ( pairs == -1 or triples == -1 ):
        return -1
    else:
        return (triples, pairs)


# In[ ]:

#同花顺 > 炸弹 > 葫芦 > 同花 > 顺子 > 三条 > 二对 > 一对 > 散牌


