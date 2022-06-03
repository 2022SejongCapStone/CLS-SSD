import Crypto.PublicKey.ElGamal as elg
from Crypto.Util.number import getRandomRange
from os import urandom
import time
from Crypto import Random
from Crypto.Math.Primality import ( generate_probable_safe_prime,
                                    test_probable_prime, COMPOSITE )
from Crypto.Math.Numbers import Integer

import sys


class AdditiveElgamalKey(elg.ElGamalKey):
    """Sub Class"""
    def __init__(self,randfunc=None,N=1): # N: max bit of msg  # added for additive HE
        super().__init__(randfunc)
        self.N=N

    def _encrypt(self, M, K):
        a=pow(self.g, K, self.p)
        b=( pow(self.y, K, self.p) * pow(self.g, M, self.p) ) % self.p   # added for additive HE
        return [int(a), int(b)]

    def _decrypt(self, M):
        if (not hasattr(self,'lookup')):
            self.lookup = {}
            for i in range(2**self.N):
                self.lookup[int(pow(self.g,i,self.p))] = i

        if (not hasattr(self, 'x')):
            raise TypeError('Private key not available in this object')

        r = Integer.random_range(min_inclusive=2,
                                 max_exclusive=self.p-1,
                                 randfunc=self._randfunc)
        a_blind = (pow(self.g, r, self.p) * M[0]) % self.p
        ax=pow(a_blind, self.x, self.p)
        plaintext_blind = (ax.inverse(self.p) * M[1] ) % self.p
        plaintext = (plaintext_blind * pow(self.y, r, self.p)) % self.p
        plaintext = self.lookup[int(plaintext)]  # added for additive HE
        return plaintext

def constructAdditive(tup):
    r"""Construct an ElGamal key from a tuple of valid ElGamal components.
    The modulus *p* must be a prime.
    The following conditions must apply:
    .. math::
        \begin{align}
        &1 < g < p-1 \\
        &g^{p-1} = 1 \text{ mod } 1 \\
        &1 < x < p-1 \\
        &g^x = y \text{ mod } p
        \end{align}
    Args:
      tup (tuple):
        A tuple with either 3 or 4 integers,
        in the following order:
        1. Modulus (*p*).
        2. Generator (*g*).
        3. Public key (*y*).
        4. Private key (*x*). Optional.
    Raises:
        ValueError: when the key being imported fails the most basic ElGamal validity checks.
    Returns:
        an :class:`ElGamalKey` object
    """

    obj=AdditiveElgamalKey()
    if len(tup) not in [3,4]:
        raise ValueError('argument for construct() wrong length')
    for i in range(len(tup)):
        field = obj._keydata[i]
        setattr(obj, field, Integer(tup[i]))

    fmt_error = test_probable_prime(obj.p) == COMPOSITE
    fmt_error |= obj.g<=1 or obj.g>=obj.p
    fmt_error |= pow(obj.g, obj.p-1, obj.p)!=1
    fmt_error |= obj.y<1 or obj.y>=obj.p
    if len(tup)==4:
        fmt_error |= obj.x<=1 or obj.x>=obj.p
        fmt_error |= pow(obj.g, obj.x, obj.p)!=obj.y

    if fmt_error:
        raise ValueError("Invalid ElGamal key components")

    return obj


#privkey = elg.generate(1024, urandom) recommended 2048
p = 172067444301411895534559176883337362238805143114568679300828522026331988387520629075001280951117910182845210523754097535990554095189115143184120700748520349875731895700657247057063402690415856916536241290613815433444376876635849600997943379177084658609355666196972679604896457719176491277337749647163615315239
g = 152099127338824065352734025795782372813741219022293709634659089225725849814863297008758857609295743149703148082918516646122258200325825724792666310463981307791002847868528259357658160079159361669564833691917200068950086825012073454980906136847162493348300873070685529469000741346791658188551027997846047456276
y = 159104751424828756721211425137395400626170577519875758232849516965346225206532682290117091607219868560718408337724951953195840849659954604538849327167644164666735613817620558809274481384958618919580966785469996714752708560100977671268316222462773865616586022643856025558154720763235691194141990976552296857855
x = 54341387290485008214971297570783543466821337945647534955349487848605100012901471359840907436679773628083304811849776884806334796630365309185515082808277968543041013720208367639712838183610972513989471619687737175401901438560430237329435735845660988496014613310611435347736842181384450314671317122793804765781


privkey = constructAdditive((p,g,y,x))
pubkey = constructAdditive((privkey.p,privkey.g,privkey.y))

#privkey = elg.construct((p,g,y,x))
#pubkey = privkey.publickey()
# print(key.p)
# print(key.g)
# print(key.y)
# print(key.x)



pln = [1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,0]
c = []
start = time.time()
for i in pln:
    K = getRandomRange(0, pubkey.p-1, urandom)
    c.append(pubkey._encrypt(i,K))
end = time.time()
print('enc time:',end-start)


# for i in c:
#     print(i[1])
start = time.time()
dec = []
for i in c:
    dec.append(privkey._decrypt(i))
end = time.time()
print('dec time:',end-start)
print(dec)
print(sys.getsizeof(pln))
print(sys.getsizeof(c))




