"""SYNTHETIC annotation fixtures only; no claimed real assessor judgments."""

from copy import deepcopy
import csv
import json
from pathlib import Path

import pandas as pd
import pytest
from sklearn.metrics import cohen_kappa_score

from src.evaluation.pilot import (
    PILOT_FIELDS, agreement_report, annotation_template, build_pilot,
    load_pilot_annotations, readiness_report, validate_pilot_annotations, validate_registry,
)


@pytest.fixture
def sample():
    data = pd.DataFrame({'player_id':list(range(1,13)), 'age':[18,19,21,22,23,24,25,26,27,28,31,32], 'position':['Attack']*12})
    scenario = {'scenario_id':'SYNTHETIC_process', 'candidate_ids':list(range(1,13)),
                'methods':{'cosine':{'top5_ids':[1,2,3,4,5]}}}
    manifest = build_pilot([scenario], data, 'a'*64)
    return data, scenario, manifest


def registry(source='SYNTHETIC'):
    return {name:{'label_source':source,'independence_confirmed':True,'review_evidence':'SYNTHETIC contract test, not human review'}
            for name in ['Fixture_A','Fixture_B']}


def graded_rows(manifest, source='SYNTHETIC'):
    rows=[]
    for assessor, sequence in [('Fixture_A',[0,1,2,3,0,1,2,3]),('Fixture_B',[0,2,2,3,1,1,2,0])]:
        for row, grade in zip(annotation_template(manifest),sequence):
            rows.append({**row, 'assessor_id':assessor,'timestamp':'2026-11-03T10:00:00+07:00',
                         'relevance_grade':grade,'evidence':'SYNTHETIC mathematical fixture; no real player',
                         'label_source':source,'decision_status':'graded','uncertainty':'medium'})
    return rows


def test_pilot_deterministic_stratified_and_blinded(sample):
    data, scenario, manifest=sample
    assert manifest==build_pilot([scenario],data.iloc[::-1],'a'*64)
    permuted=deepcopy(scenario); permuted['candidate_ids'].reverse()
    permuted['methods']['cosine']['top5_ids']=[12,11,10,9,8]
    assert manifest==build_pilot([permuted],data,'a'*64)
    assert manifest!=build_pilot([scenario],data,'a'*64,seed=13)
    case=manifest['scenarios'][0]
    assert len(case['selected_ids'])==8 and len(set(case['selected_ids']))==8
    assert all(s['selected']>0 for s in case['strata'].values())
    rows=annotation_template(manifest)
    assert validate_pilot_annotations(rows,manifest,{})=={'rows':8,'graded':0,'abstain':0,'pending':8}
    assert all(r['assessor_id']==r['timestamp']=='' and r['relevance_grade'] is None for r in rows)
    assert not {'rank','similarity_score','method'} & set(rows[0])


@pytest.mark.parametrize('n',[1,5,12,99])
def test_small_pools_and_large_sample_count(sample,n):
    data,scenario,_=sample
    m=build_pilot([scenario],data,'a'*64,per_scenario=n)
    assert len(m['scenarios'][0]['selected_ids'])==min(n,12)


@pytest.mark.parametrize('kwargs',[{'seed':-1},{'seed':True},{'seed':1.2},{'per_scenario':0},{'per_scenario':True},{'per_scenario':float('nan')}])
def test_invalid_sampling_parameters(sample,kwargs):
    data,scenario,_=sample
    with pytest.raises(ValueError):build_pilot([scenario],data,'a'*64,**kwargs)


def test_unknown_and_duplicate_pools_and_catalogue_ids(sample):
    data,scenario,_=sample
    for ids in [[1,1],[999],[1.5],[True]]:
        with pytest.raises(ValueError): build_pilot([{**scenario,'candidate_ids':ids}],data,'a'*64)
    with pytest.raises(ValueError):build_pilot([scenario,scenario],data,'a'*64)
    with pytest.raises(ValueError):build_pilot([scenario],pd.concat([data,data.iloc[:1]]),'a'*64)
    with pytest.raises(ValueError):build_pilot([scenario],data,'bad-hash')
    data.loc[0,'position']='Goalkeeper'
    with pytest.raises(ValueError):build_pilot([scenario],data,'a'*64)


@pytest.mark.parametrize('field,value',[
    ('dataset_sha256','b'*64),('rubric_version','v2'),('pilot_version','v2'),('assessment_scope','defensive_skill'),
    ('scenario_id','unknown'),('player_id',999),('player_id',True),('assessor_id','Unregistered'),
    ('timestamp','2026-11-03'),('relevance_grade',-1),('relevance_grade',4),('relevance_grade',2.),
    ('relevance_grade',True),('relevance_grade',float('nan')),('relevance_grade',float('inf')),
    ('uncertainty','certain'),('decision_status','approved'),('evidence',''),('label_source','independent_human'),
])
def test_invalid_completed_annotations(sample,field,value):
    manifest=sample[2];rows=graded_rows(manifest);rows[0][field]=value
    with pytest.raises(ValueError):validate_pilot_annotations(rows,manifest,registry())


def test_annotation_duplicates_extra_fields_and_missing_are_errors(sample):
    manifest=sample[2];rows=graded_rows(manifest)
    assert validate_pilot_annotations(rows,manifest,registry())['graded']==16
    with pytest.raises(ValueError):validate_pilot_annotations(rows+[rows[0]],manifest,registry())
    rows[0]['similarity_score']=.99
    with pytest.raises(ValueError):validate_pilot_annotations(rows,manifest,registry())
    del rows[0]['similarity_score'];del rows[0]['notes']
    with pytest.raises(ValueError):validate_pilot_annotations(rows,manifest,registry())


@pytest.mark.parametrize('identifier',['','a','user@example.com',' space ','assessor/A'])
def test_invalid_assessor_id(identifier):
    with pytest.raises(ValueError):validate_registry({identifier:registry()['Fixture_A']})


def test_registry_identity_alias_and_review_evidence():
    records=registry();records['fixture_a']=records['Fixture_A']
    with pytest.raises(ValueError):validate_registry(records)
    records=registry();records['Fixture_A']['review_evidence']=''
    with pytest.raises(ValueError):validate_registry(records)
    records=registry();records['Fixture_A']['independence_confirmed']='yes'
    with pytest.raises(ValueError):validate_registry(records)


def test_abstain_is_missing_grade_not_zero(sample):
    manifest=sample[2];row=annotation_template(manifest)[0]
    row.update(assessor_id='Fixture_A',timestamp='2026-11-03T10:00:00Z',decision_status='abstain',
               uncertainty='high',missing_evidence='SYNTHETIC missing evidence example')
    assert validate_pilot_annotations([row],manifest,registry())['abstain']==1
    row['relevance_grade']=0
    with pytest.raises(ValueError):validate_pilot_annotations([row],manifest,registry())
    row['relevance_grade']=None;row['missing_evidence']=''
    with pytest.raises(ValueError):validate_pilot_annotations([row],manifest,registry())


def test_pending_does_not_claim_timestamp_or_uncertainty(sample):
    manifest=sample[2]
    for field,value in [('relevance_grade',0),('timestamp','2026-11-03T00:00:00Z'),('uncertainty','high')]:
        rows=annotation_template(manifest);rows[0][field]=value
        with pytest.raises(ValueError):validate_pilot_annotations(rows,manifest,{})


def test_agreement_requires_independent_compatible_label_sets(sample):
    manifest=sample[2];scenario=sample[1]['scenario_id']
    empty=agreement_report(annotation_template(manifest),manifest,{},scenario_id=scenario)
    assert empty['status']=='BLOCKED' and empty['pairs']==[]
    rows=graded_rows(manifest)
    assert agreement_report(rows,manifest,registry(),scenario_id=scenario)['status']=='BLOCKED'
    one=registry();one['Fixture_B']['independence_confirmed']=False
    assert agreement_report(rows,manifest,one,scenario_id=scenario,label_source='SYNTHETIC')['status']=='BLOCKED'
    short=[r for r in rows if r['player_id']==rows[0]['player_id']]
    result=agreement_report(short,manifest,registry(),scenario_id=scenario,label_source='SYNTHETIC')
    assert result['pairs'][0]['paired_items']==1
    assert result['pairs'][0]['exact_agreement'] is None


def test_synthetic_weighted_kappa_against_sklearn(sample):
    manifest=sample[2];rows=graded_rows(manifest)
    result=agreement_report(rows,manifest,registry(),scenario_id=sample[1]['scenario_id'],label_source='SYNTHETIC')
    pair=result['pairs'][0]
    x=[r['relevance_grade'] for r in rows if r['assessor_id']=='Fixture_A']
    y=[r['relevance_grade'] for r in rows if r['assessor_id']=='Fixture_B']
    assert result['interpretation']=='SYNTHETIC_ONLY'
    assert pair['linear_weighted_kappa']==pytest.approx(cohen_kappa_score(x,y,labels=[0,1,2,3],weights='linear'))
    assert pair['exact_agreement']==sum(a==b for a,b in zip(x,y))/len(x)
    assert len(pair['disagreements'])==3


def test_constant_labels_and_permutation(sample):
    manifest=sample[2];rows=graded_rows(manifest)
    for r in rows:r['relevance_grade']=2
    call=lambda records:agreement_report(records,manifest,registry(),scenario_id=sample[1]['scenario_id'],label_source='SYNTHETIC')
    assert call(rows)==call(list(reversed(rows)))
    pair=call(rows)['pairs'][0]
    assert pair['exact_agreement']==1 and pair['linear_weighted_kappa'] is None
    assert pair['reason']=='zero_expected_disagreement_constant_labels'


def test_readiness_no_false_real_metrics_from_synthetic_or_unlabeled(sample):
    _,scenario,manifest=sample
    for rows,people in [(annotation_template(manifest),{}),(graded_rows(manifest),registry())]:
        result=readiness_report([scenario],rows,manifest,people)
        assert result['actual_relevance_metrics'] is None
        assert result['actual_agreement_summary'] is None
        assert result['cases'][0]['status']=='BLOCKED_NO_REVIEWED_HUMAN_LABELS'
    bad=deepcopy(scenario);bad['methods']['cosine']['top5_ids']=[999]
    with pytest.raises(ValueError):readiness_report([bad],[],manifest,{})
    with pytest.raises(ValueError):readiness_report([scenario],[],manifest,{},k=6)
    with pytest.raises(ValueError):readiness_report([],[],manifest,{})


def test_readiness_math_gates_with_simulated_provenance_only(sample):
    # SYNTHETIC contract test of metadata gates; never persisted as human labels.
    data,scenario,_=sample
    mini={**scenario,'candidate_ids':[1,2,3,4],'methods':{'cosine':{'top5_ids':[1,2,3,4]}}}
    manifest=build_pilot([mini],data,'a'*64)
    rows=graded_rows(manifest,source='independent_human')
    people=registry(source='independent_human')
    report=readiness_report([mini],rows,manifest,people)
    assert all(r['precision_at_k_ready'] and r['recall_at_k_ready'] and r['ndcg_at_k_ready'] for r in report['cases'][0]['assessments'])
    partial=[r for r in rows if r['player_id']!=4]
    report=readiness_report([mini],partial,manifest,people)
    assert all(not r['precision_at_k_ready'] and not r['recall_at_k_ready'] and not r['ndcg_at_k_ready'] for r in report['cases'][0]['assessments'])


def test_csv_roundtrip_and_invalid_header_grade(sample,tmp_path):
    manifest=sample[2];rows=annotation_template(manifest)
    path=tmp_path/'SYNTHETIC.csv'
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=PILOT_FIELDS);writer.writeheader();writer.writerows(rows)
    assert load_pilot_annotations(path)==rows
    invalid=deepcopy(rows);invalid[0]['relevance_grade']='NaN'
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=PILOT_FIELDS);writer.writeheader();writer.writerows(invalid)
    with pytest.raises(ValueError):load_pilot_annotations(path)
    path.write_text('bad,header\n')
    with pytest.raises(ValueError):load_pilot_annotations(path)


def test_real_pilot_no_labels_and_no_engine_leak():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'reports/day12/pilot_manifest.json').read_text(encoding='utf-8'))
    rows=load_pilot_annotations(root/'reports/day12/pilot_annotation_template.csv')
    assert len(rows)==32 and all(r['relevance_grade'] is None and not r['assessor_id'] for r in rows)
    assert all(c['selected_count']==8 for c in manifest['scenarios'])
    assert validate_pilot_annotations(rows,manifest,{})['pending']==32
    packet=pd.read_csv(root/'reports/day12/pilot_evidence.csv')
    assert not {'rank','similarity_score','method','relevance_grade'} & set(packet)
    context=packet[packet.position.isin(['Defender','Goalkeeper'])]
    assert context.goals_per90.isna().all() and context.assists_per90.isna().all()
    assert json.loads((root/'reports/day12/assessor_registry.json').read_text())=={}
