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



class envinterfacesrv(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FCommandType = models.IntegerField(verbose_name='命令类型', default=2, blank=True, null=True)
    FDeviceId = models.CharField(max_length=32, verbose_name='设备编号', blank=True, null=True)
    FSRCTimestamp = models.IntegerField(verbose_name='原始时间戳', blank=True, null=True)
    FTimestamp = models.DateTimeField(verbose_name='获取时间', blank=True, null=True)
    FSPM = models.FloatField(verbose_name='SPM粉尘数据', blank=True, null=True)
    FPM25 = models.FloatField(verbose_name='PM2.5数据', blank=True, null=True)
    FPM10 = models.FloatField(verbose_name='PM10数据', blank=True, null=True)
    FTYPE = models.IntegerField(verbose_name='数据类型', blank=True, null=True)
    FWIND_SPEED = models.FloatField(verbose_name='风速', blank=True, null=True)
    FWIND_DIRECT = models.FloatField(verbose_name='风向度数', blank=True, null=True)
    FWIND_DIRECT_STR = models.CharField(max_length=32, verbose_name='风向文字', blank=True, null=True)
    FTemperature = models.FloatField(verbose_name='温度', blank=True, null=True)
    FHumidity = models.FloatField(verbose_name='湿度', blank=True, null=True)
    FNoise = models.FloatField(verbose_name='噪音等效值', blank=True, null=True)
    FNoiseMax = models.FloatField(verbose_name='噪音峰值', blank=True, null=True)
    FLongitude = models.FloatField(verbose_name='经度', blank=True, null=True)
    FLatitude = models.FloatField(verbose_name='纬度', blank=True, null=True)
    FPressure = models.IntegerField(verbose_name='大气压值', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_EnvdetectionHisData'


class interfacesrvdata(models.Model):

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FCallSigCode = models.CharField(max_length=32, verbose_name='调用特征码', blank=True, null=True)
    FTag = models.CharField(max_length=20, verbose_name='标签', blank=True, null=True)
    FValue = models.CharField(max_length=20, verbose_name='值', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_InterfaceSrvData'