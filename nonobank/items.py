# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy import Field


class NonobankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #---------------
    # 用途描述
    #---------------
    purpose = Field()           #借款用途
    description = Field()       #借款描述
    #---------------
    # 借入记录
    #---------------
    total_loan = Field()        #共计借入
    loan_num = Field()          #借款次数
    normal_pay_off = Field()    #正常还清
    overdue_pay_off = Field()   #逾期还清
    overdue = Field()           #逾期未还
    to_paid = Field()           #待还本金
    #---------------
    # 个人背景和行为
    #---------------
    userId = Field()            #用户ID
    role = Field()              #用户角色
    name = Field()              #用户名
    gender = Field()            #性别
    age = Field()               #年龄
    registration = Field()      #户籍
    # location = Field()          #所在地分开成省市
    province = Field()
    city = Field()
    #---------------
    # 如果是学生
    #---------------
    school_name = Field()       #学校名称
    major = Field()             #专业
    admission_time = Field()    #入学时间
    #---------------
    # 如果不是学生
    #---------------
    marriage = Field()          #婚姻情况
    education = Field()         #学历

