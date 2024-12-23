from pyecharts import options as opts
from pyecharts.charts import Pie
import json

# 8.Death Rates in the United States ---> Pie Chart
file_name = 'result8.json'


def drawChart_8():
    root = "./results" + '/' + file_name + '/' + file_name
    values = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            if str(js['state']) == "USA":
                values.append(["Death(%)", round(float(js['deathRate']) * 100, 2)])
                values.append(["No-Death(%)", 100 - round(float(js['deathRate']) * 100, 2)])
    c = (
        Pie()
        .add("", values)
        .set_colors(["black", "orange"])
        .set_global_opts(title_opts=opts.TitleOpts(title="Death Rate in the U.S."))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render("graph/graph8.html")
    )


if __name__ == '__main__':
    drawChart_8()
