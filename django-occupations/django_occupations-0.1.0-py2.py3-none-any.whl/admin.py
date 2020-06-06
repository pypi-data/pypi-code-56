from django.contrib import admin
from .models import Occupation, SOCDetailedOccupation, SOCBroadOccupation, SOCMinorGroup, SOCMajorGroup, SOCIntermediateAggregationGroup, SOCHighLevelAggregationGroup, SOCDirectMatchTitles

admin.site.register(Occupation)
admin.site.register(SOCDetailedOccupation)
admin.site.register(SOCBroadOccupation)
admin.site.register(SOCMinorGroup)
admin.site.register(SOCMajorGroup)
admin.site.register(SOCIntermediateAggregationGroup)
admin.site.register(SOCHighLevelAggregationGroup)
admin.site.register(SOCDirectMatchTitles)
