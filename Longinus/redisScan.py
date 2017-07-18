# -*- coding: UTF-8 -*-

import redis
from rediscluster import StrictRedisCluster
from .models import config_redis_command


class redisScan(object):
    """
    def __init__(self, redisHost, redisPort, redisType, redisDb):
        self.host = redisHost
        self.port = int(redisPort)
        self.type = int(redisType)
        self.db = int(redisDb)
    """
    def splitCommand(self, content):
        """
        拆分命令
        """
        commandList = []

        for row in content.splitlines():
            commandList.append(row.split())

        return commandList

    def prepareCommand(self, content):
        finalResult = {'status': 0, 'msg': 'ok'}
        count = 1

        commandList = self.splitCommand(content)
        for row in commandList:
            count = config_redis_command.objects.filter(command=row[0], status=1) .count()

            if count == 0:
                finalResult['status'] = 1
                finalResult['msg'] = '不支持 %s ,请修改.' % (row[0])

                return finalResult
        return finalResult

    def getValues(self, redisHost, redisPort, redisType, redisDb, content):
        """
        执行命令,返回结果
        目前支持:
        string : get / mget / getrange / strlen
        hash : hget / hmget / hgetall / hlen / hkeys / hexists
        list : llen / lindex / lrange
        set : smembers / scard / sdiff / sinter / sismember / srandmember / sunion
        zset : zmembers / zcount
        other :
        """
        finalValue = []

        if redisType == 1:
            r = redis.Redis(host=redisHost, port=redisPort, db=redisDb)
        elif redisType == 2:
            startup_nodes = [{"host": redisHost, "port": redisPort}]
            r = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

        commandList = self.splitCommand(content)
        for row in commandList:
            key = row[0]
            command = ""
            command2 = ""
            tempList = []

            if key in ("get", "strlen", "hlen", "llen", "scard", "zcard"):
                command = "tempList.append(r.%s('%s'))" % (key, row[1])
                print(command)
                exec(command)

                for tempRow in tempList:
                    if isinstance(tempRow, bytes):
                        tempRow = str(tempRow, encoding='utf-8')

                    command2 = "finalValue.append(['%s %s','%s'])" % (key, row[1], tempRow)
                    exec(command2)

            elif key in ("mget", "hmget"):
                if key == "mget":
                    command = "tempList.append(r.%s(%s))" % (key, row[1:])
                    key = "get"
                    i = 0
                elif key == "hmget":
                    command = "tempList.append(r.%s('%s',%s))" % (key, row[1], row[2:])
                    key = "hget"
                    i = 1
                exec(command)

                for tempRow in tempList:
                    for listValue in tempRow:
                        i += 1
                        if isinstance(listValue, bytes):
                            listValue = str(listValue, encoding='utf-8')

                        if key == "get":
                            command2 = "finalValue.append(['%s %s','%s'])" % (key, row[i], listValue)
                        elif key == "hget":
                            command2 = "finalValue.append(['%s %s %s','%s'])" % (key, row[1], row[i], listValue)
                        exec(command2)

            elif key in ("getrange", "zcount"):
                command = "tempList.append(r.%s('%s', %d, %d))" % (key, row[1], int(row[2]), int(row[3]))
                exec(command)

                if isinstance(tempList[0], bytes):
                    tempList[0] = str(tempList[0], encoding='utf-8')

                command2 = "finalValue.append(['%s %s %d %d','%s'])" % (key, row[1], int(row[2]), int(row[3]), tempList[0])
                exec(command2)

            elif key in ("hget", "hexists", "sismember"):
                tmpKey = row[2].replace("\"","").replace("'","")
                command = "tempList.append(r.%s('%s','%s'))" % (key, row[1], tmpKey)
                exec(command)

                if isinstance(tempList[0], bytes):
                    tempList[0] = str(tempList[0], encoding='utf-8')

                command2 = "finalValue.append(['%s %s %s','%s'])" % (key, row[1], row[2], tempList[0])
                exec(command2)

            elif key in ("hgetall"):
                command = "tempList.append(r.%s('%s'))" % (key, row[1])
                exec(command)
                key = "hget"

                for tempRow in tempList:
                    if isinstance(tempRow, dict):
                        for dictKey in tempRow.keys():
                            dictValue = tempRow[dictKey]

                            if isinstance(dictKey, bytes):
                                dictKey = str(dictKey, encoding='utf-8')
                            if isinstance(dictValue, bytes):
                                dictValue = str(dictValue, encoding='utf-8')

                            command2 = "finalValue.append(['%s %s %s','%s'])" % (key, row[1], dictKey, dictValue)
                            exec(command2)

            elif key in ("hkeys", "smembers", "sdiff", "sinter", "sunion"):
                if key in ("hkeys", "smembers"):
                    command = "tempList.append(r.%s('%s'))" % (key, row[1])
                if key in ("sdiff", "sinter", "sunion"):
                    command = "tempList.append(r.%s(%s))" % (key, row[1:])
                exec(command)
                i = 1

                for tempRow in tempList:
                    for listValue in tempRow:
                        if isinstance(listValue, bytes):
                            listValue = str(listValue, encoding='utf-8')

                        if key in ("hkeys", "smembers"):
                            command2 = "finalValue.append(['%s %s (%d)','%s'])" \
                                    % (key, row[1], i, listValue)
                        if key in ("sdiff", "sinter", "sunion"):
                            command2 = "finalValue.append(['%s %s%s (%d)','%s'])" \
                                    % (key, row[1], "...", i, listValue)
                        exec(command2)
                        i += 1

            elif key in ("lindex"):
                command = "tempList.append(r.%s('%s',%d))" % (key, row[1], int(row[2]))
                exec(command)

                if isinstance(tempList[0], bytes):
                    tempList[0] = str(tempList[0], encoding='utf-8')

                command2 = "finalValue.append(['%s %s %d','%s'])" % (key, row[1], int(row[2]), tempList[0])
                exec(command2)

            elif key in ("lrange", "srandmember"):
                row.append('1')
                if int(row[2]) > 1000:
                    row[2] = 1000

                if key in ("lrange"):
                    command = "tempList.append(r.%s('%s',%d,%d))" % (key, row[1], int(row[2]), int(row[3]))
                    exec(command)
                    key = "lindex"
                    i = 0
                elif key in ("srandmember"):
                    command = "tempList.append(r.%s('%s',%d))" % (key, row[1], int(row[2]))
                    exec(command)
                    i = 1

                for tempRow in tempList:
                    for listValue in tempRow:
                        if isinstance(listValue, bytes):
                            listValue = str(listValue, encoding='utf-8')

                        if key in ("lindex"):
                            command2 = "finalValue.append(['%s %s %d','%s'])" % (key, row[1], i, listValue)
                        elif key in ("srandmember"):
                            command2 = "finalValue.append(['%s %s (%d)','%s'])" % (key, row[1], i, listValue)
                        exec(command2)
                        i += 1

        return finalValue
