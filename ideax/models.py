from django.db import models
from django.utils import timezone
from enum import Enum
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.signals import user_logged_in
from django.urls import reverse
from decouple import config
import random
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from martor.models import MartorField


def check_user_profile(sender, user, request, **kwargs):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile()
        user_profile.user = request.user
        user_profile.save()
        request.user.groups.add(Group.objects.get(name=settings.GENERAL_USER_GROUP))

user_logged_in.connect(check_user_profile)

class Phase(Enum):
    GROW     = (1, _('Discussion'), 'discussion', 'comments')
    RATE     = (2, _('Evaluation'), 'rate','clipboard')
    IDEATION = (3, _('Ideation'), 'ideation','ideation')
    APROVED  = (4, _('Approval'), 'aproved','star')
    ACT      = (5, _('Evolution'), 'develop','tasks')
    DONE     = (6, _('Done'), 'done', 'check')
    ARCHIVED = (7, _('Archived'), 'archived', 'archive')
    PAUSED   = (8, _('Paused'), 'paused', 'pause')


    def __init__(self, id, description, css_class, icon_class):
        self.id = id
        self.description = description
        self.css_class =  css_class
        self.css_icon_class = icon_class;


    @classmethod
    def choices(cls):
        return tuple((x.id, x.description) for x in cls)

    @classmethod
    def get_phase_by_id(cls, id):
        for temp in cls:
            if temp.id == id:
                return temp
        return None

    @classmethod
    def get_css_class(cls, id):
        return cls.get_phase_by_id(id)

class Phase_History(models.Model):
    current_phase = models.PositiveSmallIntegerField()
    previous_phase = models.PositiveSmallIntegerField()
    date_change = models.DateTimeField('data da mudança')
    idea = models.ForeignKey('Idea',on_delete=models.DO_NOTHING)
    author = models.ForeignKey('UserProfile',on_delete=models.DO_NOTHING)
    current = models.BooleanField()

class Criterion(models.Model):
    description = models.CharField(max_length=40)
    peso = models.IntegerField()

    def __str__(self):
        return self.description

class Evaluation_Item(models.Model):
    value = models.IntegerField(default=0)
    criterion = models.ForeignKey(Criterion,on_delete=models.PROTECT)

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    discarded = models.BooleanField(default=False)

    def get_all_image_header(self):
        return self.category_image_set.all()

    def __str__(self):
        return self.title

class Category_Image(models.Model):
    description = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/')
    category = models.ForeignKey('Category', models.SET_NULL,null=True)

    @classmethod
    def get_random_image(cls, category):
        id_list = Category_Image.objects.filter(category=category).values_list('id', flat=True)
        if id_list:
            return Category_Image.objects.get(id=random.choice(list(id_list)))
        return None

class Idea(models.Model):
    title = models.CharField(max_length=200)
    oportunity = models.TextField(max_length=2500, null=True)
    solution = models.TextField(max_length=2500, null=True)
    target = models.TextField(max_length=500, null=True)
    creation_date = models.DateTimeField('data criação')
    author = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    category = models.ForeignKey('Category', models.SET_NULL,null=True)
    discarded = models.BooleanField(default=False)
    score = models.FloatField(default=0)
    category_image = models.CharField(max_length=200, default=settings.MEDIA_URL+'category/default.png' )
    summary = models.TextField(max_length=140, null=True, blank=False)
    challenge = models.ForeignKey('Challenge', models.SET_NULL,null=True, blank=True)

    def count_popular_vote(self, like_boolean):
        return self.popular_vote_set.filter(like=like_boolean).count()
    def count_dislikes(self):
        return self.count_popular_vote(False)
    def count_likes(self):
        return self.count_popular_vote(True)
    def get_current_phase_history(self):
        return self.phase_history_set.get(current=True)
    def get_current_phase(self):
        return Phase.get_phase_by_id(self.phase_history_set.get(current=True).current_phase)
    def get_absolute_url(self):
        return "/idea/%i/" % self.id
    def get_approval_rate(self):
        sum = self.count_likes() + self.count_dislikes()
        if sum > 0:
            return self.count_likes()/sum*100
        else:
            return 0

class Challenge(models.Model):
    image = models.ImageField(upload_to='challenges/')
    title = models.CharField(max_length=100)
    summary = models.TextField(max_length=140, null=True, blank=False)
    requester = models.CharField(max_length=140, null=True, blank=False)
    description = models.TextField(max_length=2500)
    limit_date =  models.DateTimeField()
    active = models.BooleanField(default=True)
    author = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    featured = models.BooleanField(default=False)
    category = models.ForeignKey('Category', models.SET_NULL,null=True)
    discarted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Vote(models.Model):
    evaluation_item = models.ForeignKey(Evaluation_Item,on_delete=models.PROTECT)
    value = models.IntegerField()
    voter = models.ForeignKey('UserProfile',on_delete=models.PROTECT)
    idea = models.ForeignKey('Idea',on_delete=models.PROTECT)
    voting_date = models.DateTimeField('data da votação')

class Popular_Vote(models.Model):
    like = models.BooleanField()
    voter = models.ForeignKey('UserProfile',on_delete=models.PROTECT)
    voting_date = models.DateTimeField()
    idea = models.ForeignKey('Idea',on_delete=models.PROTECT)

class Comment(MPTTModel):
    idea = models.ForeignKey('Idea',on_delete=models.PROTECT)
    author = models.ForeignKey('UserProfile',on_delete=models.PROTECT)
    raw_comment = models.TextField()
    parent = TreeForeignKey('self', related_name='children',
                            null=True, blank=True, db_index=True,on_delete=models.PROTECT)
    date = models.DateTimeField()
    comment_phase = models.PositiveSmallIntegerField()
    deleted = models.BooleanField(default=False)
    ip = models.CharField(max_length=20, null=True)

    class MPTTMeta:
        order_insertion_by = ['-date']



class UserProfile (models.Model):
    user = models.OneToOneField('auth.User',on_delete=models.PROTECT)
    use_term_accept = models.NullBooleanField(default=False)
    acceptance_date = models.DateTimeField(null=True)
    ip = models.CharField(max_length=20, null=True)
    manager = models.NullBooleanField(default=False)

    def __str__(self):
        return self.user.username


class Dimension(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    weight = models.IntegerField()
    init_date = models.DateTimeField()
    final_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

class Category_Dimension(models.Model):
    description = models.CharField(max_length=200)
    value = models.IntegerField()
    dimension = models.ForeignKey('Dimension',on_delete=models.PROTECT)

    def __str__(self):
        return self.description

class Evaluation(models.Model):
    valuator = models.ForeignKey('UserProfile',on_delete=models.PROTECT)
    idea = models.ForeignKey('Idea',on_delete=models.PROTECT)
    dimension = models.ForeignKey('Dimension',on_delete=models.PROTECT)
    category_dimension = models.ForeignKey('Category_Dimension',on_delete=models.PROTECT)
    evaluation_date = models.DateTimeField()
    dimension_value = models.IntegerField()
    note = models.TextField(null=True)

class Use_Term(models.Model):
    creator = models.ForeignKey('UserProfile',on_delete=models.PROTECT)
    term = models.TextField(max_length=12500)
    init_date = models.DateTimeField()
    final_date = models.DateTimeField()

    @property
    def is_past_due(self):
        if timezone.now() < self.final_date:
            return True
        return False

    def is_invalid_date(self):
        if self.final_date < self.init_date:
            return True
        return False
