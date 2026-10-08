"""Read exact parts from JLCPCB's official public server-rendered detail pages."""
import concurrent.futures,datetime,gzip,hashlib,json,re,urllib.request
from pathlib import Path
OUT=Path('evidence/microphone-local-bypass-2026-10-08/official-stock');OUT.mkdir(exist_ok=True)
c=json.load(open('evidence/microphone-local-bypass-2026-10-08/placement.json'));parts={}
for r in c:
 if r['type']!='source_component':continue
 numbers=r.get('supplier_part_numbers',{}).get('jlcpcb',[])
 if len(numbers)>1:raise ValueError('Ambiguous supplier identity')
 if numbers:
  item=parts.setdefault(numbers[0],{'part_number':numbers[0],'references':[],'manufacturer_part_number':r['manufacturer_part_number']})
  if item['manufacturer_part_number']!=r['manufacturer_part_number']:raise ValueError('Inconsistent manufacturer identity')
  item['references'].append(r['name'])
def dictionaries(o):
 if isinstance(o,dict):
  yield o
  for v in o.values():yield from dictionaries(v)
 elif isinstance(o,list):
  for v in o:yield from dictionaries(v)
def check(item):
 result={**item,'url':'https://jlcpcb.com/partdetail/'+item['part_number'],'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(result['url'],timeout=30) as response:
   body=response.read();result.update(http_status=response.status,response_date=response.headers.get('Date'),response_age=response.headers.get('Age'))
  result['html_sha256']=hashlib.sha256(body).hexdigest()
  (OUT/(item['part_number']+'.html.gz')).write_bytes(gzip.compress(body,mtime=0))
  chunks=[]
  for match in re.finditer(r'self\.__next_f\.push\((\[.*?\])\)</script>',body.decode()):
   payload=json.loads(match.group(1))
   if len(payload)>1 and isinstance(payload[1],str):chunks.append(payload[1])
  flight=''.join(chunks);records=[]
  for match in re.finditer(r'(?:^|\n)[0-9a-f]+:([\[{])',flight):
   try:records.extend(dictionaries(json.JSONDecoder().raw_decode(flight[match.start(1):])[0]))
   except json.JSONDecodeError:continue
  exact=[o for o in records if o.get('componentCode')==item['part_number'] and o.get('componentModelEn')]
  stock=[o for o in exact if isinstance(o.get('overseasStockCount'),int) and isinstance(o.get('canPresaleNumber'),int)]
  if not stock:raise ValueError('Exact-part stock record missing; related-part quantities are not accepted')
  record=stock[0]
  for candidate in stock:
   if candidate['overseasStockCount']!=record['overseasStockCount']:raise ValueError('Inconsistent exact-part stock records')
  result.update(model=record['componentModelEn'],manufacturer=record['componentBrandEn'],stock_count=record['overseasStockCount'],available_to_buy=record['canPresaleNumber'],is_buy_component=record.get('isBuyComponent'),stock_record=record)
  metadata=next((o for o in exact if 'componentLibraryType' in o),{})
  result['library_type']=metadata.get('componentLibraryType');result['assembly_component_flag']=metadata.get('assemblyComponentFlag')
  result['exact_mpn_match']=record['componentModelEn']==item['manufacturer_part_number']
  result['stock_covers_one_board']=result['exact_mpn_match'] and result['available_to_buy']>=len(item['references']) and result['stock_count']>=len(item['references']) and result['is_buy_component']=='1'
 except Exception as error:result['error']=str(error);result['stock_covers_one_board']=False
 (OUT/(item['part_number']+'.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result.get(k) for k in ['part_number','model','stock_count','available_to_buy','exact_mpn_match','stock_covers_one_board','error']}),flush=True)
 return result
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--parts',nargs='*')
parser.add_argument('--workers',type=int,default=5)
args=parser.parse_args()
selected=[parts[code] for code in args.parts] if args.parts else list(parts.values())
with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:new_results=list(pool.map(check,selected))
results=[json.loads((OUT/(code+'.json')).read_text()) for code in parts if (OUT/(code+'.json')).exists()]
receipt={'source_sha256':hashlib.sha256(Path('evidence/microphone-local-bypass-2026-10-08/placement.json').read_bytes()).hexdigest(),'parts_checked':len(results),'purchased_components':sum(len(r['references']) for r in results),'covered_parts':sum(r['stock_covers_one_board'] for r in results),'results':results,'source_native':'evidence/microphone-local-bypass-2026-10-08/placement.json','scope':'Exact official JLCPCB public detail-page inventory for the actual newly generated unrouted placement; same-identity application to final routed output is a separate check; no assembler reservation, rotation or finished-order approval implied'}
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='results'}))
