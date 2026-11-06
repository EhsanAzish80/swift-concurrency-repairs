"""Install only the research test target/fixtures in disposable, pinned checkouts."""
import argparse,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--case',choices=['nio','nuke','kingfisher'],required=True);args=ap.parse_args()
root=Path(args.root).resolve();repo=root/args.case;fixtures=Path(__file__).resolve().parent/'fixtures'
manifest='Package@swift-5.9.swift' if args.case=='kingfisher' else 'Package.swift'
changed=subprocess.check_output(['git','-C',str(repo),'diff','--name-only'],text=True).splitlines()
if any(x!=manifest for x in changed):raise SystemExit('Unrelated tracked changes present; use a disposable clean checkout.')
original=subprocess.check_output(['git','-C',str(repo),'show','HEAD:'+manifest],text=True)
folder=repo/'ResearchRepro';folder.mkdir(exist_ok=True);(folder/'ResearchRepro.swift').write_text((fixtures/(args.case+'.swift')).read_text())
if args.case=='nio':
 addition='\npackage.targets.removeAll { $0.type == .test }\npackage.targets.append(.testTarget(name: "ResearchRepro", dependencies: ["NIOCore", .product(name: "DequeModule", package: "swift-collections")], path: "ResearchRepro"))\n'
else:
 module='Nuke' if args.case=='nuke' else 'Kingfisher'
 addition='\npackage.targets.append(.testTarget(name: "ResearchRepro", dependencies: ["'+module+'"], path: "ResearchRepro"))\n'
(repo/manifest).write_text(original+addition)
print('Installed test-only target; production source files were not modified.')
