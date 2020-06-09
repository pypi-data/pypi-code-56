"""# Function mixin"""

from sqlalchemy import Column, Integer, PickleType
from sqlalchemy.inspection import inspect
from sqlalchemy_mutable import MutableListType, MutableDictType


class FunctionMixin():
    """
    A mixin for 'Function models'. When called, a Function model executes its 
    function, passing in its parent (if applicable) and its args and kwargs.

    Parameters
    ----------
    parent : usually a database model or None, default=None
        The Function model's parent is usually a database model which 
        subclasses a `sqlalchemy.ext.declarative.declarative_base()`.

    func : callable or None, default=None
        The function which the Function model will execute when called.

    args : iterable, default=[]
        Arguments which the Function model will pass into its `func` when 
        called.

    kwargs : dict, default={}
        Keyword arguments which the Function model will pass into its `func` 
        when called.

    Attributes
    ----------
    parent : usually a database model of None
        Set from the `parent` parameter.

    func : callable sqlalchemy.PickleType
        Set from the `func` parameter.

    args : sqlalchemy_mutable.MutableListType
        Set from the `args` parameter.

    kwargs : sqlalchemy_mutable.MutableDictType
        Set from the `kwargs` parameter.

    Examples
    --------
    In the setup, we create a SQLAlchemy session, define a Parent model 
    subclassing `FunctionRelator`, and a Function model subclassing 
    `FunctionMixin`.

    ```python
    from sqlalchemy_function import FunctionMixin, FunctionRelator

    from sqlalchemy import create_engine, Column, ForeignKey, Integer
    from sqlalchemy.orm import relationship, sessionmaker, scoped_session
    from sqlalchemy.ext.declarative import declarative_base

    # standard session creation
    engine = create_engine('sqlite:///:memory:')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    Base = declarative_base()

    # define a Parent model with the FunctionRelator
    class Parent(FunctionRelator, Base):
    \    __tablename__ = 'parent'
    \    id = Column(Integer, primary_key=True)

    \    # Fuction models must reference their parent with a `parent` attribute
    \    functions = relationship('Function', backref='parent')

    # define a Function model with the FunctionMixin
    class Function(FunctionMixin, Base):
    \    __tablename__ = 'function'
    \    id = Column(Integer, primary_key=True)
    \    parent_id = Column(Integer, ForeignKey('parent.id'))

    Base.metadata.create_all(engine)
    ```

    We can now store and later call functions as follows.

    ```python
    def foo(parent, *args, **kwargs):
    \    print('My parent is', parent)
    \    print('My args are', args)
    \    print('My kwargs are', kwargs)
    \    return 'return value'

    parent = Parent()
    function = Function(
    \    parent, func=foo, args=['hello world'], kwargs={'goodbye': 'moon'}
    )
    parent.functions[0]()
    ```

    Out:

    ```
    My parent is <__main__.Parent object at 0x7f2bb5c12518>
    My args are ('hello world',)
    My kwargs are {'goodbye': 'moon'}
    'return value'
    ```
    """
    func = Column(PickleType)
    args = Column(MutableListType)
    kwargs = Column(MutableDictType)

    def __init__(self, parent=None, func=None, args=[], kwargs={}):
        if parent is not None:
            self.parent = parent
        self.func = func
        self.args, self.kwargs = args, kwargs
        super().__init__()

    @classmethod
    def register(cls, func):
        """
        Class method which registers a function with the Function model. This simplifies the syntax for creating Function models and associating them with their parents.

        Parameters
        ----------
        func : callable
            The registered function.

        Returns
        -------
        func : callable
            Original `func` parameter.

        Examples
        --------
        Follow the setup above.

        ```python
        @Function.register
        def foo(parent, *args, **kwargs):
        \    print('My parent is', parent)
        \    print('My args are', args)
        \    print('My kwargs are', kwargs)
        \    return 'return value'

        parent = Parent()
        Function.foo(parent, 'hello world', goodbye='moon')
        parent.functions[0]()
        ```

        Out:

        ```
        My parent is <__main__.Parent object at 0x7f2bc4269588>
        My args are ('hello world',)
        My kwargs are {'goodbye': 'moon'}
        'return value'
        ```
        """
        def add_function(parent, *args, **kwargs):
            cls(parent, func, list(args), kwargs)
        setattr(cls, func.__name__, add_function)
        return func
    
    def __call__(self):
        """
        Call `self.func`, passing in `self.parent` (if applicable) and 
        `*self.args, **self.kwargs`.

        **Note.** If the arguments or keyword arguments contain database models, 
        they will be 'unshelled' when they are passed into the function. See 
        <https://dsbowen.github.io/sqlalchemy-mutable> for more detail.

        Returns
        -------
        output : 
            Output of `self.func`.
        """
        if self.func is None:
            return
        args = self.args.unshell()
        kwargs = self.kwargs.unshell()
        if hasattr(self, 'parent'):
            return self.func(self.parent, *args, **kwargs)
        return self.func(*args, **kwargs)