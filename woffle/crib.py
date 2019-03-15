"""
w o f f l e

An NLP project template for dummies, by dummies
-- show and tell crib sheet: Wednesday 6th
"""

# Preliminary talk through on how its intended to be obtained and set up
#  1. git clone into named directory
#  2. the makefile structure and behaviour


# The breakdown of work into tasks

with open('data/example_comments.txt') as handle:
    text = handle.read().splitlines()
"""
I do it this way because this means I don't have to worry about \n chars
so long as you end up with a list corresponding to the different pieces of text
you are intending to work with then your preferred mechanism is fine so long as
it isn't adding additional structure we don't need (looking at pandas...)
"""

# now we have our text lets import the things we need to do stuff with it
# for this example we will build a simple sentiment polarity scorer using the
# functionality which comes with woffle today
from woffle.functions.generics import compose
# talk about what compose means
from woffle.parse.deter.parse  import parse
from woffle.embed.sentiment    import embed
from woffle.cluster.deter      import cluster

"""
talk through the directory structure in all of its monstrous glory
then talk about themes!!
"""

# themes are a means by which tasks can be given opinionated and reasonable
# set of default functions for performing the task

# the import block above is completely equivalent to:

from woffle.functions.generics import compose
from woffle.sentiment          import parse, embed
# from here the sentiment scoring is super straight forward:

scores = compose(embed, parse)(text)
labels = [    'negative' if score < -0.33
         else 'neutral'  if score <= 0.33
         else 'positive'
         for score in scores
         ]
# here the clustering and labelling have overlapped but once you have the
# scores, you can then zip or combine text, scores and labels in any way


# that was a really straight forward example using default settings so let's
# shift focus and look at something a little more complicated and try to
# replicate part of optimus using woffle

# this bit takes a long time because it loads fasttext's model into memory
from woffle.hcluster import parse, embed, cluster, select

# let's get some data that looks a bit more like what optimus is good at
with open('data/example_cluster.txt') as handle:
    text = handle.read().splitlines()

target = parse(text)
embedding = list(embed(target))
clusters = cluster(embedding, 7)
labels = select(text, clusters)

for t, l in zip(text, labels):
    print(f"{t:>30s} : {l}")

# so far, so straight forward (you can reduce this to much less code but
# this is an example of how to build it up)

# what happens if we want to try to use BERT for the embeddings instead of
# fasttext?

from woffle.embed.numeric.bert.embed import embed

target = parse(text)
embedding = list(embed(target))
clusters = cluster(embedding, 7)
labels = select(text, clusters)

for t, l in zip(text, labels):
    print(f"{t:>30s} : {l}")


# As a user woffle, hopefully I've shown, is really easy to pick up and use
# however, it could still use some work in structure as the real effort here
# comes in understanding and following the hierarchy to implement things
# which are not covered in its default functionality. Here we offer many
# different things as part of woffle.functions but the onus is on those who
# wish to use the new functionality to follow the structure that is there
# (or whatever it becomes, feedback wanted/needed!!!) and decide whether the
# thing they are doing is likely to be done by others and so needs to be
# built into the back end

# let's have a quick run through of the things we offer to help roll your own
from woffle.functions.generics import id, compose, compose_
from woffle.functions.lists    import mapmap, foldl, foldl1, unpack, unpackG, strip


# id: polymorphic identity function
id(1)
id('4')

# compose: used above, mathematical composition of functions
# compose_: exactly what compose does but arguments are reversed - this is here
# for those that don't like mathematical composition
compose(str.upper, str.strip)(' hello  world ')
compose_(str.strip, str.upper)(' hello  world ') # does exactly the same


# and that's it so far for generics, but we have a lot more list operations
# and they revolve around the structure of your data types

# mapmap: for when you have multiple layers of structure to map a map over
mapmap(lambda x: x**2, [[1,2], [2,3,4]])

# unpack: make a list of lists into a list
# unpackG: as unpack but return a generator expression
unpack([[1,2], [2,3,4]])
for i in unpackG([[1,2], [2,3,4]]):
    print(i)

# strip: remove values from a list which evaluate to False
strip(['hi', '', 0,  'pepeHands'])

# all of these functions really form the backbone of how woffle was built and
# find use across a large swathe of the code

# if you think woffle may be of use to you or if you would like to add to it
# then you need to think about the steps in the workflow, if you can break it
# down into the 4 tasks mentioned then please PR and get things added!

# There is already a train directory in the hierarchy but there is nothing in
# it yet, if this is something you are interested in please PR and get it
# added.

# That is all for today, the examples you have seen are available in the
# examples directory of the repo along with a much more in depth re-working of
# optimus, pull it and give it a go!
