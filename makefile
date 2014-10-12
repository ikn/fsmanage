.PHONY: all doc doc-clean test coverage coverage-clean distclean

all:

doc:
	$(MAKE) -C doc/ html

doc-clean:
	$(MAKE) -C doc/ clean

test:
	PYTHONPATH=. python3 test.py -v

coverage:
	PYTHONPATH=. coverage3 run test.py
	coverage3 report
	coverage3 html

coverage-clean:
	$(RM) -r .coverage htmlcov

distclean: doc-clean coverage-clean
	find -regex '^\(.*/\)?__pycache__\(/.*\)?' -delete
