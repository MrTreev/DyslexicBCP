LETTERS=A AE B C D E F G H I J K L M N O P Q R S T U V W X Y Z
DROPCAPS=$(foreach char,${LETTERS},resources/images/dropcaps/${char}.png)
${DROPCAPS}: resources/fonts/.intermediate ;
.INTERMEDIATE: resources/fonts/.intermediate
resources/fonts/.intermediate: resources/fonts/export.py
	fontforge \
		-script $< \
		resources/fonts/OpenDyslexic3-Regular.ttf \
		resources/images/dropcaps

BCPDEPS	+=	$(wildcard pages/*.tex)
BCPDEPS	+=	$(wildcard pages/parts/*.tex)
BCPDEPS	+=	OpenDyslexic3.fontspec
BCPDEPS	+=	${DROPCAPS}
BCP.pdf: ${BCPDEPS} BCP.tex
	Rscript build.r BCP.tex

BCP-a5.pdf: BCP.pdf
	pdfposter -mA5 $< $@

.DEFAULT_GOAL:=all
.PHONY: all
all: BCP.pdf

.PHONY: release
release: BCP.pdf BCP-a5.pdf

.PHONY: clean
clean:
	rm -f resources/fonts/.intermediate ${DROPCAPS} \
		BCP.aux BCP.fdb_latexmk BCP.fls BCP.log BCP.pdf \
		BCP-a5.pdf \
		$(wildcard pages/*.aux)
