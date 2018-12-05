 
##  écrire les noms du binôme  ici  et aussi dans le  nom de fichier
## dm_algo_2018_gallot_leo_lemattre_benjamin

##-------------symboles ---------
class Symbole(object): 
    def __init__(self, arite, face): 
        self.arite = arite 
        self.face  = face
    
    def __str__(self):
        return self.face
    
def arite(symbole):   
    return symbole.arite
    
def face(symbole):        
    return symbole.face

def carArite(c):
    if (c == '-'):
        return 1
    if (c in ['+', '*', '>', '=']):
        return 2
    else:
         return 0

def symboleCreer(c):
    s=Symbole(carArite(c),c)
    return s

def symbolePrint(s):
    print("(%d,%c)"%(s.arite, s.face))

#-------------------------- arbre binaire ----------------*/
class  NoeudAbin:
    def __init__(self,val, g=None, d=None):
        	self.valeur=val
        	self.gauche=g
        	self.droit = d

def crAbin(s,  g=None, d=None):
    return NoeudAbin(s,g,d)

def feuilleCreer( c):
    return crAbin(symboleCreer(c), None, None)

def  g(a):
    return a.gauche

def d(a):
    return a.droit

def r(a):
    return a.valeur

# Question 1 

def  abinCopier(a):
    if a == None:
        return None
    return crAbin(r(a), g(a), d(a))
    
def postfixeRec( A):
    if (A!=None):
        s=r(A)
        postfixeRec(g(A))
        postfixeRec(d(A))
        print("%c"%s.face,end="")

#Question 2

def infixeRec(A):
    mot = ""
    if A != None:
        if arite(r(A)) != 0: 
            mot += "("+ infixeRec(g(A))
        mot += face(r(A))
        if arite(r(A)) != 0:
            mot += infixeRec(d(A)) + ")"
    else:
        return mot
    return mot

def infixeIt(A):
    mot = ""
    pile = NoeudPileAbin(A)
    current = g(A)
    while(pile != None or current != None):
        if r(current) != None:
            if sommet(pile) == "(":
                mot += ")"
                pile = depiler(pile)
                current = g(A)
            else :
                mot += "("
                pile = empiler("(",pile)
        else:
            current = sommet(pile)
            mot += face(r(current))
            pile = depiler(pile)
            d(A) 
    return mot


#-------------pile d'arbres binaires ---------------*/
class NoeudPileAbin:
    def __init__(self,val,suivant=None):
        self.valeur=val
        self.suivant=suivant
        
def empiler(A, pile=None):
        return  NoeudPileAbin(A, pile)

def depiler(pile):
    return (pile.suivant)

def sommet(pile):
    return pile.valeur

def pileAfficher(pile):
    p = pile
    print("[",end="")
    while(p!=None):
        postfixeRec(p.valeur)
        print(", ", end="")
        p=p.suivant
    print("]",end="")

#------------------- formules ----------------------
def variablecreer(p):
    return feuilleCreer(p)

def et(g,d):
    return crAbin(symboleCreer('*'),g,d)

def  ou(g,d):
    return crAbin(symboleCreer('+'),g,d)

def imp(g,d):
    return crAbin(symboleCreer('>'),g,d)

def equiv(g,d):
    return crAbin(symboleCreer('='),g,d)

def neg(g):
    return crAbin(symboleCreer("*"),None,g)

 
#------------------------- lecture ecriture postfixe -----------
def  abinEstUnaire( A):
    return (r(A).arite==1)

def abinEstBinaire(A):
    return r(A).arite==2

def abinEstVariable( A):
    return r(A).arite==0

def postfixeToAbin(mot):
    pile = NoeudPileAbin(None)

    for i in range(0, len(mot)):
        if arite(symboleCreer(mot[i])) == 0:
            temp = feuilleCreer(mot[i])
            pile = empiler(temp, pile)
        
        elif arite(symboleCreer(mot[i])) == 1:
            temp = sommet(pile)
            pile = depiler(pile)
            arbre = crAbin(symboleCreer(mot[i]), None, temp)
            pile = empiler(arbre, pile)

        else:
            arbreD = sommet(pile)
            pile = depiler(pile)
            arbreG = sommet(pile)
            pile  = depiler(pile)
            arbre = crAbin(symboleCreer(mot[i]), arbreG, arbreD)
            pile = empiler(arbre, pile)
    
    return sommet(pile)

        
#------------------------------ reecriture -------------------*/	
def reecrireEquiv(a):
    if a == None:
        return None

    if face(r(a)) == "=":
        arbreG = crAbin(symboleCreer(">"), g(a), d(a))
        arbreD = crAbin(symboleCreer(">"), d(a), g(a))
        a.valeur = symboleCreer("*")
        a.gauche = arbreG
        a.droit = arbreD
    
    reecrireEquiv(g(a))
    reecrireEquiv(d(a))

    return a
            
def reecrireImp(a):
    if a == None:
        return None
    
    if face(r(a)) == ">":
        arbreG = crAbin(symboleCreer("-"), None, g(a))
        a.valeur = symboleCreer("+")
        a.gauche = arbreG
    
    reecrireImp(g(a))
    reecrireImp(d(a))

    return a

def reecrireNeg(a): 
    if a == None:
        return None
    postfixeRec(a)
    print("\n")
    if face(r(a)) == "-":
        if face(r(d(a))) == "-":
            a = d(d(a))
        elif face(r(d(a))) == "+":
            arbreG = crAbin(symboleCreer("-"), None, g(d(a)))
            arbreD = crAbin(symboleCreer("-"), None, d(d(a)))
            a.gauche = arbreG
            a.droit = arbreD
            a.valeur = symboleCreer("*") 

        elif face(r(d(a))) == "*":
            arbreG = crAbin(symboleCreer("-"), None, g(d(a)))
            arbreD = crAbin(symboleCreer("-"), None, d(d(a)))
            a.gauche = arbreG
            a.droit = arbreD
            a.valeur = symboleCreer("+") 
    


    print("fin : \n")
    postfixeRec(a)

    reecrireNeg(g(a))
    reecrireNeg(d(a))
     
    return a




            

def reecrireOuEt( a):
    pass
    
def fnc(A):
    pass
#--------------- forme clausale ------------*/

class NoeudClause:
    def __init__(self,val, suiv):
        self.val=val
        self.suivt=suiv

def  ajClauseDevant(a , c=None):
    return NoeudClause(a, c)

class  NoeudListeDeClauses:
    def __init__(self, val,  suiv):
        self.val=val
        self.suivt = suiv

def ajListeDeClausesDevant(c ,  lc=None):
    return NoeudListeDeClauses(c, l)
	
def estNeg(A):
    return (r(A).face=='-')
def estOu(A):
    return (r(A).face=='+')
def estEt(A):
    return (r(A).face=='*')
    
def afficheNeg(A):
    print("-%c"%r(d(A)).face,  end="")
    
    

def append(c, d):
    if (c==None):
       return d
    if (d==None):
        return c
    pointeur=c
    while(pointeur !=None):
        d=ajClauseDevant(pointeur.val  , d)
        pointeur = pointeur.suivt
    return d

def appendLc(lc, ld):
    if (lc==None):
       return ld
    if (ld==None):
        return lc
    pointeur=lc
    while(pointeur !=None):
        ld=ajListeDeClausesDevant(pointeur.val  , ld)
        pointeur = pointeur.suivt
    return ld
    
def afficheClause(c):
    print("{", end="")
    p=c
    while(p!=None):
        A=p.val
        if (estNeg(A)):
            print("-%c, "%r(d(A)).face, end="")
        else:
            print("%c, "%r(A).face, end="")
        p=p.suivt
    print("}",  end="")

def  afficheListeDeClauses(lc):
    print("{", end="")
    p= lc
    while(p!=None):
        afficheClause(p.val)
        print(", ", end="")
        p=p.suivt
    print("}", end="")

# {{}}
def videToLc():
	c=None
	lc = ajListeDeClausesDevant(c ,None)
	return lc

#--p devient------ {{p}}

def  feuilleToLc(A):
    pass

# -{{p}} devient {{-p}}
def negToLc( lc):
    pass
    
# {{a, b}} + {{c, d}} = {a,b,c,d}
def ouToLc(glc, dlc):
    pass

# {{a,b}, {a,c}} et {{e,f}, {d,f}}
def etToLc(c, d):
    pass

def  fncToLc(A):
    pass
    

##-------------tests---------------
	
def testSymbole():
        p=symboleCreer('p')
        plus=symboleCreer('+')
        print("plus est le symbole {%d,%c} "%(plus.arite, plus.face))
        symbolePrint(p)

def testAbin():
        p=symboleCreer('p')
        s=symboleCreer('s')
        A=crAbin(symboleCreer('+'),feuilleCreer('p'), feuilleCreer('q'))
        B=crAbin(symboleCreer('*'),crAbin(p,None, None), crAbin(s,None, None))
        C=crAbin(symboleCreer('>'),A,B)
        C=crAbin(symboleCreer('='),C,C)
        postfixeRec(C); print(", ",end=""); postfixeRec(g(d(C))); print(", ",end="");symbolePrint(r(C))
  
def testPile():
    A=crAbin(symboleCreer('+'),feuilleCreer('p'), feuilleCreer('q'))
    pile = None
    pile=empiler(A, pile)
    A=crAbin(symboleCreer('*'),feuilleCreer('s'), feuilleCreer('r'))
    pile=empiler(A, pile)
    pileAfficher(pile)
    B = sommet(pile)
    pile=depiler(pile)
    postfixeRec(B)

def testSaisiePostfixe():
	mot="pq+rs*>"
	A = postfixeToAbin(mot)
	postfixeRec(A)

def testReecriture():
	mot="pq=-"
	A = postfixeToAbin(mot)
	rA = reecrireEquiv(A)
	postfixeRec(A)
	print(" devient ", end="")
	postfixeRec(rA)
	print(" après réecriture de = \n", end="")
	A=rA
	rA = reecrireImp(rA)
	postfixeRec(A)
	print(" devient ")
	postfixeRec(rA)
	print(" après réecriture de >  \n")
	A=rA
	rA = reecrireNeg(A)
	postfixeRec(A)
	print(" devient ")
	postfixeRec(rA)
	print(" après réecriture de - \n")

	mot="pq*---"
	A = postfixeToAbin(mot)
	rA = reecrireNeg(A)
	postfixeRec(A)
	print(" devient ")
	postfixeRec(rA)
	print(" après réecriture de - \n")
	
	mot="pq*rs*+"
	A = postfixeToAbin(mot)
	rA = reecrireOuEt(A)
	postfixeRec(A)
	print(" devient ")
	postfixeRec(rA)
	print(" après réecriture de + et * \n")
	infixeRec(A)
	print(" devient ")
	infixeRec(rA)
	print(" après réecriture de + et * \n")


def  testFormule():
    p=variablecreer('p'); q=variablecreer('q'); u=variablecreer('u')
    A=ou(p,q)
    B=et(neg(p), neg(q))
    C=equiv(neg(A),B)
    postfixeRec(C); print(", ")
    C=equiv(neg(imp(p,u)),imp(neg(u), neg(p)))
    postfixeRec(C)

def  testLc():
    p =feuilleCreer('p')
    q =feuilleCreer('q')
    cc = ajClauseDevant(p,None)
    cc=  ajClauseDevant(q,cc)
    cd = ajClauseDevant(neg(p),ajClauseDevant(q,None))
    ce = append(cc,cd)
    lc = ajListeDeClausesDevant(cc, None)
    lc = ajListeDeClausesDevant(cd, ajListeDeClausesDevant(cc, lc))
    afficheClause(ce)
    print("\n", end="")
    afficheListeDeClauses(lc)
    print("\n")
    lc = appendLc(lc,ajListeDeClausesDevant(cc, lc))
    afficheListeDeClauses(lc)

def testFncToLc():
    mot="pq+"
    A=postfixeToAbin(mot)
    #postfixeRec(A)
    lc=fncToLc(A)
    afficheListeDeClauses(lc)
    mot="pq+rs+*"
    A = postfixeToAbin(mot)
    lc=fncToLc(A)
    afficheListeDeClauses(lc)
    
def testComplet():
    mot="pq=qs>*p*s>"
    A = postfixeToAbin(mot)
    postfixeRec(A); print("\n")
    rA=fnc(A) ; postfixeRec(rA); print("\n")
    lc=fncToLc(rA); afficheListeDeClauses(lc)
    
def main():
    # a = crAbin(symboleCreer('='),crAbin(symboleCreer('='),feuilleCreer('a'),feuilleCreer('b')),crAbin(symboleCreer('='),feuilleCreer('c'),feuilleCreer('d')))
    # print("1")
    # a = postfixeToAbin("pq=-")
    # postfixeRec(a)
    # print("\n")
    
    # print("2")
    # ra = reecrireEquiv(a)
    # postfixeRec(ra)
    # print("\n")
    
    # print("3")
    # raa = reecrireImp(ra)
    # postfixeRec(raa)
    # print("\n")
    
    # print("4")
    # raaa = reecrireNeg(raa)
    # postfixeRec(raaa)


    a = postfixeToAbin("b-ac+-+-")
    postfixeRec(a)
    print("\n")

    reecrireNeg(a)

    print("testcommit")


    # testSymbole()
    # testAbin()
    #testPile()
    # testFormule()
    # testSaisiePostfixe()
    #testReecriture()
    #testLc()
    #testFncToLc()
    #testComplet()

main()