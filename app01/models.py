from django.db import models

# Create your models here.

# #
# class Foo(models.Model):
#     name = models.CharField(max_length=1)




class Business(models.Model):
    #id
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32,null=True,default='SA')


#创建主机表
class Host(models.Model):
    nid = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=32,db_index=True)
    ip = models.GenericIPAddressField(db_index=True)
    port = models.IntegerField()
    b = models.ForeignKey("Business", to_field="id")

class Application(models.Model):
    name = models.CharField(max_length=32)
    r = models.ManyToManyField('Host')

# #自定义外检表
# class HostToApp(models.Model):
#     hobj = models.ForeignKey(to='Host',to_field='nid')
#     aobj = models.ForeignKey(to='Application',to_field='id')
