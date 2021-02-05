from django.db import models
import uuid
from six import python_2_unicode_compatible


# Create your models here.

@python_2_unicode_compatible
class personnel(models.Model):
    TYPE_CHOICES = (
        (None, '请选择数据'),
        (0, '管理人员'),
        (1, '班组长'),
        (2, '员工')
    )

    SEX_CHOICES = (
        (None, '请选择数据'),
        (0, '男'),
        (1, '女')
    )

    MARITAL_CHOICES = (
        (None, '请选择数据'),
        (0, '未婚'),
        (1, '已婚'),
        (2, '离异')
    )

    STATUS_CHOICES = (
        (None, '请选择数据'),
        (0, '登记'),
        (1, '退场'),
        (2, '禁用')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FName = models.CharField(max_length=32, verbose_name='人员姓名', blank=True, null=True)
    FType = models.IntegerField(choices=TYPE_CHOICES, default=2, verbose_name='员工类型')
    FWorktypeID = models.CharField(max_length=32, verbose_name='所属工种', blank=True, null=True)
    FGroupID = models.CharField(max_length=32, verbose_name='所属班组', blank=True, null=True)
    FTeamID = models.CharField(max_length=32, verbose_name='所属施工队', blank=True, null=True)
    FIsSafetrain = models.BooleanField(default=False, verbose_name='是否进行安全培训')
    FSpecialequ = models.BooleanField(default=False, verbose_name='是否操作特种设备')
    FSafetrainDate = models.DateField(blank=True, null=True, verbose_name='培训时间')
    FSafetrainHour = models.IntegerField(verbose_name='培训课时', default=0, blank=True, null=True)
    FEntranceannex = models.ImageField(upload_to='safetrain/', verbose_name='进场附件', blank=True, null=True)
    FIDcard = models.CharField(max_length=18, verbose_name='身份证号', blank=True, null=True)
    FIDcardbeginDate = models.DateField(blank=True, null=True, verbose_name='身份证有效起始日期')
    FIDcardendDate = models.DateField(blank=True, null=True, verbose_name='身份证有效结束日期')
    FIDcardIsIndefinite = models.BooleanField(default=False, verbose_name='身份证长期有效')
    FSex = models.IntegerField(choices=SEX_CHOICES, verbose_name='性别', blank=True, null=True)
    FNation = models.CharField(max_length=32, verbose_name='民族', blank=True, null=True)
    FBirthday = models.DateField(blank=True, null=True, verbose_name='出生日期')
    FNaviveplace = models.CharField(max_length=32, verbose_name='籍贯', blank=True, null=True)
    FHomeaddress = models.CharField(max_length=128, verbose_name='家庭住址', blank=True, null=True)
    FSignorg = models.CharField(max_length=32, verbose_name='签发机关', blank=True, null=True)
    FTel = models.CharField(max_length=32, verbose_name='联系方式', blank=True, null=True)
    FPolitident = models.CharField(max_length=32, verbose_name='政治面貌', blank=True, null=True)
    FSpeciality = models.CharField(max_length=32, verbose_name='特长', blank=True, null=True)
    FMarital = models.IntegerField(choices=MARITAL_CHOICES, verbose_name='婚姻状况', blank=True, null=True)
    FLevelofedu = models.CharField(max_length=32, verbose_name='文化程度', blank=True, null=True)
    FTempaddress = models.CharField(max_length=32, verbose_name='暂住地址', blank=True, null=True)
    FBank = models.CharField(max_length=32, verbose_name='开户银行', blank=True, null=True)
    FBankaccount = models.CharField(max_length=32, verbose_name='银行账号', blank=True, null=True)
    FEmercontact = models.CharField(max_length=32, verbose_name='紧急联系人', blank=True, null=True)
    FEmercontacttel = models.CharField(max_length=32, verbose_name='紧急联系人电话', blank=True, null=True)
    FPhoto = models.ImageField(upload_to='hrpic/', default='', verbose_name='照片', blank=True, null=True)
    FContractState = models.BooleanField(default=True, verbose_name='劳动合同')
    FQuitDate = models.DateTimeField(blank=True, null=True, verbose_name='退场日期')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FStatus = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name='状态')
    FWoTuGUID = models.CharField(max_length=32, verbose_name='沃土平台GUID', blank=True, null=True)
    FWoTuFaceGUID = models.CharField(max_length=1000, verbose_name='沃土平台人脸GUID', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_Personnel'
        ordering = ['FType', 'FWorktypeID']


class personcertif(models.Model):
    SKILL_CHOICES = (
        (None, '请选择数据'),
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
        (3, '特种工')
    )

    FID = models.UUIDField(primary_key=True, default=uuid.uuid1)
    FPID = models.CharField(max_length=32, blank=True, null=True)
    FCertitypeID = models.CharField(max_length=32, verbose_name='证书类别')
    FSkilllevel = models.IntegerField(choices=SKILL_CHOICES, verbose_name='技能等级', blank=True, null=True)
    FCertificateNo = models.CharField(max_length=32, verbose_name='证书编号')
    FIssueOrg = models.CharField(max_length=32, verbose_name='签发机关', blank=True, null=True)
    FIssueDate = models.DateField(blank=True, null=True, verbose_name='发证日期')
    FLimitDate = models.DateField(blank=True, null=True, verbose_name='有效日期')
    FDesc = models.CharField(max_length=1024, verbose_name='备注', blank=True, null=True)
    FCertiFilepath = models.ImageField(upload_to='certificate/', default='', verbose_name='证书', blank=True, null=True)
    CREATED_PRJ = models.CharField(max_length=32, verbose_name='所属项目', blank=True, null=True)
    CREATED_ORG = models.CharField(max_length=32, verbose_name='创建组织', blank=True, null=True)
    CREATED_BY = models.CharField(max_length=32, verbose_name='创建人', blank=True, null=True)
    CREATED_TIME = models.DateTimeField(blank=True, null=True, verbose_name='创建时间')
    UPDATED_BY = models.CharField(max_length=32, verbose_name='更新人', blank=True, null=True)
    UPDATED_TIME = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'T_PersonnelCertificate'




