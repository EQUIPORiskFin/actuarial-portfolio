install.packages("reticulate")
reticulate::install_miniconda()
library(reticulate)
py_config()
py_run_string("
import numpy as np 
x=np.random.normal(0,1,1000)
print(x.mean())
")
py_install(c("numpy","pandas","matplotlib","seaborn","statsmodels","openpyxl","pyxlsb","pyarrow"))
py_require("sklearn.model_selection")
library(reticulate)

py_run_string("import pyarrow; print(pyarrow.__version__)")
