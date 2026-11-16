import os, sqlite3, secrets, hmac, hashlib, json, base64
from flask import Flask, request, session, jsonify, send_from_directory
app=Flask(__name__); app.secret_key=os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config.update(MAX_CONTENT_LENGTH=35*1024*1024,SESSION_COOKIE_HTTPONLY=True,SESSION_COOKIE_SAMESITE='Lax',SESSION_COOKIE_SECURE=os.environ.get('HTTPS')=='1')
def db():
 c=sqlite3.connect(os.environ.get('DB_PATH','gelaender.db')); c.execute('CREATE TABLE IF NOT EXISTS models (id TEXT PRIMARY KEY, data TEXT NOT NULL)'); return c
@app.get('/')
def home(): return send_from_directory('static','index.html')
@app.post('/api/login')
def login():
 d=request.get_json(); role=d.get('role'); pw=os.environ.get('ADMIN_PASSWORD' if role=='admin' else 'TEAM_PASSWORD','');
 if role not in ('admin','team') or not pw or not hmac.compare_digest(str(d.get('password','')),pw): return jsonify(error='Anmeldung fehlgeschlagen'),401
 session.clear(); session['role']=role; return jsonify(role=role)
@app.post('/api/logout')
def logout(): session.clear(); return jsonify(ok=True)
@app.get('/api/session')
def status(): return jsonify(role=session.get('role',''))
@app.route('/api/models',methods=['GET','POST'])
def models():
 if not session.get('role'): return jsonify(error='Anmeldung erforderlich'),401
 with db() as c:
  if request.method=='GET': return jsonify([json.loads(x[0]) for x in c.execute('SELECT data FROM models')])
  if session['role']!='admin': return jsonify(error='Keine Berechtigung'),403
  d=request.get_json(); name=str(d.get('name','')).strip(); number=str(d.get('number','')).strip()
  try: weight=float(d['weight']); assert 0<=weight<100000
  except (ValueError,KeyError,TypeError,AssertionError): return jsonify(error='Ungültiges Gewicht'),400
  if not name or not number: return jsonify(error='Name und Nummer erforderlich'),400
  for p in d.get('photos',[]):
   if not isinstance(p,str) or not p.startswith('data:image/jpeg;base64,'): return jsonify(error='Ungültiges Foto'),400
  if any(json.loads(r[0]).get('number','').casefold()==number.casefold() and r[1]!=d.get('id') for r in c.execute('SELECT data,id FROM models')): return jsonify(error='Musternummer bereits vorhanden'),409
  d['id']=d.get('id') or secrets.token_hex(12); d['weight']=weight; c.execute('INSERT OR REPLACE INTO models VALUES (?,?)',(d['id'],json.dumps(d))); return jsonify(d)
@app.delete('/api/models/<id>')
def delete(id):
 if session.get('role')!='admin': return jsonify(error='Keine Berechtigung'),403
 with db() as c: c.execute('DELETE FROM models WHERE id=?',(id,))
 return jsonify(ok=True)
if __name__=='__main__':
 if not os.environ.get('ADMIN_PASSWORD') or not os.environ.get('TEAM_PASSWORD'): raise SystemExit('ADMIN_PASSWORD und TEAM_PASSWORD setzen (siehe README).')
 app.run(host='0.0.0.0',port=8000,debug=False)
