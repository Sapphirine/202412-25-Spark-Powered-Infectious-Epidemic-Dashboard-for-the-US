from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.charts import Bar
import json
from pyecharts.commons.utils import JsCode

# 9. Showing weird behavior abruptly increase or decrease → line overlap bar graphs

file_name = 'result9.json'


def drawChart_9():
    root = "./results" + '/' + file_name + '/' + file_name
    date = []
    cases = []
    deaths = []
    abnormal_dates = []
    abnormal_cases = []
    abnormal_deaths = []

    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            date.append(str(js['date']))
            cases.append(int(js['caseIncrease']))
            deaths.append(int(js['deathIncrease']))
            abnormal_dates.append(str(js['date']))
            if js.get('abnormalIncrease') or js.get('abnormalDecrease'):
                abnormal_cases.append(int(js['caseIncrease']))
                abnormal_deaths.append(int(js['deathIncrease']))
            else:
                abnormal_cases.append(0)
                abnormal_deaths.append(0)

    line = (
        Line()
        .add_xaxis(date)
        .add_yaxis("Cases", cases)
        .add_yaxis("Deaths", deaths)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="Weird Cases and Deaths"))
    )


    bar = (
        Bar()
        .add_xaxis(abnormal_dates)
        .add_yaxis("Abnormal Cases", abnormal_cases, label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis("Abnormal Deaths", abnormal_deaths, label_opts=opts.LabelOpts(is_show=False))
    )
    line.overlap(bar)

    line.render("graph/graph9.html")


if __name__ == '__main__':
    drawChart_9()
