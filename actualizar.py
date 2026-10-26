import json, urllib.request, html, os
from datetime import datetime
from zoneinfo import ZoneInfo

URL=('https://api.open-meteo.com/v1/forecast?latitude=36.86164&longitude=-4.03365'
 '&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m'
 '&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum'
 '&timezone=Europe%2FMadrid&forecast_days=5')
MAP={0:('Despejado','☀'),1:('Mayormente despejado','🌤'),2:('Parcialmente nuboso','⛅'),3:('Nublado','☁'),45:('Niebla','☁'),48:('Niebla','☁'),51:('Llovizna','🌦'),53:('Llovizna','🌦'),55:('Llovizna','🌧'),61:('Lluvia','🌧'),63:('Lluvia','🌧'),65:('Lluvia intensa','🌧'),71:('Nieve','❄'),73:('Nieve','❄'),75:('Nieve','❄'),80:('Chubascos','🌦'),81:('Chubascos','🌧'),82:('Chubascos fuertes','🌧'),95:('Tormenta','⛈'),96:('Tormenta','⛈'),99:('Tormenta','⛈')}
DAYS=['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']
def fmt(value,suffix=''):
 if value is None:return '—'
 return str(round(value))+suffix
def main():
 try:
  req=urllib.request.Request(URL,headers={'User-Agent':'EstacionSedella/1.0'})
  with urllib.request.urlopen(req,timeout=25) as r: data=json.load(r)
 except Exception as e:
  if os.path.exists('index.html'):
   print('No se pudo actualizar, conservando datos anteriores: '+str(e));return
  raise
 c=data['current'];d=data['daily']; condition,icon=MAP.get(c.get('weather_code'),('Variable','⛅'))
 now=datetime.now(ZoneInfo('Europe/Madrid'))
 cards=''
 for i,day in enumerate(d['time']):
  weekday=DAYS[datetime.strptime(day,'%Y-%m-%d').weekday()]
  label='Hoy' if i==0 else weekday
  caption,emoji=MAP.get(d['weather_code'][i],('Variable','⛅'))
  cards+=('<div class="day"><div class="dayname">'+label+'</div><div class="symbol">'+emoji+'</div>'
    +'<div class="daytemps">'+fmt(d['temperature_2m_max'][i],'°')+' / '+fmt(d['temperature_2m_min'][i],'°')+'</div>'
    +'<div class="small">Lluvia '+fmt(d['precipitation_probability_max'][i],'%')+'</div></div>')
 page='''<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><meta http-equiv="refresh" content="3600"><title>Estación Sedella</title><style>
*{box-sizing:border-box}body{margin:0;background:#0f1d30;color:#fff;font-family:Arial,Helvetica,sans-serif} .wrap{padding:16px;max-width:1100px;margin:0 auto}.top{overflow:hidden;border-bottom:1px solid #45536a;padding-bottom:8px}.place{float:left;font-size:26px;font-weight:bold}.updated{float:right;color:#b4c6dd;font-size:12px;margin-top:9px}.main{overflow:hidden;padding:16px 0}.left{float:left;width:49%}.right{float:right;width:49%}.clock{font-size:76px;letter-spacing:1px;font-weight:bold;line-height:1}.date{font-size:18px;color:#bfd2e7;padding-top:10px}.current{font-size:52px;font-weight:bold}.current span{font-size:35px}.condition{color:#bfd2e7;font-size:16px}.facts{clear:both;overflow:hidden;margin-top:20px}.fact{width:24%;float:left;background:#253a53;margin-right:1%;border-radius:8px;padding:13px 6px;text-align:center}.fact:last-child{margin-right:0}.fact strong{display:block;font-size:24px}.fact small{color:#b4c6dc;font-size:12px}.forecast{clear:both;margin-top:18px;overflow:hidden}.day{float:left;width:19.2%;margin-right:1%;background:#253a53;border-radius:8px;text-align:center;padding:11px 1px;min-height:125px}.day:last-child{margin-right:0}.dayname{font-weight:bold}.symbol{font-size:24px;margin:7px 0}.daytemps{font-weight:bold}.small{font-size:11px;color:#b9d0e8;margin-top:7px}.footer{padding-top:14px;color:#bbcada;font-size:12px;text-align:center}.footer a{color:#bfe0ff}@media(max-width:650px){.clock{font-size:56px}.current{font-size:42px}.place{font-size:21px}.updated{font-size:10px}.fact strong{font-size:18px}.fact small{font-size:10px}.day{min-height:118px}}
</style></head><body><div class="wrap"><div class="top"><div class="place">SEDELLA · MÁLAGA</div><div class="updated">Datos: __UPDATED__</div></div><div class="main"><div class="left"><div class="clock" id="clock">--:--</div><div class="date" id="date"></div></div><div class="right"><div class="current"><span>__ICON__</span> __TEMP__</div><div class="condition">__CONDITION__</div></div></div><div class="facts"><div class="fact"><strong>__FEELS__</strong><small>Sensación</small></div><div class="fact"><strong>__HUM__</strong><small>Humedad</small></div><div class="fact"><strong>__RAIN__</strong><small>Precipitación actual</small></div><div class="fact"><strong>__WIND__</strong><small>Viento km/h</small></div></div><div class="forecast">__CARDS__</div><div class="footer">Fuente: Open-Meteo · Actualiza datos en el servidor cada 2 h · <a href="https://www.aemet.es/es/eltiempo/prediccion/municipios/sedella-id29087">Consultar AEMET</a> · <a href="javascript:location.reload()">Recargar</a></div></div><script type="text/javascript">function pad(n){return (n<10?'0':'')+n;}function clock(){var d=new Date();document.getElementById('clock').innerHTML=pad(d.getHours())+':'+pad(d.getMinutes());var names=['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];var months=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];document.getElementById('date').innerHTML=names[d.getDay()]+', '+d.getDate()+' de '+months[d.getMonth()];}clock();setInterval(clock,15000);</script></body></html>'''
 replacements={'__UPDATED__':now.strftime('%d/%m/%Y %H:%M'),'__ICON__':icon,'__TEMP__':fmt(c.get('temperature_2m'),' °C'),'__CONDITION__':condition,'__FEELS__':fmt(c.get('apparent_temperature'),'°'),'__HUM__':fmt(c.get('relative_humidity_2m'),'%'),'__RAIN__':fmt(c.get('precipitation'),' mm'),'__WIND__':fmt(c.get('wind_speed_10m')),'__CARDS__':cards}
 for k,v in replacements.items():page=page.replace(k,html.escape(v) if k!='__CARDS__' else v)
 with open('index.html','w',encoding='utf-8') as f:f.write(page)
 print('Actualizado '+now.isoformat())
if __name__=='__main__':main()
