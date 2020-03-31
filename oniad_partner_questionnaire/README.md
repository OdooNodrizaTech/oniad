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
--- | --- | --- | ---
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
id | name
--- | ---
1 | Believer
2 | Embajador
3 | Amigo

### res.partner.formation.type
id | name
--- | ---
1 | Cursos
2 | Master
3 | Grado
4 | A empresas

### res.partner.inversor.type
id | name
--- | ---
1 | Potencial
2 | Actual

### res.partner.market.target
id | name
--- | ---
1 | B2B
2 | B2C

### res.partner.partner.type
id | name | stakeholder | user
--- | --- | --- | ---
1 | Stakeholder | True | False
2 | Usuario | False | True

### res.partner.social.network
id | name
--- | ---
1 | Linkedin
2 | Twitter
3 | Youtube
4 | Otras

### res.partner.stakeholder.type
id | name | fan | investor | teacher | association | communicator
--- | --- | --- | --- | --- | --- | ---
1 | Fan | True | False | False | False | False
2 | Inversor | False | True | False | False | False
3 | Profesor | False | False | True | False | False
4 | Asociación | False | False | False | True | False
5 | Comunicador | False | False | False | False | True

### res.partner.user.type
id | name
--- | ---
1 | Potencial
2 | Registrado
3 | Bautizado
 
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
