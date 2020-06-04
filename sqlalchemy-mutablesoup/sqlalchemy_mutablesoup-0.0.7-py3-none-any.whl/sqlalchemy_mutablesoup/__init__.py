"""# Mutable BeautifulSoup database type

## Examples

#### Setup

```python
from sqlalchemy_mutablesoup import MutableSoupType

from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# standard session creation
engine = create_engine('sqlite:///:memory:')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
session = Session()
Base = declarative_base()

# define and instantiate a model with a MutableSoupType column.
class Model(Base):
\    __tablename__ = 'model'
\    id = Column(Integer, primary_key=True)
\    soup = Column(MutableSoupType)
    
Base.metadata.create_all(engine)

model = Model()
session.add(model)
```

#### Setting soup objects

```python
model.soup = '<p>Hello World.</p>'
model.soup
```

Out:

```
<p>Hello World.</p>
```

#### Setting soup elements: basic use

```python
model.soup.set_element(parent_selector='p', val='Hello Moon.')
session.commit()
model.soup
```

Out:

```
<p>Hello Moon.</p>
```

#### Creating soup elements with a `gen_target` function

```python
def gen_span_tag(*args, **kwargs):
\    print('My args are:', args)
\    print('My kwargs are:', kwargs)
\    return '<span></span>'

model.soup.set_element(
\    parent_selector='p',
\    val='Span text',
\    target_selector='span',
\    gen_target=gen_span_tag,
\    args=['hello world'],
\    kwargs={'hello': 'moon'},
)
session.commit()
model.soup
```

Out:

```
My args are: ('hello world',)
My kwargs are: {'hello': 'moon'}
<p>Hello Moon.<span></span></p>
```

#### Registering changes

Call `changed` to register other changes with the database.

```python
model.soup.select_one('p')['style'] = 'color:red;'
model.soup.changed()
session.commit()
model.soup
```

Out:

```
<p style="color:red;">Hello Moon.<span></span></p>
```
"""

from bs4 import BeautifulSoup
from flask import Markup
from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TypeDecorator, Unicode

from copy import copy


class SoupBase(BeautifulSoup):
    """
    Base for `MutableSoup` objects. Interits from `bs4.BeautifulSoup`.
    """
    def text(self, selector):
        """
        Get text from html element.

        Parameters
        ----------
        selector : str
            CSS selector.

        Returns
        -------
        text : str or None
            Return text from selected html element. Return `None` if no 
            element is selected.
        """
        elem = self.select_one(selector)
        return None if elem is None else elem.text

    def copy(self):
        """
        Returns
        -------
        self : sqlalchemy_mutablesoup.SoupBase
            Shallow copy of `self`.
        """
        return copy(self)

    def render(self):
        """
        Render html for insertion into a Jinja template.
        
        Returns
        -------
        rendered : flask.Markup
            Rendered html.
        """
        return Markup(str(self))

    def set_element(
            self, parent_selector, val, target_selector=None, 
            gen_target=None, args=(), kwargs={}
        ):
        """
        Set a soup element.

        Parameters
        ----------
        parent_selector : str
            CSS selector for the parent of the html element being set (the 
            'target element').

        val : str or bs4.BeautifulSoup
            Value to which the target element will be set. If `val` 
            evaluates to `False`, the target element is cleared.

        target_selector : str or None, default=None
            CSS selector for the target element; a child of the parent 
            element. If `None`, the parent element is treated as the target 
            element.

        gen_target : callable or None, default=None
            Callable which generates the target element if none of the 
            parent element's children are selected by the `target_selector`. 
            The output of `gen_target` should be a string or `bs4.
            BeautifulSoup` object.

        args : iterable
            Arguments for `gen_target`.

        kwargs : dict
            Keyword arguments for `gen_target`.

        Returns
        -------
        self : sqlalchemy_mutablesoup.SoupBase
        """
        parent = self.select_one(parent_selector)
        target = self._get_target(
            parent, target_selector, gen_target, args, kwargs
        )
        target.clear()
        if val:
            target.append(self._convert_to_soup(val))
        return self

    def _get_target(self, parent, target_selector, gen_target, args, kwargs):
        """
        Get the target element. If the target element cannot be found using 
        the `target_selector`, the `gen_target` method creates a target 
        element and it is appended to the parent element.

        Arguments
        ---------
        parent : bs4.Tag
            Parent soup element. Additional arguments follow the definitions 
            of `set_element`.

        Returns
        -------
        target : bs4.Tag
            Target soup element. If the `target_selector` is `None`, the 
            target element is the parent element.
        """
        if target_selector is None:
            return parent
        target = parent.select_one(target_selector)
        if target is None:
            target = self._convert_to_soup(gen_target(*args, **kwargs))
            parent.append(target)
        return target

    def _convert_to_soup(self, obj):
        """
        Convert an object to a `bs4.BeautifulSoup` object.

        Arguments
        ---------
        obj : str or `bs4.BeautifulSoup`
            Object to convert.

        Returns
        -------
        soup : bs4.BeautifulSoup
            Converted object.
        """
        return (
            obj if isinstance(obj, BeautifulSoup) 
            else BeautifulSoup(str(obj), 'html.parser')
        )


class MutableSoup(Mutable, SoupBase):
    """
    Mutable BeautifulSoup database object. Inherits from `SoupBase`. Note 
    that a `MutableSoup` object can be set using a string or 
    `bs4.BeautifulSoup` object.
    """
    @classmethod
    def coerce(cls, key, obj):
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, str):
            return cls(obj, 'html.parser')
        if isinstance(obj, BeautifulSoup):
            return cls(str(obj), 'html.parser')
        return super().coerce(key, obj)

    def set_element(self, *args, **kwargs):
        """
        Inherits from `SoupBase.set_element`. The only addition is that this 
        method also registers that it has changed.

        Returns
        -------
        self : sqlalchemy_mutable.MutableSoup
        """
        super().set_element(*args, **kwargs)
        self.changed()
        return self

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d


class MutableSoupType(TypeDecorator):
    """
    Mutable BeautifulSoup database type associated with `MutableSoup` object.
    """
    impl = Unicode

    def process_bind_param(self, value, dialect):
        """Encode as string when storing in database."""
        return str(value)

    def process_result_value(self, value, dialect):
        """Restore `BeautifulSoup` object when accessing from database."""
        return None if value is None else BeautifulSoup(value, 'html.parser')


MutableSoup.associate_with(MutableSoupType)