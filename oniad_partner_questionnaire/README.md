El módulo contiene el desarrollo para implementar funcionalidades relacionadas especialmente con el contacto, con el objetivo de segmentarlo mucho mejor.

Se introducen los siguientes datos por defecto en la instalación:

### res.partner.agency.activity
```
<record id="res_partner_agency_activity_data_1" model="res.partner.agency.activity">
<field name="id">1</field>
<field name="name">Web / Ecommerce</field>
</record>
<record id="res_partner_agency_activity_data_2" model="res.partner.agency.activity">
<field name="id">2</field>
<field name="name">ERP / CRM</field>
</record>
<record id="res_partner_agency_activity_data_3" model="res.partner.agency.activity">
<field name="id">3</field>
<field name="name">SEM / PPC / Social Ads</field>
</record>
<record id="res_partner_agency_activity_data_4" model="res.partner.agency.activity">
<field name="id">4</field>
<field name="name">RTB / Programatic</field>
</record>
<record id="res_partner_agency_activity_data_5" model="res.partner.agency.activity">
<field name="id">5</field>
<field name="name">Afiliacion / Email</field>
</record>
<record id="res_partner_agency_activity_data_6" model="res.partner.agency.activity">
<field name="id">6</field>
<field name="name">Community Management</field>
</record>
<record id="res_partner_agency_activity_data_7" model="res.partner.agency.activity">
<field name="id">7</field>
<field name="name">Compra de medios</field>
</record>
<record id="res_partner_agency_activity_data_8" model="res.partner.agency.activity">
<field name="id">1</field>
<field name="name">Diseño gráfico</field>
</record>
<record id="res_partner_agency_activity_data_9" model="res.partner.agency.activity">
<field name="id">9</field>
<field name="name">Impresion y merchandising</field>
</record>
<record id="res_partner_agency_activity_data_10" model="res.partner.agency.activity">
<field name="id">10</field>
<field name="name">Branding</field>
</record>
<record id="res_partner_agency_activity_data_11" model="res.partner.agency.activity">
<field name="id">11</field>
<field name="name">Audiovisual</field>
</record>
<record id="res_partner_agency_activity_data_12" model="res.partner.agency.activity">
<field name="id">12</field>
<field name="name">Gabinete de prensa</field>
</record>
<record id="res_partner_agency_activity_data_13" model="res.partner.agency.activity">
<field name="id">13</field>
<field name="name">Eventos</field>
</record>
```

### res.partner.agency.type
```
<record id="res_partner_agency_type_data_1" model="res.partner.agency.type">
<field name="id">1</field>
<field name="name">Consultor</field>
</record>
<record id="res_partner_agency_type_data_2" model="res.partner.agency.type">
<field name="id">2</field>
<field name="name">Micro-agencia</field>
</record>
<record id="res_partner_agency_type_data_3" model="res.partner.agency.type">
<field name="id">3</field>
<field name="name">Agencia</field>
</record>
```

### res.partner.asociation.geo
```
<record id="res_partner_asociation_geo_data_1" model="res.partner.asociation.geo">
<field name="id">1</field>
<field name="name">Local / regional</field>
</record>
<record id="res_partner_asociation_geo_data_2" model="res.partner.asociation.geo">
<field name="id">2</field>
<field name="name">Nacional</field>
</record>
<record id="res_partner_asociation_geo_data_3" model="res.partner.asociation.geo">
<field name="id">3</field>
<field name="name">Internacional</field>
</record>
```

### res.partner.asociation.type
```
<record id="res_partner_asociation_type_data_1" model="res.partner.asociation.type">
<field name="id">1</field>
<field name="name">Marketing</field>
</record>
<record id="res_partner_asociation_type_data_2" model="res.partner.asociation.type">
<field name="id">2</field>
<field name="name">Empresarial</field>
</record>
<record id="res_partner_asociation_type_data_3" model="res.partner.asociation.type">
<field name="id">3</field>
<field name="name">ONG</field>
</record>
```

### res.partner.communication.area
```
<record id="res_partner_communication_area_data_1" model="res.partner.communication.area">
<field name="id">1</field>
<field name="name">Generalista</field>
</record>
<record id="res_partner_communication_area_data_2" model="res.partner.communication.area">
<field name="id">2</field>
<field name="name">Economía / Empresa</field>
</record>
<record id="res_partner_communication_area_data_3" model="res.partner.communication.area">
<field name="id">3</field>
<field name="name">Emprendedores / Startup</field>
</record>
<record id="res_partner_communication_area_data_4" model="res.partner.communication.area">
<field name="id">4</field>
<field name="name">Otros</field>
</record>
```

### res.partner.communication.geo
```
<record id="res_partner_communication_geo_data_1" model="res.partner.communication.geo">
<field name="id">1</field>
<field name="name">Local / Regional</field>
</record>
<record id="res_partner_communication_geo_data_2" model="res.partner.communication.geo">
<field name="id">2</field>
<field name="name">Nacional</field>
</record>
<record id="res_partner_communication_geo_data_3" model="res.partner.communication.geo">
<field name="id">3</field>
<field name="name">Internacional</field>
</record>
```

### res.partner.communicator.type
```
<record id="res_partner_communicator_type_data_1" model="res.partner.communicator.type">
<field name="id">1</field>
<field name="name">Periodista</field>
<field name="influencer">False</field>
</record>
<record id="res_partner_communicator_type_data_2" model="res.partner.communicator.type">
<field name="id">2</field>
<field name="name">Blogger</field>
<field name="influencer">False</field>
</record>
<record id="res_partner_communicator_type_data_3" model="res.partner.communicator.type">
<field name="id">3</field>
<field name="name">Influencer</field>
<field name="influencer">True</field>
</record>
```

### res.partner.customer.type
```
<record id="res_partner_customer_type_data_1" model="res.partner.customer.type">
<field name="id">1</field>
<field name="name">Anunciante</field>
<field name="advertiser">True</field>
<field name="agency">False</field>
</record>
<record id="res_partner_customer_type_data_2" model="res.partner.customer.type">
<field name="id">2</field>
<field name="name">Agencia</field>
<field name="advertiser">False</field>
<field name="agency">True</field>
</record>
```

### res.partner.educational.center.type
```
<record id="res_partner_educational_center_type_data_1" model="res.partner.educational.center.type">
<field name="id">1</field>
<field name="name">Academia</field>
</record>
<record id="res_partner_educational_center_type_data_2" model="res.partner.educational.center.type">
<field name="id">2</field>
<field name="name">Escuela de negocios</field>
</record>
<record id="res_partner_educational_center_type_data_3" model="res.partner.educational.center.type">
<field name="id">3</field>
<field name="name">Universidad</field>
</record>
<record id="res_partner_educational_center_type_data_4" model="res.partner.educational.center.type">
<field name="id">4</field>
<field name="name">Libre</field>
</record>
```

### res.partner.fan.level
```
<record id="res_partner_fan_level_data_1" model="res.partner.fan.level">
<field name="id">1</field>
<field name="name">Believer</field>
</record>
<record id="res_partner_fan_level_data_2" model="res.partner.fan.level">
<field name="id">2</field>
<field name="name">Embajador</field>
</record>
<record id="res_partner_fan_level_data_3" model="res.partner.fan.level">
<field name="id">3</field>
<field name="name">Amigo</field>
</record>
```

### res.partner.formation.type
```
<record id="res_partner_formation_type_data_1" model="res.partner.formation.type">
<field name="id">1</field>
<field name="name">Cursos</field>
</record>
<record id="res_partner_formation_type_data_2" model="res.partner.formation.type">
<field name="id">2</field>
<field name="name">Master</field>
</record>
<record id="res_partner_formation_type_data_3" model="res.partner.formation.type">
<field name="id">3</field>
<field name="name">Grado</field>
</record>
<record id="res_partner_formation_type_data_4" model="res.partner.formation.type">
<field name="id">4</field>
<field name="name">A empresas</field>
</record>
```

### res.partner.inversor.type
```
<record id="res_partner_inversor_type_data_1" model="res.partner.inversor.type">
<field name="id">1</field>
<field name="name">Potencial</field>
</record>
<record id="res_partner_inversor_type_data_2" model="res.partner.inversor.type">
<field name="id">2</field>
<field name="name">Actual</field>
</record>
```

### res.partner.market.target
```
<record id="res_partner_market_target_data_1" model="res.partner.market.target">
<field name="id">1</field>
<field name="name">B2B</field>
</record>
<record id="res_partner_market_target_data_2" model="res.partner.market.target">
<field name="id">2</field>
<field name="name">B2C</field>
</record>
```

### res.partner.partner.type
```
<record id="res_partner_partner_type_data_1" model="res.partner.partner.type">
<field name="id">1</field>
<field name="name">Stakeholder</field>
<field name="stakeholder">True</field>
<field name="user">False</field>
</record>
<record id="res_partner_partner_type_data_2" model="res.partner.partner.type">
<field name="id">2</field>
<field name="name">Usuario</field>
<field name="stakeholder">False</field>
<field name="user">True</field>
</record>
```

### res.partner.social.network
```
<record id="res_partner_social_network_data_1" model="res.partner.social.network">
<field name="id">1</field>
<field name="name">Linkedin</field>
</record>
<record id="res_partner_social_network_data_2" model="res.partner.social.network">
<field name="id">2</field>
<field name="name">Twitter</field>
</record>
<record id="res_partner_social_network_data_3" model="res.partner.social.network">
<field name="id">3</field>
<field name="name">Youtube</field>
</record>
<record id="res_partner_social_network_data_4" model="res.partner.social.network">
<field name="id">4</field>
<field name="name">Otras</field>
</record>
```

### res.partner.stakeholder.type
```
<record id="res_partner_stakeholder_type_data_1" model="res.partner.stakeholder.type">
<field name="id">1</field>
<field name="name">Fan</field>
<field name="fan">True</field>
<field name="investor">False</field>
<field name="teacher">False</field>
<field name="association">False</field>
<field name="communicator">False</field>
</record>
<record id="res_partner_stakeholder_type_data_2" model="res.partner.stakeholder.type">
<field name="id">2</field>
<field name="name">Inversor</field>
<field name="fan">False</field>
<field name="investor">True</field>
<field name="teacher">False</field>
<field name="association">False</field>
<field name="communicator">False</field>
</record>
<record id="res_partner_stakeholder_type_data_3" model="res.partner.stakeholder.type">
<field name="id">3</field>
<field name="name">Profesor</field>
<field name="fan">False</field>
<field name="investor">False</field>
<field name="teacher">True</field>
<field name="association">False</field>
<field name="communicator">False</field>
</record>
<record id="res_partner_stakeholder_type_data_4" model="res.partner.stakeholder.type">
<field name="id">4</field>
<field name="name">Asociación</field>
<field name="fan">False</field>
<field name="investor">False</field>
<field name="teacher">False</field>
<field name="association">True</field>
<field name="communicator">False</field>
</record>
<record id="res_partner_stakeholder_type_data_5" model="res.partner.stakeholder.type">
<field name="id">5</field>
<field name="name">Comunicador</field>
<field name="fan">False</field>
<field name="investor">False</field>
<field name="teacher">False</field>
<field name="association">False</field>
<field name="communicator">True</field>
</record>
```

### res.partner.user.type
```
<record id="res_partner_user_type_data_1" model="res.partner.user.type">
<field name="id">1</field>
<field name="name">Potencial</field>
</record>
<record id="res_partner_user_type_data_2" model="res.partner.user.type">
<field name="id">2</field>
<field name="name">Registrado</field>
</record>
<record id="res_partner_user_type_data_3" model="res.partner.user.type">
<field name="id">3</field>
<field name="name">Bautizado</field>
</record>
```
 
En el apartado Configuración > Técnico se añade el apartado "Oniad Partner Questionnaire" con los siguientes apartados:

- Tipos de cliente
- Tipos de stakeholder
- Niveles de fan
- Tipos de inversor
- Tipos de centro educativo
- Tipos de formación
- Tipos de asociación
- Geo de asociación
- Redes sociales
- Ámbitos de comunicación
- Geo de comunicacion
- Tipos de comunicadores
- Tipos de usuario
- Tipos de cliente
- Tipos de agencias
- Mercados objetivos
- Sectores
- Actividades
- Actividades de agencias
