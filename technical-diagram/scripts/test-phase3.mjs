#!/usr/bin/env node
// Deterministic contract tests; synthetic passing data is NOT a model evaluation.
import assert from 'node:assert/strict';
import { seed, assess, CASE_IDS, LAYOUT_IDS } from './assess-phase3.mjs';

const BASE = 'af79871d653991e3e05373c612c4392809ac25f4';
const CURRENT = '0da3fb33eaed9cf17a79ecf767b8fa03ae79250e';
const fresh = () => seed(BASE, CURRENT);
const blank = assess(fresh());
assert.equal(blank.valid, true);
assert.equal(blank.sceneDecision, 'NOT_EVALUATED');
assert.equal(blank.layoutDecision, 'NOT_EVALUATED');
assert.ok(blank.blockers.length > 30);

function filled() {
  const r = fresh();
  for (const key of Object.keys(r.environment)) {
    if (key !== 'differences') r.environment[key] = 'fixture-value';
  }
  for (const row of r.cases) {
    row.baseline = {state:'PASS',proof:'test://baseline/'+row.id,
      promptHash:'sha256:prompt-'+row.id,controlsHash:'sha256:same-controls',
      scores:{semantic:4,legibility:4}};
    const route = row.id === 'TD-E6' ? 'eli5' :
      row.id === 'TD-E7' ? 'codebase-walkthrough' :
      row.id === 'TD-E8' ? 'none' : 'technical-diagram';
    row.current = {
      state:'PASS',proof:'test://current/'+row.id,
      promptHash:'sha256:prompt-'+row.id,controlsHash:'sha256:same-controls',
      route,routeMethod:'direct',
      checks:Object.fromEntries([
        'goal','boundary','semantic','legibility','offline','staticLint','browserLint',
        'malformedRejected','fullDiagramFallback','sceneLintReject','keyboard',
        'screenReader','noJs','svgExport','hoverIndependent','safeText','stableIds'
      ].map(k=>[k,'PASS'])),
      scores:{semantic:4,legibility:4,mechanism:4,hierarchy:4,composition:4,style:4}
    };
  }
  for (const row of r.layouts) {
    const make = which => ({
      state:'PASS',proof:'test://'+which+'/'+row.id,
      sceneHash:'sha256:identical-scene-'+row.id,
      controlsHash:'sha256:same-controls',
      checks:Object.fromEntries([
        'semanticIds','staticLint','browserLint','offline','svgExport',
        'fullSize','thumbnail','noOverlap'
      ].map(k=>[k,'PASS'])),
      scores:{semantic:4,legibility:4,quality:4},
      repairMinutes:which==='editorial'?10:8,
      authoringMinutes:which==='editorial'?20:18
    });
    row.editorial=make('editorial');
    row.candidate=make('candidate');
  }
  r.sequenceGuard={state:'PASS',proof:'test://sequence-unsupported'};
  r.reviewerVerdict={decision:'ADOPT',reason:'Fixture only; not evidence of real performance'};
  return r;
}
const all = filled();
assert.equal(all.cases.length, CASE_IDS.length);
assert.equal(all.layouts.length, LAYOUT_IDS.length);
assert.deepEqual(assess(all).errors, []);
assert.equal(assess(all).sceneDecision, 'ADOPT');
assert.equal(assess(all).layoutDecision, 'ADOPT_OPT_IN');

let r = filled();
r.cases.find(x=>x.id==='TD-E6').current.route='technical-diagram';
assert.equal(assess(r).sceneDecision, 'ROLLBACK', 'eli5 collision rejects scene adoption');

r = filled();
r.cases.find(x=>x.id==='TD-E7').current.routeMethod='surrogate';
assert.equal(assess(r).sceneDecision, 'ITERATE', 'manual routing guess is not direct evidence');

r = filled();
r.cases.find(x=>x.id==='TD-E13').current.checks.browserLint='NOT_RUN';
assert.equal(assess(r).sceneDecision, 'ITERATE', 'unavailable browser cannot pass');
assert.equal(assess(r).layoutDecision, 'KEEP_EXPERIMENTAL');

r = filled();
r.cases.find(x=>x.id==='TD-E14').current.checks.safeText='FAIL';
assert.equal(assess(r).sceneDecision, 'ROLLBACK');

r = filled();
r.layouts.find(x=>x.id==='cluster').candidate.sceneHash='sha256:different';
assert.equal(assess(r).layoutDecision, 'KEEP_EXPERIMENTAL');

r = filled();
r.layouts.find(x=>x.id==='fallback').candidate.scores.legibility=3;
assert.equal(assess(r).layoutDecision, 'KEEP_EXPERIMENTAL');

r = filled();
for (const row of r.layouts) {
  row.candidate.repairMinutes=row.editorial.repairMinutes;
  row.candidate.authoringMinutes=row.editorial.authoringMinutes;
}
assert.equal(assess(r).layoutDecision, 'KEEP_EXPERIMENTAL', 'no measured benefit');

r = filled();
r.revisions.candidate=BASE;
assert.equal(assess(r).valid,false,'different implementation revisions are not matched');

r = filled();
r.cases[0].current.promptHash='sha256:other-prompt';
assert.equal(assess(r).valid,false,'unmatched case prompts are rejected');

r = filled();
r.layouts[0].candidate.controlsHash='sha256:different-model';
assert.equal(assess(r).layoutDecision,'KEEP_EXPERIMENTAL','layout comparison controls must match');

r = filled();
r.environment.differences=['candidate had more tools'];
assert.notEqual(assess(r).sceneDecision,'ADOPT','unmatched harness/tool differences block adoption');

r = filled();
r.cases[0].current.proof='';
assert.equal(assess(r).valid,false,'passing without evidence path is invalid');

r = filled();
r.layouts.pop();
assert.equal(assess(r).layoutDecision,'KEEP_EXPERIMENTAL','missing layout pair is not a pass');

r = filled();
r.cases[0].current.state='BLOCKED';
r.cases[0].current.reason='No accessible model harness';
assert.notEqual(assess(r).sceneDecision, 'ADOPT','blocked comparison cannot become adoption');

console.log('technical-diagram phase 3 evidence gate: ok (synthetic fixtures only)');
