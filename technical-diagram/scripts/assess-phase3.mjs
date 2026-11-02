#!/usr/bin/env node
// Phase 3 evaluation receipt gate. No model calls; incomplete evidence never passes.
// --assess validates the record; --strict additionally requires an adoption verdict.
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
const CASE_IDS = Array.from({length:18},(_,i)=>'TD-E'+(i+1));
const LAYOUT_IDS = ['linear','fallback','branchy-loop','cluster','linear-edit'];

function seed(base,current) {
  const blank=()=>({state:'NOT_RUN',reason:'Matched run has not been performed'});
  return {schemaVersion:1,
    description:'Unexecuted receipt scaffold; NOT a passing evaluation',
    revisions:{baseline:base,current,candidate:current,suite:current,evaluator:current},
    environment:{model:'NOT_RUN',harness:'NOT_RUN',harnessVersion:'NOT_RUN',
      toolAccess:'NOT_RUN',permissions:'NOT_RUN',artifactSupport:'NOT_RUN',
      browserDriver:'NOT_RUN',promptSetHash:'NOT_RUN',platform:'NOT_RUN',differences:[]},
    cases:CASE_IDS.map(id=>({id,baseline:blank(),current:blank()})),
    layouts:LAYOUT_IDS.map(id=>({id,editorial:blank(),candidate:blank()})),
    sequenceGuard:blank(),
    reviewerVerdict:{decision:'NOT_RUN',reason:'Requires human review of matched artifacts'}};
}
function assess(report) {
  const errors=[],blockers=[],regressions=[],layoutFailures=[];
  const add=(arr,msg)=>arr.push(msg);
  const sha=s=>typeof s==='string'&&/^[0-9a-f]{40}$/.test(s);
  const text=s=>typeof s==='string'&&s.trim().length>0;
  const score=s=>Number.isInteger(s)&&s>=1&&s<=5;
  if(!report||report.schemaVersion!==1)return {valid:false,sceneDecision:'NOT_EVALUATED',
    layoutDecision:'NOT_EVALUATED',errors:['Unsupported receipt schema'],blockers,regressions};
  for(const k of ['baseline','current','candidate','suite','evaluator'])
    if(!sha(report.revisions?.[k]))add(errors,'Missing 40-character revision: '+k);
  if(report.revisions?.candidate!==report.revisions?.current)
    add(errors,'ELK must compare the same candidate commit as editorial');
  if(report.revisions?.baseline===report.revisions?.current)
    add(errors,'Baseline and current revisions must differ');
  for(const k of ['model','harness','harnessVersion','toolAccess','permissions',
    'artifactSupport','browserDriver','promptSetHash','platform'])
    if(!text(report.environment?.[k])||report.environment[k]==='NOT_RUN')
      add(blockers,'Environment not recorded: '+k);
  if(!Array.isArray(report.environment?.differences)||report.environment.differences.some(d=>!text(d)))
    add(errors,'environment.differences must be an array of explanations');
  const statuses=['PASS','FAIL','NOT_RUN','BLOCKED'];
  function state(v,name) {
    if(!v||!statuses.includes(v.state)){add(errors,name+': invalid state');return false;}
    if(['PASS','FAIL'].includes(v.state)&&!text(v.proof))
      add(errors,name+': executed state must provide artifact/trace proof');
    if(['NOT_RUN','BLOCKED'].includes(v.state)&&!text(v.reason))
      add(blockers,name+': provide reason for unexecuted state');
    return true;
  }
  const byId=(arr,ids,kind)=>{
    const map=new Map();
    if(!Array.isArray(arr)){add(errors,kind+' must be array');return map;}
    for(const row of arr){
      if(!ids.includes(row?.id)||map.has(row?.id))
        add(errors,kind+': unexpected or duplicate ID '+String(row?.id));
      else map.set(row.id,row);
    }
    return map;
  };
  let executed=0,completedLayouts=0,improvement=false;
  const caseMap=byId(report.cases,CASE_IDS,'cases');
  for(const id of CASE_IDS){
    const row=caseMap.get(id);
    if(!row){add(blockers,id+': missing matched case');continue;}
    for(const condition of ['baseline','current']){
      const v=row[condition],ref=id+'/'+condition;
      if(!state(v,ref))continue;
      if(['NOT_RUN','BLOCKED'].includes(v.state)){add(blockers,ref+': '+v.reason);continue;}
      if(condition==='baseline')continue;
      executed++;
      if(v.state==='FAIL'){add(regressions,ref+': failed');continue;}
      const route=id==='TD-E6'?'eli5':id==='TD-E7'?'codebase-walkthrough':
        id==='TD-E8'?'none':'technical-diagram';
      if(v.route!==route)add(regressions,ref+': expected route '+route+', got '+String(v.route));
      if(v.routeMethod!=='direct')add(blockers,ref+': routing was not directly observed');
      const req=id==='TD-E8'?['goal']:id==='TD-E6'||id==='TD-E7'?
        ['goal','boundary']:id==='TD-E16'?
        ['malformedRejected','fullDiagramFallback','sceneLintReject']:
        ['goal','semantic','legibility','offline','staticLint','browserLint'];
      if(id==='TD-E13')req.push('keyboard','screenReader','noJs','svgExport','hoverIndependent');
      if(id==='TD-E14')req.push('keyboard','safeText','stableIds');
      if(id==='TD-E17')req.push('keyboard','screenReader','hoverIndependent');
      if(id==='TD-E18')req.push('noJs','svgExport');
      for(const check of req){
        const s=v.checks?.[check];
        if(s==='FAIL')add(regressions,ref+': '+check+' failed');
        else if(s!=='PASS')add(blockers,ref+': '+check+' not verified');
      }
      const visual=!['TD-E6','TD-E7','TD-E8','TD-E16'].includes(id);
      if(visual)for(const field of ['semantic','legibility']){
        const val=v.scores?.[field],prior=row.baseline?.scores?.[field];
        if(!score(val))add(blockers,ref+': missing human score '+field);
        else if(val<3)add(regressions,ref+': '+field+' below 3');
        if(score(prior)&&score(val)&&val<prior)add(regressions,ref+': '+field+' regressed from baseline');
      }
      if(['TD-E1','TD-E2','TD-E3','TD-E4','TD-E5','TD-E9','TD-E10','TD-E11','TD-E12'].includes(id)){
        const grades=['mechanism','hierarchy','composition','style'].map(k=>v.scores?.[k]);
        if(!grades.every(score))add(blockers,ref+': visual rubric incomplete');
        else if(['TD-E1','TD-E2','TD-E5'].includes(id)){
          grades.sort((a,b)=>a-b);
          if((grades[1]+grades[2])/2<4)add(regressions,ref+': visual median below 4');
        }
      }
    }
  }
  const layoutMap=byId(report.layouts,LAYOUT_IDS,'layouts');
  for(const id of LAYOUT_IDS){
    const row=layoutMap.get(id);
    if(!row){add(blockers,'layout/'+id+': missing matched scene');continue;}
    for(const k of ['editorial','candidate']){
      const v=row[k],ref='layout/'+id+'/'+k;
      if(!state(v,ref))continue;
      if(v.state==='FAIL'){add(layoutFailures,ref+': failed');continue;}
      if(v.state!=='PASS'){add(blockers,ref+': '+v.reason);continue;}
      if(!text(v.sceneHash))add(blockers,ref+': semantic scene digest missing');
      for(const check of ['semanticIds','staticLint','browserLint','offline','svgExport','fullSize','thumbnail','noOverlap']){
        if(v.checks?.[check]==='FAIL')add(layoutFailures,ref+': '+check+' failed');
        else if(v.checks?.[check]!=='PASS')add(blockers,ref+': '+check+' not verified');
      }
      for(const metric of ['semantic','legibility','quality']){
        if(!score(v.scores?.[metric]))add(blockers,ref+': '+metric+' human grade missing');
        else if(v.scores[metric]<3)add(layoutFailures,ref+': '+metric+' below 3');
      }
      for(const metric of ['repairMinutes','authoringMinutes']){
        if(!Number.isFinite(v[metric])||v[metric]<0)
          add(blockers,ref+': '+metric+' not measured');
      }
    }
    if(row.editorial?.state==='PASS'&&row.candidate?.state==='PASS'){
      completedLayouts++;
      if(row.editorial.sceneHash!==row.candidate.sceneHash)
        add(layoutFailures,'layout/'+id+': matched semantic scenes differ');
      for(const metric of ['semantic','legibility','quality']){
        const a=row.editorial.scores?.[metric],b=row.candidate.scores?.[metric];
        if(score(a)&&score(b)&&b<a)
          add(layoutFailures,'layout/'+id+': '+metric+' fell below editorial');
      }
      for(const metric of ['repairMinutes','authoringMinutes']){
        if(Number.isFinite(row.editorial[metric])&&Number.isFinite(row.candidate[metric])&&
          row.candidate[metric]<row.editorial[metric])improvement=true;
      }
    }
  }
  if(state(report.sequenceGuard,'sequenceGuard')&&report.sequenceGuard.state!=='PASS')
    add(blockers,'Fixed-rail sequence rejection not verified');
  if(report.reviewerVerdict?.decision!=='ADOPT'||!text(report.reviewerVerdict.reason))
    add(blockers,'Human adoption verdict missing');
  const valid=errors.length===0;
  const sceneBlocks=blockers.filter(x=>!x.startsWith('layout/')&&!x.startsWith('Fixed-rail'));
  const sceneDecision=!executed?'NOT_EVALUATED':regressions.length?'ROLLBACK':
    !valid||sceneBlocks.length?'ITERATE':'ADOPT';
  const layoutDecision=!completedLayouts&&!layoutFailures.length?'NOT_EVALUATED':
    layoutFailures.length?'KEEP_EXPERIMENTAL':
    !valid||blockers.length||regressions.length||
    completedLayouts!==LAYOUT_IDS.length||!improvement?'KEEP_EXPERIMENTAL':'ADOPT_OPT_IN';
  return {valid,sceneDecision,layoutDecision,executedCases:executed,completedLayouts,
    measuredImprovement:improvement,errors,blockers,regressions,layoutFailures};
}

export { seed, assess, CASE_IDS, LAYOUT_IDS };
if (process.argv[1] && resolve(process.argv[1]) === resolve(new URL(import.meta.url).pathname)) {
  const [action,path] = process.argv.slice(2);
  if (action === '--init' && path) {
    const report = seed('af79871d653991e3e05373c612c4392809ac25f4',
      '0da3fb33eaed9cf17a79ecf767b8fa03ae79250e');
    await writeFile(resolve(path), JSON.stringify(report,null,2)+'\n', {flag:'wx'});
    console.log('Created unexecuted receipt template: '+path);
  } else if ((action === '--assess'||action === '--strict') && path) {
    const report = JSON.parse(await readFile(resolve(path),'utf8'));
    const result = assess(report);
    console.log(JSON.stringify(result,null,2));
    if (!result.valid || (action === '--strict' &&
      (result.sceneDecision !== 'ADOPT'||result.layoutDecision !== 'ADOPT_OPT_IN'))) process.exitCode=1;
  } else {
    console.error('Usage: assess-phase3.mjs --init <new.json> | --assess <receipt.json> | --strict <receipt.json>');
    process.exitCode=2;
  }
}
