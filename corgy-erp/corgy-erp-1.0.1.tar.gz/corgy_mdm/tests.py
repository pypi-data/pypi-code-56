from django.test import TestCase
import datetime
from . import models as mdm_models
from django.contrib.auth import models as auth_models
from django.utils import timezone

# Create your tests here.

class PersonModelTestCase(TestCase):
    """
    Unit tests of master data for person.
    """

    def setUp(self):
        pass

    def test_create(self):
        """Test creation of default ad minimal necessary data of personal master data model"""
        permanent_address = mdm_models.Address()
        permanent_address.save()

        person = mdm_models.PersonModel.objects.create(
            name = 'test-person',
            birthdate=timezone.datetime(year=2020, month=1, day=2),
            name_of_mother = 'name of mother',
            permanent_address = permanent_address,
        ) # type: mdm_models.PersonModel
        # tself.assertIsNotNone(person.pk)

class BusinessFormModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        business_form = mdm_models.BusinessFormModel.objects.create(
            name = 'my-business-form'
        )

class EnvironmentalClassificationModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        environmental_class = mdm_models.EnvironmentalClassificationModel(
            name = 'my-environmental-class'
        )


class InsuranceSuspensionModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        insurance_suspension = mdm_models.InsuranceSuspensionModel.objects.create(
            name = 'my-insurance-suspension'
        )


class LegalRelationshipModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        legal_relationship = mdm_models.LegalRelationshipModel.objects.create(
            name = 'my-legal-relationship'
        )


class PretenceModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        pretence = mdm_models.PretenceModel.objects.create(
            name = 'my-pretence'
        )



class SmallBusinessTaxContributionDiscountModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        small_business_tax_contribution_discount = mdm_models.SmallBusinessTaxContributionDiscountModel.objects.create(
            name = 'my-small-business-tax-contribution-discount'
        )


class SocialContributionDiscountModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        social_contribution_discount = mdm_models.SocialContributionDiscountModel.objects.create(
            name = 'my-social-contribution-discount'
        )


class EnvironmentalClassificationModel(TestCase):

    def setUp(self):
        pass

    def test_create(self):

        environmental_classification = mdm_models.EnvironmentalClassificationModel.objects.create(
            name = 'my-environmental-classification'
        )





class OrganizationModelTestCase(TestCase):
    """
    Unit tests of master data for organization.
    """

    def setUp(self):

        pass

    def test_create(self):
        """Test creation of default and minimal necessary data of organization master data model."""

        business_form = mdm_models.BusinessFormModel.objects.create(
            name='my-business-form'
        )

        organization = mdm_models.OrganizationModel.objects.create(
            name = 'test-org',
            business_form = business_form,
        ) # type:mdm_models.OrganizationModel

        # self.assertIsNotNone(organization.pk)

