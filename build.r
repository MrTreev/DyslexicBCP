args <- commandArgs(trailingOnly = TRUE)
options(tinytex.verbose = TRUE)
options(tinytex.clean = TRUE)
options(tinytex.engine = 'lualatex')
options(tinytex.engine_args = '-shell-escape')
if (length(args) != 2) stop("Usage: build.r <texfile> <output_pdf>", call. = FALSE)

tinytex::latexmk(args[1], pdf_file = args[2])