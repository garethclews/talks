---
title: The Unix Chainsaw Massacre
author: g | p

patat:
  incrementalLists: true
  slideLevel: 2
  images:
    backend: auto
  wrap: true
  margins:
    left: 8
    right: 8
  theme:
    code: [onDullBlack]
    codeBlock: [onDullBlack]
  pandocExtensions:
    - patat_extensions
    - autolink_bare_uris
...
# Look... I got some good barbecue here!

## Tools, tools everywhere
You can do an awful lot on the command line without even thinking about opening
python or R. Your *nix OS is a whole ecosystem of useful tools pre-made and
ready to be smushed together.

The purpose of this talk is to show you some of them and try to convince you to
try something a little bit different for laborious tasks - even if its outside
your projects.

## Command line vs (and with!) your favourite tools
You can even *use* your preferred scripting language from the command line. In
fact the further python goes down the design road it has the more it is being
used as syntactic sugar over a foreign function interface - especially in the
data science area.


Things that understanding your operating system will let you do that opening an
IDE generally don't:

- Schedule jobs to run at a specific time interval/date and time
- Parellelise the computations for free*
- Direct access to tools can simplify ideas of what is going on

*almost, you just need to know how.


# I just can't take no pleasure in killing. There's just some things you gotta do. Don't mean you have to like it.

## Starter for 10
Let's look at some useful tools

- generating a sequence of numbers
- combining functions
- finding a value in a data stream
- counting the number of numbers containing a 7 between 1 and 1000

## IO operations
Because having to generate your own data all the time is laborious

- writing a file
- reading in a file
- redirecting input and output


## Getting data out of sources

- JSON files: use jq
- Websites: use curl (or wget)
- All of the standard databases have command line interfaces
- Tools even exist for converting excel spreadsheets to **useful** formats




## Combining what we know so far

- Read in the entirety of Alice in Wonderland
- Programmatically extract the lines giving the chapter titles
- Remove the cruft to just get a list of titles


## Further down the rabbithole

```bash
< data/wonderland.txt |\
  tr '[:upper:]' '[:lower:]' |\
  grep -oE '\w{2,}' |\
  grep -E '^a.*e$' |\
  sort | uniq -c | sort -nr |\
  (echo "word,count" && awk '{print $2","$1}') |\
  head |\
  csvlook
```

## A most complex series of events

Let's try something more analytical *but equally as forced*

The file `games.csv` contains the results for a whole pile of tournament League
of Legends games. I want to know, what is the most commonly picked first
character for games that are won by the team that pick first.

### Information

- Column 5 is the winning team variable, we want this to be team 1
- Column 12 corresponds to the first picked hero of the draft phase


## The code

```bash
< data/games.csv |\
    awk -F"," '$5=="1" {print $12}' |\
    sed 1d |\
    sort | uniq -c | sort -nr | head -10 |\
    while read line; do
        echo $line | awk -v ORS=' ' {'print $1'};
        x=$(echo $line | awk {'print $2'});
        cat data/champion_info.json |\
        jq --argjson x $x '.[] | select(.id == $x) | .name'
    done |\
    column -t -s '"'
```


## ...and why you wouldn't do it like that

- For the same reason you never write your python or R code verbatim
- Functions
- Scripts

# Come on, guys; quit goofing on me.

## Machine learning on the command line

- caffe
- skll
- fasttext


# That's the last goddamn hitchhiker I ever pick up.

## Where's my damn function?

Ever forget where you defined that python function you now need to use elsewhere?

```bash
grep -Er "def main\(" **/*.{ipynb,py} | awk -F":" '{print $1}'
```


## Oh, SH*T

Finding whether you have dropped AWS creditials anywhere in a git repo

```bash
git grep -Ew '[A-Z0-9]{20}'
```

..which can also be attained by doing 

```bash
git ls-tree --full-tree -r --name-only HEAD | xargs egrep -w '[A-Z0-9]{20}'
```


## Updating that archive

```bash
zip --filesync -r data.zip ./data
```


