from pyomo.core import *
import random

IDS = set()
models = set()
N = 1000

for _ in xrange(N):
  model = ConcreteModel()
  model.foo = Param(initialize=random.randint(2, 10))
  IDS.add(id(model))
  models.add(model)


print len(IDS)
print "Percent of IDs that are unique: {0:.2%}".format(1.*len(IDS)/N)
