from pyecharts import options as opts
from pyecharts.charts import Line
import json
from pyecharts.commons.utils import JsCode
from datetime import datetime

# 10. Prediction → line graphs

file1_name = 'result1.json'
file2_name = 'result10.json'


def drawChart_10():
    root = "./results" + '/' + file1_name + '/' + file1_name
    date = []
    cases = []
    deaths = []
    new_date = []
    predicted_cases = []
    predicted_deaths = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            date.append(str(js['date']))
            cases.append(int(js['cases']))
            deaths.append(int(js['deaths']))
            date_str = str(js['date'])
            date_object = datetime.strptime(date_str, "%Y-%m-%d")
            reference_date = datetime.strptime("2022-04-15", "%Y-%m-%d")
            if date_object <= reference_date:
                new_date.append(str(js['date']))
                predicted_cases.append(int(js['cases']))
                predicted_deaths.append(int(js['deaths']))

    root2 = "./results" + '/' + file2_name + '/' + file2_name
    with open(root2, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            new_date.append(str(js['date']))
            predicted_cases.append(int(js['predicted_cases']))
            predicted_deaths.append(int(js['predicted_deaths']))

    line1 = (
        Line()
        .add_xaxis(date)
        .add_yaxis("Cases", cases)
        .add_yaxis("Deaths", deaths)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

    )

    line2 = (
        Line()
        .add_xaxis(new_date)
        .add_yaxis("Predicted Cases", predicted_cases)
        .add_yaxis("Predicted Deaths", predicted_deaths)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Linear Regression Prediction"
            ),
            legend_opts=opts.LegendOpts(
                orient="horizontal",  # Makes the legend horizontal
                pos_top="90%",  # Places it at the bottom of the chart
                pos_left="center"  # Centers the legend horizontally)
            )
        )
    )

    line2.overlap(line1)
    line2.render("graph/graph10.html")


if __name__ == '__main__':
    drawChart_10()
