from localstack.utils.aws import aws_models
OoRdM=super
OoRdY=None
OoRdp=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  OoRdM(LambdaLayer,self).__init__(arn)
  self.cwd=OoRdY
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,OoRdp,env=OoRdY):
  OoRdM(RDSDatabase,self).__init__(OoRdp,env=env)
 def name(self):
  return self.OoRdp.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
