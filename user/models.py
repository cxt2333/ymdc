from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=200)
    phone = models.IntegerField(blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(default=0)

    class Meta:
        db_table = 'user'


class Foods(models.Model):
    fid = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=255)
    food_price = models.FloatField()
    food_describe = models.CharField(max_length=255)
    sell_num = models.IntegerField(default=0)
    food_img = models.CharField(max_length=255)
    type_id = models.ForeignKey('Type', models.DO_NOTHING, db_column='type_id')

    class Meta:
        managed = False
        db_table = 'foods'
        ordering = ['fid']


class Type(models.Model):
    tid = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'type'


class Cart(models.Model):
    cid = models.AutoField(primary_key=True)
    c_food_num = models.IntegerField()
    c_is_select = models.IntegerField()
    food_id = models.ForeignKey('Foods', models.DO_NOTHING, db_column='food_id')
    user_id = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')

    class Meta:
        managed = False
        db_table = 'cart'


class Order(models.Model):
    oid = models.AutoField(primary_key=True)
    o_price = models.FloatField()
    o_time = models.DateTimeField(auto_now=True)
    o_status = models.IntegerField()
    user_id = models.ForeignKey('User', models.DO_NOTHING, db_column='user_id')

    class Meta:
        managed = False
        db_table = 'order'
        ordering = ['-o_time']


class Orderfoods(models.Model):
    ofid = models.AutoField(primary_key=True)
    of_food_num = models.IntegerField()
    food_id = models.ForeignKey('Foods', models.DO_NOTHING, db_column='food_id')
    order_id = models.ForeignKey('Order', models.DO_NOTHING, db_column='order_id')

    class Meta:
        managed = False
        db_table = 'orderfoods'
