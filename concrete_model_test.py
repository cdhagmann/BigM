from pyomo.core import *
import random

def mem_strip(model):
  return repr(model).strip('>').split()[-1]

model = ConcreteModel()
print mem_strip(model), id(model)

MEM = set()
IDS = set()

for _ in xrange(100):
  model = ConcreteModel()
  model.foo = Param(initialize=random.randint(2, 10))
  MEM.add(mem_strip(model))
  IDS.add(id(model))

print len(MEM), len(IDS)
