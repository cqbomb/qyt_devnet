#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# 参考文档
# http://visjs.org/network_examples.html

# 图片所在目录
DIR = '/static/images/top/'
EDGE_LENGTH_MAIN = 150

# 添加节点
nodes = []

nodes.append({'id': 1, 'label': 'IOS路由器', 'image': DIR + 'router_isr.png', 'shape': 'image'})
nodes.append({'id': 2, 'label': 'ASA防火墙', 'image': DIR + 'firepower2120.png', 'shape': 'image'})
nodes.append({'id': 3, 'label': 'Core_SW', 'image': DIR + 'nexus9200.png', 'shape': 'image'})
nodes.append({'id': 4, 'label': 'Access_SW1', 'image': DIR + 'nexus9200.png', 'shape': 'image'})
nodes.append({'id': 5, 'label': 'Access_SW2', 'image': DIR + 'nexus9200.png', 'shape': 'image'})
nodes.append({'id': 6, 'label': 'WIN7', 'image': DIR + 'desktop_new.png', 'shape': 'image'})
nodes.append({'id': 7, 'label': '互联网', 'image': DIR + 'internet_ico.png', 'shape': 'image'})

# 添加连线
edges = []

edges.append({'from': 1, 'to': 2, 'length': EDGE_LENGTH_MAIN, 'label': "IOS:E0/0 --- ASA G1"})  # 可以做注释
edges.append({'from': 1, 'to': 7, 'length': EDGE_LENGTH_MAIN, 'color': {'color': 'red'}})  # 可以做颜色
edges.append({'from': 2, 'to': 3, 'length': EDGE_LENGTH_MAIN, 'color': {'color': 'green'}, 'value': 8, 'title': 'CoreSW到ASA'})  # 调整粗细, 与线路描述
edges.append({'from': 3, 'to': 4, 'length': EDGE_LENGTH_MAIN})
edges.append({'from': 3, 'to': 5, 'length': EDGE_LENGTH_MAIN})
edges.append({'from': 4, 'to': 6, 'length': EDGE_LENGTH_MAIN})


@login_required()
def top(request):  # 返回拓扑图页面'top_map.html', 拓扑图使用过JS获取JSON数据后绘制的
    return render(request, 'top_map.html')


@login_required()
def top_json(request):  # 提供拓扑图绘制的JSON数据, 返回节点列表和连线列表
    return JsonResponse({'nodes': nodes, 'edges': edges})
