# Explanation of priorities (#A, #B, #C)
#  #A: Needs to be in prototype
#  #B: Needs to be in when deploying to production
#  #C: Better behaviour, but at this stage non-essential

# TODO: [#C] Ensure the DAG model also appears in the API documentation, Add
#            something like, marshall_with to DagCollection.get
# TODO: [#C] Remove 'message' field from Flask-RestPlus error response. See
#            also: https://github.com/noirbizarre/flask-restplus/pull/377
# TODO: [#A] Update Flask RestPlus when available, since 0.13.0 depends on
#            deprecated werkzeug functionality.
