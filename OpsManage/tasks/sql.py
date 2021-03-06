#!/usr/bin/env python  
# _#_ coding:utf-8 _*_ 
import json
from celery import task
from OpsManage.utils import base
from OpsManage.models import (Global_Config,Email_Config,
                              SQL_Execute_Histroy)
from orders.models import Order_System
from django.contrib.auth.models import User
from channels import Group as CGroups

@task  
def recordSQL(exe_user,exe_db,exe_sql,exec_status,exe_result=None):
    try:
        config = Global_Config.objects.get(id=1)
        if config.sql == 1:
            SQL_Execute_Histroy.objects.create(
                                      exe_user = exe_user,
                                      exe_db = exe_db,
                                      exe_sql = exe_sql,
                                      exec_status = exec_status,
                                      exe_result = exe_result
                                      )
        return True
    except Exception,e:
        print e
        return False 
    
@task  
def sendOrderNotice(order_id,mask):
    try:
        config = Email_Config.objects.get(id=1)
        order = Order_System.objects.get(id=order_id)
    except:
        return False
    if order.order_type == 1:
        order_type = '代码部署'
        order_content = order.project_order.order_content
    else:
        order_type = 'SQL更新'
        order_content = order_content = str(order.sql_audit_order.order_sql).replace(';',';<br>')
    content = """<strong>申请人：</strong>{user}<br> 
                 <strong>工单类型：</strong>{order_type}<br>
                 <strong>更新内容：</strong><br>{order_content}<br>
                 <strong>工单地址：</strong><a href='{site}/db/sql/order/run/{order_id}/'>点击查看工单</a><br>
                 <strong> 授权人：</strong>{auth}<br>
                 <strong>状态：</strong>{mask}<br>""".format(order_id=order_id,user=User.objects.get(id=order.order_user).username,
                                                          site=config.site,auth=User.objects.get(id=order.order_executor).username,
                                                          order_content=order_content,mask=mask,order_type=order_type)
    try:
        to_user = User.objects.get(id=order.order_executor)
    except Exception, ex:
        return ex
    if order.order_status == 1:to_username = User.objects.get(id=order.order_executor).username
    else:to_username = User.objects.get(id=order.order_user).username
    CGroups(to_username).send({'text': json.dumps({"title":"你有一条新的工单需要处理<br>","type":"info","messages":content})})
    if order.order_cancel:
        content += "<strong>撤销原因：</strong>{order_cancel}".format(order_cancel=order.order_cancel)

    if config.subject:subject = "{sub} {oub} {mask}".format(sub=config.subject,oub=order.order_subject,mask=mask)
    else:subject = "{oub} {mask}".format(mask=mask,oub=order.order_subject)
    if config.cc_user:
        cc_to = config.cc_user
    else:cc_to = None
    base.sendEmail(e_from=config.user,e_to=to_user.email,cc_to=cc_to,
                   e_host=config.host,e_passwd=config.passwd,
                   e_sub=subject,e_content=content)
    return True    