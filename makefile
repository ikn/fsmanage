.PHONY: all doc doc-clean distclean

all:

doc:
	$(MAKE) -C doc/ html

doc-clean:
	$(MAKE) -C doc/ clean

distclean: doc-clean
