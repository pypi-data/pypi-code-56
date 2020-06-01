
from emora._flows._nlu_personal import _nlu_personal
from emora._flows._nlu_user_profiling import _nlu_user_profiling
from emora._flows._nlu_topic_specific import _nlu_topic_specific
from emora._flows._nlu_testing import _nlu_testing
from emora._flows._nlu_privacy import _nlu_privacy
from emora._flows._nlu_world import _nlu_world
from emora._flows._nlu_disbelief import _nlu_disbelief
from emora._flows._nlu_relationships import _nlu_relationships
from emora._flows._nlu_requests import _nlu_requests

personal_nlu = {}
for d in [_nlu_personal,_nlu_disbelief,_nlu_user_profiling,_nlu_privacy,_nlu_relationships,
          _nlu_requests,_nlu_world,_nlu_topic_specific,_nlu_testing]:
    personal_nlu.update(d)

romantic_partner = '[[!my $partner=#ONT(partner)]]'
children = '[[!my $child=#ONT(child)]]'
sibling = '[[!my $sibling=#ONT(sibling)]]'
work = '[[!my {work,job,boss}]]'
school = '[[!my {school,college,university}]]'
pet = '[my cat]'
repeat = '<{' \
         '[![!{can,will,could} you]? repeat, {that,what you said,you said}?],' \
         '[![!{can,will,could} you]? say {that,it} again],' \
         '[!what did you, just? say],' \
         '[!what was that]' \
         '}, #CNC(movies), #CNC(music), #CNC(sports), #CNC(external_news)> #COPY(__goal_return_state__)'

global_update_rules = {
    '#CONTRACTIONS': '',
    romantic_partner: '',
    children: '',
    sibling: '',
    work: '#SET($is_employed=True)',
    school: '#SET($is_student=True)',
    pet:'',
    repeat: '#REPEAT (15.0)'
}