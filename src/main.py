import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional
import networkx as nx
import matplotlib.pyplot as plt

from . import datatypes

df = pd.read_csv('data/history.csv')

# print(df)

def datetime_convert(date: str, time: str) -> datetime:
    time_format = '%m/%d/%Y %H:%M:%S'
    return datetime.strptime(date + " " + time, time_format)

def clump_sittings(df: pd.DataFrame) -> List[pd.DataFrame]:
    CLUMP_TIME: timedelta = timedelta(minutes=10)  # Time between next site to consider to be part of one sitting

    clumps: List[List[pd.DataFrame]] = [[]]

    if len(df) == 0:
        # Why did you give me a blank dataframe, lmao
        return []

    first_row = df.iloc[-1]

    last_time: datetime = datetime_convert(first_row['date'], first_row['time'])
    

    current_clump_head = 0

    # for row in reversed_df.iterrows():
    for idx in reversed(df.index):
        row = df.iloc[idx]
        # print(row)
        time_stamp: datetime = datetime_convert(row['date'], row['time'])

        # print(f"{last_time} - {time_stamp} = {last_time - time_stamp}")
        # Compares the time between the last row and the current row
        # Checks if it is greater than the clump time (meaning it is within a sitting)
        if last_time - time_stamp < CLUMP_TIME:
            clumps[current_clump_head].append(row)
        else:
            # Creates a new clump list
            clumps.append([row])
            current_clump_head += 1
        
        last_time = time_stamp

    return clumps

clumps = clump_sittings(df)
# print(clumps)
# clumps = clump_sittings(df)

graphs: List[nx.DiGraph] = []

for clump in clumps:
    graph = nx.DiGraph()

    last_domain = ""
    last_time: datetime = datetime_convert(clump[0]['date'], clump[0]['time'])
    last_node = datatypes.search(
        title="",
        domain="",
        url="",
        time=last_time,
    )
    for search in clump:
        current_domain=search['url'].split('//')[1].split('/')[0]
        if current_domain != last_domain:
            current_time = datetime_convert(search['date'], search['time'])
            new_node = datatypes.search(
                title=search['title'],
                domain=current_domain,
                url=search['url'],
                time=current_time,
                duration=current_time-last_time
            )
            # print(f"Domain: {current_domain} | {current_time} - {last_time} = {current_time - last_time}")
            last_time = current_time
            last_domain = current_domain
        graph.add_edge(last_node, new_node)
    graphs.append(graph)

G = graphs[0]
# print(G.edges)
print(nx.info(G))
nx.draw_networkx(G, pos = nx.spring_layout(G))
plt.savefig("test.png")
# def plot_graphs(graphs: List[nx.DiGraph]):
#     for graph in graphs:
#         nx.draw(graph, with_labels=True)