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
