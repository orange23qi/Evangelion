# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-11 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='redis_information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redis_id', models.IntegerField(blank=True, verbose_name='节点编号')),
                ('cluster_id', models.IntegerField(blank=True, verbose_name='集群编号')),
                ('cluster_name', models.CharField(blank=True, max_length=30, verbose_name='集群名称')),
                ('host', models.CharField(blank=True, max_length=20, verbose_name='集群IP地址')),
                ('port', models.IntegerField(blank=True, verbose_name='redis端口')),
                ('role', models.CharField(max_length=1, verbose_name='集群中的角色')),
                ('type', models.IntegerField(blank=True, verbose_name='集群类型: 1.M-S/2.Cluster/0.已经下线')),
                ('master_id', models.IntegerField(blank=True, verbose_name='主节点地址')),
                ('remark', models.CharField(max_length=20, verbose_name='备注')),
            ],
        ),
    ]