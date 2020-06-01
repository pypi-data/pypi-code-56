from pynwb import register_class
from pynwb.file import DynamicTable
from hdmf.common.table import VectorData
from hdmf.utils import docval, call_docval_func, get_docval, getargs


@register_class('SurveyTable', 'ndx-survey-data')
class SurveyTable(DynamicTable):
    """
    Table for storing survey data
    """

    __columns__ = (
        {'name': 'unix_timestamp', 'description': 'UNIX time of survey response', 'required': True,
         'index': False},
    )

    @docval(dict(name='name', type=str, doc='name of this SurveyTable',
                 default='SurveyTable'),  # required
            dict(name='description', type=str, doc='Description of this DynamicTable',
                 default='references the survey table'),
            *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'))
    def __init__(self, **kwargs):
        call_docval_func(super(SurveyTable, self).__init__, kwargs)


@register_class('QuestionResponse', 'ndx-survey-data')
class QuestionResponse(VectorData):
    """
    Response data and question
    """
    __nwbfields__ = ('name',)

    @docval(dict(name='name', type=str, doc='name of this QuestionResponse', default='QuestionResponse'),
            dict(name='description', type=str, doc='description of this QuestionResponse', default='QuestionResponse'),
            dict(name='options', type=('array_data', 'data'), doc='Response options', default='QuestionResponse'),
           *get_docval(VectorData.__init__, 'data'))
    def __init__(self, **kwargs):
        call_docval_func(super(QuestionResponse, self).__init__, kwargs)
        self.options = getargs('options', kwargs)
