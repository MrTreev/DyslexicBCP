LETTERS=A AE B C D E F G H I J K L M N O P Q R S T U V W X Y Z
DROPCAPS=$(foreach char,${LETTERS},resources/images/dropcaps/${char}.png)
${DROPCAPS}: resources/fonts/.intermediate ;
.INTERMEDIATE: resources/fonts/.intermediate
resources/fonts/.intermediate: resources/scripts/glyph2dropcap.py
	fontforge \
		-script $< \
		resources/fonts/OpenDyslexic3-Regular.ttf \
		resources/images/dropcaps

PDFDEPS	+=	OpenDyslexic3.fontspec
PDFDEPS	+=	resources/preamble.sty
PDFDEPS	+=	${DROPCAPS}

BCPDEPS	+=	$(wildcard bcp/*.tex)
BCPDEPS	+=	$(wildcard bcp/parts/*.tex)
BCPDEPS	+=	${PDFDEPS}
BCP.pdf: BCP.tex ${BCPDEPS}
	Rscript build.r $< $@

KJVDEPS	+=	$(wildcard kjv/*.tex)
KJVDEPS	+=	${PDFDEPS}
KJV.pdf: KJV.tex ${KJVDEPS}
	Rscript build.r $< $@

%-a5.pdf: %.pdf
	pdfposter -mA5 $< $@

.DEFAULT_GOAL:=all
.PHONY: all
all: BCP.pdf KJV.pdf

.PHONY: release
release: BCP.pdf BCP-a5.pdf KJV.pdf KJV-a5.pdf

.PHONY: clean
clean:
	rm -f resources/fonts/.intermediate ${DROPCAPS} \
		BCP.aux BCP.fdb_latexmk BCP.fls BCP.log BCP.pdf BCP-a5.pdf \
		KJV.aux KJV.fdb_latexmk KJV.fls KJV.log KJV.pdf KJV-a5.pdf \
		$(wildcard pages/*.aux)
