from localstack.utils.aws import aws_models
NQMAd=super
NQMAL=None
NQMAp=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  NQMAd(LambdaLayer,self).__init__(arn)
  self.cwd=NQMAL
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,NQMAp,env=NQMAL):
  NQMAd(RDSDatabase,self).__init__(NQMAp,env=env)
 def name(self):
  return self.NQMAp.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
