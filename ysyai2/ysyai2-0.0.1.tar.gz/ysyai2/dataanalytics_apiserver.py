from starlette.applications import Starlette
from starlette.responses import JSONResponse
import uvicorn
import datetime
import dateutil.relativedelta
from ysyai2.canvas.apidata import *
from ysyai2.cache import *
import json
from ysyai2.utils import *
import logging

import asyncio

from pandas.io.json import json_normalize
import pandas as pd

import time
import re



from ysyai2.canvas.grade import *

import traceback
import time

from ysyai2.canvas.proc import *
from pathlib import Path
from ysyai2.canvas.myfeedback import *

logging.basicConfig(filename='ysyai2.log',level=logging.CRITICAL,format='%(asctime)s %(levelname)s:%(message)s')


app = Starlette(debug=True)


config_path=Path('config.json')
with config_path.open(mode='r') as f:
    config=json.load(f)

base_string=config['base_string']
token_string=config['token_string']
authcode=config['authcode']
sgtc_conn_str=config['sgtc_conn_string']
sgtc_enrol_yr_num=config['sgtc_enrol_yr_num']
term1a_str=config['term1a_date_str']
num_workers=config['num_workers']
canvas_grade_conn_string=config['canvas_grade_conn_string']
semester1_start_str=config['semester1_start_str'],
semester2_start_str=config['semester2_start_str']
include_sgtc=config['include_sgtc']


if include_sgtc:
    print("importing ysysgtc...")
    from ysysgtc.enrolments.data import *
    from ysysgtc.enrolments.assembler import *
    from ysysgtc.enrolments.transform import *
    from ysysgtc.enrolments.newstudentsconfirmed import *
    from ysysgtc.enrolments.offersleavers import *
    from ysysgtc.enrolments.historicaldata import *
    from ysysgtc.enrolments.historicalproc import *
    from ysysgtc.enrolments.futurestudentstatusdata import *
    from ysysgtc.enrolments.capacity import *
    from ysysgtc.enrolments.waitinglist import *
    from ysysgtc.enrolments.transferinout import *

p=Path('cache')
cache=PickleCache(p)

api_dict=config['api_dict']

learn_data=CanvasDataStore.from_token(cache=cache,
                                      api_dict=api_dict,
                                      url=base_string,
                                      token=token_string,
                                      num_workers=num_workers)

@check_authcode
async def proc_refreshdata(input_authcode,real_authcode):
    try:
        await learn_data.refresh_data()
        r='Refresh data finished successfully'
        return JSONResponse(r)
    except Exception as e:
        tb=traceback.format_exc()
        logging.critical(str(e))
        logging.critical(tb)
        return JSONResponse(str(e))


@check_authcode
async def proc_canvas_myfeedback_dump(input_authcode,real_authcode,table_name='canvas_myfeedback_dump_current'):
    try:
        start_time=time.time()
        r_assignments=learn_data.get_assignments()
        r_assignmentgroups=learn_data.load_obj('assignmentgroups')        
        r_courses=learn_data.load_obj('courses')       
        r_submissions=learn_data.load_obj('submissions')
        r_enrollments=learn_data.load_obj('enrollments')
        r_terms=learn_data.load_obj('enrollmentterms')
        r_terms=json.loads(''.join(r_terms))['enrollment_terms']

        df_submissions = pd.DataFrame.from_dict(r_submissions, orient='columns')
        df_assignments=pd.DataFrame.from_dict(r_assignments, orient='columns')
        df_assignmentgroups=pd.DataFrame.from_dict(r_assignmentgroups, orient='columns')
        df_enrolments=pd.DataFrame.from_dict(r_enrollments, orient='columns')
        df_courses=pd.DataFrame.from_dict(r_courses, orient='columns')
        df_terms=pd.DataFrame.from_dict(r_terms, orient='columns')

        df=proc_myfeedback_dump(df_submissions,df_assignments,df_assignmentgroups,\
            df_enrolments,df_terms,df_courses,term1a_str,table_name=table_name)        
        
        #df_sample=df[:230000]   
        save_grade_to_db(df, canvas_grade_conn_string,table_name=table_name)
        
        end_time=time.time()
        print(f'canvas myfeedback dump size: {len(df)}')
        print(f'canvas myfeedback dump time: {(end_time-start_time)/60} mins')
        r="save canvas myfeedback data to sql server successfully"
        return JSONResponse(r)

    except Exception as e:
        tb = traceback.format_exc()
        logging.critical(str(e))
        logging.critical(tb)
        return JSONResponse(str(e)+'\n'+tb)


@app.route('/dumpcanvasmyfeedbackcurrent')
async def dumpcanvasgrade(request):
    input_authcode=request.query_params['authcode'] if 'authcode' in request.query_params else ''
    #return await proc_refreshdata(input_authcode=input_authcode,real_authcode=authcode)
    refresh_task = asyncio.ensure_future(proc_canvas_myfeedback_dump(input_authcode=input_authcode,real_authcode=authcode))
    return await refresh_task        

@app.route('/dumpcanvasmyfeedbackpast')
async def dumpcanvasgrade(request):
    input_authcode=request.query_params['authcode'] if 'authcode' in request.query_params else ''
    #return await proc_refreshdata(input_authcode=input_authcode,real_authcode=authcode)
    refresh_task = asyncio.ensure_future(proc_canvas_myfeedback_dump(input_authcode=input_authcode,real_authcode=authcode,table_name='canvas_myfeedback_dump_past'))
    return await refresh_task      


@check_authcode
async def proc_canvas_grade_dump(input_authcode,real_authcode,table_name='canvas_grade_dump_current'):
    try:
        start_time=time.time()
        r_assignments=learn_data.get_assignments()
        r_assignmentgroups=learn_data.load_obj('assignmentgroups')        
        r_courses=learn_data.load_obj('courses')       
        r_submissions=learn_data.load_obj('submissions')
        r_enrollments=learn_data.load_obj('enrollments')
        r_terms=learn_data.load_obj('enrollmentterms')
        r_terms=json.loads(''.join(r_terms))['enrollment_terms']

        df_submissions = pd.DataFrame.from_dict(r_submissions, orient='columns')
        df_assignments=pd.DataFrame.from_dict(r_assignments, orient='columns')
        df_assignmentgroups=pd.DataFrame.from_dict(r_assignmentgroups, orient='columns')
        df_enrolments=pd.DataFrame.from_dict(r_enrollments, orient='columns')
        df_courses=pd.DataFrame.from_dict(r_courses, orient='columns')
        df_terms=pd.DataFrame.from_dict(r_terms, orient='columns')
        
        if table_name=='canvas_grade_dump_current':
            df_submissions=filter_grade_submissions(df_submissions,df_assignments,term1a_str)
        else:
            df_submissions=filter_grade_submissions_score(df_submissions)
        df_grade=merge_grade_assignments_and_groups(df_assignments,df_assignmentgroups)
        end_time=time.time()
        print(f'canvas grade dump size: {len(df_grade)}')
        print(f'canvas grade dupm time: {(end_time-start_time)/60} mins')
        df_grade=filter_grade_assignments(df_grade)
        df_grade=merge_grade_submissions(df_grade,df_submissions)
        end_time=time.time()
        print(f'canvas grade dump size: {len(df_grade)}')
        print(f'canvas grade dupm time: {(end_time-start_time)/60} mins')
        df_grade=merge_grade_courses(df_grade,df_courses)
        df_grade=merge_grade_enrollments(df_grade,df_enrolments)
        end_time=time.time()
        print(f'canvas grade dump size: {len(df_grade)}')
        print(f'canvas grade dupm time: {(end_time-start_time)/60} mins')
        df_grade=merge_grade_terms(df_grade,df_terms)

        df_grade=extract_grade_collumns(df_grade)
        #df_grade_sample=df_grade[:10000]
        if table_name=='canvas_grade_dump_current':
            save_grade_to_db(df_grade, canvas_grade_conn_string)
            #pass
        else:
            save_grade_to_db(df_grade, canvas_grade_conn_string,table_name=table_name)
            #pass
        end_time=time.time()
        print(f'canvas grade dump size: {len(df_grade)}')
        print(f'canvas grade dump time: {(end_time-start_time)/60} mins')
        r="save canvas grade data to sql server successfully"
        return JSONResponse(r)

    except Exception as e:
        tb = traceback.format_exc()
        logging.critical(str(e))
        logging.critical(tb)
        return JSONResponse(str(e)+'\n'+tb)


@app.route('/dumpcanvasgradecurrent')
async def dumpcanvasgrade(request):
    input_authcode=request.query_params['authcode'] if 'authcode' in request.query_params else ''
    #return await proc_refreshdata(input_authcode=input_authcode,real_authcode=authcode)
    refresh_task = asyncio.ensure_future(proc_canvas_grade_dump(input_authcode=input_authcode,real_authcode=authcode))
    return await refresh_task


@app.route('/dumpcanvasgradeall')
async def dumpcanvasgrade(request):
    input_authcode=request.query_params['authcode'] if 'authcode' in request.query_params else ''
    #return await proc_refreshdata(input_authcode=input_authcode,real_authcode=authcode)
    refresh_task = asyncio.ensure_future(proc_canvas_grade_dump(input_authcode=input_authcode,real_authcode=authcode,table_name='canvas_grade_dump_all'))
    return await refresh_task

@app.route('/')
async def homepage(request):
    return JSONResponse('This is Data Analytics API server')

@app.route('/refreshdata')
async def refreshdata(request):
    input_authcode=request.query_params['authcode'] if 'authcode' in request.query_params else ''
    #return await proc_refreshdata(input_authcode=input_authcode,real_authcode=authcode)
    refresh_task = asyncio.ensure_future(proc_refreshdata(input_authcode=input_authcode,real_authcode=authcode))
    return await refresh_task


@app.route('/coursesections')
async def coursesections(request):
    try:
        jstr=learn_data.load_obj('coursesections')
        jstr=''.join(jstr)
        jstr = '['+re.sub(r"}{", "},{", jstr)+']'
        r_coursesections=json.loads(jstr)
        
        return JSONResponse(r_coursesections)
    except Exception as e:
        return JSONResponse(str(e))

@app.route('/enrollmentterms')
async def enrollmentterms(request):
    try:
        r_terms=learn_data.load_obj('enrollmentterms')
        r_terms=json.loads(''.join(r_terms))
        r_terms=r_terms['enrollment_terms']
        return JSONResponse(r_terms)
    except Exception as e:
        return JSONResponse(str(e))

async def process_assignments(request):
    r_assignments=learn_data.get_assignments()
    df_assignments=pd.DataFrame.from_dict(r_assignments, orient='columns')
    df_assignments=add_assignments_filterdate(df_assignments)
    df_assignments['is_pub']=df_assignments.loc[:,:].apply(lambda x: 'P' if x.published else '', axis=1)
    df=filter_assignments(df_assignments,term1a_str)
    df=df.fillna(0)
    r_filtered=df.to_dict('records')
    return r_filtered

@app.route('/assignments')
async def assignments(request):
    try:
        task = asyncio.ensure_future(process_assignments(request))
        r_filtered = await task
        return JSONResponse(r_filtered)
    except Exception as e:
        tb = traceback.format_exc()        
        logging.critical(str(e))
        logging.critical(tb)
        return JSONResponse(str(e))

async def process_enrollments(request):
    r_enrollments=learn_data.load_obj('enrollments')
    df_enrolments=pd.DataFrame.from_dict(r_enrollments, orient='columns')
    recent_date_enrol=get_recent_date(12)
    conditions_enrol=df_enrolments['updated_at']>recent_date_enrol
    df=df_enrolments.loc[conditions_enrol,:]
    df=df.fillna(0)
    r_filtered=df.to_dict('records')
    return r_filtered

@app.route('/enrollments')
async def enrollments(request):
    try:
        task = asyncio.ensure_future(process_enrollments(request))
        r_filtered= await task
        return JSONResponse(r_filtered)
    except Exception as e:
        return JSONResponse(str(e))

async def process_canvas_user_id_link(request):
    #r=learn_data.get_enrollments()
    r_enrollments=learn_data.load_obj('enrollments')
    df_enrolments=pd.DataFrame.from_dict(r_enrollments, orient='columns')
    
    #recent_date_enrol=get_recent_date(12)
    #conditions_enrol=df_enrolments['updated_at']>recent_date_enrol
    #df_enrolments=df_enrolments.loc[conditions_enrol,:]
    #df_enrolments=df_enrolments.fillna(0)

    df_enrolments['sis_user_id_letter']=df_enrolments['sis_user_id'].str[:1]
    df_enrolments['sis_user_id_number']=df_enrolments['sis_user_id'].str[1:]
    conditions_canvas_user_id_link = (df_enrolments['sis_user_id'].isnull()!=True) & (df_enrolments['type']=='StudentEnrollment')
    df=df_enrolments.loc[conditions_canvas_user_id_link,['user_id','type','sis_user_id_letter','sis_user_id_number']]
    
    r_filtered=df.to_dict('records')
    return r_filtered


@app.route('/canvas_user_id_link')
async def canvas_user_id_link(request):
    try:        
        task = asyncio.ensure_future(process_canvas_user_id_link(request))
        r_filtered = await task
        return JSONResponse(r_filtered)
    except Exception as e:
        return JSONResponse(str(e))

@app.route('/users')
async def users(request):
    try:
        r=learn_data.load_obj('users')
        #await asyncio.sleep(10)
        return JSONResponse(r)
    except Exception as e:
        return JSONResponse(str(e))

@app.route('/quizzes')
async def quizzes(request):
    try:
        r=learn_data.get_quizzes()
        #await asyncio.sleep(10)
        return JSONResponse(r)
    except Exception as e:
        return JSONResponse(str(e))

async def process_submissions(request):
    r=learn_data.load_obj('submissions')
    r_assignments=learn_data.load_obj('assignments')
    #df = pd.DataFrame.from_dict(json_normalize(r), orient='columns')
    #fix the str has no keys issue in r
    for idx,o in enumerate(r):
        if hasattr(o, 'keys')==False:
            logging.info(f"error:{idx}")
            del(r[idx])
    df = pd.DataFrame.from_dict(r, orient='columns')
    df_assignments = pd.DataFrame.from_dict(r_assignments, orient='columns')
    df_assignments=add_assignments_filterdate(df_assignments)
    df_assignments=filter_assignments(df_assignments,term1a_str)
    #recent_oneyear=get_recent_oneyear()
    #recent_date=get_recent_date(1)
    df=filter_submssions(df,df_assignments)
    df=df[df.columns.difference(['url','preview_url','attachments','external_tool_url','turnitin_data','discussion_entries','anonymous_id','body','workflow_state','seconds_late','extra_attempts','graded_at','cached_due_date','posted_at'])]
    #df=df[df['submitted_at']>recent_oneyear]
    df=df.fillna(0)
    r_filtered=df.to_dict('records')
    #r_filtered=df.to_json(orient='records')
    return r_filtered    

@app.route('/submissions')
async def submissions(request):
    try:       
        task = asyncio.ensure_future(process_submissions(request))
        r_filtered = await task
        return JSONResponse(r_filtered)
    except Exception as e:
        tb=traceback.format_exc()
        logging.critical(str(e))
        logging.critical(tb)
        return JSONResponse(str(e))

@app.route('/courses')
async def courses(request):
    try:
        r=learn_data.load_obj('courses')
        return JSONResponse(r)
    except Exception as e:
        return JSONResponse(str(e))

@app.route('/assignmentgroups')
async def assignmentgroups(request):
    try:
        r=learn_data.load_obj('assignmentgroups')
        return JSONResponse(r)
    except Exception as e:
        return JSONResponse(str(e))



@app.route('/test_parallel_query/{id}')
async def test_parallel_query(request):
    time.sleep(1)
    id=request.path_params['id']
    
    id_str=f'This is the id: {id}'
    print(id_str)
    ids=[int(id),2*int(id),3*int(id)]
    return JSONResponse(ids)

async def process_sgtc_enrolments(request):
    #init the processors
    conn = pyodbc.connect(sgtc_conn_str)
    enrol_dl = EnrolDataLoader(db_conn=conn,term1a_str=term1a_str)
    #hist_leavers_dl=HistoricalLeaversDataLoader(db_conn=conn)
    hist_dl=HistoricalDataLoader(db_conn=conn)
    hist_future_dl=HistoricalFutureDataLoader(db_conn=conn)
    student_status_dl=FutureStudentStatusDataLoader(db_conn=conn)
    procs=[CurrentEnrolProc,ConfirmedNewStuProc,NewStuPriorYearProc,OffersOutstandingProc,LeaversProc,HistoricalLeaversProc,HistoricalCurrentEnrolProc,HistoricalNewStudentProc,HistoricalOffersProc,CapacityProc,WaitingListInterviewProc,WaitingListNotActionedProc,TransferOutProc,TransferInProc]
    enrol_assembler=EnrolAssembler(procs=procs,num_of_years=sgtc_enrol_yr_num,term1a_str=term1a_str)

    #load data
    enrol_dl.load_data()
    #hist_leavers_dl.load_data()
    hist_dl.load_data()
    hist_future_dl.load_data()
    student_status_dl.load_data()
    df_dict=enrol_dl.get_data_dict()
    #df_dict.update(hist_leavers_dl.get_data_dict())
    df_dict.update(hist_dl.get_data_dict())
    df_dict.update(hist_future_dl.get_data_dict())
    df_dict.update(student_status_dl.get_data_dict())

    #calculate enrolment stats
    r=enrol_assembler(df_dict=df_dict)        
    return r


@app.route('/sgtc_enrolments')
async def sgtc_enrolments(request):
    try:
        task=asyncio.ensure_future(process_sgtc_enrolments(request))
        r = await task

        return JSONResponse(r)
    except Exception as e:
        #time.sleep(60)
        #init_sgtc_process_withretry()
        logging.critical(str(e))
        return JSONResponse(str(e))


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
