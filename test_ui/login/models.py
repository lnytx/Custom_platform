from django.db import models

# Create your models here.


class quanxian(models.Model):
    class Meta:  
        permissions = (('can_view','查看'), 
                       ('can_add','添加'),
                       ('can_edit','编辑'),
                       ('can_delete','删除'),
                       ('can_super','超级')
                       
                       )
