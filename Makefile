ENV=. venv/bin/activate &&
PYTHON=$(ENV) python

all : requirements deviantart-photos kittens-photos

virtualenv.py :
	wget --no-check-certificate https://raw.github.com/pypa/virtualenv/master/virtualenv.py

venv : virtualenv.py
	python virtualenv.py -p python2.7 $@	

requirements : freeze.txt venv
	$(ENV) pip install -r $<
	touch $@

freeze.txt :
	$(ENV) pip freeze > $@

%-photos : requirements
	$(PYTHON) tumblrscraper.py $(@:-photos=) 100000

clean :
	rm -f *.db *.pyc
