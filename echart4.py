from pyecharts import options as opts
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType
import json

# 4. Drawing the 10 most cases in the U.S. by states → Word Cloud Map
file_name = 'result4.json'


def drawChart_4():
    root = "./results" + '/' + file_name + '/' + file_name
    data = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            row = (str(js['state']), int(js['totalCases']))
            data.append(row)

    c = (
        WordCloud()
        .add("", data, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
        .set_global_opts(title_opts=opts.TitleOpts(title="Top10 cases in U.S by state"))
        .render("graph/graph4.html")
    )


if __name__ == '__main__':
    drawChart_4()