ENV=. venv/bin/activate &&
PYTHON=$(ENV) python

all : requirements

venv :
	virtualenv -p python2.7 $@	

requirements : freeze.txt venv
	$(ENV) pip install -r $<
	touch $@

freeze.txt :
	$(ENV) pip freeze > $@

scrape : requirements
	$(PYTHON) tumblrscraper.py

clean :
	
