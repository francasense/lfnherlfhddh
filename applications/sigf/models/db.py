# -*- coding: utf-8 -*-
import psycopg2

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

from gluon.contrib.appconfig import AppConfig
#
myconf = AppConfig(reload=True)
####
if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL('postgres://postgres:k6h7j7v1@ec2-52-32-97-114.us-west-2.compute.amazonaws.com:5432/sigf') #amazon

else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)

response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

from gluon.tools import Auth, Service, PluginManager

db.define_table('t_departamento', Field('f_name', type='string',label='Departamento'),format='%(f_name)s')

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=myconf.get('host.names'))
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user']= [
                                              Field('f_departamento', db.t_departamento, label='Departamento'),
                                              Field('f_cpf', type="string", label='CPF')
                                              ]
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True


db.define_table('t_time',
    Field('f_nome', type='string',label=T('Descrição')),
    Field('f_qtd_jogadores', type='integer',label=T('numero de Jogadores')),auth.signature,
    format='%(f_nome)s'
                #,migrate=settings.migrate
               )
