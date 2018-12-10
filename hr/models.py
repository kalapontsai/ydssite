from django.db import models
import django.utils.timezone as timezone
import datetime

#   cid name    type    notnull dflt_value  pk
#0   0   id  integer 1       1
#1   1   issue_date  datetime    1       0
#2   2   issuer  varchar(16) 1       0
#3   3   effect_date date    1       0
#4   4   badge_list  text    1       0
#5   5   note    text    0       0

class lunch(models.Model):
    issue_date = models.DateTimeField('填寫日期', default = timezone.now)
    issuer = models.CharField('填寫人',max_length=16)
    effect_date = models.DateField('停用日期', default=datetime.date.today)
    badge_list = models.TextField('停用者工號')
    note = models.TextField('備註',blank=True,null=True)
    
    def __str__(self): return (self.issue_date.strftime("%Y-%m-%d") + ' : ' + self.issuer + ' : ' + self.effect_date.strftime("%Y-%m-%d"))

class meeting_room(models.Model):
	int_room_number = models.IntegerField('會議室號碼', default = 0)
	datetime_issue = models.DateTimeField('預約日期', default = timezone.now)
	date_reserve = models.DateField('使用日期', default = timezone.now)
	time_start = models.TimeField('開始時間', default = timezone.now)
	time_end = models.TimeField('結束時間', default = timezone.now)
	char_topic = models.CharField('會議用途',max_length=255)
	txt_issuer_dep = models.TextField('申請人部門',max_length=16)
	txt_issuer_badge = models.TextField('申請人工號',max_length=6)
	txt_hr_badge = models.TextField('管理人工號',max_length=6, blank=True,null=True)
	datetime_approve = models.DateTimeField('確認時間', blank=True,null=True)
	note = models.TextField('備註',blank=True,null=True)

	def __str__(self): return (str(self.int_room_number) + ')' + self.datetime_issue.strftime("%Y/%m/%d %H:%M") + ' // '\
     + self.date_reserve.strftime("%Y/%m/%d") + ' - ' + self.time_start.strftime("%H:%M")\
      + '  => ' + self.char_topic + ' --- ' + self.txt_issuer_dep)
