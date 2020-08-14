El módulo contiene las funcionalidades para implementar todo lo relativo con la API de Sendinblue

### odoo.conf
- #sendinblue
- sendinblue_api_key=xxxxx

### Parámetros de configuración
- oniad_sendinblue_auto_generate_leads_sendinblue_list_id
- oniad_sendinblue_auto_generate_leads_user_id_default
- oniad_sendinblue_auto_generate_leads_tag_ids_default

Dentro del apartado de Configuración > Técnico se añade el apartado "Oniad Sendinblue" con los diferentes submenus:

- Sendinblue Atributos
- Sendinblue Contactos
- Sendinblue Enumeration
- Sendinblue Carpetas
- Sendinblue Listas

 

Existen diferentes crones definidos que interactúan con la API y generan todos los datos que corresponde:

### Cron Auto Generate Leads Sendinblue 
Frecuencia: 1 vez cada 12 horas

Descripción: 

Revisa todos los sendinblue_contact filtrando por sendinblue_list_ids definido en configuración
Respecto a los datos anteriores busca todos los que no tengan un crm_lead asociado y los crea
Crea el crm_lead como tipo 'lead' u 'opportunity' de acuerdo a si ese email tiene ya un contacto en Odoo OniAd o no. Todos los leads se le asignan a un account por defecto y se definen con los campos:
commercial_activity_type=hunter
lead_oniad_type=catchment

### Cron Sendinblue Get Attributes 
Frecuencia: 1 vez al día

Descripción: Se obtiene de la API de Sendinblue todos los atributos para únicamente tenerlos en Odoo Oniad y usarlos posteriormente y/o a futuro

### Cron Sendinblue Get Contacts 
Frecuencia: 1 vez al día

Descripción: Se obtiene de la API de Sendinblue todas los contactos para únicamente tenerlos en Odoo Oniad y usarlos posteriormente y/o a futuro

### Cron Sendinblue Get Folders 
Frecuencia: 1 vez al día

Descripción: Se obtiene de la API de Sendinblue todos los folders para únicamente tenerlos en Odoo Oniad y usarlos posteriormente y/o a futuro

### Cron Sendinblue Get Lists 
Frecuencia: 1 vez al día

Descripción: Se obtiene de la API de Sendinblue todas las listas para únicamente tenerlos en Odoo Oniad y usarlos posteriormente y/o a futuro
