# Less than

Today's topic:

+ boolean dominance
+ continuous dominance
+ Fast era assessment

## Three types of "less than"

1. _Between candidate pairs_: For deciding if candidate "_X_" is better than
candidate "_Y_".
2. _Between sets of candidates from the same optimizer_: For
deciding early termination; i.e. if sets of candiadtes
found in _era+1_ is no better that _era_.
3.  _Between sets of candidates from different  optimizers_:
For comparing the final eras generated by different optimizers. 


Note that comparison type1 is between two items while
the other comparisons are between sets.

Note also that comparison type1 _must_ be fast
while type2 can be a little slower and type3 can be very slow indeed.
Why? Well:

+ Comparison type1 occurs within the inner most loop of the optimizers.
So it this one is slow, everything is slow. Here, we are willing to
trade (some) accuracy for raw speed.
+ Comparison type2 occurs once per era. So while it should be fast.
it need not as lightning fast as type1.
+ Comparison type3 occurs when all the optimizers are finished and
some analytics task is comparing the optimizers. This one must be
very thorough and, since it is only called once, is allowed to be not-so-fast.

## Comparison Type3:  _Between sets of candidates from different  optimizers_

For comparing the final eras generated by different optimizers. 

Collect a performance statistic:

+  hypervolume
+  spread
+  compute the _loss_ statisic described below between all
   pairs of candidates in era0 and last era.

Repeat the above for 20 different seeds.

Compare with the stats methods discussed last week.

Warning:

+ When comparing N optimizers for R repeats....\
    + For each repeat, generate one new baseline, then...
         + Run each optimizer for each repeat.
   
        
## Comparison Type2: Between sets of candidates from the same optimizer


For deciding early termination; i.e. if sets of candiadtes found in era+1 is no better that era.

Here, we do some approximate stats comparisons between eras. This is always heuristic and
done using "engineering judgment"

Krall's Bstop method:

+ For each objective do
    + If any "improvement", give yourself five more lives
         + Here, "improvement" could be
	          + Sort the values for that objective in _era_ and _era+1_
		      + Run the fast _a12_ test to check for true difference
              + Be mindful of objectives minimizing or maximizing.
+ If no improvement on anything,
     + Lives - 1


## Comparison Type1: Between Candidate pairs

Assumes:

+ Two candidates _X,Y_
+ Objectives _1,2,..i,..n_.
+ A predicate _better(i,Xi,Yi)_;
     + i.e. for objective "_i_" is _Xi_ from _X_ better than _Yi_ from _Y_?
     + e.g. when minimizing all goals,
	      + _better(any,Xi,Yi) =  Xi &lt; Yi_.

Engineering choice: should _Xi,Yi_ be normalized _0..1_?

+ Often used, simplifies all calcs.

### Aggregation functions

Some function that inputs "N" objectives and returns one number. E.g. if cost is twice as important
as speed then:

+ _(2*cost + 1*speed)/3_

Problems with aggregation functions:

+ Analysis highly biased by the "magic weights"

Solution:

+ Run with multiple, randomly assigned, magic weights.
+ See later, MOEA/D
    + Actually adds a trick so that different, but somewhat similar, weights, can share their insights
      with the optimizer
	+ Very cool.


### bdom = Boolean domination

The standard. Used widely in multi-objective domiantion

+ Better on at least one
+ Worse on none.

Visualized as the outer skin of the hypervolume

+ The non-dominated candidates have an unobscured  view of heaven.


![img](img/pareto.png)

Code (warning, written, not run):

```python

def gt(x,y): return x > y
def lt(x,y): return x < y

def better(i):  return lt

def objs(x):
  "Returns the objectives inside x"
  return x.objs # for example

def bdom(x,y):
  bettered = False
  for i,(xi,yi) in enumerate(zip(objs(x),obs(y))):
    if better(i)(xi,yi)
       bettered = True
	if xi != yi  
	   return False # not better and not equal, therefor worse
  return bettered
  ```

Problems with Boolean domination:

+ As number of objectives grows, more and more candidates are not dominated.
    + The crowd problem... number of candidate solutions explodes and everything else slows down.
    + See later: crowd pruning in NSGA-II.
	      + Very cool- prunes crowds in near linear time.
+ Only returns true/false.
    + Does not report _how much_ "_X_" dominates "_Y_"
    + Cannot distinguish between things that are very similar, but dominated, versuse
      very different.
	+ I.e. can't recognize nuances.


![img](img/pareto1.png)

### cdom = Continuous Domination

As suggested by Zitzler in the IBEA algorithm, 2004 (the "Z" in DTLZ and ZDT):

+ Eckart Zitzler and Simon Kunzli
  [Indicator-Based Selection in Multiobjective Search](http://www.simonkuenzli.ch/docs/ZK04.pdf),
  Proceedings of the 8th International Conference on
  Parallel Problem Solving from Nature (PPSN VIII)
  September 2004, Birmingham, UK

Differences between Xi and Yi are registered on an exponential scale, so any differences SHOUT louder.

+ Sum the differences between Xi and Yi, raised to an exponential power
+ Normalized by the number of objectives


Yes, this is an an aggregation function, but it assumes equal weights on all objectives

The following code asks what is lost between candidates. The loss function is not
symmetric (due to ties) so we compute loss from X to Y and back again. And the dominating
candidate is the one that losses less than the other guy.


```python
# Written, not run

def loss1(i,x,y):
    return (x - y) if better(i) == lt else (y - x)

def expLoss(i,x,y,n):
    return math.exp( loss1(i,x,y) / n)

def loss(x, y):
    x,y    = objs(x), objs(y)
    n      = min(len(x), len(y)) #lengths should be equal 
    losses = [ expLoss(i,xi,yi,n)
	             for i, (xi, yi) 
	               in enumerate(zip(x,y)) ]
	return sum(losses) / n
	
def cdom(x, y):
   "x dominates y if it losses least"		
   return x if loss(x,y) < loss(y,x) else y
```

Note extensions: loss difference is greater than some epsilon.

Continuous domination very much better for larger number of objectives:

+ Used in GALE.
+ Also used in Abdel Salam Sayyad, Tim Menzies, and Hany Ammar,
  [On the Value of User Preferences in Search-Based
   Software Engineering: A Case Study in Software
   Product Lines](http://menzies.us/pdf/13ibea.pdf), ICSE 2013.
    + Five goal problem:
        + Minimize design constraint violation
        + Maximize use of possible parts of the design
        + Maximize use of design parts we have used before
        + Minimize construction cost (sum of the construction cost of the parts)
	    + Minimize expected defects (sum of the defects seen in past uses of the parts)
    + Using some _bdom_ inference devices: NSGA-II, MOCell, SPEA2, etc 
    + Using one _cdom_ inference (IBEA)	


![img](img/sayyad13.png)



 
  
