Error Issue
====

I am having a weird bug where I cannot seem to be able to run the same model twice consistantly. I am running Pyomo 4.0, but I was having the same problem on Pyomo 3.5 which is why I had upgraded in the first place.

I have a concrete model that I cannot run twice on "large" models. It will run twice on small data sets and it will run once on larger data sets, but not twice. Below is the output is you were to run `python BigMModel.py`:

```python
['i1', 'i2', 'i3', 'i4', 'i5', 'i6'] ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
Selected Tech10: $42,316.35 [17.86%] (19.11 seconds)
19.11 seconds
['i1', 'i2', 'i3', 'i4', 'i5', 'i6'] ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
ERROR: Rule failed when generating expression for constraint BigM_MHE_LOWER with index i1:
AttributeError: 'NoneType' object has no attribute 'cname'
ERROR: Constructing component 'BigM_MHE_LOWER' from data=None failed:
AttributeError: 'NoneType' object has no attribute 'cname'
Traceback (most recent call last):
File "BigMModel.py", line 721, in <module>
instance, T = solve_big_m_model(gap=.2)
File "BigMModel.py", line 461, in solve_big_m_model
instance = big_m_model(PUTAWAY, PICKING)
File "BigMModel.py", line 251, in big_m_model
model.BigM_MHE_LOWER = Constraint(model.PUTAWAY, rule=BigM_MHE_LOWER)
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/block.py", line 396, in __setattr__
self.add_component(name, val)
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/block.py", line 676, in add_component
val.construct(data)
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/constraint.py", line 340, in construct
tmp = apply_indexed_rule(self, _self_rule, _self_parent, val)
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/misc.py", line 59, in apply_indexed_rule
return rule(model, index)
File "BigMModel.py", line 249, in BigM_MHE_LOWER
return -model.M_MHE * (1 - model.theta_put[i]) <= expr
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/numvalue.py", line 434, in __le__
return generate_relational_expression(_le, self, other)
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/expr.py", line 1411, in generate_relational_expression
raise TypeError(chainedInequalityErrorMessage())
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/expr.py", line 66, in chainedInequalityErrorMessage
generate_relational_expression.chainedInequality.to_string(buf)
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/expr.py", line 491, in to_string
precedence=_my_precedence )
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/expr.py", line 771, in to_string
precedence=_sub_precedence )
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/component.py", line 488, in to_string
ostream.write(self.__str__())
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/component.py", line 482, in __str__
return self.cname(True)
File "/usr/local/lib/python2.7/dist-packages/Pyomo-4.0-py2.7.egg/pyomo/core/base/component.py", line 499, in cname
base = c.cname(fully_qualified, name_buffer)
AttributeError: 'NoneType' object has no attribute 'cname'
```
