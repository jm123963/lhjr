import plotly_express as px
import plotly.graph_objects as go


fig = go.Figure(
    data=[go.Table(
        header=dict(values=list(data.columns),  # 表头取值是data列属性
                    fill_color='paleturquoise',  # 填充色和文本位置
                    align='left'),
        cells=dict(values=[data.性别,data.年龄,data.成绩],  # 单元格的取值就是每个列属性的Series取值
                   fill_color='lavender',
                   align='left'
                  )
        
    )]
)

fig.show()



