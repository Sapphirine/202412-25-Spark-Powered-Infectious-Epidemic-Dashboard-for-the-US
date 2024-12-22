from pyecharts import options as opts
from pyecharts.charts import Line
import json


# 2. plot the number of new confirmed cases and deaths per day → line graphs

file_name = 'result2.json'


def drawChart_2():
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
            cases.append(int(js['caseIncrease']))
            deaths.append(int(js['deathIncrease']))

    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add_xaxis(xaxis_data=date)
        .add_yaxis(
            series_name="new confirmed cases",
            y_axis=cases,
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="Max")

                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(type_="average", name="Average")]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Daily New Confirmed Cases Line Chart in the United States",
                                      subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
        .render("graph/graph2-1.html")
    )
    (
        Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add_xaxis(xaxis_data=date)
        .add_yaxis(
            series_name="new confirmed death",
            y_axis=deaths,
            markpoint_opts=opts.MarkPointOpts(
                data=[opts.MarkPointItem(type_="max", name="Max")]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="Average"),
                    opts.MarkLineItem(symbol="none", x="90%", y="max"),
                    opts.MarkLineItem(symbol="circle", type_="max", name="Top"),
                ]
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Daily New Confirmed Deaths Line Chart in the United States", subtitle=""),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
        .render("graph/graph2-2.html")
    )


if __name__ == '__main__':
    drawChart_2()