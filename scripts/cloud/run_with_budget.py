"""Run one Linux cloud operation, retaining its log and explicit resource outcome."""
import argparse,json,os,signal,subprocess,sys,time
from pathlib import Path

def memory_limit():
    limits=[]
    for name in ['/sys/fs/cgroup/memory.max','/sys/fs/cgroup/memory/memory.limit_in_bytes']:
        p=Path(name)
        if p.exists() and p.read_text().strip().isdigit():
            n=int(p.read_text().strip())
            if n<2**60:limits.append(n)
    for line in Path('/proc/meminfo').read_text().splitlines():
        if line.startswith('MemTotal:'):limits.append(int(line.split()[1])*1024)
    return min(limits)

def process_group_rss(group_id):
    total=0
    for directory in Path('/proc').iterdir():
        if not directory.name.isdigit():continue
        try:
            pid=int(directory.name)
            if os.getpgid(pid)!=group_id:continue
            for line in (directory/'status').read_text().splitlines():
                if line.startswith('VmRSS:'):total+=int(line.split()[1])*1024
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
    return total

def process_group_has_live_members(group_id):
    for directory in Path('/proc').iterdir():
        if not directory.name.isdigit():continue
        try:
            if os.getpgid(int(directory.name))!=group_id:continue
            for line in (directory/'status').read_text().splitlines():
                if line.startswith('State:') and line.split()[1]!='Z':return True
        except (FileNotFoundError,ProcessLookupError,PermissionError):continue
    return False

def stop_process_group(child):
    """Stop descendants even when the direct parent exits before them."""
    try:os.killpg(child.pid,signal.SIGTERM)
    except ProcessLookupError:return
    deadline=time.monotonic()+10
    while process_group_has_live_members(child.pid) and time.monotonic()<deadline:
        child.poll()
        time.sleep(.1)
    if process_group_has_live_members(child.pid):
        try:os.killpg(child.pid,signal.SIGKILL)
        except ProcessLookupError:pass
    child.wait()

def run():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=int,default=900)
    parser.add_argument('--memory-mib',type=int)
    parser.add_argument('--log',required=True)
    parser.add_argument('command',nargs=argparse.REMAINDER)
    args=parser.parse_args()
    if sys.platform!='linux':parser.error('Cloud-only: native routing is stopped on the Mac.')
    command=args.command[1:] if args.command[:1]==['--'] else args.command
    if not command:parser.error('Provide the actual build or routing command after --.')
    if args.seconds<=0 or args.memory_mib is not None and args.memory_mib<=0:parser.error('Resource budgets must be positive.')
    log_path=Path(args.log);log_path.parent.mkdir(parents=True,exist_ok=True)
    reserve_limit=int(memory_limit()*.65)
    limit=min(reserve_limit,args.memory_mib*1024**2) if args.memory_mib else reserve_limit
    lock=Path('.cloud-routing.lock')
    try:lock_fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    except FileExistsError:parser.error('Another cloud operation owns .cloud-routing.lock; inspect its PID before removing a stale lock.')
    os.write(lock_fd,str(os.getpid()).encode());os.close(lock_fd)
    started=time.monotonic();peak=0;termination=None;child=None
    try:
        with log_path.open('w') as output:
            child=subprocess.Popen(command,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
            while child.poll() is None:
                peak=max(peak,process_group_rss(child.pid))
                if peak>limit:termination='MEMORY_BUDGET_REACHED'
                elif time.monotonic()-started>args.seconds:termination='TIME_BUDGET_REACHED'
                if termination:
                    stop_process_group(child)
                    break
                time.sleep(.5)
        outcome={'command':command,'exit_code':child.returncode,'termination':termination,'elapsed_seconds':round(time.monotonic()-started,2),'peak_process_group_rss_bytes':peak,'memory_budget_bytes':limit,'completed_command':termination is None,'passing_validation_inferred':False}
        log_path.with_suffix(log_path.suffix+'.outcome.json').write_text(json.dumps(outcome,indent=2)+'\n')
        print(json.dumps(outcome))
        return 124 if termination else child.returncode
    finally:
        if child and (child.poll() is None or process_group_has_live_members(child.pid)):
            stop_process_group(child)
        lock.unlink(missing_ok=True)

if __name__=='__main__':sys.exit(run())
