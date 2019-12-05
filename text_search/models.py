# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

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
