from django.contrib import admin
from . import models as mdm_models

# Register your models here.

@admin.register(mdm_models.IndependentActivityDeclarationCostModel)
class IndependentActivityDeclarationCostAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.DependenceLegitimacyModel)
class DependenceLegitimacyAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.DependenceQualityModel)
class DependenceQualityAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.BusinessFormModel)
class BusinessFormAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.EnvironmentalClassificationModel)
class EnvironmentalClassificationAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']


@admin.register(mdm_models.InsuranceSuspensionModel)
class InsuranceSuspensionAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.EmploymentQualityModel)
class EmploymentQualityAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.SmallBusinessTaxContributionDiscountModel)
class SmallBusinessTaxContributionDiscountAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.SocialContributionDiscountModel)
class SocialContributionDiscountAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.PretenceModel)
class PretenceAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.LegalRelationshipModel)
class LegalRelationshipAdmin(admin.ModelAdmin):
    fields = ['code', 'name']
    list_display = ['code', 'name']
    search_fields = ['code', 'name']

@admin.register(mdm_models.PersonModel)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(mdm_models.OrganizationModel)
class OrganizationAdmin(admin.ModelAdmin):
    pass


