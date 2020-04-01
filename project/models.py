from django.db import models
import uuid
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible

class project(models.Model):
    # 平台版,工地版用字段
    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPrjID = models.CharField(max_length=32, verbose_name='项目编码')
    FPrjname = models.CharField(max_length=128, verbose_name='项目名称')
    FShortname = models.CharField(max_length=128, verbose_name='项目简称', blank=True, null=True)
    FPrjtypeID = models.CharField(max_length=32, verbose_name='工程类别', blank=True, null=True)
    FPrjuseID = models.CharField(max_length=32, verbose_name='工程用途', blank=True, null=True)
    FPrjstate = models.CharField(max_length=32, verbose_name='工程状态', blank=True, null=True)
    FStructypeID = models.CharField(max_length=32, verbose_name='结构类型', blank=True, null=True)
    FPrjcost = models.FloatField(verbose_name='工程造价', default=0.0, blank=True, null=True)
    FArea = models.FloatField(verbose_name='建筑面积', default=0.0, blank=True, null=True)
    provid = models.CharField(max_length=32, verbose_name='所属省份', blank=True, null=True)
    cityid = models.CharField(max_length=32, verbose_name='所属城市', blank=True, null=True)
    areaid = models.CharField(max_length=32, verbose_name='所属区域', blank=True, null=True)
    FAddress = models.CharField(max_length=128, verbose_name='项目地址', blank=True, null=True)
    FLong = models.FloatField(verbose_name='经度', blank=True, null=True)
    FLat = models.FloatField(verbose_name='经度', blank=True, null=True)
    FSigDate = models.DateField(verbose_name='合同签订日期', blank=True, null=True)
    FSigbeginDate = models.CharField(max_length=100, verbose_name='合同工期', blank=True, null=True)
    FSigendDate = models.DateField(verbose_name='合同截止日期', blank=True, null=True)
    FBeginDate = models.CharField(max_length=100, verbose_name='实际工期', blank=True, null=True)
    FEndDate = models.DateField(verbose_name='实际截止日期', blank=True, null=True)
    FPrjmanager = models.CharField(max_length=32, verbose_name='项目经理', blank=True, null=True)
    FPrjmanagertel = models.CharField(max_length=32, verbose_name='项目经理电话', blank=True, null=True)
    FWinOrgID = models.CharField(max_length=32, verbose_name='中标单位', blank=True, null=True)
    FWinAtten = models.CharField(max_length=32, verbose_name='中标单位联系人', blank=True, null=True)
    FWinAttenTel = models.CharField(max_length=32, verbose_name='中标单位联系人电话', blank=True, null=True)
    FConstrOrgID = models.CharField(max_length=32, verbose_name='施工单位', blank=True, null=True)
    FConstrAtten = models.CharField(max_length=32, verbose_name='施工单位联系人', blank=True, null=True)
    FConstrAttenTel = models.CharField(max_length=32, verbose_name='施工单位联系人电话', blank=True, null=True)
    FBuildOrgID = models.CharField(max_length=32, verbose_name='建设单位', blank=True, null=True)
    FBuildAtten = models.CharField(max_length=32, verbose_name='建设单位联系人', blank=True, null=True)
    FBuildAttenTel = models.CharField(max_length=32, verbose_name='建设单位联系人电话', blank=True, null=True)
    FDesignOrgID = models.CharField(max_length=32, verbose_name='设计单位', blank=True, null=True)
    FDesignAtten = models.CharField(max_length=32, verbose_name='设计单位联系人', blank=True, null=True)
    FDesignAttenTel = models.CharField(max_length=32, verbose_name='设计单位联系人电话', blank=True, null=True)
    FSuperviseOrgID = models.CharField(max_length=32, verbose_name='监理单位', blank=True, null=True)
    FSuperviseAtten = models.CharField(max_length=32, verbose_name='监理单位联系人', blank=True, null=True)
    FSuperviseAttenTel = models.CharField(max_length=32, verbose_name='监理单位联系人电话', blank=True, null=True)
    FUserOrgID = models.CharField(max_length=32, verbose_name='业主单位', blank=True, null=True)
    FUserAtten = models.CharField(max_length=32, verbose_name='业主单位联系人', blank=True, null=True)
    FUserAttenTel = models.CharField(max_length=32, verbose_name='业务单位联系人电话', blank=True, null=True)
    FPrjdesc = models.CharField(max_length=1024, verbose_name='工程概况', blank=True, null=True)
    FStatus = models.BooleanField(default=True, verbose_name='状态')
    FManageORG = models.CharField(max_length=32, verbose_name='管理组织', blank=True, null=True)

    # 政务版用字段
    FAffDept = models.CharField(max_length=1000, verbose_name='所属科室', blank=True, null=True)
    FIsFullRenov = models.BooleanField(default=False, verbose_name='是否全装修交付')

    # 基础字段
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 疫情防控使用字段
    FIsReport = models.BooleanField(default=False, verbose_name='是否报备')
    FReportTime = models.DateTimeField(verbose_name='报备时间', blank=True, null=True)
    FIsRepeatWork = models.BooleanField(default=False, verbose_name='是否报备')
    FRepeatWorkTime = models.DateTimeField(verbose_name='复工时间', blank=True, null=True)
    FDutyPerson = models.CharField(max_length=50, verbose_name='留守人员', blank=True, null=True)

    #劳务实名制使用字段
    FcontractorCorpCode = models.CharField(max_length=100, verbose_name='总承包单位统一社会信用代码', blank=True, null=True)
    FcontractorCorpName = models.CharField(max_length=32, verbose_name='总承包单位名称', blank=True, null=True)
    FbuilderLicenses = models.CharField(max_length=20, verbose_name='施工许可证号', blank=True, null=True)

    class Meta:
        db_table = "T_Project"
