import json
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.sans-serif'] = ['Simsun']
matplotlib.rcParams['font.size'] = 11

data = json.load(open("partition/res.json", encoding="utf-8"))
plot_num = 1
for d in data:
    plt.subplot(3,3, plot_num)
    start_year = d['start_year']
    end_year = d['end_year']
    years = [i for i in range(start_year, end_year+1)]
    idx = start_year
    for part in d['partition_res']:
        length = len(part)
        end = idx + length
        x = [i for i in range(idx, end)]
        plt.plot(x, part)
        idx = end
    plot_num += 1
plt.show()
