"""
b e  m o r e  f u n c t i o n a l


Functional programming in python!

Stolen from/inspired by rexim, the guy is amazing and I'm not going to 'cheat'
by using the functional programming modules which exist for python to
talk about thinking in a functional way (itertools, functools, operator)
"""

# Golden rules for pure functional programming in python
#
# 1. no loops
# 2. no if statements outside of ternary operators
#    (for the C folk the python equivalent of `x?y:z` is `y if x else z`
#     so completely avoiding typing if is harder because of syntax)
# 3. function definitions are a single return
# 4. no side effects    <-- important
# 5. no assignments inside functions
# 6. no lists
# 7. functions may only have at most one argument


# Quick segue:
# Functional programming languages tend to allow you to use a declarative style
# rather than an imperative style. What does this mean?
# *Imperative*: you tell the computer exactly how to build the thing you want
# *Declarative*: you tell the computer only __what__ you want
#
# For example:
#### imperatively:
result = []
for i in range(1000):
    if i % 17 == 0:
        result.append(i)

#### declaratively:
result = [i for i in range(1000) if i % 17 == 0]
# if you are not comfortable with writing code this way then I am truly sorry
# because you're in for a lot of it


#-- WORKING WITHOUT LOOPS -------------------------------------------------------
## if you need a loop, write a recursion!
## This is a super easy thing to do really. For example we will write a
## function to sum all numbers up to some i

#-- writing a function to sum integers up to some value i
def sum(i):
    return 0 if i==0 else i + sum(i-1)

## Segue (let's call it the bridge?)
## we can alternaively even use lazy evaluation in python (via yield), which is
## one of the best strengths of haskell but also causes some of the most
## confusion amongst people who don't know how to handle thunks so I'm going to
## completely avoid talk along those lines because we are thinking how to write
## python code in a functional programming way rather than writing python in a
## haskell-y way





#-- dealing with functions with more than one argument
def add(x):
    return lambda y: x + y
# or probably nicer to read?
addL = lambda x: lambda y: x + y
# or to more clearly see what lambda x and lambda y are doing
addL = (lambda x: (lambda y: x + y))

# EXAMPLE


# so we can now do things like
add1 = add(1)  # partial application, almost
# partial functions are more complicated things to throw around because they
# are mutable themselves but they give you an idea of how the application goes
# but we can now apply add1 like:
add1(2)





#-- no arrays!!!
## how on earth can we get around not having lists?
## well a list is really a value followed by another list, and we can implement
## this easily using an object we haven't restricted ourselves from using
## which is the hash map (aka a dictionary in python parlance)
##
## NOTE: doing this so that I don't have to really deal with how functional
## languages actually implement lists because its more complex than this. I should
## really do all of this with named tuples
pair = lambda x: lambda y: (x, y)

## to work with these we will need a couple of functions which work on the pair
## and I'm going to name them after the function names in haskell just because
fst = lambda p: p[0]
snd = lambda p: p[1]
## lastly we need an idea of an empty list, which we shall use None to represent



# once you have a pair, you can then chain and chain and chain and chain and then
# you can mimic the way purely functional programming languages think about lists
xs = pair (3) (pair (2) (pair (1) (None)))
# then:
fst(xs)  ## takes the head
snd(xs)  ## gives the tail -- warning, this is tail in the functional sense

# and we will create new labels for these functions accordingly
head = fst
tail = snd




#-- Working without state

# working in this way is wonderful, but we aren't allowing our functional programs
# to have side effects (let's pretend that we are running this program rather than
# using a REPL) - let's write a function that lets us bridge the gap between pure
# functional here and the dirty world of IO, and to do that we will convert our
# concept of lists into that of python lists
def pairs2list(xs):
    """
    Working with dirty IO so we are not bound by our basic rules here
    """
    result = []
    while xs:
        result.append(head(xs))
        xs = tail(xs)
    return result
# defining arrays in our way above is a little clunky for users inputting info
# we probably want a dirty function to go the other way so that we can then
# pass information into our pure functional program
def list2pairs(array):
    """
    Take lists and move to a nice functional paradigm to be safe
    """
    result = None
    for i in array[::-1]:  # if we traverse front to back we get a reversed pair!
        result = pair (i) (result)
    return result

# let's check our identity function
Xs = [i for i in range(1,11)]
pairs2list(list2pairs(Xs))



## Ok, let's tackle a simple problem in a functional way

# Operating on lists -- FOLDING
xs = list2pairs(Xs)

# this is a horrible thing to have to write because python makes it so
# but in functional languages you'll find it built in
#
# folding is also super duper important
fold = lambda f: lambda h: lambda t: f(h)(fold(f)(head(t))(tail(t))) if t else h

mul = lambda x: lambda y: x * y

fold (mul) (head(xs)) (tail(xs))

# ewwww, that fold is horrible looking (probably just me tbh)
# but this gives you a general function to apply any abstract function to
# a list to collapse that list!! To do this now the 'best' way (aka my way)
# is to do something like
import functools
import operator

pypo = lambda f, y: functools.reduce(f, y)

# just to check it using the dirty state-filled world:
pypo(operator.mul, Xs)



# Points to take away and things you could do right now (that aren't this)
# horrid
#
# 1. Consider using functions and functions of functions and functions of
#    functions of functions instead of other ways of doing things
# 2. Consider dropping imperative style for declarative style
# 3. Split your code into dirty and stateless sections
# 4. Think of the rules I've laid out and how you might do it in this way when
#    you are just doing your own thing
# 5. Please use functools, itertools and operator, they are wonderful


# example things these modules blow through
x = [i**2 for i in range(1,11)]
y = [i**3 for i in range(1,11)]

# unpacking tuples is lovely
# so we can really easy get the pairwise differences of the squares and cubes
print(*itertools.starmap(operator.sub, zip(y,x)))
# or how about the sum of all of the combinations?
print(*(i+j for i,j in itertools.product(x,y)))

