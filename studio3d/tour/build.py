# Gera tour.build.js: plantas (plans/*.js, com apto.json embutido) + motor (tour.js)
import json, os
D = os.path.dirname(os.path.abspath(__file__))
rd = lambda p: open(os.path.join(D, p), encoding='utf-8').read()
apto = json.load(open(os.path.join(D, 'plans/apto.json'), encoding='utf-8'))
parts = [rd('plans/casa.js'), rd('plans/apto.js').replace('__APTO__', json.dumps(apto, ensure_ascii=False, separators=(',', ':'))), rd('tour.js')]
js = '\n'.join(parts)
assert '&&' not in js, 'operador proibido no WordPress'
open(os.path.join(D, 'tour.build.js'), 'w', encoding='utf-8').write(js)
print('tour.build.js', len(js))
