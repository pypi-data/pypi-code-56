from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject
from mycms.view_handlers.mycms_view import ArticleList

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import OperationalError

import logging
logger = logging.getLogger("mycms.page_handlers")


# #####################
# We ensure that the base page types are already created.
# #####################

from mycms.view_handlers import page_types


class AllArticlesPage(page_types.BasePage):
    

    def __init__(self, page_object, request=None):
        self.page_object = page_object
        self.request = request
        self._article_list = None

    #TODO: Refactor the code so that there is only one articles() method used 
    #by all and just control by a flag whether we want to recursively or not.

    def articles(self):

        """Here we load all pages that says we are their parent."""

        from django.db.models import Q

        # ######################################################################
        # This loads up all the articles that are 
        # of type single_page or multipage and has the provided parent. 
       
        limit, offset, page = self.get_list_params()
       
        if  ((self._article_list is None) or 
             (limit != self._article_list.limit) or
             (offset != self._article_list.offset) or
             (page != self._article_list.page)
             ):
        
            # the above "if" works because the first boolean tests if 
            #self._article_list is None and the rest are not evaluated further. 
            
            #This is a lame attempt at ensuring that multple calls to article 
            #is avoided by caching the results so that when processing the 
            #template we do not need to execute this code any further. 
            
            
            offset = page*limit - limit
                
            
            #Get the results via offset and limit.
            obj_list = CMSEntries.objects.filter(
                                                 (Q(page_type = page_types.singlepageview_pagetype_obj ) | 
                                                  Q(page_type = page_types.multipageview_pagetype_obj)
                                                  ) & Q( lists_include = True)  & Q(published=True)
                                                 ) [offset:offset+limit]
            
            
            num_entries = CMSEntries.objects.filter(
                                        (Q(page_type = page_types.singlepageview_pagetype_obj ) | 
                                         Q(page_type = page_types.multipageview_pagetype_obj)
                                         ) &
                                         Q( lists_include = True)  & Q(published=True)
                                        ) [offset:offset+limit].count()
            
            num_total_cmsentries = CMSEntries.objects.filter(
                                                 (Q(page_type = page_types.singlepageview_pagetype_obj ) | 
                                                  Q(page_type = page_types.multipageview_pagetype_obj)
                                                  ) &
                                                  Q( lists_include = True)  & Q(published=True) ).count()
            
            
            
            self._article_list = ArticleList(obj_list, num_total_cmsentries, page)
            self._article_list.limit = limit
            self._article_list.offset = offset                        
            self._article_list.num_total_cmsentries = num_total_cmsentries
            
            
            for obj in obj_list:
                self._article_list.append(ViewObject(page_object=obj))

        
        return self._article_list



    def get_categories(self):
        """Returns a list of all child categories of type: CATEGORY"""

        obj_list = CMSEntries.objects.filter(path__path__parent__id = self.page_object.id,
                                             page_type=page_obj.page_type)

        return obj_list



    def page_types(self):

        """
        Refactor me into a parent class.
        returns a list fo page_types
        """


        pagetype_objs = CMSPageTypes.objects.all()

        return pagetype_objs


    def on_create(self):
        pass
