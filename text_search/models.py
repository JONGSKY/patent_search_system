# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Patent(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    type = models.CharField(max_length=100, blank=True, null=True)
    number = models.CharField(max_length=64)
    country = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    kind = models.CharField(max_length=10, blank=True, null=True)
    num_claims = models.PositiveSmallIntegerField(blank=True, null=True)
    firstnamed_assignee_id = models.PositiveIntegerField(blank=True, null=True)
    firstnamed_assignee_persistent_id = models.CharField(max_length=64, blank=True, null=True)
    firstnamed_assignee_location_id = models.PositiveIntegerField(blank=True, null=True)
    firstnamed_assignee_persistent_location_id = models.CharField(max_length=128, blank=True, null=True)
    firstnamed_assignee_city = models.CharField(max_length=256, blank=True, null=True)
    firstnamed_assignee_state = models.CharField(max_length=20, blank=True, null=True)
    firstnamed_assignee_country = models.CharField(max_length=10, blank=True, null=True)
    firstnamed_assignee_latitude = models.FloatField(blank=True, null=True)
    firstnamed_assignee_longitude = models.FloatField(blank=True, null=True)
    firstnamed_inventor_id = models.PositiveIntegerField(blank=True, null=True)
    firstnamed_inventor_persistent_id = models.CharField(max_length=36, blank=True, null=True)
    firstnamed_inventor_location_id = models.PositiveIntegerField(blank=True, null=True)
    firstnamed_inventor_persistent_location_id = models.CharField(max_length=128, blank=True, null=True)
    firstnamed_inventor_city = models.CharField(max_length=256, blank=True, null=True)
    firstnamed_inventor_state = models.CharField(max_length=20, blank=True, null=True)
    firstnamed_inventor_country = models.CharField(max_length=10, blank=True, null=True)
    firstnamed_inventor_latitude = models.FloatField(blank=True, null=True)
    firstnamed_inventor_longitude = models.FloatField(blank=True, null=True)
    num_foreign_documents_cited = models.PositiveIntegerField()
    num_us_applications_cited = models.PositiveIntegerField()
    num_us_patents_cited = models.PositiveIntegerField()
    num_total_documents_cited = models.PositiveIntegerField()
    num_times_cited_by_us_patents = models.PositiveIntegerField()
    earliest_application_date = models.CharField(max_length=20, blank=True, null=True)
    patent_processing_days = models.PositiveIntegerField(blank=True, null=True)
    uspc_current_mainclass_average_patent_processing_days = models.PositiveIntegerField(blank=True, null=True)
    cpc_current_group_average_patent_processing_days = models.PositiveIntegerField(blank=True, null=True)
    term_extension = models.PositiveIntegerField(blank=True, null=True)
    detail_desc_length = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent'


class PatentEmbedding(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    embedding = models.TextField()

    class Meta:
        managed = False
        db_table = 'patent_embedding'


class PatentNgram(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    ngram_words = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent_ngram'


class PatentTextNgram(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    ngram_words = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent_text_ngram'


class Patentsview(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    title = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    kind = models.CharField(max_length=10, blank=True, null=True)
    number = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'patentsview'
