from bs4 import BeautifulSoup
import requests 
from tqdm import tqdm 
import re 

def scraper(candidate, party, year, candidate_url):
	r2 = requests.get(candidate_url)
	t2 = r2.text

	s2 = BeautifulSoup(t2, 'html.parser')
	attrs = {'class': None, 'href': True, 'width': None}
	samples = s2.find_all('a', attrs = attrs)
	samples = samples[13:-1]

	root = 'http://www.presidency.ucsb.edu/'
	urls = [] 

	for sample in samples: 
		url = root + sample['href'][2:]
		urls.append(url)
			
	print 'collecting speeches for ' + candidate + ' , year ' + str(year)
	speeches = []
	for url in tqdm(urls):
		speeches.append(get_speech(url))
		
	speeches = ' '.join(speeches) 

	save_file = str(year) + '_' + party + '_' + candidate + '.txt'
	print 'saving speeches to txt' 
	with open(save_file, 'a') as f:
		f.write(speeches)
	return 
	
def get_speech(speech_url):
	
	r1 = requests.get(speech_url) 
	t1 = r1.text 
	s1 = BeautifulSoup(t1, 'html.parser')
	samples = s1.find_all('span', 'displaytext')
	return samples[0].text.encode('utf8') 
	
	
def get_candidates(election_url):
	
	def conditions(tag):
		if tag.name != 'span':
			return False 
		c1 = tag['class'] == ['roman']
		exp = re.compile('(?<=\w)\s(?=\w)')
		temp = [m.start() for m in re.finditer(exp, tag.text)]
		c2 = len(temp) == 1
		c3 = 'Party' not in tag.text 
		return c1 and c2 and c3 
		
	def collect_candidate_url(text):
		names = [] 
		s3 = BeautifulSoup(text, 'html.parser')
		samples = s3.find_all('span', 'roman')
		samples = s3.find_all(conditions) 
		exp = re.compile('(?<=\W)\w')
		for sample in samples:
			start = [m.start() for m in re.finditer(exp, sample.text)][-1]
			names.append(sample.text[start:].strip())
		samples = s3.find_all('a', text='campaign speeches')
		root = 'http://www.presidency.ucsb.edu/'
		urls = [] 
		for sample in samples: 
			urls.append(sample['href'])
		candidates = {} 
	
		for i in range(len(names)):
			candidates[names[i]] = root + urls[i] 
		return candidates 
	
	year = election_url[31:35]
	r3 = requests.get(election_url)
	t3 = r3.text
	split = t3.index('Republican Party')
	d = t3[:split]
	r = t3[split:]
	
	r_candidates = collect_candidate_url(r)
	d_candidates = collect_candidate_url(d)
	return r_candidates, d_candidates, year 

def get_election_speeches(election_url):
	reps, dems, year = get_candidates(election_url)	
	print 'collecting republican speeches'
	for rep, url in reps.items(): 
		scraper(rep, 'rep', year, url)
	print 'collecting democrat speeches' 
	for dem, url in dems.items(): 
		scraper(dem, 'dem', year, url)
	return 
	
elections = [
	'http://www.presidency.ucsb.edu/2016_election.php',
	'http://www.presidency.ucsb.edu/2012_election.php',
	'http://www.presidency.ucsb.edu/2008_election.php']


for election in elections:
	get_election_speeches(election)

	
candidates = {'clinton': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=70&campaign=2016CLINTON&doctype=5000',
	'sanders': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=107&campaign=2016SANDERS&doctype=5000', 
	'omalley': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=112&campaign=2016OMALLEY&doctype=5000',
	'chaffee': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=113&campaign=2016CHAFEE&doctype=5000', 
	'webb': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=118&campaign=2016WEBB&doctype=5000', 
	'trump': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=45&campaign=2016TRUMP&doctype=5000',
	'kasich':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=114&campaign=2016KASICH&doctype=5000',
	'cruz': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=103&campaign=2016CRUZ&doctype=5000',
	'rubio': 'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=105&campaign=2016RUBIO&doctype=5000', 
	'carson':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=108&campaign=2016CARSON&doctype=5000',
	'bush':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=101&campaign=2016BUSH&doctype=5000',
	'christie':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=117&campaign=2016CHRISTIE&doctype=5000',
	'fiorina':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=106&campaign=2016FIORINA&doctype=5000', 
	'santorum':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=96&campaign=2016SANTORUM&doctype=5000',
	'paul':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=104&campaign=2016PAUL&doctype=5000',
	'huckabee':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=77&campaign=2016HUCKABEE&doctype=5000',
	'pataki':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=111&campaign=2016PATAKI&doctype=5000',
	'graham':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=110&campaign=2016GRAHAM&doctype=5000',
	'jindal':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=116&campaign=2016JINDAL&doctype=5000',
	'walker':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=109&campaign=2016WALKER&doctype=5000',
	'perry':'http://www.presidency.ucsb.edu/2016_election_speeches.php?candidate=78&campaign=2016PERRY&doctype=5000'
	}
