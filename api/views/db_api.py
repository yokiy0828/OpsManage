#!/usr/bin/env python  
# _#_ coding:utf-8 _*_
from rest_framework import viewsets,permissions
from api import serializers
from OpsManage.models import *
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import permission_required
from OpsManage.tasks.sql import sendOrderNotice
from orders.models import Order_System
from OpsManage.data.base import MySQLPool
from django.http import JsonResponse
from OpsManage.utils.logger import logger
from OpsManage.utils import mysql as MySQL

@api_view(['POST' ])
@permission_required('OpsManage.can_add_database_server_config',raise_exception=True)
def db_list(request,format=None):
    """
    List all order, or create a server assets order.
    """     
    if request.method == 'POST':
        serializer = serializers.DataBaseServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_required('OpsManage.can_change_database_server_config',raise_exception=True)
def db_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = DataBase_Server_Config.objects.get(id=id)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    if request.method == 'PUT':
        serializer = serializers.DataBaseServerSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_database_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
@api_view(['POST' ])
@permission_required('OpsManage.can_add_inception_server_config',raise_exception=True)
def inc_list(request,format=None):
    """
    List all order, or create a server assets order.
    """     
    if request.method == 'POST':
        serializer = serializers.InceptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_required('OpsManage.can_change_inception_server_config',raise_exception=True)
def inc_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Inception_Server_Config.objects.get(id=id)
    except Inception_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = serializers.InceptionSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_inception_server_config'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
# @api_view(['PUT', 'DELETE'])
# @permission_required('OpsManage.can_change_order_systemr',raise_exception=True)
# def sql_order_detail(request, id,format=None):
#     """
#     Retrieve, update or delete a server assets instance.
#     """
#     try:
#         snippet = Order_System.objects.get(id=id)
#     except Order_System.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'PUT':
#         if int(request.data.get('order_status')) == 4:
#             sendOrderNotice.delay(id,mask='【已取消】')  
#         elif int(request.data.get('order_status')) == 6:
#             sendOrderNotice.delay(id,mask='【已授权】')  
#         serializer = serializers.AuditSqlOrderSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#      
#     elif request.method == 'DELETE':
#         if not request.user.has_perm('OpsManage.can_delete_order_system'):
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)       
    
    
@api_view(['POST' ])
@permission_required('OpsManage.can_add_sql_custom_high_risk_sql',raise_exception=True)
def sql_custom_list(request,format=None):
    """
    List all order, or create a server assets order.
    """     
    if request.method == 'POST':
        serializer = serializers.CustomSQLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT', 'DELETE'])
@permission_required('OpsManage.can_change_custom_high_risk_sql',raise_exception=True)
def sql_custom_detail(request, id,format=None):
    """
    Retrieve, update or delete a server assets instance.
    """
    try:
        snippet = Custom_High_Risk_SQL.objects.get(id=id)
    except Custom_High_Risk_SQL.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = serializers.CustomSQLSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_custom_high_risk_sql'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    
@api_view(['PUT', 'DELETE'])
@permission_required('OpsManage.can_change_sql_execute_histroy',raise_exception=True)
def sql_exec_logs(request, id,format=None):
    try:
        snippet = SQL_Execute_Histroy.objects.get(id=id)
    except SQL_Execute_Histroy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
     
    if request.method == 'DELETE':
        if not request.user.has_perm('OpsManage.can_delete_sql_execute_histroy'):
            return Response(status=status.HTTP_403_FORBIDDEN)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST','GET'])
@permission_required('OpsManage.can_read_database_server_config',raise_exception=True)  
def db_status(request, id,format=None):
    try:
        dbServer = DataBase_Server_Config.objects.get(id=id)
    except DataBase_Server_Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    if request.method == 'POST':
        dataList = []
        mysql = MySQLPool(host=dbServer.db_host,port=dbServer.db_port,user=dbServer.db_user,passwd=dbServer.db_passwd,dbName=dbServer.db_name)
        version = mysql.execute(sql='SELECT VERSION() as version;')
        if isinstance(version, tuple):
            data = {}
            data['name'] = 'Version'
            try:
                data['value'] = version[1][0][0]
                dataList.append(data)
            except Exception,ex:
                data['value'] =  '未知'
                logger.warn(msg="获取MySQL版本信息失败: {ex}".format(ex=ex))
        status = mysql.execute(sql='show status;')
        if isinstance(status, tuple):
            for ds in status[1]:
                data = {}
                if ds[0].lower() in MySQL.keysList:
                    data['value'] = ds[1]
                    data['name'] = ds[0].capitalize()
                    dataList.append(data)
        logs = mysql.execute(sql='show global variables;')
        if isinstance(logs, tuple):
            for ds in logs[1]:
                data = {}
                if ds[0].lower() in MySQL.keysList:
                    data['value'] = ds[1]
                    data['name'] = ds[0].capitalize()
                    dataList.append(data)            
        return JsonResponse({"code":200,"msg":"success","data":dataList})
        