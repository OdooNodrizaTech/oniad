Añade modelos específicos para Oniad

### Parámetros de configuración:
- oniad_stripe_journal_id
- oniad_credit_product_id
- oniad_service_product_id
- oniad_welcome_lead_template_id
- oniad_account_invoice_journal_id
- oniad_account_invoice_product
- oniad_payment_mode_id_with_credit_limit
- oniad_payment_term_id_default_with_credit_limit

### odoo.conf
#sqs_oniad
- sqs_oniad_accountmanager_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-accountmanager
- sqs_oniad_address_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-address
- sqs_oniad_campaign_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-campaign
- sqs_oniad_campaign_report_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-campaign-report
- sqs_oniad_country_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-country
- sqs_oniad_country_state_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-country-state
- sqs_oniad_transaction_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-transaction
- sqs_oniad_user_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-user
- sqs_oniad_usertag_url=https://sqs.eu-west-1.amazonaws.com/534422648921/oniad-odoo_dev-command-oniad-usertag

Existen URls públicas para usuarios logeados en Odoo:

http://deverp.oniad.com/oniad_address/7
http://deverp.oniad.com/oniad_user/1

Que re-direccionarán al res.partner que corresponda.


## Crones

### Account Invoice Generate (OniAd Transaction) 
Frecuencia: 1 vez al mes

Día: 01/xx/xxxx

Descripción: 

Revisa todas las transacciones con fecha <= ultimo día del mes anterior
Respecto a los resultados anteriores, agrupa los pagos con contacto y genera una factura por contacto con tantas líneas como pagos.
Para cada línea calculará el importe SIN iva siempre que el contacto esté definido a impuestos

### SQS Oniad Accountmanager 
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-accountmanager | Prod
oniad-odoo_dev-command-oniad-accountmanager | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.accountmanager

### SQS Oniad Address 
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-address | Prod
oniad-odoo_dev-command-oniad-address | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.address

### SQS Oniad Campaign 
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-campaign | Prod
oniad-odoo_dev-command-oniad-campaign | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.campaign

### SQS Oniad Campaign Report 
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-campaign-report | Prod
oniad-odoo_dev-command-oniad-campaign-report | Dev

y realiza las operaciones de actualización respecto a los elementos del modelo: oniad.campaign

### SQS Oniad Country
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-country | Prod
oniad-odoo_dev-command-oniad-country | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.country

### SQS Oniad Country State
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-country-state | Prod
oniad-odoo_dev-command-oniad-country-state | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.country.state

### SQS Oniad Transaction 
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-transaction | Prod
oniad-odoo_dev-command-oniad-transaction | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.transaction

### SQS Oniad User
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-user | Prod
oniad-odoo_dev-command-oniad-user | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.user

### SQS Oniad Usertag 
Frecuencia: 1 vez cada 5 minutos

Descripción: 

Consulta los SQS
nombre | entorno
--- | ---
oniad-odoo-command-oniad-usertag | Prod
oniad-odoo_dev-command-oniad-usertag | Dev

y realiza las operaciones de creación/actualización respecto a los elementos del modelo: oniad.user

### Oniad User Auto Generate Welcome Lead id
Frecuencia: 1 vez cada hora

Descripción:
Respecto a todos los oniad_user que tengan partner_id creado y estos tengan user_id (comercial) asignado y de tipo user o agency se creará el lead de bienvenida (ya sea respecto a teléfono o email)
