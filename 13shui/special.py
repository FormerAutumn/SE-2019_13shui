cardlist=[(1,3),(1,3),(1,3),(1,2),(1,4),(1,4),(1,4),(1,2),(1,5),(1,5),(1,5),(1,5),(1,6)]
def CouYiSe():
    if len(cardlist)!= 13:
        return 0
    record = [0]*4
    for card in cardlist:
        record[card[0]- 1]+=1
    if record[1] == 0 and record[2] == 0:
        return 1
    elif record[0] == 0 and record[3] == 0:
        return 1



def LiuDuiBan():
    if len(cardlist)!= 13:
        return 0
    record = [0]*13
    for card in cardlist:
        record[card[1]- 2]+=1
    count=0
    for i in record:
        if i==2:
            count+=1
    if count==6:
        return 1
    else:
        return 0



def QuanDa():
    if len(cardlist)!= 13:
        return 0
    for card in cardlist:
        if card[1]<8 :
            return 0
    return 1



def QuanXiao():
    if len(cardlist)!= 13:
        return 0
    for card in cardlist:
        if card[1]>8 :
            return 0
    return 1



def getSanList(numList):
    sanList = []
    for num1 in numList:
        num2 = num1 + 1
        num3 = num1 + 2
        ''' if num1 == 12:
            num3 = 1'''
        if num2 in numList and num3 in numList:
            san = []
            san.append(num1)
            san.append(num2)
            san.append(num3)
            if not san in sanList:
                sanList.append(san)
    return sanList
##判断10张片是否是两个5张顺子
def isWuShun(nList):
    wuList = []
    for num1 in nList:
        num2 = num1 + 1
        num3 = num1 + 2
        num4 = num1 + 3
        num5 = num1 + 4
        '''if num2==1:
            continue
        if num1 == 10:
            num5 = 1'''
        if num2 in nList and num3 in nList and num4 in nList and num5 in nList:
            tmpList = []
            tmpList.append(num1)
            tmpList.append(num2)
            tmpList.append(num3)
            tmpList.append(num4)
            tmpList.append(num5)
            if not tmpList in wuList:
                wuList.append(tmpList)

    for i in wuList:
        for j in wuList:
            tmpList = []
            tmpList += nList
            for ii in i:
                if ii in tmpList:
                    tmpList.remove(ii)
            for jj in j:
                if jj in tmpList:
                    tmpList.remove(jj)

            if not tmpList:
                return 1
    return 0
def SanShunZi():
    if len(cardlist) != 13:
        return 0
    numList = []
    for card in cardlist:
        numList.append(card[1])
    sanList = []
    sanList = getSanList(numList)

    for i in sanList:
        nList = []
        nList += numList  ## 删除三顺牌，剩余十张牌
        for j in i:
            nList.remove(j)
        if isWuShun(nList):
            return 1
    return 0



def SanTongHua():
    if len(cardlist)!= 13:
        return 0
    record = [0]*4
    for card in cardlist:
        record[card[0]- 1]+=1
    wu=0
    san=0
    ba=0
    shi=0
    for i in record:
        if i==5:
            wu+=1
        elif i==3:
            san+=1
        elif i==8:
            ba+=1
        elif i==10:
            shi+=1
    if (wu==2 and san==1)or(wu==1 and ba==1)or(shi==1 and san==1):
        return 1
    else:
        return 0



def SanTongHuaShun():
    if len(cardlist)!= 13:
        return 0
    record = [[],[],[],[]]
    for card in cardlist:
        record[card[0]- 1].append(card[1])
    wu=0
    san=0
    ba=0
    shi=0
    shisan=0
    for i in record:
        if len(i)==5:
            wu+=1
        elif len(i)==3:
            san+=1
        elif len(i)==8:
            ba+=1
        elif len(i)==10:
            shi+=1
        elif len(i)==13:
            shisan+=1
    if (wu==2 and san==1)or(wu==1 and ba==1)or(shi==1 and san==1)or shisan==1:
        for i in record:
            if i:
                i.sort()
                for j in range(len(i)-1):
                    if i[j+1]-i[j]!=1:
                        return 0
        return 1
    else:
        return 0



def SanZhaDan():
    if len(cardlist)!= 13:
        return 0
    record = [0]*13
    for card in cardlist:
        record[card[1]- 2]+=1
    si=0
    for i in record:
        if i==4:
            si+=1
    if si==3:
        return 1
    else:
        return 0



def ShiErHuangZu():
    if len(cardlist)!= 13:
        return 0
    record = [0]*13
    for card in cardlist:
        record[card[1]- 2]+=1
    huangzu=0
    for i in record:
        if i>=11:
            huangzu+=1
    if huangzu>=12:
        return 1
    else:
        return 0



def SiTaoSanTiao():
    if len(cardlist)!= 13:
        return 0
    record = [0]*13
    for card in cardlist:
        record[card[1]- 2]+=1
    santiao=0
    zhadan=0
    for i in record:
        if i==3:
            santiao+=1
        elif i==4:
            zhadan+=1
    if santiao==4 or (santiao==3 and zhadan==1):
        return 1
    else:
        return 0



def ShuangGuaiChongSan():
    if len(cardlist)!= 13:
        return 0
    record = [0]*13
    for card in cardlist:
        record[card[1]- 2]+=1
    dui=0
    santiao=0
    zhadan=0
    for i in record:
        if i==2:
            dui+=1
        elif i==3:
            santiao+=1
        elif i==4:
            zhadan+=1
    if (dui==3 and santiao==2)or(dui==2 and santiao==3)or(dui==3 and santiao==1 and zhadan==1)or(dui==1 and santiao==2 and zhadan==1):
        return 1
    else:
        return 0


def WuDuiChongSan():
    if len(cardlist)!= 13:
        return 0
    record = [0]*13
    for card in cardlist:
        record[card[1]- 2]+=1
    dui=0
    santiao=0
    for i in record:
        if i==2:
            dui+=1
        elif i==3:
            santiao+=1
    if dui==5 and santiao==1:
        return 1
    else:
        return 0



def YiTiaoLong():
    i=[]
    for card in cardlist:
        i.append(card[1])
    i.sort()
    for j in range(len(i) - 1):
        if i[j + 1] - i[j] != 1:
            return 0
    return 1



def ZhiZhunQingLong():
    if CouYiSe() and YiTiaoLong():
        return 1
    else:
        return 0



"""
print("CouYiSe()=",CouYiSe(),"\nLiuDuiBan()=",LiuDuiBan(),"\nQuanDa()=",QuanDa(),"\nQuanXiao()=",QuanXiao(),"\nSanShunZi()=",SanShunZi(),
      "\nSanTongHua()=",SanTongHua(),"\nSanTongHuaShun()=",SanTongHuaShun(),"\nSanZhaDan()=",SanZhaDan(),"\nShiErHuangZu()=",ShiErHuangZu(),"\nSiTaoSanTiao()=",SiTaoSanTiao(),
      "\nShuangGuaiChongSan=",ShuangGuaiChongSan(),"\nWuDuiChongSan()=",WuDuiChongSan(),"\nYiTiaoLong()=",YiTiaoLong(),"\nZhiZhunQingLong()=",ZhiZhunQingLong())
"""
