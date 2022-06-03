import Crypto.PublicKey.ElGamal as elg
import json
from os import urandom
print('start generating..')
privkey = elg.generate(1024,urandom)
obj = {'p':int(privkey.p),'g':int(privkey.g),'y':int(privkey.y),'x':int(privkey.x)}

#store to db
with open('key.json','w') as f:
    f.write(json.dumps(obj, sort_keys=True, indent=4))
