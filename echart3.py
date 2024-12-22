from pyecharts.components import Table
from pyecharts.options import ComponentTitleOpts
import json

# 3. Draw the cumulative number of diagnoses, deaths, and morbidity and mortality rates by state
# in the United States as of 22.5.12 --> Table
file_name = 'result3.json'


def drawChart_3():
    root = "./results" + '/' + file_name + '/' + file_name
    allState = []
    with open(root, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            js = json.loads(line)
            row = []
            row.append(str(js['state']))
            row.append(int(js['totalCases']))
            row.append(int(js['totalDeaths']))
            row.append(float(js['deathRate']))
            allState.append(row)

    table = Table()

    headers = ["State name", "Total cases", "Total deaths", "Death rate"]
    rows = allState
    table.add(headers, rows)
    table.set_global_opts(
        title_opts=ComponentTitleOpts(title="U.S. state-by-state outbreaks at a glance", subtitle="")
    )
    table.render("graph/graph3.html")


if __name__ == '__main__':
    drawChart_3()