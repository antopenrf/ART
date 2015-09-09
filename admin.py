import wx

## global fontsizes
gfontsizeS=7
gfontsize=9
gfontsizeL=11

## global font type
gfont_para = wx.FONTFAMILY_ROMAN  ## font for paramter descriptions




## color types
c_white=(255, 255, 255)
c_yellow=(255, 255, 200)
c_lightgreen=(230, 255, 222)
c_green=(0,255,0)
c_blue=(0,0,80)
c_lightblue=(192, 222, 255)
c_lightblue2=(132, 162, 255)
c_lighterblue=(212, 242, 255)
c_silver=(240,240,245)
c_silver1=(230,230,235)

# function to reverse the tags and values of the entered dictionary
def revdict(d):
    result={}
    for each in d:
        result[d[each]]=each
    return result
# function to locate the max among the items of the list
def maxinlist(alist):
    temp=alist[0]
    for x in alist[1:]:
        if x>temp:
            temp=x
    return temp
        
# function to locate the max among the items of the list
def mininlist(alist):
    temp=alist[0]
    for x in alist[1:]:
        if x<temp:
            temp=x
    return temp

# function to remove duplicated items of the entered list
def duplicateditem(alist):
    if len(alist)<2:
        return []
    else:
        duplicated=[]
        while len(alist)>=2:
            first=alist[0]
            m=1
            for each in alist[1:]:
                if each == first:
                    alist.remove(each)
                    if m==1: duplicated.append(first)
                    m+=1
            alist.remove(first)
        return duplicated
            
        
# function to make a list of single item            
def makelist(alist):
    if type(alist)==list:
        return alist
    else:
        return[alist]
