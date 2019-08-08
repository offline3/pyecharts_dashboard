

# Pyecharts-Dashboard

## 简介

本工具用于实现[pyecharts]("https://github.com/pyecharts/pyecharts")多图的布局，可在web端动态的调整图表大小及位置，方便数据大屏的构建。

## 依赖

pyecharts-dashboard使用selenium控制浏览器以提供图表布局的UI界面，使用selenium需要[下载驱动]("https://www.seleniumhq.org/download/")(目前在firefox和chrome测试均通过)

同时,需要安装以下python包

```bash
pip install bs4 selenium pyecharts
```

## 使用方法
本工具适合在交互式python环境中使用，如jupyter notebook等

```
from pyecharts_dashboard.dashboard import Dashboard
```

```
#示例化对象，需设置浏览器类型(chrome 或 firefox)
dashboard = Dashboard('chrome')

#添加图纸pyecharts图表
dashboard.add(bar)
dashboard.add(chart)

#打开UI界面
dashboard.render()#此时自动打开网页，在可在网页中进行图表的调整#


#预览结果
dashboard.preview()

#设置分辨率，并刷新（如果需要根据电脑调整分辨率可使用以下方法，调整分辨率的目的在于生成的Dashboard能够刚好布满整个电脑屏幕）
dashboard.resolution = (1920,1080)
dashboard.render()

#保存当前布局,结果保存在当前文件下的html文件夹中
dashboard.save()
```

## 待做

dashboard删减图表

dashboard图表修改
