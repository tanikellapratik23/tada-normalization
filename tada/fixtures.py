"""Seeded synthetic fixtures constructed from the approved schemas, never API examples."""
from copy import deepcopy
from pathlib import Path
import json
import random
from .contracts import schema_for, resolve, SCHEMAS


def sample(schema, root, rng, depth=0, complete=False, name=''):
    schema=resolve(schema,root)
    if 'enum' in schema:return schema['enum'][0]
    kind=schema.get('type','object' if 'properties' in schema else 'string')
    if isinstance(kind,list):kind=next((k for k in kind if k!='null'),'null')
    if kind=='object':
        props=schema.get('properties',{})
        keys=props if complete and depth<4 else schema.get('required',[])
        if depth>9:return {}
        return {k:sample(props[k],root,rng,depth+1,complete,k) for k in keys if k in props}
    if kind=='array':return []
    if kind=='boolean':return False
    if kind in ('integer','number'):
        return max(schema.get('minimum',0),1)
    if kind=='null':return None
    if schema.get('format')=='date-time':return '2026-01-15T00:00:00Z'
    if schema.get('format')=='date' or 'date' in name.lower() or 'yyyy-mm-dd' in schema.get('description',''):return '2026-01-15'
    if name in ('zipCode','zipcode'):return '28202'
    if name=='country':return 'USA'
    if schema.get('format')=='byte':return ''
    if schema.get('format') in ('uri','url'):return 'https://example.invalid/synthetic'
    length=max(schema.get('minLength',0),min(schema.get('maxLength',32),12))
    return ('synthetic'+str(rng.randrange(1000,9999)))[:length]


def merge(dest, values):
    for key,value in values.items():
        if isinstance(value,dict) and isinstance(dest.get(key),dict):merge(dest[key],value)
        else:dest[key]=deepcopy(value)


def generate(seed=42):
    rng=random.Random(seed)
    bundle=[]
    for provider, entities in SCHEMAS.items():
        for entity in entities:
            schema,root,evidence=schema_for(provider,entity)
            raw=sample(schema,root,rng,complete=entity=='employee')
            ctx={'tenant_id':'synthetic-demo','company_id':'1','employee_id':'101','record_id':'1','payroll_run_id':'501'}
            overrides={
             'company': {'id':'1' if provider=='prismhr' else 1},
             'employee':{'id':'101' if provider=='prismhr' else 101},
             'direct_deposit':{'id':201},'deduction':{'id':301},'payroll_run':{'id':501},'paycheck':{'id':601},
             'compensation':{'id':701},'pay_info':{},'demographics':{}
            }[entity]
            if provider=='prismhr':
                overrides={
                 'company':{'id':'1','clientName':'Synthetic Northwind','legalName':'Synthetic Northwind LLC','statusClass':'A'},
                 'employee':{'id':'101','firstName':'Avery','lastName':'Example','middleInitial':'Q','preferredName':'Avery',
                    'client':{'statusClass':'A','firstHireDate':'2024-01-15','lastHireDate':'2024-01-15','manager':'102'},
                    'compensation':{'payMethod':'H','hourlyPay':'25.125','salary':'0','annualPay':'52260','standardHours':'80'},
                    'contactInformation':{'emailAddress':'avery@example.invalid'}},
                 'direct_deposit':{'transitNum':'000000000','accountNum':'000000000001','accountType':'C','method':'P','amount':25,'status':'D'},
                 'deduction':{'deductionCode':'SYN401','deductionType':'K','amount':5,'usePercent':True,'period':'1','startDate':'2026-01-01'},
                 'payroll_run':{'batchId':'501','type':'R','payDate':'2026-01-30','grossEarnings':'2000.00'},
                 'paycheck':{'voucherId':'601','batchId':'501','employeeId':'101','totalEarnings':2000,'netPay':1500,'payDate':'2026-01-30',
                     'payPeriodStart':'2026-01-01','payPeriodEnd':'2026-01-15','employeeTax':[{'empTaxDeductCode':'FIT','empTaxAmount':400,'empTaxableAmount':2000,'empOverLimitAmount':0}],
                     'deduction':[{'deductCode':'SYN401','deductAmount':100,'deductDescription':'Synthetic retirement','deductType':'K','deductUnionId':'','planId':'SYN401'}], 'earning':[{'payCode':'REG','chargeDate':'2026-01-15','hoursWorked':80,'hoursUnits':80,'payAmount':25}],
                     'employerContributions':[{'code':'SYN401','description':'Employer match','amount':50}]}
                }[entity]
            elif provider=='isolved':
                extra={
                 'company':{'legalName':'Synthetic Northwind LLC','dbaName':'Synthetic Northwind'},
                 'employee':{'nameAddress':{'firstName':'Avery','lastName':'Example','zipCode':'28202','state':'NC'},'hourlyRate':25.125,
                       'annualSalary':52260,'normalHours':80,'employmentStatus':'Active','hireDate':'2024-01-15T00:00:00Z'},
                 'direct_deposit':{'accountNumber':'000000000001','routingNumber':'000000000','accountType':'Checking','percent':25,'sequenceNumber':1,'status':'Active'},
                 'deduction':{'employeeId':101,'payItemName':'Synthetic retirement','payItemCode':'SYN401','payItemType':'Deduction','calcParams':[{'paramType':'TenantPercent','paramValue':5}]},
                 'payroll_run':{'runNumber':7,'payDate':'2026-01-30T00:00:00Z','periodBeginDate':'2026-01-01T00:00:00Z','periodEndDate':'2026-01-15T00:00:00Z'},
                 'paycheck':{'employeeId':101,'grossPay':2000,'netPay':1500,'payrollRunNumber':7,'checkDate':'2026-01-30T00:00:00Z',
                    'earnings':[{'itemCode':'REG','checkDollars':2000,'checkHours':80,'ytdDollars':6000}],
                    'deductions':[{'itemCode':'SYN401','checkDollars':100,'ytdDollars':300}],
                    'taxes':[{'itemCode':'FIT','checkDollars':400,'isEmployeeTax':True}]}
                }[entity];overrides.update(extra)
            else:
                extra={
                 'employee':{'username':'synthetic.avery','first_name':'Avery','last_name':'Example','primary_email':'avery@example.invalid',
                     'address':{'country':'USA','zip':'28202'},'status':'Active','dates':{'hired':'2024-01-15'}},
                 'direct_deposit':{'type':'DIRECT_DEPOSIT','sequence':1,'active':True,'active_from':'2026-01-01','active_to':'9999-12-31',
                     'calc_method':{'type':'NET_PAY','display_name':'Percentage of net'},'percentage':25,'account_type':'CHECKING',
                     'account_number':'000000000001','routing_number':'000000000','_links':{'self':'https://example.invalid/deposits/201'}},
                 'deduction':{'deduction':{'code':'SYN401','name':'Synthetic retirement'},'effective_from':'2026-01-01','effective_to':'9999-12-31',
                     'ee_calc_method':{'method':{'type':'TENANT_PERCENT'},'percent':5}},
                 'payroll_run':{'type':{'id':1},'pay_date':'2026-01-30','status':'FINALIZED','start_date':'2026-01-01','end_date':'2026-01-15'},
                 'paycheck':{'employee':{'account_id':101},'type':{'id':1},'pay_date':'2026-01-30','status':'FINALIZED',
                     'earnings':[{'earning':{'code':'REG','name':'Regular'},'ee_amount':2000,'hours':80}],
                     'deductions':[{'deduction':{'code':'SYN401','name':'Retirement'},'ee_amount':100,'er_amount':50}],
                     'taxes':[{'company_tax':{'code':'FIT','name':'Federal'},'ee_amount':400}]},
                 'compensation':{'employee':{'account_id':101},'effective_from':'2026-01-01','amount':52000,'hourly_pay':25,
                     'currency':'USD','amount_period':'YEAR','time':288000000,'time_period':'PAY_PERIOD','num_pp_in_year':26},
                 'pay_info':{'standard_work_day':28800000,'payroll_classification':'REGULAR','default_job':{'id':10}},
                 'demographics':{}
                }[entity];overrides.update(extra)
            merge(raw,overrides)
            if entity in ('company','employee','payroll_run'):ctx.pop('employee_id')
            if entity=='employee':ctx['record_id']='101'
            if entity=='payroll_run':ctx['record_id']='501'
            if entity=='direct_deposit' and provider=='prismhr':ctx['record_id']='deposit-slot-1'
            if entity=='deduction' and provider=='prismhr':ctx['record_id']='SYN401'
            bundle.append({'provider':provider,'entity':entity,'context':ctx,'record':raw,'evidence':evidence})
    # UKG company metadata is caller supplied, explicitly distinguished from provider response fixtures.
    bundle.append({'provider':'ukg-ready','entity':'company','context':{'tenant_id':'synthetic-demo','company_id':'1'},
                   'record':{'id':1,'name':'Synthetic Northwind'},'evidence':'caller context'})
    return bundle


def write(directory, seed=42):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    records=generate(seed)
    (directory/'synthetic.json').write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
    (directory/'manifest.json').write_text(json.dumps({'seed':seed,'generator':'tada.fixtures.generate',
      'reference_commit':'4034f3347cba0abedb75443e8f782364ad108331','records':len(records),'data_classification':'synthetic only'},indent=2)+'\n')
