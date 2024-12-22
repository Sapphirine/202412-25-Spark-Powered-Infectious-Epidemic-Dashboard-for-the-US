from pyecharts import options as opts
from pyecharts.charts import Bar
import json

# 1. Plot the cumulative number of confirmed cases and deaths per day → double bar graphs

file_name = 'result1.json'


def drawChart_1():
    root = "./results" + '/' + file_name + '/' + file_name
    date = []
    cases = []
    deaths = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            date.append(str(js['date']))
            cases.append(int(js['cases']))
            deaths.append(int(js['deaths']))

    d = (
        Bar()
        .add_xaxis(date)
        .add_yaxis("Cumulative daily cases", cases, stack="stack1")
        .add_yaxis("Cumulative daily deaths", deaths, stack="stack1")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Cumulative daily cases and deaths in the United States", pos_top='5%'))
        .render("graph/graph1.html")
    )


if __name__ == '__main__':
    drawChart_1()
