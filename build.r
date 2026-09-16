args <- commandArgs(trailingOnly = TRUE)
options(tinytex.verbose = TRUE)
options(tinytex.engine = 'lualatex')
options(tinytex.engine_args = '-shell-escape')
if (length(args) != 1) stop("Invalid file to build", call. = FALSE)

tinytex::latexmk(args[1])