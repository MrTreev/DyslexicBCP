.PHONY: all
all: BCP.pdf

.PHONY: clean
clean:
	rm -f BCP.aux BCP.fdb_latexmk BCP.fls BCP.log BCP.pdf

BCP.pdf: BCP.tex $(wildcard pages/*.tex) OpenDyslexic3.fontspec $(wildcard resources/**)
	Rscript build.r
