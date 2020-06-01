from localstack.utils.aws import aws_models
tqTKL=super
tqTKF=None
tqTKR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tqTKL(LambdaLayer,self).__init__(arn)
  self.cwd=tqTKF
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,tqTKR,env=tqTKF):
  tqTKL(RDSDatabase,self).__init__(tqTKR,env=env)
 def name(self):
  return self.tqTKR.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
