import random
from ngram_score import ngram_score
import re

# load our quadgram model
with open ('quadgrams.txt', 'r') as ngram_file:
	ngrams = ngram_file.readlines()
fitness = ngram_score(ngrams)

# helper function, converts an integer 0-25 into a character
def i2a(i): return 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[i%26]

# decipher a piece of text using the substitution cipher and a certain key
def sub_decipher(text,key):
	invkey = [i2a(key.index(i)) for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
	ret = ''
	for c in text:
		if c.isalpha(): ret += invkey[ord(c.upper())-ord('A')]
		else: ret += c
	return ret

def break_simplesub(ctext,startkey=None):
	''' perform hill-climbing with a single start. This function may have to be called many times
		to break a substitution cipher. '''
	# make sure ciphertext has all spacing/punc removed and is uppercase
	ctext = re.sub('[^A-Z]','',ctext.upper())
	parentkey,parentscore = startkey or list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'),-99e99
	if not startkey: random.shuffle(parentkey)
	parentscore = fitness.score(sub_decipher(ctext,parentkey))
	count = 0
	while count < 1000:
		a = random.randint(0,25)
		b = random.randint(0,25)
		child = parentkey[:]
		# swap two characters in the child
		child[a],child[b] = child[b],child[a]
		score = fitness.score(sub_decipher(ctext,child))
		# if the child was better, replace the parent with it
		if score > parentscore:
			parentscore, parentkey = score, child[:]
			count = 0 # reset the counter
		count += 1
	return parentscore, parentkey

ctext = 'fvoxoxfvwdepagxmwxfpukleofxhwevefuygzepfvexwfvufgeyfryedojhwffoyhxcwgmlxeylawfxfurwfvoxecfezfvwbecpfpeejuygoyfefvwxfpwwfxojumwuxfuffvwawuxflecaazubwjwoyfvwyepfvwuxfhwfjlopwckaohvfjlzopwoaahevupgwpfvuywjoywjdwyfufjupouvbuaajwuaoupkecygjwoyfvwuxxdofvyeacmwbvuzoyhlecpwzcbroyhdofvfvwgcgwdveheffvwrwlxfelecpxuzwuygfvexwfvufbuyfgempoyhxcofxbplfelecpcybawxujfexwffawgoxkcfwxfvechvflecgfubrawfvoxdofvuaoffawjepwfubfmcffvwyuhuoyzcghwkubrwpxogeyfryediubroxvwgufwupwswplfojwofvoyrezaorxuyhmcfxvofjuyfvwlpwubepkepufoeyuygojukwpxeyozobufoeyezzpwwgejzepuaaleczoaagebrwfxaorwfvufxubeybwkfzepwohyfeluaadvoawaudlwpxjcggldufwpuygfpexxfuaaecfezmcxoywxxoxiuoazepjwuyglecpwxcoyhjwbosoaalwnvomoffvoxoyfvwbecpfpeejheeygeofogupwlecbeyhpufcaufoeyxfvwzauhoxxoybwywdbplkfejohvfvuswyxumubrgeepxocxweagbplkfe'

print "Substitution Cipher solver, you may have to wait several iterations"
print "for the correct result. Press ctrl+c to exit program."
# keep going until we are killed by the user
i = 0
maxscore = -99e99
while 1:
	i += 1 # keep track of how many iterations we have done
	score, key = break_simplesub(ctext,list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
	if score > maxscore:
		maxscore,maxkey = score,key[:]
		print '\nbest score so far:',maxscore,'on iteration',i
		print '	best key: '+''.join(maxkey)
		print '	plaintext: '+ sub_decipher(ctext,maxkey)
