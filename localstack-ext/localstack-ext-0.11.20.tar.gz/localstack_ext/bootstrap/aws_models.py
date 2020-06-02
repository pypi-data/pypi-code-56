from localstack.utils.aws import aws_models
RAFaP=super
RAFaU=None
RAFal=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  RAFaP(LambdaLayer,self).__init__(arn)
  self.cwd=RAFaU
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,RAFal,env=RAFaU):
  RAFaP(RDSDatabase,self).__init__(RAFal,env=env)
 def name(self):
  return self.RAFal.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
