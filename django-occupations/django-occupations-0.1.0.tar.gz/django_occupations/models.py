"""
Database models for django_occupations.
"""
from django.db import models
from model_utils.models import TimeStampedModel


class Occupation(TimeStampedModel):
    """
    An occupation is a grouping of a number of individual jobs. Thus, an
    occupational definition is a collective description of a number of similar individual jobs
    performed, with minor variations, in different establishments.

    If you are planning to restrict your use of django-occupations to occupations listed on the US 
    Office of Management and Budget Standard Occupational Classification (SOC) system, then you 
    will end up with one Occupation for every SOCDetailedOccupation. Occupations are separated out 
    to allow for one extra layer of abstraction in case you want to specify occupations outside of 
    the SOC standard. 

    .. no_pii:
    """

    name = models.CharField(max_length=256, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    soc_occupation = models.ForeignKey('SOCDetailedOccupation', null=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<Occupation, ID: {self.id}, Name: {self.name}>"

    def get_description():
        """
        TODO: Return local description if it's available, or the SOC description as a backup, or empty if neither is available
        """
        return

    def is_catchall():
        """
        TODO: Returns True if the SOC code ends in a 9 or have "All other" at the end of the description
        """
        return


class SOCDetailedOccupation(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    .. no_pii:
    """

    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    soc_code = models.IntegerField(null=True)
    broad_occupation = models.ForeignKey('SOCBroadOccupation', null=True,
                                   on_delete=models.SET_NULL)

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<SOCDetailedOccupation, ID: {self.id}, Name: {self.name}>"


class SOCBroadOccupation(TimeStampedModel):
    """
    TODO: replace with a brief description of the model.

    .. no_pii:
    """

    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    soc_code = models.IntegerField(null=True)
    minor_group = models.ForeignKey('SOCMinorGroup', null=True,
                                   on_delete=models.SET_NULL)


    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<SOCBroadOccupation, ID: {self.id}, Name: {self.name}>"


class SOCMinorGroup(TimeStampedModel):
    """
    SOC Minor Occupational Groups

    .. no_pii:
    """

    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    soc_code = models.IntegerField(null=True)
    major_group = models.ForeignKey('SOCMajorGroup', null=True,
                                   on_delete=models.SET_NULL)


    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<SOCMinorGroup, ID: {self.id}, Name: {self.name}>"


class SOCMajorGroup(TimeStampedModel):
    """
    SOC Major Occupational Groups

    .. no_pii:
    """

    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True, null=True)
    soc_code = models.IntegerField(null=True)
    intermediate_aggregation_group = models.ForeignKey('SOCIntermediateAggregationGroup', null=True,
                                   on_delete=models.SET_NULL)
    high_level_aggregation_group = models.ForeignKey('SOCHighLevelAggregationGroup', null=True,
                                   on_delete=models.SET_NULL)


    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<SOCMajorGroup, ID: {self.id}, Name: {self.name}>"


class SOCIntermediateAggregationGroup(TimeStampedModel):
    """
    BLS recommended intermediate-level aggregations

    Refer to Table 6 on https://www.bls.gov/soc/2018/soc_2018_manual.pdf

    .. no_pii:
    """

    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<SOCIntermediateAggregationGroup, ID: {self.id}, Name: {self.name}>"


class SOCHighLevelAggregationGroup(TimeStampedModel):
    """
    BLS recommended high-level aggregations

    Refer to Table 6 on https://www.bls.gov/soc/2018/soc_2018_manual.pdf

    .. no_pii:
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<SOCHighLevelAggregationGroup, ID: {self.id}, Name: {self.name}>"


class SOCDirectMatchTitles(TimeStampedModel):
    """
    TODO: This is a placeholder for DirectMatchTitles. Refer to https://www.bls.gov/soc/2018/home.htm#match 

    .. no_pii:
    """

    # TODO: add field definitions

    def __str__(self):
        """
        Get a string representation of this model instance.
        """
        return f"<SOCDirectMatchTitles, ID: {self.id}, Name: {self.name}>"
