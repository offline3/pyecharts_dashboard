from pyecharts.charts import Page
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re

class Dashboard():

    def __init__(self,title = "Pyecharts-Dashboard"):
        self.title = title
        self.charts = Page()
        self.nums = 0
        self.ID_list = []
        self.resolution = [1920,1080] #分辨率设置
        self.render_path = ""
        self.browser = None

    def add(self,chart):
        '''
        加入新图
        '''
        try:
            chart.chart_id = 'dashboard_subplot_{}'.format(self.nums)
        except AttributeError:
            print('参数错误！参数类型不能为{}'.format(type(chart)))
            return

        self.charts.add(chart)
        self.ID_list.append(chart.chart_id)
        self.nums += 1

    def render(self):
        '''
        使用selenium渲染
        '''
        self.render_path = os.getcwd() + os.sep + 'html' + os.sep + self.title + '.html'
        self.charts.render(self.render_path)

        self.add_js()
        if self.browser is None:
            self.browser = webdriver.Chrome()
        self.browser.get(r'file:///' + self.render_path)
    
    def revised_css():
        '''
        修改div属性
        '''
        
    def add_js(self):
        '''
        解析html文档
        '''
        with open(self.render_path,'r+',encoding = 'utf-8') as html:
            self.html_bs = BeautifulSoup(html,'lxml')

        head = self.html_bs.find('head')
        add_on_scripts = []

        #添加js资源
        add_on_scripts.append(self.html_bs.new_tag('script',**{
            'src':"https://libs.baidu.com/jquery/2.0.0/jquery.min.js",
            'type':"text/javascript"
            }))
        add_on_scripts.append(self.html_bs.new_tag('script',**{
            'src':"http://code.jquery.com/ui/1.12.1/jquery-ui.min.js",
            'type':"text/javascript",
            }))
        add_on_scripts.append(self.html_bs.new_tag('link',**{
            'href':"http://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css",
            'type':"text/css",
            'media':"all",
            'rel':"stylesheet"
            }))
        add_on_scripts.append(self.html_bs.new_tag('script',**{
            'src':"https://cdn.bootcss.com/css-element-queries/1.2.1/ResizeSensor.js",
        }))

        #设置div可拖动和大小可改动
        func_tags = self.html_bs.new_tag('script',**{'type':"text/javascript"})
        func = '''
                $(document).ready(function() {
        '''   
        ra_para = r'{grid:20}'
        da_para = r'{grid:[20,20],snap: true}'

        for chart_id in self.ID_list:
            
            func += r'$("#{}").resizable({});$("#{}").draggable({});'.format(chart_id,ra_para,chart_id,da_para)    
        func += r'});'

        func_tags.string = func
        add_on_scripts.append(func_tags)
        
        #添加新标签
        for tag in add_on_scripts:
            head.append(tag)
        
        #设置子div样式，使子div与父div同步变化
        body = self.html_bs.find('body')

        set_style_func = ''
        for chart_id in self.ID_list:
            set_style_func += '$("#{} > div:nth-child(1)").width("100%");'.format(chart_id)
            set_style_func += '$("#{} > div:nth-child(1)").height("100%");'.format(chart_id)
            set_style_func += '$("#{}").css({}).css("border-style", "dashed").css("border-width", "1px");'.format(chart_id,'{position: "absolute"}')
            set_style_func += "new ResizeSensor(jQuery('#{}'), function() {});".format(chart_id,'{' + 'chart_' +chart_id+'.resize();'+'}')
        set_style_func_tags = self.html_bs.new_tag('script')
        set_style_func_tags.string = set_style_func

        body.append(set_style_func_tags)

        new_html = str (self.html_bs)
        with open(self.render_path,'w',encoding='utf-8') as f:
            f.write(new_html)

    def refresh(self):
        '''
        更新画布
        '''
        page_source = self.browser.page_source
        page_source_soup = BeautifulSoup(page_source,'lxml')
        self.style_dict = {}

        pattern = re.compile(r"width:(.*?)px.*?height:(.*?)px.*?left:(.*?)px.*?top:(.*?)px")

        for chart_id in self.ID_list:
            div = page_source_soup.find('div',{'id':chart_id})
            #匹配标签值，当div位于边缘位置时，没有top和left值
            position_para = pattern.findall(div['style'])
            if len(position_para) == 0:
                position_para = re.findall(r"width:(.*?)px.*?height:(.*?)px",div['style'])
            try:
                    self.style_dict[chart_id] = position_para[0]
            except Exception as e:
                print('更新错误：{}'.format(e))

    def save(self):
        '''
        保存结果
        '''
        save_path = self.render_path + '_DashBoard' + r'.html'
    
    def __del__(self):
        if self.browser is not None:
            self.browser.quit()