import os,sys,time,datetime,subprocess,json,signal
from pathlib import Path
B=Path(os.environ.get('REPRO_ROOT',Path(__file__).resolve().parent))
repo,label,*flags=sys.argv[1:]
env=dict(os.environ,CLANG_MODULE_CACHE_PATH=str(B/'module-cache'),SWIFTPM_MODULECACHE_OVERRIDE=str(B/'module-cache'))
cmd=['swift','test','--disable-sandbox','--package-path',str(B/repo),'--cache-path',str(B/'cache'),'--filter','ResearchRepro','--jobs','4','-v',*flags]
start=time.time();meta={'command':cmd,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'production_revision':subprocess.check_output(['git','-C',str(B/repo),'rev-parse','HEAD'],text=True).strip()}
with (B/'logs'/f'{label}.log').open('w') as log:
 p=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
 try:code=p.wait(timeout=300);meta['timed_out']=False
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGTERM);code=p.wait();meta['timed_out']=True
meta.update(exit_code=code,elapsed_seconds=round(time.time()-start,3),ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(B/'logs'/f'{label}.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta));sys.exit(0)
