import numpy as np

# constants
CARD_VALUE = {1:'2', 2:'3', 3:'4', 4:'5', 5:'6', 6:'7', 7:'8',
              8:'9', 9:'t', 10:'j', 11:'q', 12:'k', 13:'a'}    
HCP = {'a':4, 'k':3, 'q':2, 'j':1}
PACK  = list(range(1, 53))
MAX_ITERATIONS = 100000
H1toH4 = set([0,1,2,3])
# end constants

# globals
shuffled_pack = list()
# end globals



def combo_match(c, hx, hy):
    """
        c   partnership criteria
        hx  hand x meta ([ns,nh,nd,nc],[hcpTotal,hcpS, hcpH, hcpD, hcpC])
        hy  hand x meta ([ns,nh,nd,nc],[hcpTotal,hcpS, hcpH, hcpD, hcpC])

       returns true if match found else false  
    """
    item = ([sum(x) for x in zip(*[hx[0],hy[0]])], [sum(x) for x in zip(*[hx[1],hy[1]])]) 
    return hand_match(c, item)
        

def ps(ms, ps_criteria):
    """
       ms   meta_sol "row"
       return ((index_x, index_y), (index_oppoA, index_oppoB )) if partnership match else false
    """
    a,b,c,d = ms
    # ab
    if combo_match(ps_criteria, a,b):
        return ((0,1),(2,3))
    if combo_match(ps_criteria, a,c):
        return ((0,2),(1,3))
    if combo_match(ps_criteria, a,d):
        return ((0,3),(1,2))
    if combo_match(ps_criteria, b,c):
        return ((1,2),(0,3))
    if combo_match(ps_criteria, b,d):
        return ((1,3),(0,2))
    if combo_match(ps_criteria, c,d):
        return ((2,3),(0,1))
    return False


def criteria_set(criteria):
    if len(list(filter(lambda x: x == 'x', criteria['hcp']))) != 5 or \
       len(list(filter(lambda x: x == 'x', criteria['suit']))) != 4:  
        return True
    return False



def fail(criteria, actual):
    if actual >= criteria[0] and actual <= criteria[1]:
        return False
    return True

def hand_match(c, h):
    """
       c criteria
       h hand

       c = {hcp: [(minTotal, maxTotal), s, h, d, c]
            suit:[(minS, maxS), h, d, c]

       h[0] ==> suit
       h[1] ==> hcp

       returns true if match found else false  
    """
    # hcp
    if c['hcp'][0] != 'x':
        # hcpTotal
        if fail(c['hcp'][0], h[1][0]):
            return False
    if c['hcp'][1] != 'x':
        # hcpSpade
        if fail(c['hcp'][1], h[1][1]):
            return False
    if c['hcp'][2] != 'x':
        # hcpHeart
        if fail(c['hcp'][2], h[1][2]):
            return False
    if c['hcp'][3] != 'x':
        # hcpDiamond
        if fail(c['hcp'][3], h[1][3]):
            return False
    if c['hcp'][4] != 'x':
        # hcpClub
        if fail(c['hcp'][4], h[1][4]):
            return False
    # suit
    if c['suit'][0] != 'x':
        # spades
        if fail(c['suit'][0], h[0][0]):
            return False
    if c['suit'][1] != 'x':
        # hearts
        if fail(c['suit'][1], h[0][1]):
            return False
    if c['suit'][2] != 'x':
        # diamonds
        if fail(c['suit'][2], h[0][2]):
            return False
    if c['suit'][3] != 'x':
        # clubs
        if fail(c['suit'][3], h[0][3]):
            return False
    return True

def face_value(num):
    """
       face_value AB where A is suit and B card value
       A          s, h, d, c
       B          2,3,4,5,6,7,8,9,t,j,q,k,a
    """
    if num <=13:
        return '%s%s' % ('c', CARD_VALUE[num-0])
    elif num <=26:
        return '%s%s' % ('d', CARD_VALUE[num-13])
    elif num <=39:
        return '%s%s' % ('h', CARD_VALUE[num-26])
    elif num <=52:
        return '%s%s' % ('s', CARD_VALUE[num-39])

def make_hand(ns, ne):
    """
        ns starting index
        ne ending index
    """
    if ns < 52 and ne <= 52:
        return shuffled_pack[ns:ne]
    elif ns < 52 and ne > 52:
        return shuffled_pack[ns:] + shuffled_pack[:ne-52]
    elif ns > 51 and ne > 51:
        return shuffled_pack[ns-52:ne-52]
    
def summary(card_set):
    # suit = [ns, nh, nd, nc]
    suit = [0,0,0,0]
    # hcp = [hcpTotal, hcpS, hcpH, hcpD, hcpC]
    hcp = [0,0,0,0,0]    
    for each in card_set:
        if each[0] == 's':
            suit[0] = suit[0] + 1
            hcp[0] = hcp[0] + HCP.get(each[1],0)
            hcp[1] = hcp[1] + HCP.get(each[1],0)
        elif each[0] == 'h':
            suit[1] = suit[1] + 1
            hcp[0] = hcp[0] + HCP.get(each[1],0)
            hcp[2] = hcp[2] + HCP.get(each[1],0)
        elif each[0] == 'd':
            suit[2] = suit[2] + 1
            hcp[0] = hcp[0] + HCP.get(each[1],0)
            hcp[3] = hcp[3] + HCP.get(each[1],0)
        elif each[0] == 'c':
            suit[3] = suit[3] + 1
            hcp[0] = hcp[0] + HCP.get(each[1],0)
            hcp[4] = hcp[4] + HCP.get(each[1],0)
    return (suit, hcp)


def get_deal(hand_criteria, ps_criteria):
    """
       hand_criteria_set    boolean  
       ps_crtieria      choose partnership based on hcp and distribution
       return ( (handSelected, partner), (oppoA, oppoB) )
    """
    global PACK
    global shuffled_pack
    iteration = 0
    hand_criteria_set = criteria_set(hand_criteria)
    ps_criteria_set = criteria_set(ps_criteria)
    while iteration < MAX_ITERATIONS:
        np.random.shuffle(PACK)
        shuffled_pack = list(map(face_value, PACK))
        # make multiple hands
        solution = []
        index = 0
        while index <= 51:
            h1 = make_hand(index,index+13)
            h2 = make_hand(index+13,index+13+13)
            h3 = make_hand(index+13+13,index+13+13+13)
            h4 = make_hand(index+13+13+13,index+13+13+13+13)
            solution.append((h1,h2,h3,h4))
            index = index + 1
        # create hand summary
        meta_sol = []    
        for each in solution:
            l = []
            for hand in each:
                l.append(summary(hand))
            meta_sol.append(l) 
        # end create hand summary        

        if hand_criteria_set and not ps_criteria_set:
            # find a hand only
            for index, each in enumerate(meta_sol):
                for j,item in enumerate(each):
                    if hand_match(hand_criteria, item):
                        temp = list(H1toH4.difference(set([j])))
                        print (temp)
                        return {'cards': ( (solution[index][j],solution[index][temp[0]]),(solution[index][temp[1]],solution[index][temp[2]]) ),
                                'meta': ((meta_sol[index][j],meta_sol[index][temp[0]]),(meta_sol[index][temp[1]],meta_sol[index][temp[2]])),
                                'iteration': iteration,
                                'criteria': {'hand': hand_criteria, 'partnership': ps_criteria}
                                }
            # end find a hand
            
        
        elif ps_criteria_set and not hand_criteria_set:
            # find a partnership only
            for index, each in enumerate(meta_sol):
                result = ps(meta_sol[index], ps_criteria)
                if result:
                    # partnership solution found
                    return {'cards': ((solution[index][result[0][0]],solution[index][result[0][1]]),(solution[index][result[1][0]],solution[index][result[1][1]])),
                            'meta': ((meta_sol[index][result[0][0]],meta_sol[index][result[0][1]]),(meta_sol[index][result[1][0]],meta_sol[index][result[1][1]])),
                            'iteration': iteration,
                            'criteria': {'hand': hand_criteria, 'partnership': ps_criteria}
                            }
                    



        elif ps_criteria_set and hand_criteria_set:
            # find hand and partnership
            for index, each in enumerate(meta_sol):
                result = ps(meta_sol[index], ps_criteria)
                if result:
                    # partnership solution found
                    if hand_match(hand_criteria, meta_sol[index][result[0][0]]):
                        return {'cards': ((solution[index][result[0][0]],solution[index][result[0][1]]),(solution[index][result[1][0]],solution[index][result[1][1]])),
                                'meta': ((meta_sol[index][result[0][0]],meta_sol[index][result[0][1]]),(meta_sol[index][result[1][0]],meta_sol[index][result[1][1]])),
                                'iteration': iteration,
                                'criteria': {'hand': hand_criteria, 'partnership': ps_criteria}
                                }
                    if hand_match(hand_criteria, meta_sol[index][result[0][1]]):
                        return {'cards': ((solution[index][result[0][1]],solution[index][result[0][0]]),(solution[index][result[1][0]],solution[index][result[1][1]])),
                                'meta': ((meta_sol[index][result[0][0]],meta_sol[index][result[0][1]]),(meta_sol[index][result[1][0]],meta_sol[index][result[1][1]])),
                                'iteration': iteration,
                                'criteria': {'hand': hand_criteria, 'partnership': ps_criteria}
                                }

        iteration = iteration + 1
    return 'no solution found'

def steer_deal(hand_criteria, ps_criteria):
    """
        hand_criteria    choose hand based on hcp and distribution
        ps_crtieria      choose partnership based on hcp and distribution
        steer deal to fastest method
        always called first
    """
    hand_criteria_set = criteria_set(hand_criteria)
    ps_criteria_set = criteria_set(ps_criteria)
    if not hand_criteria_set and not ps_criteria_set:
        return get_no_criteria_deal()
    else:
        return get_deal(hand_criteria, ps_criteria)


"""
# hand criteria

hand_criteria = {
    'hcp': [(15,17),'x','x','x','x'],
    'suit': [(5,7), (5,5),'x','x']
    }

hand_criteria = {
    'hcp': ['x','x','x','x','x'],
    'suit': ['x','x','x','x']
    }

hand_criteria = {
    'hcp': [(13,13),'x','x','x','x'],
    'suit': [(5,7),'x','x','x']
    }

hand_criteria = {
    'hcp': [(13,15),'x','x','x','x'],
    'suit': [(5,8),'x','x','x']
    }


# end hand criteria


# partnership criteria, combined values
ps_criteria = {
    'hcp': [(26,26),'x','x','x','x'],
    'suit': [(9,9),'x','x','x']
    }
ps_criteria = {
    'hcp': ['x','x','x','x','x'],
    'suit': ['x','x','x','x']
    }


# end partnership criteria
"""
h_c = {
    'hcp': [(13,13),'x','x','x','x'],
    'suit': [(5,7),'x','x','x']
    }

ps_c = {
    'hcp': [(26,26),'x','x','x','x'],
    'suit': [(9,9),'x','x','x']
    }

r = steer_deal(h_c, ps_c)


