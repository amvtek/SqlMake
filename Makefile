#
# Makefile
#

all:
	@echo "Makefile needs your attention"

.PHONY : lint
lint :
	flake8 sqlmake/

.PHONY : clean
clean :
	rm -rf *.egg-info
	rm -rf dist

# vim:ft=make
#
