from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class elevatorinterfacesrv(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FElevatorID = models.CharField(max_length=32, verbose_name='电梯设备FID', blank=True, null=True)
    hoist_box_id = models.CharField(max_length=32, verbose_name='黑匣子编号', blank=True, null=True)
    cage_id = models.IntegerField(verbose_name='吊笼编号', blank=True, null=True)
    door_lock_state = models.IntegerField(verbose_name='门锁状态', blank=True, null=True)
    driver_identification_state = models.IntegerField(verbose_name='身份认证状态', blank=True, null=True)
    height_percentage = models.FloatField(verbose_name='高度百分比', blank=True, null=True)
    hoist_system_state = models.CharField(max_length=32, verbose_name='系统状态', blank=True, null=True)
    hoist_time = models.CharField(max_length=32, verbose_name='时间戳', blank=True, null=True)
    real_time_gradient1 = models.FloatField(verbose_name='实时倾斜度1', blank=True, null=True)
    real_time_gradient2 = models.FloatField(verbose_name='实时倾斜度2', blank=True, null=True)
    real_time_height = models.FloatField(verbose_name='实时高度', blank=True, null=True)
    real_time_lifting_weight = models.FloatField(verbose_name='实时起重量', blank=True, null=True)
    real_time_number_of_people = models.IntegerField(verbose_name='实时人数', blank=True, null=True)
    real_time_or_alarm = models.IntegerField(verbose_name='结果返回类型', blank=True, null=True)
    real_time_speed = models.FloatField(verbose_name='实时速度', blank=True, null=True)
    real_time_speed_direction = models.IntegerField(verbose_name='运行方向', blank=True, null=True)
    tilt_percentage1 = models.FloatField(verbose_name='倾斜百分比1', blank=True, null=True)
    tilt_percentage2 = models.FloatField(verbose_name='倾斜百分比2', blank=True, null=True)
    weight_percentage = models.FloatField(verbose_name='重量百分比', blank=True, null=True)
    system_state = models.CharField(max_length=32, verbose_name='系统状态', blank=True, null=True)
    wind_speed = models.FloatField(verbose_name='加工速度', blank=True, null=True)
    elevator_manager = models.CharField(max_length=32, verbose_name='安全员', blank=True, null=True)
    elevator_mgrtel = models.CharField(max_length=32, verbose_name='安全员电话', blank=True, null=True)
    elevator_oper = models.CharField(max_length=32, verbose_name='操作员', blank=True, null=True)
    elevator_opertel = models.CharField(max_length=32, verbose_name='操作员电话', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_ElevatorHisData'
