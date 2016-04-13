# -*- coding: utf-8 -*-

INCIDENT_OWNER = u"""{incident.owner.userprofile.username_cn}：
"""
INCIDENT_DETAIL = u"""
设备编号：中集e栈{incident.terminal_no}
系统链接：http://127.0.0.1:8000/ticketmgr/detail/{incident.id}
小区地址：{incident.terminal_no.terminal_location} {incident.terminal_no.terminal_name}。
安装位置：大堂。
报障人姓名：{incident.creator.userprofile.username_cn}
故障描述：{incident.descrip}。
备注：{incident.remark}。
箱号：{incident.box_no}。
快递员电话：{incident.postman_mobile}。
收件人电话：{incident.take_mobile}。
快递单号：{incident.package_id}。
是否加急：{incident.priority}。
投递时间：{incident.deliver_time}。
取件时间：{incident.take_time}。
一级原因：故障。"""

MAIL_TEMPLATE = {
    "create": INCIDENT_OWNER +
              u"""您好，中集e栈{incident.terminal_no}发生新故障，请检查。""" +
              INCIDENT_DETAIL,
    "update": INCIDENT_OWNER +
              u"""您好，中集e栈{incident.terminal_no}故障内容已更新，请检查。""" +
              INCIDENT_DETAIL,
    "transfer": INCIDENT_OWNER +
                u"""您好，中集e栈{incident.terminal_no}故障已转由你处理，请检查。""" +
                INCIDENT_DETAIL,
    "reopen": INCIDENT_OWNER +
              u"""您好，中集e栈{incident.terminal_no}故障已重新开启，请检查。""" +
              INCIDENT_DETAIL
}

MIALSUBJECT = {"create": u"""{incident.terminal_no.terminal_name} 故障新建通知 """,
               "update": u"""{incident.terminal_no.terminal_name} 故障更新通知 """,
               "transfer": u"""{incident.terminal_no.terminal_name} 故障转入通知 """,
               "reopen": u"""{incident.terminal_no.terminal_name} 故障重开通知 """}