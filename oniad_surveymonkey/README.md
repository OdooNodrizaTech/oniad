El módulo contiene el desarrollo con la API de surveymonkey para obtener sus datos.

### odoo.conf
```
#surveymonkey
surveymonkey_api_access_token=xxxx
```

### Parámetros de sistema
```
oniad_surveymonkey_api_version
oniad_surveymonkey_datawarehouse_survey_ids_need_check
survey_oniad_datawarehouse_rds_endpoint
survey_oniad_datawarehouse_rds_user
survey_oniad_datawarehouse_rds_password
survey_oniad_datawarehouse_rds_database
``` 

Existen diferentes crons que realizan diferentes acciones respecto a SurveyMonkey:

### Cron Oniad Surveymonkey Survey Responses 
Frecuencia: cada 3 horas

Descripción: 

Revisa todas las respuestas de las survey_id definidas en configuración y de todas las que el estado es 'completado' realiza la acción de guardar esa respuesta.
Adicionalmente y si procede guardar las variables personalizadas para esa respuesta.
Adicionalmente y si procede guarda las páginas que tiene esa encuesta, las preguntas y las posibles respuestas a esas preguntas

Todo esto lo realiza contra la API de Surveymonkey y se hace unicamente para tener en Odoo OniAd todos esos datos para usarlos posteriormente

### Surveymonkey Survey Response Items Send Datawarehouse 
Frecuencia: 1 vez al día

Descripción: Revisa todos los resultados de las encuestas de Surveymonkey (previamente guardadas en Odoo) de unas encuestas en concreto que NO se hayan enviado previamente a DataWarehouse (RDS) y que NO sean resultados de prueba
