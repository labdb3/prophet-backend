import numpy as np
import model.myGM.xlsx_reader as xlsx_reader
interval = [1963, 1968, 1972, 1977, 1987, 1993, 2006, 2009, 2013]
arr = np.array(interval)
res = xlsx_reader.first_order_GM(interval)
print(res)