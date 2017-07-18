# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser


class redis_information(models.Model):
    redis_id = models.IntegerField('节点编号', blank=True)
    cluster_id = models.IntegerField('集群编号', blank=True)
    cluster_name = models.CharField('集群名称', max_length=30, blank=True)
    host = models.CharField('集群IP地址', max_length=20, blank=True)
    port = models.IntegerField('redis端口', blank=True)
    role = models.CharField('集群中的角色', max_length=1)
    type = models.IntegerField('集群类型: 1.M-S/2.Cluster/0.已经下线', blank=True)
    master_id = models.IntegerField('主节点地址', blank=True)
    remark = models.CharField('备注', max_length=20)


class config_redis_command(models.Model):
    command = models.CharField('命令', max_length=30, blank=True)
    status = models.IntegerField('状态: 1.支持/0.不支持', blank=True)
