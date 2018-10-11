from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.PROTECT)
    use_term_accept = models.NullBooleanField(default=False)
    acceptance_date = models.DateTimeField(null=True)
    ip = models.CharField(max_length=20, null=True)
    manager = models.NullBooleanField(default=False)

    class Meta:
        db_table = 'ideax_userprofile'

    def __str__(self):
        return self.user.username
