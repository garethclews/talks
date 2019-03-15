#--  starter for 10  ------------------------------------------------------------

# 1
seq 1 20

# 2 & 3
seq 1 20 | grep 7

# 4
seq 1 1000 | grep 7 | wc -l



#-- io operations ---------------------------------------------------------------

# writing to a file

# creating:
echo "Numbers" > data/words.txt
# appending
seq 3 31 >> data/words.txt


# reading a file
cat words.txt
# why cat?
# alternatively:
< words.txt

# how about something with a little structure?
< data/iris.json | jq '.'
# well that's a big block of mess, what if we only want some of the inner structure?
< data/iris.json | jq '.[]'

# selecting a subset of the data from this
< data/iris.json | jq '.[] | select(.species == "setosa")'

# making sure we actually get the right number (sense check for the disbelievers)
< data/iris.json | jq '.[] | select(.species == "setosa")' | wc -l

# more complicated:
< data/iris.json | jq '.[] | select(.species == "setosa") | .petalLength'
# or
< data/iris.json | jq '.[] | select(.petalLength > 4.3) | .species' | sort | uniq -c | sort -nr


# getting web data
## example
curl -s http://www.gutenberg.org/files/76/76-0.txt | head -n 10

# saving it
curl -o data/wonderland.txt -s http://www.gutenberg.org/files/76/76-0.txt

# database working tools:
sqlite --help
postgres --help



#-- munging ---------------------------------------------------------------------

# start with some basic data
echo "bar\nfoo\nfoo\nbar\nfoo\nbar\nbar"

# sorting it
echo "bar\nfoo\nfoo\nbar\nfoo\nbar\nbar" | sort

# now look for the unique entries and count them
echo "bar\nfoo\nfoo\nbar\nfoo\nbar\nbar" | sort | uniq -c

# finally reorder them in descending numerical order
echo "bar\nfoo\nfoo\nbar\nfoo\nbar\nbar" | sort | uniq -c | sort -nr

## this can either be turned into something resembling a CSV file:
echo "bar\nfoo\nfoo\nbar\nfoo\nbar\nbar" | sort | uniq -c | sort -nr | awk '{print $2","$1}'
## or turned into a more likable looking table
echo "bar\nfoo\nfoo\nbar\nfoo\nbar\nbar" | sort | uniq -c | sort -nr | column -t
# this is just to show column exist, its not GNU column though so I get so sad...


# deleting rows that are useless to us such as headers...
cat data/words.txt | sed 1d


# exploring data - searching for something inside a file
< data/wonderland.txt | grep -E '^CHAPTER [IVXLCDM]{1,}\. .*$'

# getting just the title chapters
< data/wonderland.txt | grep -E '^CHAPTER [IVXLCDM]{1,}\. .*$' | sed 's/.*\. \(.*\)$/\1/'


#-- Further down the rabbit hole --------------------------------------
< data/wonderland.txt |\
  tr '[:upper:]' '[:lower:]' |\
  grep -oE '\w{2,}' |\
  grep -E '^a.*e$' |\
  sort | uniq -c | sort -nr |\
  (echo "word,count" && awk '{print $2","$1}') |\
  head |\
  csvlook



# or replacing the end to find out how many words of this form there are:

< data/wonderland.txt |\
  tr '[:upper:]' '[:lower:]' |\
  grep -oE '\w{2,}' |\
  grep -E '^a.*e$' |\
  sort | uniq -c | sort -nr |\
  awk '{print $2","$1}' |\
  wc -l




#-- A more applicable 'real' example
< data/games.csv |\
    awk -F"," '{print $12}' |\
    sed 1d |\
    sort | uniq -c | sort -nr | head -10 |\
    while read line; do
        echo $line | awk -v ORS=' ' {'print $1'};
        x=$(echo $line | awk {'print $2'});
        cat data/champion_info.json |\
        jq --argjson x $x '.[] | {id: .id, name: .name} | select(.id == $x) | .name'
    done |\
    column -t -N "Picks,Character" -s '"' -R "Picks"
