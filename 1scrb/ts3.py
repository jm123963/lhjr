import pandas as pd
from jinja2 import Environment, FileSystemLoader


data = {'strategy_name': '第一个策略',
        'start_time': '2020-01-01',
        'end_time': '2021-06-01',
        'money': 20000}

env = Environment(loader=FileSystemLoader('./'))



template = env.get_template('template.html')

with open("out.html", 'w+', encoding='utf-8') as f:
    out = template.render(strategy_name=data['strategy_name'],
                          start_time=data['start_time'],
                          end_time=data['end_time'],
                          money=data['money'])
    f.write(out)
    f.close()