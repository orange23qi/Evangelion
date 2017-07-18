# -*- coding: UTF-8 -*-

import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import redis_information
from .redisScan import redisScan

redisScan = redisScan()


@csrf_exempt
def getRedisList(request):
    """
    根据redis类型,获取列表
    """
    if request.is_ajax():
        redisType = request.POST.get('redisType')
    else:
        redisType = request.POST('redisType')

    finalResult = {'status': 0, 'msg': 'ok', 'data': []}

    if redisType is None or len(redisType) == 0:
        finalResult['status'] = 1
        finalResult['msg'] = '请选择集群类型'
        return HttpResponse(json.dumps(finalResult), content_type='application/json')
    elif redisType == 'Master-Slave':
        typeId = 1
    elif redisType == 'Cluster':
        typeId = 2

    data = redis_information.objects.values("cluster_name").filter(type=typeId).distinct()
    result = []
    i = 0

    for row in data:
        result.append(data[i]["cluster_name"])
        i += 1

    finalResult['data'] = result

    return HttpResponse(json.dumps(finalResult), content_type='application/json')


@csrf_exempt
def execCommand(request):
    """
    执行redis命令,并返回结果
    """
    if request.is_ajax():
        redisCluster = request.POST.get('redisCluster')
        redisType = request.POST.get('redisType')
        commandContent = request.POST.get('commandContent')
        redisDbId = request.POST.get('redisDbId')
    else:
        redisCluster = request.get('redisCluster')
        redisType = request.get('redisType')
        commandContent = request.get('commandContent')
        redisDbId = request.get('redisDbId')

    finalResult = {'status': 0, 'msg': 'ok', 'data': []}

    if redisCluster is None or len(redisCluster) == 0:
        finalResult['status'] = 1
        finalResult['msg'] = '请选择集群'
        return HttpResponse(json.dumps(finalResult), content_type='application/json')
    elif commandContent is None or len(commandContent) == 0:
        finalResult['status'] = 1
        finalResult['msg'] = '请输入命令'
        return HttpResponse(json.dumps(finalResult), content_type='application/json')

    checkResult = redisScan.prepareCommand(commandContent)
    if checkResult['status'] == 1:
        finalResult['status'] = 1
        finalResult['msg'] = checkResult['msg']
        return HttpResponse(json.dumps(finalResult), content_type='application/json')

    if redisType == 'Master-Slave':
        typeId = 1
        data = redis_information.objects.get(cluster_name=redisCluster)
    elif redisType == 'Cluster':
        typeId = 2
        data = redis_information.objects.filter(cluster_name=redisCluster)[0]

    redisHost = data.host
    redisPort = data.port
    redisDb = int(redisDbId[2:])

    result = []
    result = redisScan.getValues(redisHost, redisPort, typeId, redisDb, commandContent)

    finalResult['data'] = result
    print(result)
    print(type(result[0][1]))

    return HttpResponse(json.dumps(finalResult), content_type='application/json')
