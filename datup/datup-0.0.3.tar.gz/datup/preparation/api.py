'''
The api take the preparation methods and send it to the root datup folder
'''

from datup.preparation.data_preparation import (
    col_cast, 
    featureselection_correlation, 
    Error,
    CorrelationError
) 