from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import json

#6. Find out the 10 states with the fewest cases in the U.S. → Word Cloud Chart
file_name = 'result6.json'


def drawChart_6():
    root = "./results" + '/' + file_name + '/' + file_name
    data = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            row=(str(js['state']),int(js['totalCases']))
            data.append(row)

    c = (
    WordCloud()
    .add("", data, word_size_range=[100, 20], shape=SymbolType.DIAMOND)
    .set_global_opts(title_opts=opts.TitleOpts(title="Least 10 cases in U.S by state"))
    .render("graph/graph6.html")
    )


if __name__ == '__main__':
    drawChart_6()