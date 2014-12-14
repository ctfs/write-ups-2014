# SECCON CTF 2014: Binary Karuta

**Category:** Web
**Points:** 400
**Description:**

> <http://binkaruta.pwn.seccon.jp/binkaruta/>

## Write-up

In Binary Karuta, the point is to correctly identify the CPU architecture of the binary hex dump displayed. If you wait over 60 seconds, it will time out and you will have to start again. You need to guess the correct CPU architecture 100 times in order to get the flag. There are no tricks to this. This game is to determine how well you are are reading binary hex with your eyes! There are around 35 different architectures being used for this so it will be good practice for you to get familiar with exotic binary.

### Exploration

Loading up the website shows a screen where an `xxd`-formatted string is shown of what is presumed to be a subset of some binary. Underneath there are seven architectures listed. Clicking one returns whether or not your response was correct and loads the next question. Sometimes there is a rate limit where you must wait 60 seconds before you can interact with the server again. Quick analysis suggests that you are rate limited based on IP address, not session.

### API

The JavaScript on the page suggests that there is one API endpoint to both get the question and answer a question. The state of which problem you are responding to is stored in the browser’s cookies. The two actions on the end point are as follows:

#### Get question

```bash
$ curl 'http://binkaruta.pwn.seccon.jp/cgi-bin/q.cgi'
m68k,m32r,mcore,mmix,i386,mips16,h8300,Bgkii/9G+hSoFCBUcHkD/3QJN230bfVt9m/wABANFg0lb3QAlA0jGwN5AgD/HSNDCHkAAAFa/hZuDURGInkCABAZEW9wABBe/hRIeQIAEBkRb3AAEIgQkABe/hRIQCB5AgAQDUFvcAAQXv4UGnkCABANQW9wABCIEJAAXv4UGg10jBKUAHkCAIAZEQ1AXv4USA1SDWENQF7+FBoNUUwEC4ELARGBEwkRgRMJb/EABg1S6gPiAA0iRwgNEgsCb/IABnkCALB5ARt8b3AAEIggkABe/hQaGTNv8wAOb/MADBlVGWZ5AgAsb3MABh0jTwwNMgkiCSNv8wAKQAh5AgCEbw==,0,0
```

The first seven values are the list of possible architectures for the binary. The next value is a base64-encoded string of the subset of the binary.

#### Answer Question

```python
import requests
cookies = {}

# Answer is a 1-based index of the list of possible architectures given with the question.
# It is assumed that the server pulls the question out of the session.
url = 'http://binkaruta.pwn.seccon.jp/cgi-bin/q.cgi'
resp = requests.post(url, cookies=cookies, data={ 'A': 1 })
print resp.text
# => arm,mips16,m6811,avr,mmix,sh64,v850,AQ8iDQ0B4wFaUeYBJl4iDQ0BOwINDj8BDRLADQIBIg0NDMgBDf3KAgz9wAEBAiIBARgiDg4B4wLHquYC6bYiDg4COwIOFD8BDgzADgIBIg4ODcgBDgzKAg0MwAEBAiIBARYi/f0B4wEQXeYB1i8i/f0BOwL9BT8B/RvA/QIBIv39DsgB/Q3KAg4NwAEBAiIBAQoiDAwB4wIUU+YCAkQiDAwCOwIMCT8BDBfADAIBIgwM/cgBDA7KAv0OwAEBAiIBAQgiDQ0B4wHmgeYB2KEiDQ0BOwINDj8BDRLADQIBIg0NDMgBDf3KAgz9wAEBAiIBARQiDg4B4wL7yOYC59MiDg==,3,0
```

The thing to note is that when you answer a question, whether you’re right or wrong, it sends you the next question. Also, it’s important to note the last two values: the `3` is the correct response for the previous question answered; the `0` is the number of consecutive correct responses you’ve given.

### Solution

I solved this problem by building a **Naive Bayes Classifier** to give me the probability that the binary belongs to any given architecture.
To do this I needed two things:

1. ***A dataset of binaries and their correct architectures***
2. ***A function that turns a binary into a set of features***

#### Scraping data

The thing to note from the API is that regardless of whether or not you guess the correct response, you get the correct answer to the problem.
This is a goldmine for scraping.
This means while playing the game, if your classifier guesses incorrectly, you can still get the correct response and log it for future training.
You can find my code to do this in [`solve.py`](solve.py).

#### Building features

My strategy was to first take the unique set of all non-overlapping 64-bit sequences in all the binaries. Then for a given binary, for all 64-bit sequences, list whether or not the binary contains the sequence (regardless of whether they overlap). The idea was that opcode formats are somewhat unique across architectures and that there should be a mapping from 64-bit sequences to opcode formats. I never validated this assumption beyond the fact that it seemed to work. The actual code for this is in [`solve.py`](solve.py), but the pseudocode is something like this:

```
for word in all_words:
  features['contains(%s)' % word] = (word in binary)
```

#### Training the model

The implementation of Naive Bayes I used was provided by [NLTK](http://www.nltk.org/). The API is extremely simple.

```python
labelled_data = [(compute_features(binary), architecture)
                  for binary, architecture in data]
classifier = nltk.NaiveBayesClassifier.train(labelled_data)

print classifer.classify(compute_features(new_binary))
# => architecture
```

### The script

To automate this process I had a script that would automatically flip flop between playing the game, collecting data, and retraining the classifier. After every 500 guesses, I would stop, retrain the classifier on the complete dataset, then use that in the scraper to try to guess the correct response. Every time I retrained the model, I would cross-validate to make sure that the predictive power of my model was in fact increasing with more data. If the predictive power of my model went down with more data, that would be a sign of a bad feature vector. Luckily that didn’t happen.

### Bootstrapping a dataset

Unfortunately due to rate limiting, I can’t just run this script with no data. Every time you guess an incorrect answer, the server will rate limit you for 60 seconds. However, if you simply hit the server with a fresh session and never send the server any data, you’ll almost never be rate limited.
We can use this to our advantage to bootstrap a dataset. Since we’re given seven possible architectures for the given binary, we know that at least one is correct. We can feed in every architecture into the classifier as a valid example for the given binary to create an approximate classifier.

The beauty of a Naive Bayes Classifier is that if your feature vector does in fact exhibit a unique pattern for a given architecture, the false examples won’t receive much weight because they won’t exhibit any statistical patterns unique from one another. I actually bootstrapped a decent classifier by scraping 7000 samples, 1000 of which were accurate. You can see my code to bootstrap the dataset in `bootstrap.py`.

#### Increasing predictiveness of the model

Since the server actually provides you a list of seven possible architectures for the binary, you can increase the predictive power of the model pretty easily. Instead of just using the `classify()` function, you can use the `prob_classify()` to get a list of the likelihood the binary belongs to each architecture. You can then just take the maximum of the intersection of the two sets.

### Flag

After running the script with bootstrapped data for a while, then trimming out the false data from the training set I had a classifier that was accurate enough to correctly guess the binary 170 times in a row. On the 100th consequtive request an addition field is returned. That field is the flag.

```
SECCON{EnjOy_KaRUtA}
```

## Other write-ups and resources

* none yet
