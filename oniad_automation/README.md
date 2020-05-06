El módulo contiene el desarrollo que permite diferentes tareas automáticas respecto a leads

## Parámetros de configuración
```
oniad_automation_welcome_lead_mail_template_id
``` 

## Crones

### Automation Welcome Leads 

Frecuencia: 1 vez cada hora

Limitaciones: Solo se envía de Lunes-Viernes en horario de 08:00 - 18:00

Descripción: Revisa todos los leads de tipo oportunidad, activos, ni ganados ni perdidos, que tienen usuario asignado, commercial_activity_type=account, lead_oniad_type=welcome, phone=False, mobile=False y que NO tienen ninguna actividad realizada. Se envía un email y se cambia la siguiente actividad y la fecha de la misma (+7 dias).
