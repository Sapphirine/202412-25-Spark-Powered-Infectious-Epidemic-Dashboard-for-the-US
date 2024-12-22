from pyecharts import options as opts
from pyecharts.charts import Funnel
import json

# 7.Find the 10 states with the fewest deaths in the U.S. → Funnel Chart
file_name = 'result7.json'


def drawChart_7():
    root = "./results" + '/' + file_name + '/' + file_name
    data = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            data.insert(0, [str(js['state']), int(js['totalDeaths'])])

    c = (
        Funnel()
        .add(
            "State",
            data,
            sort_="ascending",
            label_opts=opts.LabelOpts(position="inside", font_size=12)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="Funnel Chart - Least 10 deaths in U.S by state",

            ),
            legend_opts=opts.LegendOpts(
                orient="horizontal",  # Makes the legend horizontal
                pos_top="90%",  # Places it at the bottom of the chart
                pos_left="center"  # Centers the legend horizontally
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True)
        )
        .render("graph/graph7.html")
    )


if __name__ == '__main__':
    drawChart_7()
