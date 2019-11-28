# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Application(models.Model):
    application_id = models.CharField(primary_key=True, max_length=36)
    patent_id = models.CharField(max_length=20)
    type = models.CharField(max_length=20, blank=True, null=True)
    number = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'application'
        unique_together = (('application_id', 'patent_id'),)


class Assignee(models.Model):
    assignee_id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    name_first = models.CharField(max_length=64, blank=True, null=True)
    name_last = models.CharField(max_length=64, blank=True, null=True)
    organization = models.CharField(max_length=256, blank=True, null=True)
    num_patents = models.PositiveIntegerField()
    num_inventors = models.PositiveIntegerField()
    lastknown_location_id = models.PositiveIntegerField(blank=True, null=True)
    lastknown_persistent_location_id = models.CharField(max_length=128, blank=True, null=True)
    lastknown_city = models.CharField(max_length=128, blank=True, null=True)
    lastknown_state = models.CharField(max_length=20, blank=True, null=True)
    lastknown_country = models.CharField(max_length=10, blank=True, null=True)
    lastknown_latitude = models.FloatField(blank=True, null=True)
    lastknown_longitude = models.FloatField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField()
    persistent_assignee_id = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = 'assignee'


class AssigneeCpcGroup(models.Model):
    assignee_id = models.PositiveIntegerField()
    group_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'assignee_cpc_group'


class AssigneeCpcSubsection(models.Model):
    assignee_id = models.PositiveIntegerField()
    subsection_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'assignee_cpc_subsection'


class AssigneeInventor(models.Model):
    assignee_id = models.PositiveIntegerField()
    inventor_id = models.PositiveIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'assignee_inventor'


class AssigneeNberSubcategory(models.Model):
    assignee_id = models.PositiveIntegerField()
    subcategory_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'assignee_nber_subcategory'


class AssigneeUspcMainclass(models.Model):
    assignee_id = models.PositiveIntegerField()
    mainclass_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'assignee_uspc_mainclass'


class AssigneeYear(models.Model):
    assignee_id = models.PositiveIntegerField()
    patent_year = models.SmallIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'assignee_year'


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


class Claim(models.Model):
    uuid = models.CharField(max_length=36)
    patent_id = models.CharField(max_length=20, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    dependent = models.IntegerField(blank=True, null=True)
    sequence = models.IntegerField(blank=True, null=True)
    exemplary = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'claim'


class CpcCurrent(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.PositiveIntegerField()
    section_id = models.CharField(max_length=10, blank=True, null=True)
    subsection_id = models.CharField(max_length=20, blank=True, null=True)
    subsection_title = models.CharField(max_length=512, blank=True, null=True)
    group_id = models.CharField(max_length=20, blank=True, null=True)
    group_title = models.CharField(max_length=256, blank=True, null=True)
    subgroup_id = models.CharField(max_length=20, blank=True, null=True)
    subgroup_title = models.CharField(max_length=512, blank=True, null=True)
    category = models.CharField(max_length=36, blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)
    num_assignees_group = models.PositiveIntegerField(blank=True, null=True)
    num_inventors_group = models.PositiveIntegerField(blank=True, null=True)
    num_patents_group = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date_group = models.DateField(blank=True, null=True)
    last_seen_date_group = models.DateField(blank=True, null=True)
    years_active_group = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_current'
        unique_together = (('patent_id', 'sequence'),)


class CpcCurrentCopy(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.PositiveIntegerField()
    section_id = models.CharField(max_length=10, blank=True, null=True)
    subsection_id = models.CharField(max_length=20, blank=True, null=True)
    group_id = models.CharField(max_length=20, blank=True, null=True)
    subgroup_id = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=36, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_current_copy'
        unique_together = (('patent_id', 'sequence'),)


class CpcCurrentGroup(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    section_id = models.CharField(max_length=10, blank=True, null=True)
    group_id = models.CharField(max_length=20)
    group_title = models.CharField(max_length=512, blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_current_group'
        unique_together = (('patent_id', 'group_id'),)


class CpcCurrentGroupApplicationYear(models.Model):
    group_id = models.CharField(primary_key=True, max_length=20)
    application_year = models.PositiveSmallIntegerField()
    sample_size = models.PositiveIntegerField()
    average_patent_processing_days = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_current_group_application_year'
        unique_together = (('group_id', 'application_year'),)


class CpcCurrentGroupCopy(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    section_id = models.CharField(max_length=10, blank=True, null=True)
    group_id = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cpc_current_group_copy'
        unique_together = (('patent_id', 'group_id'),)


class CpcCurrentGroupPatentYear(models.Model):
    group_id = models.CharField(primary_key=True, max_length=20)
    patent_year = models.PositiveSmallIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'cpc_current_group_patent_year'
        unique_together = (('group_id', 'patent_year'),)


class CpcCurrentSubsection(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    section_id = models.CharField(max_length=10, blank=True, null=True)
    subsection_id = models.CharField(max_length=20)
    subsection_title = models.CharField(max_length=512, blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_current_subsection'
        unique_together = (('patent_id', 'subsection_id'),)


class CpcCurrentSubsectionCopy(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    section_id = models.CharField(max_length=10, blank=True, null=True)
    subsection_id = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'cpc_current_subsection_copy'
        unique_together = (('patent_id', 'subsection_id'),)


class CpcCurrentSubsectionPatentYear(models.Model):
    subsection_id = models.CharField(primary_key=True, max_length=20)
    patent_year = models.PositiveSmallIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'cpc_current_subsection_patent_year'
        unique_together = (('subsection_id', 'patent_year'),)


class CpcGroup(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=256, blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_group'


class CpcSubgroup(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_subgroup'


class CpcSubsection(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=256, blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cpc_subsection'


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


class Examiner(models.Model):
    examiner_id = models.PositiveIntegerField(primary_key=True)
    name_first = models.CharField(max_length=64, blank=True, null=True)
    name_last = models.CharField(max_length=64, blank=True, null=True)
    role = models.CharField(max_length=20, blank=True, null=True)
    group = models.CharField(max_length=20, blank=True, null=True)
    persistent_examiner_id = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = 'examiner'


class Foreignpriority(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.IntegerField()
    foreign_doc_number = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=64, blank=True, null=True)
    kind = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'foreignpriority'
        unique_together = (('patent_id', 'sequence'),)


class GovernmentInterest(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=255)
    gi_statement = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'government_interest'


class GovernmentOrganization(models.Model):
    organization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    level_one = models.CharField(max_length=255, blank=True, null=True)
    level_two = models.CharField(max_length=255, blank=True, null=True)
    level_three = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'government_organization'


class Inventor(models.Model):
    inventor_id = models.PositiveIntegerField(primary_key=True)
    name_first = models.CharField(max_length=64, blank=True, null=True)
    name_last = models.CharField(max_length=64, blank=True, null=True)
    num_patents = models.PositiveIntegerField()
    num_assignees = models.PositiveIntegerField()
    lastknown_location_id = models.PositiveIntegerField(blank=True, null=True)
    lastknown_persistent_location_id = models.CharField(max_length=128, blank=True, null=True)
    lastknown_city = models.CharField(max_length=128, blank=True, null=True)
    lastknown_state = models.CharField(max_length=20, blank=True, null=True)
    lastknown_country = models.CharField(max_length=10, blank=True, null=True)
    lastknown_latitude = models.FloatField(blank=True, null=True)
    lastknown_longitude = models.FloatField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField()
    persistent_inventor_id = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = 'inventor'


class InventorCoinventor(models.Model):
    inventor_id = models.PositiveIntegerField()
    coinventor_id = models.PositiveIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'inventor_coinventor'


class InventorCpcGroup(models.Model):
    inventor_id = models.PositiveIntegerField()
    group_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'inventor_cpc_group'


class InventorCpcSubsection(models.Model):
    inventor_id = models.PositiveIntegerField()
    subsection_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'inventor_cpc_subsection'


class InventorNberSubcategory(models.Model):
    inventor_id = models.PositiveIntegerField()
    subcategory_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'inventor_nber_subcategory'


class InventorRawinventor(models.Model):
    uuid = models.AutoField(primary_key=True)
    name_first = models.CharField(max_length=64, blank=True, null=True)
    name_last = models.CharField(max_length=64, blank=True, null=True)
    patent_id = models.CharField(max_length=20, blank=True, null=True)
    inventor_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inventor_rawinventor'


class InventorUspcMainclass(models.Model):
    inventor_id = models.PositiveIntegerField()
    mainclass_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'inventor_uspc_mainclass'


class InventorYear(models.Model):
    inventor_id = models.PositiveIntegerField()
    patent_year = models.SmallIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'inventor_year'


class Ipcr(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.IntegerField()
    section = models.CharField(max_length=20, blank=True, null=True)
    ipc_class = models.CharField(max_length=20, blank=True, null=True)
    subclass = models.CharField(max_length=20, blank=True, null=True)
    main_group = models.CharField(max_length=20, blank=True, null=True)
    subgroup = models.CharField(max_length=20, blank=True, null=True)
    symbol_position = models.CharField(max_length=20, blank=True, null=True)
    classification_value = models.CharField(max_length=20, blank=True, null=True)
    classification_data_source = models.CharField(max_length=20, blank=True, null=True)
    action_date = models.DateField(blank=True, null=True)
    ipc_version_indicator = models.DateField(blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipcr'
        unique_together = (('patent_id', 'sequence'),)


class Lawyer(models.Model):
    lawyer_id = models.PositiveIntegerField(primary_key=True)
    name_first = models.CharField(max_length=64, blank=True, null=True)
    name_last = models.CharField(max_length=64, blank=True, null=True)
    organization = models.CharField(max_length=256, blank=True, null=True)
    num_patents = models.PositiveIntegerField()
    num_assignees = models.PositiveIntegerField()
    num_inventors = models.PositiveIntegerField()
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField()
    persistent_lawyer_id = models.CharField(max_length=36)

    class Meta:
        managed = False
        db_table = 'lawyer'


class Location(models.Model):
    location_id = models.PositiveIntegerField(primary_key=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=60, blank=True, null=True)
    state_fips = models.CharField(max_length=2, blank=True, null=True)
    county_fips = models.CharField(max_length=3, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    num_assignees = models.PositiveIntegerField()
    num_inventors = models.PositiveIntegerField()
    num_patents = models.PositiveIntegerField()
    persistent_location_id = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'location'


class LocationAssignee(models.Model):
    location_id = models.PositiveIntegerField(primary_key=True)
    assignee_id = models.PositiveIntegerField()
    num_patents = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_assignee'
        unique_together = (('location_id', 'assignee_id'),)


class LocationCpcGroup(models.Model):
    location_id = models.PositiveIntegerField()
    group_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'location_cpc_group'


class LocationCpcSubsection(models.Model):
    location_id = models.PositiveIntegerField()
    subsection_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'location_cpc_subsection'


class LocationInventor(models.Model):
    location_id = models.PositiveIntegerField(primary_key=True)
    inventor_id = models.PositiveIntegerField()
    num_patents = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'location_inventor'
        unique_together = (('location_id', 'inventor_id'),)


class LocationNberSubcategory(models.Model):
    location_id = models.PositiveIntegerField()
    subcategory_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'location_nber_subcategory'


class LocationUspcMainclass(models.Model):
    location_id = models.PositiveIntegerField()
    mainclass_id = models.CharField(max_length=20)
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'location_uspc_mainclass'


class LocationYear(models.Model):
    location_id = models.PositiveIntegerField()
    year = models.SmallIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'location_year'


class Nber(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    category_id = models.CharField(max_length=20, blank=True, null=True)
    category_title = models.CharField(max_length=512, blank=True, null=True)
    subcategory_id = models.CharField(max_length=20, blank=True, null=True)
    subcategory_title = models.CharField(max_length=512, blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nber'


class NberCategory(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nber_category'


class NberCopy(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    category_id = models.CharField(max_length=20, blank=True, null=True)
    subcategory_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nber_copy'


class NberSubcategory(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=512, blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nber_subcategory'


class NberSubcategoryPatentYear(models.Model):
    subcategory_id = models.CharField(primary_key=True, max_length=20)
    patent_year = models.PositiveSmallIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'nber_subcategory_patent_year'
        unique_together = (('subcategory_id', 'patent_year'),)


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
    firstnamed_assignee_persistent_id = models.CharField(max_length=36, blank=True, null=True)
    firstnamed_assignee_location_id = models.PositiveIntegerField(blank=True, null=True)
    firstnamed_assignee_persistent_location_id = models.CharField(max_length=128, blank=True, null=True)
    firstnamed_assignee_city = models.CharField(max_length=128, blank=True, null=True)
    firstnamed_assignee_state = models.CharField(max_length=20, blank=True, null=True)
    firstnamed_assignee_country = models.CharField(max_length=10, blank=True, null=True)
    firstnamed_assignee_latitude = models.FloatField(blank=True, null=True)
    firstnamed_assignee_longitude = models.FloatField(blank=True, null=True)
    firstnamed_inventor_id = models.PositiveIntegerField(blank=True, null=True)
    firstnamed_inventor_persistent_id = models.CharField(max_length=36, blank=True, null=True)
    firstnamed_inventor_location_id = models.PositiveIntegerField(blank=True, null=True)
    firstnamed_inventor_persistent_location_id = models.CharField(max_length=128, blank=True, null=True)
    firstnamed_inventor_city = models.CharField(max_length=128, blank=True, null=True)
    firstnamed_inventor_state = models.CharField(max_length=20, blank=True, null=True)
    firstnamed_inventor_country = models.CharField(max_length=10, blank=True, null=True)
    firstnamed_inventor_latitude = models.FloatField(blank=True, null=True)
    firstnamed_inventor_longitude = models.FloatField(blank=True, null=True)
    num_foreign_documents_cited = models.PositiveIntegerField()
    num_us_applications_cited = models.PositiveIntegerField()
    num_us_patents_cited = models.PositiveIntegerField()
    num_total_documents_cited = models.PositiveIntegerField()
    num_times_cited_by_us_patents = models.PositiveIntegerField()
    earliest_application_date = models.DateField(blank=True, null=True)
    patent_processing_days = models.PositiveIntegerField(blank=True, null=True)
    uspc_current_mainclass_average_patent_processing_days = models.PositiveIntegerField(blank=True, null=True)
    cpc_current_group_average_patent_processing_days = models.PositiveIntegerField(blank=True, null=True)
    term_extension = models.PositiveIntegerField(blank=True, null=True)
    detail_desc_length = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patent'


class PatentAssignee(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    assignee_id = models.PositiveIntegerField()
    location_id = models.PositiveIntegerField(blank=True, null=True)
    sequence = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'patent_assignee'
        unique_together = (('patent_id', 'assignee_id'), ('assignee_id', 'patent_id'),)


class PatentContractawardnumber(models.Model):
    patent = models.ForeignKey(GovernmentInterest, models.DO_NOTHING, primary_key=True)
    contract_award_number = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'patent_contractawardnumber'
        unique_together = (('patent', 'contract_award_number'),)


class PatentExaminer(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    examiner_id = models.PositiveIntegerField()
    role = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'patent_examiner'
        unique_together = (('patent_id', 'examiner_id'), ('examiner_id', 'patent_id'),)


class PatentGovintorg(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=255)
    organization = models.ForeignKey(GovernmentOrganization, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patent_govintorg'
        unique_together = (('patent_id', 'organization'),)


class PatentInventor(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    inventor_id = models.PositiveIntegerField()
    location_id = models.PositiveIntegerField(blank=True, null=True)
    sequence = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'patent_inventor'
        unique_together = (('patent_id', 'inventor_id'), ('inventor_id', 'patent_id'),)


class PatentLawyer(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    lawyer_id = models.PositiveIntegerField()
    sequence = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'patent_lawyer'
        unique_together = (('patent_id', 'lawyer_id'), ('lawyer_id', 'patent_id'),)


class Pctdata(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    doc_type = models.CharField(max_length=20)
    kind = models.CharField(max_length=2)
    doc_number = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    number_102_date = models.DateField(db_column='102_date', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    number_371_date = models.DateField(db_column='371_date', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'pctdata'
        unique_together = (('patent_id', 'kind'),)


class PostPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    class Meta:
        managed = False
        db_table = 'post_post'


class Usapplicationcitation(models.Model):
    citing_patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.IntegerField()
    cited_application_id = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True)
    kind = models.CharField(max_length=10, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usapplicationcitation'
        unique_together = (('citing_patent_id', 'sequence'),)


class Uspatentcitation(models.Model):
    citing_patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.IntegerField()
    cited_patent_id = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uspatentcitation'
        unique_together = (('citing_patent_id', 'sequence'),)


class UspcCurrent(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.PositiveIntegerField()
    mainclass_id = models.CharField(max_length=20, blank=True, null=True)
    mainclass_title = models.CharField(max_length=256, blank=True, null=True)
    subclass_id = models.CharField(max_length=20, blank=True, null=True)
    subclass_title = models.CharField(max_length=512, blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uspc_current'
        unique_together = (('patent_id', 'sequence'),)


class UspcCurrentCopy(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    sequence = models.PositiveIntegerField()
    mainclass_id = models.CharField(max_length=20, blank=True, null=True)
    subclass_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uspc_current_copy'
        unique_together = (('patent_id', 'sequence'),)


class UspcCurrentMainclass(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    mainclass_id = models.CharField(max_length=20)
    mainclass_title = models.CharField(max_length=256, blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uspc_current_mainclass'
        unique_together = (('patent_id', 'mainclass_id'),)


class UspcCurrentMainclassApplicationYear(models.Model):
    mainclass_id = models.CharField(primary_key=True, max_length=20)
    application_year = models.PositiveSmallIntegerField()
    sample_size = models.PositiveIntegerField()
    average_patent_processing_days = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uspc_current_mainclass_application_year'
        unique_together = (('mainclass_id', 'application_year'),)


class UspcCurrentMainclassCopy(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    mainclass_id = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'uspc_current_mainclass_copy'
        unique_together = (('patent_id', 'mainclass_id'),)


class UspcCurrentMainclassPatentYear(models.Model):
    mainclass_id = models.CharField(primary_key=True, max_length=20)
    patent_year = models.PositiveSmallIntegerField()
    num_patents = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'uspc_current_mainclass_patent_year'
        unique_together = (('mainclass_id', 'patent_year'),)


class UspcMainclass(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=256, blank=True, null=True)
    num_patents = models.PositiveIntegerField(blank=True, null=True)
    num_inventors = models.PositiveIntegerField(blank=True, null=True)
    num_assignees = models.PositiveIntegerField(blank=True, null=True)
    first_seen_date = models.DateField(blank=True, null=True)
    last_seen_date = models.DateField(blank=True, null=True)
    years_active = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uspc_mainclass'


class UspcSubclass(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'uspc_subclass'


class Wipo(models.Model):
    patent_id = models.CharField(primary_key=True, max_length=20)
    field_id = models.CharField(max_length=3, blank=True, null=True)
    sequence = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'wipo'
        unique_together = (('patent_id', 'sequence'),)


class WipoField(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    sector_title = models.CharField(max_length=60, blank=True, null=True)
    field_title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wipo_field'
