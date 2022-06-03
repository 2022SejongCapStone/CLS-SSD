import json
from random import randint
randint(0,2**64-1)
obj = {1:{0:{0:['q','q','q',randint(0,2**64-1)],1:['w','q','q',randint(0,2**64-1)],2:['e','q','q',randint(0,2**64-1)]}}, 2:{4:{3:['r','q','q',randint(0,2**64-1)],4:['t','q','q',randint(0,2**64-1)]},5:{5:['y','q','q',randint(0,2**64-1)]}}}

with open('test.json','w') as f:
    f.write(json.dumps(obj, sort_keys=True, indent=4))