from pyecharts import options as opts
from pyecharts.charts import PictorialBar
from pyecharts.globals import SymbolType
import json

# 5. Draw the top 10 deaths in the U.S. by states → horizontal bar graphs
file_name = 'result5.json'


def drawChart_5():
    root = "./results" + '/' + file_name + '/' + file_name
    state = []
    totalDeath = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            state.insert(0, str(js['state']))
            totalDeath.insert(0, int(js['totalDeaths']))

    c = (
        PictorialBar()
        .add_xaxis(state)
        .add_yaxis(
            "",
            totalDeath,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol=SymbolType.ROUND_RECT,
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="PictorialBar- Top10 deaths in the U.S. by states"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            ),
        )
        .render("graph/graph5.html")
    )


if __name__ == '__main__':
    drawChart_5()
