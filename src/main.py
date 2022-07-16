import pandas as pd
from datetime import datetime, timedelta
from typing import List
import networkx as nx

from . import datatypes
df = pd.read_csv('data/history.csv')

print(df)

def datetime_convert(date: str, time: str) -> datetime:
    time_format = '%m/%d/%Y %H:%M:%S'
    return datetime.strptime(date + " " + time, time_format)

def clump_sittings(df: pd.DataFrame) -> List[pd.DataFrame]:
    CLUMP_TIME: timedelta = timedelta(minutes=10)  # Time between next site to consider to be part of one sitting

    clumps: List[List[pd.DataFrame]] = [[]]

    if len(df) == 0:
        # Why did you give me a blank dataframe, lmao
        return []

    reversed_df = df.iloc[::-1]
    
    first_row = reversed_df.iloc[0]

    last_time: datetime = datetime_convert(first_row['date'], first_row['time'])
    

    current_clump_head = 0

    for idx in reversed_df.index:
        row = reversed_df.iloc[idx]
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
# clumps = clump_sittings(df)

graphs: List[nx.DiGraph] = []

for clump in clumps:
    graph = nx.DiGraph()
    for search in clump:
        # print(search)
        data = datatypes.search(
            title=search['title'],
            domain=search['url'].split('//')[1].split('/')[0],
            url=search['url'],
            time=datetime_convert(search['date'], search['time'])
        )
        graph.add_node(data)
    graphs.append(graph)