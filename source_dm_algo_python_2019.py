#  écrire les noms du binôme  ici  et aussi dans le  nom de fichier
# dm_algo_2018_gallot_leo_lemattre_benjamin

# -------------symboles ---------
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
    return crAbin(r(a),g(a),d(a))
    
def postfixeRec( A):
    if (A!=None):
        s=r(A)
        postfixeRec(g(A))
        postfixeRec(d(A))
        print("%c"%s.face,end="")   

#Question 2

def infixeRec(A):
    if A != None:
        if arite(r(A)) != 0: 
            print("(", end = "")
            infixeRec(g(A))
        print(face(r(A)), end="")
        if arite(r(A)) != 0:
            infixeRec(d(A))
            print(")", end="")

def infixeIt(a):
    current = a
    pile = NoeudPileAbin(None)
    pile_parenthese = NoeudPileAbin(None)
    done = 0
    nbParenthese = 0

    while (not done):

        if current is not None:
            if current != None and arite(current.valeur) >= 1:
                pile_parenthese = empiler("(", pile_parenthese)
                print("(", end="")

            pile = empiler(current, pile)
            current = current.gauche

        else:
            if sommet(pile) != None:
                current = sommet(pile)
                pile = depiler(pile)
                
                if sommet(pile_parenthese) == "(" and arite(current.valeur) == 0:
                    print("%", end="")
                    pile_parenthese = depiler(pile_parenthese)
                print(current.valeur, end="")
                current = current.droit
            else:
                done = 1
  


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
    return crAbin(symboleCreer("-"),None,g)

 
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
    b = abinCopier(a)
    if b == None:
        return None

    if face(r(b)) == "=":
        arbreG = crAbin(symboleCreer(">"), g(b), d(b))
        arbreD = crAbin(symboleCreer(">"), d(b), g(b))
        b.valeur = symboleCreer("*")
        b.gauche = arbreG
        b.droit = arbreD
    b.gauche = reecrireEquiv(g(b))
    b.droit = reecrireEquiv(d(b))
    return b
            
def reecrireImp(a):
    b=abinCopier(a)
    if b == None:
        return None
    
    if face(r(b)) == ">":
        arbreG = crAbin(symboleCreer("-"), None, g(b))
        b.valeur = symboleCreer("+")
        b.gauche = arbreG
    
    b.gauche = reecrireImp(g(b))
    b.droit = reecrireImp(d(b))

    return b

def reecrireNeg(a): 
    b = abinCopier(a)
    if b == None:
        return None

    if face(r(b)) == "-":
        if face(r(d(b))) == "-":
            b = reecrireNeg(d(d(b)))
        elif face(r(d(b))) == "+":
            arbreG = crAbin(symboleCreer("-"), None, g(d(b)))
            arbreD = crAbin(symboleCreer("-"), None, d(d(b)))
            b.gauche = reecrireNeg(arbreG)
            b.droit = reecrireNeg(arbreD)
            b.valeur = symboleCreer("*") 
        elif face(r(d(a))) == "*":
            arbreG = crAbin(symboleCreer("-"), None, g(d(b)))
            arbreD = crAbin(symboleCreer("-"), None, d(d(b)))
            b.gauche = reecrireNeg(arbreG)
            b.droit = reecrireNeg(arbreD)
            b.valeur = symboleCreer("+")
    return b


def reecrireOuEt(a):
    b=abinCopier(a)
    if b == None:
        return None

    if face(r(b)) == "+":
        if face(r(g(b))) == "*" and face(r(d(b))) != "*":
            arbreG = crAbin(symboleCreer("+"), g(g(b)), d(b))
            arbreD = crAbin(symboleCreer("+"), d(g(b)), d(b))
            b.gauche = reecrireOuEt(arbreG)
            b.droit = reecrireOuEt(arbreD)
            b.valeur = symboleCreer("*") 
        elif face(r(g(b))) != "*" and face(r(d(b))) == "*":
            arbreG = crAbin(symboleCreer("+"), g(b), g(d(b)))
            arbreD = crAbin(symboleCreer("+"), g(b), d(d(b)))
            b.gauche = reecrireOuEt(arbreG)
            b.droit = reecrireOuEt(arbreD)
            b.valeur = symboleCreer("*") 
        elif face(r(g(b))) == "*" and face(r(d(b))) == "*":
            arbreGG = crAbin(symboleCreer("+"), g(g(b)), g(d(b)))
            arbreGD = crAbin(symboleCreer("+"), g(g(b)), d(d(b)))
            arbreDG = crAbin(symboleCreer("+"), d(g(b)), g(d(b)))
            arbreDD = crAbin(symboleCreer("+"), d(g(b)), d(d(b)))
            arbreG = crAbin(symboleCreer("*"),arbreGG,arbreGD)
            arbreD = crAbin(symboleCreer("*"),arbreDG,arbreDD)
            b.gauche = reecrireOuEt(arbreG)
            b.droit = reecrireOuEt(arbreD)
            b.valeur = symboleCreer("*") 
    return b
    
def fnc(a):
    return reecrireOuEt(reecrireNeg(reecrireNeg(reecrireImp(reecrireEquiv(a)))))

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
    return NoeudListeDeClauses(c, lc)
	
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

def  feuilleToLc(a):
     return ajListeDeClausesDevant(ajClauseDevant(a))

# -{{p}} devient {{-p}}
def negToLc( lc):
    return feuilleToLc(neg(lc.val.val))
    
# {{a, b}} + {{c, d}} = {a,b,c,d}
def ouToLc(glc, dlc):
   return ajListeDeClausesDevant(append(glc.val,dlc.val))


# {{a,b}, {a,c}} et {{e,f}, {d,f}}
def etToLc(c, d):
    return appendLc(c,d)

def  fncToLc(a):
    if arite(r(a)) == 0 :
        return feuilleToLc(a)
    elif arite(r(a)) == 1:
        return negToLc(fncToLc(d(a)))
    elif arite(r(a)) == 2:
        if face(r(a)) == '+':
            return ouToLc(fncToLc(g(a)),fncToLc(d(a)))
        else:
            return etToLc(fncToLc(g(a)),fncToLc(d(a)))


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

    mot = "pq+rs+*"
    arbre = postfixeToAbin(mot)
    infixeRec(arbre)
    print('\n')
    infixeIt(arbre)
    #testSymbole()
    #testAbin()
    #testPile()
    # testFormule()
    # testSaisiePostfixe()
    #testReecriture()
    #testLc()
    #testFncToLc()
    #testComplet()

main()
