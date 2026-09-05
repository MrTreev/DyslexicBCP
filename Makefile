.PHONY: all
all: BCP.pdf

LETTERS=A AE B C D E F G H I J K L M N O P Q R S T U V W X Y Z
DROPCAPS=$(foreach char,${LETTERS},resources/images/dropcaps/${char}.png)
${DROPCAPS}: resources/fonts/.intermediate ;
.INTERMEDIATE: resources/fonts/.intermediate
resources/fonts/.intermediate: resources/fonts/export.py
	fontforge \
		-script $< \
		resources/fonts/OpenDyslexic3-Regular.ttf \
		resources/images/dropcaps

BCPDEPS	=	BCP.tex
BCPDEPS	+=	$(wildcard pages/*.tex)
BCPDEPS	+=	OpenDyslexic3.fontspec
BCPDEPS	+=	${DROPCAPS}
BCP.pdf: ${BCPDEPS}
	Rscript build.r

.PHONY: clean
clean:
	rm -f BCP.aux BCP.fdb_latexmk BCP.fls BCP.log BCP.pdf
