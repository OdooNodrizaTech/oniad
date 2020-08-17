El módulo contiene el desarrollo para todo lo relacionado con facturas
 

## odoo.conf
- #docs_oniad_com
- s3_bucket_docs_oniad_com=docs-oniad-com

## crm.lead
Si existe el valor oniad_user_id > 0 mostrará el link https://platform.oniad.com/backend/admin/supadmin/card/{onioad_user_id} correspondiente

Si el valor is_survey=True mostrará el link: https://es.surveymonkey.com/r/7T2H5N5?partner_id={partner_id}&lead_id={lead_Id}&oniad_user_id={oniad_user_id}
 

## res.partner
Si existe el valor oniad_user_id > 0 mostrará el link https://platform.oniad.com/backend/admin/supadmin/card/{onioad_user_id} correspondiente

## Crones

### Account Invoice Uuid Generate 

Frecuencia: Nunca

Descripción: Genera el uuid de las facturas que no lo tienen definido
