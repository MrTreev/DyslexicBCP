.PHONY: all
all: BCP.pdf

.PHONY: clean
clean:
	rm -f BCP.aux BCP.fdb_latexmk BCP.fls BCP.log BCP.pdf

BCP.pdf: BCP.tex
	Rscript build.r
