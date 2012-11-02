ENV=. venv/bin/activate &&
PYTHON=$(ENV) python

all : deviantart-photos

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
	$(PYTHON) tumblrscraper.py $(@:-photos=) 10000
	touch $@

clean :
	rm -f *.db *.pyc
