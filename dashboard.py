from pyecharts.charts import Page
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from selenium import webdriver
from bs4 import BeautifulSoup
import webbrowser
import os
import re

class Dashboard():
    '''
    用于布局pyehcharts生成的图表
    '''
    def __init__(self,browser_type,title = "Pyecharts-Dashboard",resolution = [1920,1080]):
        '''
        browser_type:str  firefox 或 chrome
        title:str  标题
        resolution:list  分辨率
        '''
        self.title = title
        self.charts = Page(page_title="Pyecharts-Dashboard")
        self.nums = 0
        self.browser_type = browser_type

        self._resolution = resolution #分辨率设置
        self.__ID_list = []
        self.__original_html_path = ""
        self.__browser = None

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self,value):
        if len(value) != 2:
            raise ValueError("resolution 设置错误")
        self._resolution = value

    @property
    def browser_type(self):
        return self._browser_type
    
    @browser_type.setter
    def browser_type(self,value):
        if value == 'chrome' or value == 'firefox':
            self._browser_type = value
        else:
            raise ValueError("browser_type参数错误，只支持firefox或chrome！")

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
        self.__ID_list.append(chart.chart_id)
        self.nums += 1

    def render(self):
        '''
        使用selenium渲染
        '''

        if 'html' not in os.listdir():
            os.mkdir('html')
        
        self.__original_html_path = os.getcwd() + os.sep + 'html' + os.sep + self.title + '.html'
        self.charts.render(self.__original_html_path)
        
        self.__add_js()
        if self.__browser is None:
            if self._browser_type == "chrome":
                self.__browser = webdriver.Chrome()
            else:
                self.__browser = webdriver.Firefox()
        
        #打开浏览器窗口
        self.__browser.get(r'file:///' + self.__add_js_html_path)
        
    def __add_js(self):
        '''
        解析html文档
        '''
        with open(self.__original_html_path,'r+',encoding = 'utf-8') as f:
            self.__original_html = f.read()
            html_bs = BeautifulSoup(self.__original_html,'lxml')

        head = html_bs.find('head')
        add_on_scripts = []

        #添加js资源
        add_on_scripts.append(html_bs.new_tag('script',**{
            'src':"https://libs.baidu.com/jquery/2.0.0/jquery.min.js",
            'type':"text/javascript"
            }))
        add_on_scripts.append(html_bs.new_tag('script',**{
            'src':"http://code.jquery.com/ui/1.12.1/jquery-ui.min.js",
            'type':"text/javascript",
            }))
        add_on_scripts.append(html_bs.new_tag('link',**{
            'href':"http://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css",
            'type':"text/css",
            'media':"all",
            'rel':"stylesheet"
            }))
        add_on_scripts.append(html_bs.new_tag('script',**{
            'src':"https://cdn.bootcss.com/css-element-queries/1.2.1/ResizeSensor.js",
        }))

        #设置div可拖动和大小可改动
        func_tags = html_bs.new_tag('script',**{'type':"text/javascript"})
        func = '''
                $(document).ready(function() {
        ''' 
        #js 参数设置  
        ra_para = r'{grid:5}'
        da_para = r'{grid:[10,10],snap: true}'

        for chart_id in self.__ID_list:
            func += r'$("#{}").resizable({});$("#{}").draggable({});'.format(chart_id,ra_para,chart_id,da_para)    
        func += r'});'

        #修改标签内容
        func_tags.string = func
        add_on_scripts.append(func_tags)
        
        #添加新标签
        for tag in add_on_scripts:
            head.append(tag)
        
        #设置子div样式，使子div与父div同步变化
        body = html_bs.find('body')

        #设置父div属性
        set_style_func = '$(".box").width({}).height({}).css("border-style", "dashed").css("border-width", "1px");'.format(self.resolution[0],self.resolution[1])
        
        for chart_id in self.__ID_list:
            set_style_func += '$("#{} > div:nth-child(1)").width("100%");'.format(chart_id)
            set_style_func += '$("#{} > div:nth-child(1)").height("100%");'.format(chart_id)
            set_style_func += '$("#{}").css({}).css("border-style", "dashed").css("border-width", "1px");'.format(chart_id,'{position: "absolute"}')
            set_style_func += "new ResizeSensor(jQuery('#{}'), function() {});".format(chart_id,'{' + 'chart_' +chart_id+'.resize();'+'}')
        set_style_func_tags = html_bs.new_tag('script')
        set_style_func_tags.string = set_style_func

        #插入标签
        body.append(set_style_func_tags)

        #设置容器边框
        box_tag = html_bs.new_tag('style')
        box_tag.string = '.box{}'.format("{ width:" + str(self.resolution[0]) +";height:" + str(self.resolution[1]) + ";border-style:dashed;border-width:1px;position:absolute;" + "}" )
        body.append(box_tag)
        #保存添加js后的文档    
        self.__add_js_html_path = os.getcwd() + os.sep + 'html' + os.sep + self.title + "_temp" + '.html'
        with open(self.__add_js_html_path,'w',encoding='utf-8') as f:
            f.write(str (html_bs))

    def __get_current_dashboard(self,filepath):
        '''
        获取当前的布局方案
        '''
        page_source = self.__browser.page_source
        page_source_soup = BeautifulSoup(page_source,'lxml')
        self.style_dict = {}

        pattern = re.compile(r"width:(.*?)px.*?height:(.*?)px.*?left:(.*?)px.*?top:(.*?)px")

        for chart_id in self.__ID_list:
            div = page_source_soup.find('div',{'id':chart_id})
            #匹配标签值，当div位于边缘位置时，没有top和left值
            position_para = pattern.findall(div['style'])
            if len(position_para) == 0:
                position_para = re.findall(r"width:(.*?)px.*?height:(.*?)px",div['style'])
            try:
                para = position_para[0]
                if len(para) == 4:
                    self.style_dict[chart_id] = "width:{}px;height:{}px;position:absolute;left:{}px;top:{}px;".format(para[0],para[1],para[2],para[3])
                elif len(para) == 2:
                    self.style_dict[chart_id] = "width:{}px;height:{}px;position:absolute;".format(para[0],para[1])
                else:
                    print("获取布局异常,位置参数个数为{}".format(len(para)))
            except Exception as e:
                print('获取布局错误：{}'.format(e))
                return

        html_bs = BeautifulSoup(self.__original_html,'lxml')
        for chart_id,style in self.style_dict.items():
            div = html_bs.find('div',{'id':chart_id})
            div['style'] = style
        
        
        with open(filepath,'w',encoding = 'utf-8') as f:
            f.write(str(html_bs))

    def preview(self):
        '''
        预览布局
        '''
        preview_html_path = os.getcwd() + os.sep + 'html' + os.sep + self.title + "_preview" + '.html'
        self.__get_current_dashboard(preview_html_path)
        webbrowser.open(preview_html_path)

    def save(self):
        '''
        保存结果
        '''
        self.__get_current_dashboard(self.__original_html_path)

    def __del__(self):
        if self.__browser is not None:
            self.__browser.quit()