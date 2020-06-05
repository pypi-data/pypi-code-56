"""# Ordering item"""

from sqlalchemy.inspection import inspect

class OrderingItem():
    """
    The `OrderingItem` base should be subclasses in SQLAlchemy database models 
    which are children of `orderinglist` relationships.

    This ensures that setting the child's parent attribute gives the child the 
    appropriate index (the `Column` on which the `orderinglist` is sorted).
    """

    # OrderingItem overrides the __setattr__ method to check for orderinglist 
    # relationships. These attributes need to be set through the super() 
    # method, and are considered 'exempt'.
    _exempt_attrs_oi = [
        '_orderinglist_parent_indicator', '_orderinglist_parent_attrs'
    ]

    def __new__(cls, *args, **kwargs):
        """
        Set class orderinglist parent indicators and orderinglist parent 
        attributes.

        Attributes
        ----------
        _orderinglist_parent_indicator : dict
            Maps attribute names to boolean indicator that the attribute has a 
            relationship to this class with an `orderinglist` collection 
            class. If so, the attribute is considered a 'parent'.

        _orderinglist_parent_attrs : dict
            Maps parent attribute names to `(child_list, order_by)` tuple. `child_list` is the name of the child list attribute of the parent object. `order_by` is the name of the index attribute; the column on which the `orderinglist` is sorted.
        """
        if not hasattr(cls, '_orderinglist_parent_indicator'):
            cls._orderinglist_parent_indicator = {}
            cls._orderinglist_parent_attrs = {}
        try:
            return super().__new__(cls, *args, **kwargs)
        except:
            return super().__new__(cls)

    def __setattr__(self, name, value):
        """Set attribute

        Before setting an attribute, determine if it is the parent of an 
        orderinglist relationship to self. If so, use `append` insead of 
        `__setattr__` to add `self` to the parent's list of children. `append` 
        actives `orderlist` collection class methods to update the index of 
        `self`.
        """
        if name in self._exempt_attrs_oi:
            return super().__setattr__(name, value)
        is_parent = self._orderinglist_parent_indicator.get(name)
        if is_parent is None:
            # this attribute has not yet been seen
            # need to determine if it is a parent
            is_parent = self._set_orderinglist_parent(name)
        if is_parent:
            childlist, order_by = self._orderinglist_parent_attrs[name]
            if value is None:
                super().__setattr__(name, None)
                super().__setattr__(order_by, None)
            else:
                getattr(value, childlist).append(self)
        else:
            super().__setattr__(name, value)
    
    @classmethod
    def _set_orderinglist_parent(cls, name):
        """
        Set the orderinglist parent status for a previously unseen attribute.

        Arguments
        ---------
        name : str
            Name of the previously unseen attribute.
        """
        if not hasattr(cls, name):
            is_parent = False
        else:
            mapper = inspect(cls).mapper
            rel = [r for r in mapper.relationships if r.key == name]
            if not rel:
                is_parent = False
            else:
                is_parent = cls._handle_relationship_ol(name, rel)
        cls._orderinglist_parent_indicator[name] = is_parent
        return is_parent

    @classmethod
    def _handle_relationship_ol(cls, name, rel):
        """
        `self._set_orderinglist_parent` calls this method when setting the 
        `orderinglist` parent status for an attribute which has a relationship 
        to `self`.

        Arguments
        ---------
        name : str
            Name of the attribute.

        rel : sqlalchemy.orm.relationship
            Relationship of the named attribute to `self`.
        """
        reverse_rel = list(rel[0]._reverse_property)
        if not reverse_rel:
            return False
        reverse_rel = reverse_rel[0]
        cc = reverse_rel.collection_class
        if (
            hasattr(cc, '__module__') 
            and cc.__module__ == 'sqlalchemy.ext.orderinglist'
        ):
            # this expects that the 0th `order_by` column is the index 
            # attribute of the `orderinglist` collection class
            cls._orderinglist_parent_attrs[name] = (
                reverse_rel.key, reverse_rel.order_by[0].name
            )
            return True
        return False
    
    @classmethod
    def _store_orderinglist_parent_attrs(cls, name, reverse_rel):
        """Store attributes of a parent of an orderinglist relationship

        Key attributes are (childlist, order_by). This method expects the 
        zeroth order_by column is the index of the orderinglist collection 
        class.
        """
        cls._orderinglist_parent_attrs[name] = (
            reverse_rel.key, reverse_rel.order_by[0].name
        )