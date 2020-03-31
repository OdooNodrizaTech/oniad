El módulo contiene el desarrollo para implementar funcionalidades relacionadas especialmente con el contacto, con el objetivo de segmentarlo mucho mejor.

Se introducen los siguientes datos por defecto en la instalación:

### res.partner.agency.activity
id | name
--- | ---
1 | Web / Ecommerce
2 | ERP / CRM
3 | SEM / PPC / Social Ads
4 | RTB / Programatic
5 | Afiliacion / Email
6 | Community Management
7 | Compra de medios
8 | Diseño gráfico
9 | Impresion y merchandising
10 | Branding
11 | Audiovisual
12 | Gabinete de prensa
13 | Eventos

### res.partner.agency.type
id | name
--- | ---
1 | Consultor
2 | Micro-agencia
3 | Agencia

### res.partner.asociation.geo
id | name
--- | ---
1 | Local / regional
2 | Nacional
3 | Internacional

### res.partner.asociation.type
id | name
--- | ---
1 | Marketing
2 | Empresarial
3 | ONG

### res.partner.communication.area
id | name
--- | ---
1 | Generalista
2 | Economía / Empresa
3 | Emprendedores / Startup
4 | Otros

### res.partner.communication.geo
id | name
--- | ---
1 | Local / Regional
2 | Nacional
3 | Internacional

### res.partner.communicator.type
id | name | influencer
--- | --- | ---
1 | Periodista | False
2  Blogger | False
3| Influencer | True

### res.partner.customer.type
id | name | advertiser | agency
--- | --- | ---
1 | Anunciante | True | False
2| Agencia | False | True

### res.partner.educational.center.type
id | name
--- | ---
1 | Academia
2 | Escuela de negocios
3 | Universidad
4 | Libre

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
