from mycms.models import CMSEntries
from mycms.models import CMSPageTypes
from mycms.view_handlers.mycms_view import ViewObject

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.utils import OperationalError
from mycms.view_handlers.mycms_view import ArticleList

from mycms.view_handlers import page_types

import logging
logger = logging.getLogger("mycms.page_handlers")

class MultiPageList(list):
    
    def __init__(self, total_entries):
        
        super(MultiPageList, self).__init__()
        self.total_entries = total_entries
        self.current_page_obj = None
    
    
    
    @property
    def page_range(self):
        """
        Returns the range of pages to display
        """
        return self
        
    @property
    def has_previous(self):
        """
        Returns boolean, True if there is a previous page
        and False if we are at the beginning.
        """
        
        if self.current_page_obj.page_number == 1:
            return False
        else:
            return True
        
    @property 
    def page(self):
        """
        Returns 
        """
        pass
    
    @property
    def next_page(self):
        """
        Returns the next page. 
        """
        if self.current_page_obj.page_number < len(self) -1 :
            return self[self.current_page_obj.page_number + 1]
        pass   


    @property
    def has_next(self):
        
        last_page_number = len(self)
        if self.current_page_obj.page_number < last_page_number:
            return True
        else:
            return False
        
    @property
    def has_previous(self):
        
        last_page_number = len(self)
        if self.current_page_obj.page_number > 1:
            return True
        else:
            return False
        
    @property
    def previous_page(self):
        if self.has_previous:
            obj = self[self.current_page_obj.page_number -2 ]
            print(obj.title)
            return obj
        
        else:
            return None
            
    @property
    def next_page(self):
        if self.has_next:
            return self[self.current_page_obj.page_number -2 ]
            
            
        
class MultiPage(object):

    def __init__(self, page_object, request=None):

        #page_object is a mycms.models.CMSEntries instance.
        #which represents the page.

        self.page_object = page_object
        self.page_number = 1 #This is always the first page.

        try:
            self.memberpageview_pagetype_obj = CMSPageTypes.objects.get(page_type="MEMBERPAGE")

        except ObjectDoesNotExist as e:

            msg = "Could not load MEMBERPAGE view object. Going to create it."
            logger.debug(msg)
            self.memberpageview_pagetype_obj, _ = CMSPageTypes.objects.get_or_create(page_type="MEMBERPAGE",
                                                             text = "MemberPage Article",
                                                             view_class = "MemberPage",
                                                             view_template = "MemberPage.html"
                                                             )

        except MultipleObjectsReturned as e:
            msg = "Got more than 1 CMSMultiPageType: MULTIPAGE. Database is inconsistent. Will return the first one."
            logger.info(msg)

            memberpageview_pagetype_obj = CMSMultiPageTypes.objects.filter(page_type="MEMBERPAGE")[0]


    @property
    def is_multipage(self):
        return True


    @property
    def articles(self):
        """
        Return al the pages that have the same parent as us.
        """
        
        from django.db.models import Q
        #Get CMS entries starting at offset and give limit number results
        """
        Get the CMSEntries whose parent is the same as our parent. 
        Starting at the offset and give limit number of results. 
        """
      
        """
        This page_object is the parent of the sub articles. 
        Each cms entry has a path whose parent.path == the path of this
        page_object. We use this relation to find all children.
        """
        try:
            
            children  = CMSEntries.objects.filter( Q(path__parent__path=self.page_object.path) & 
                                                    Q(published=True) & 
                                                    Q(lists_include=True) 
                                                 )
        except Exception as e:
            print(e)
        #need to know the total cmsentries in mycms.
        children_count = children.count()
        article_list = MultiPageList(total_entries = children_count)      
        
        #We are the first in the list
        self.page_object.page_number = 1
        article_list.append(self.page_object)
        article_list.current_page_obj = self.page_object
        
        
        index = 1
        
        for obj in children :
            #BUG: We are just adding everythign into the article_list here!
            index = index + 1
            obj.page_number = index
            if self.page_object.id == obj.id:
                obj.current_page = True
                article_list.current_page_obj = obj
            else:
                obj.current_page = False
            article_list.append(obj)
        return article_list
    

    #def articles(self):
        #"""Here we load all pages that says we are their parent."""

        #obj_list = CMSEntries.objects.filter(page_type = self.memberpageview_pagetype_obj,
                                             #path__parent__id = self.page_object.path.id)
        ##wrap the entries of the obj_list into their view_handler representations
        #view_list = []
        #for obj in obj_list:
            #view_list.append(ViewObject(page_object=obj))
        #return view_list

    #def page_types(self):
        #"""
        #Refactor me into a parent class.
        #returns a list fo page_types
        #"""
        #pagetype_objs = CMSPageTypes.objects.filter(page_type="MEMBERPAGE")

        #return pagetype_objs

    #def on_create(self):

        #print("Created a new article {}".format(self.page_object.title))


    #@property 
    #def first_page_object(self):
        ##We are the first page object
        #return self.page_object

    #@property
    #def member_page_objects(self):

        #member_cmsentries =  CMSEntries.objects.filter(
            #path__parent=self.page_object.path).order_by('page_number')
        #return member_cmsentries

    #@property 
    #def first_page_object(self):
        ##The first_page_object is always the parent. No need to do 
        ##anything here since it is implemented in the CMSEntry 
        
        #return self.page_object.parent
        
    #@property
    #def first_page(self):
        ##Legacy implementatin. THIS IS VERY MISLEADING. should be 
        ##renamed as first_member_page.

        #entries = CMSEntries.objects.filter(
            #path__parent=self.page_object.path).order_by('page_number')
        
        #num_entries = len(entries)
        #print(num_entries)
        #if entries.count() > 0:
            #return entries[0]
        #else:
            #return None
        
    #@property
    #def has_first_page(self):
        
        #if self.first_page == None:
            #return False
        #else:
            #return True
        
class MemberPage(page_types.BasePage):

    def __init__(self, page_object, request=None):

        self.page_object = page_object
        self._page_number = 0 

        self.last_member_page = 1

    def on_create(self):
        """
        A new member page has been created. Append it as the last page.

        """
        print("Created a memberpage called {}".format(self.page_object.title))
        my_parent_object = CMSEntries.objects.get(path=self.page_object.path.parent)

        print(my_parent_object.title)
        my_siblings = CMSEntries.objects.filter(path__parent=self.page_object.path.parent)

        for sibling in my_siblings:
            print(sibling.title)

        last_page_num = self.last_member_page_object.page_number
        self.page_object.page_number = last_page_num + 1
        self.page_object.save()

  
    #@property
    #def member_page_objects(self):

        #return CMSEntries.objects.filter(path__parent=self.page_object.path.parent).order_by('page_number')

    #@property
    #def first_member_page_object(self):
        #pass

    #@property
    #def last_member_page_object(self):

        #c = self.member_page_objects.count()

        #if c==1:
            #return self.member_page_objects[0]

        #elif c==0:
            #return None
        #else:
            ##We have more than one
            #return self.member_page_objects[c-1]


    #@property
    #def next_page(self):

        #"""
        #Get the next page by getting all the pages that have greater page_number than us.
        #"""

        #next_pages = CMSEntries.objects.filter(path__parent=self.page_object.path.parent, page_number__gt=self.page_object.page_number).order_by('page_number')
        #num_results = len(next_pages)
        #if  num_results > 0:
            #return next_pages[0]
        #else:
            #return None

    #@property
    #def previous_page(self):
        #previous_pages = CMSEntries.objects.filter(path__parent=self.page_object.path.parent, page_number__lt=self.page_object.page_number).order_by('-page_number')

        #num_results = len(previous_pages) 
        #if num_results > 0:
            #return previous_pages[0]
        #else:
            #return None



    #@property
    #def first_page(self):

        #entries = CMSEntries.objects.filter(path__parent=self.page_object.path.parent).order_by('page_number')

        #return entries[0]


    #@property
    #def is_last_page(self):
        #entries = CMSEntries.objects.filter(path__parent=self.page_object.path.parent).order_by('-page_number')
        
        #if entries[0] == self.page_object:
            #return True
        #else:
            #return False
       
    #@property
    #def is_first_page(self):
        #if self.page_object == self.first_page:
            #return True
        #else:
            #return False
    @property
    def page_number(self):
        return self._page_number
    
    @page_number.setter
    def page_number(self, page_number):
        
        self._page_number = page_number
        
    @property
    def articles(self):
        """
        Return al the pages that have the same parent as us.
        """
        
        from django.db.models import Q
        #Get CMS entries starting at offset and give limit number results
        """
        Get the CMSEntries whose parent is the same as our parent. 
        Starting at the offset and give limit number of results. 
        """
        limit, offset, page = self.get_list_params()
        try:
        
            page_cmsentries  = CMSEntries.objects.filter( Q(path__parent__id = self.page_object.parent().path.id) & 
                                                          Q(published=True) & 
                                                          Q(lists_include=True) 
                                                          )[offset:offset+limit]
        except Exception as e:
            # We hit here if there are no children
            print(e)
            pass
    
    
        #Get all the siblings of this page. Siblings are cmsentries that 
        #have the same parent as this entry's parent. 
        all_cmsentries = CMSEntries.objects.filter( Q(path__parent__id = self.page_object.parent().path.id) & 
                                                    Q(published=True) & 
                                                    Q(lists_include=True) 
                                                    )
        
        #need to know the total cmsentries in mycms.
        all_cmsentries_count = all_cmsentries.count()
    
        article_list = MultiPageList(total_entries = all_cmsentries_count)      
    
    
        #insert the parent 
        
        parent = CMSEntries.objects.get(path = self.page_object.parent().path)
        article_list.append(parent)
        index = 1
        
        for obj in page_cmsentries:
            #BUG: We are just adding everythign into the article_list here!
            index = index + 1
            obj.page_number = index
            if self.page_object.id == obj.id:
                obj.current_page = True
                article_list.current_page_obj = obj
            else:
                obj.current_page = False
            article_list.append(obj)
        return article_list
        