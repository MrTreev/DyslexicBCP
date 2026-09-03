options(tinytex.verbose = TRUE)
options(tinytex.engine = 'lualatex')
options(tinytex.engine_args = '-shell-escape')
tinytex::latexmk("BCP.tex")