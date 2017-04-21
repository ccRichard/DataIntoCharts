# coding: utf-8

"""
    echarts.datastructure
    ~~~~~~~~~~~~~~~~~~~~~

    Datastructure for describing the chart types.
"""

import math
from .option import Series


class Line(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Line, self).__init__('line', name=name, data=data, **kwargs)

    # 计算数据list的中位数
    def get_median(self):
        data_list = self.data[:]
        data_list.sort()
        size = len(data_list)
        half = size // 2

        data_median = (float(data_list[half]) + float(data_list[~half])) / 2

        return data_median

    # 获取top99
    def get_top(self):
        data_list = list()
        for i in self.data:
            data_list.append(float(i))

        data_list.sort()
        size = len(data_list)

        index = int(math.ceil(size * 0.99) - 1)
        return data_list[index]

    @property
    def json(self):
        # print(self.data)
        """JSON format data."""
        json = {
            'type': self.type,
            'data': self.data,
            'markPoint': {
                'data': [
                    {'type': 'max', 'name': '最大值'},
                    {'type': 'min', 'name': '最小值'}
                ]
            },
            'markLine': {
             'data': [
                 # {'type': 'average', 'name': '平均值'},
                 {'name': '中位数', 'yAxis': self.get_median()},
                 {'name': 'top99', 'yAxis': self.get_top()}
             ]
            }
        }
        if self.name:
            json['name'] = self.name
        if self._kwargs:
            json.update(self._kwargs)

        return json


class Bar(Series):
    " Docs "
    def __init__(self, name=None, data=None, **kwargs):
        super(Bar, self).__init__('bar', name=name, data=data, **kwargs)


class Pie(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Pie, self).__init__('pie', name=name, data=data, **kwargs)


class Scatter(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Scatter, self).__init__(
            'scatter', name=name, data=data, **kwargs
        )


class EffectScatter(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(EffectScatter, self).__init__(
            'effectScatter', name=name, data=data, **kwargs
        )


class Radar(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Radar, self).__init__('radar', name=name, data=data, **kwargs)


class Treemap(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Treemap, self).__init__(
            'treemap', name=name, data=data, **kwargs
        )


class Boxplot(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Boxplot, self).__init__(
            'boxplot', name=name, data=data, **kwargs
        )


class Candlestick(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Candlestick, self).__init__(
            'candlestick', name=name, data=data, **kwargs
        )


class Heatmap(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Heatmap, self).__init__(
            'heatmap', name=name, data=data, **kwargs
        )


class Map(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Map, self).__init__('map', name=name, data=data, **kwargs)


class Parallel(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Parallel, self).__init__(
            'parallel', name=name, data=data, **kwargs
        )


class Lines(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Lines, self).__init__('lines', name=name, data=data, **kwargs)


class Graph(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Graph, self).__init__('graph', name=name, data=data, **kwargs)


class Sankey(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Sankey, self).__init__('sankey', name=name, data=data, **kwargs)


class Funnel(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Funnel, self).__init__('funnel', name=name, data=data, **kwargs)


class Gauge(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Gauge, self).__init__('gauge', name=name, data=data, **kwargs)


# The following chart types are only available in echarts 2 version.

class K(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(K, self).__init__('k', name=name, data=data, **kwargs)


class Force(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Force, self).__init__('force', name=name, data=data, **kwargs)


class Chord(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Chord, self).__init__('chord', name=name, data=data, **kwargs)


class Venn(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Venn, self).__init__('venn', name=name, data=data, **kwargs)


class Tree(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(Tree, self).__init__('tree', name=name, data=data, **kwargs)


class EventRiver(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(EventRiver, self).__init__(
            'eventRiver', name=name, data=data, **kwargs
        )


class WordCloud(Series):
    def __init__(self, name=None, data=None, **kwargs):
        super(WordCloud, self).__init__(
            'wordCloud', name=name, data=data, **kwargs
        )

VERSION_2 = (
    Line, Bar, Scatter, K, Pie, Radar, Chord, Force, Map,
    Gauge, Funnel, EventRiver, Venn, Treemap, Tree, WordCloud, Heatmap
)
VERSION_3 = (
    Line, Bar, Pie, Scatter, EffectScatter, Radar, Treemap, Boxplot,
    Candlestick, Heatmap, Map, Parallel, Lines, Graph, Sankey, Funnel, Gauge
)
VERSION_ALL = tuple(set(VERSION_2).union(set(VERSION_3)))
