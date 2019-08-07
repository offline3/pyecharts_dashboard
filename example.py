#!/usr/bin/env python
# coding: utf-8

# In[3]:


from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Boxplot


# In[4]:


def boxpolt_base() -> Boxplot:
    v1 = [
        [850, 740, 900, 1070, 930, 850, 950, 980, 980, 880]
        + [1000, 980, 930, 650, 760, 810, 1000, 1000, 960, 960],
        [960, 940, 960, 940, 880, 800, 850, 880, 900]
        + [840, 830, 790, 810, 880, 880, 830, 800, 790, 760, 800],
    ]
    v2 = [
        [890, 810, 810, 820, 800, 770, 760, 740, 750, 760]
        + [910, 920, 890, 860, 880, 720, 840, 850, 850, 780],
        [890, 840, 780, 810, 760, 810, 790, 810, 820, 850, 870]
        + [870, 810, 740, 810, 940, 950, 800, 810, 870],
    ]
    c = Boxplot()
    c.add_xaxis(["expr1", "expr2"]).add_yaxis("A", c.prepare_data(v1)).add_yaxis(
        "B", c.prepare_data(v2)
    ).set_global_opts(title_opts=opts.TitleOpts(title="BoxPlot-基本示例"))
    return c


# In[6]:


bar = (
    Bar()
    .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
    .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
)
chart = boxpolt_base()


# In[8]:

#from pyecharts_dashboard.dashboard import Dashboard
from dashboard import Dashboard


# In[10]:


#示例化对象，需设置浏览器类型
dashboard = Dashboard('chrome')


# In[11]:


#添加图纸1
dashboard.add(bar)


# In[12]:


#添加图纸2
dashboard.add(chart)


# In[13]:


#打开UI界面
dashboard.render()


# In[17]:


#预览结果
dashboard.preview()


# In[15]:


#设置分辨率，并刷新
dashboard.resolution = (1920,1080)
dashboard.render()


# In[16]:


#保存当前布局,结果保存在当前文件下的html文件夹中
dashboard.save()


# In[ ]:




