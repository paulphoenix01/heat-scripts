from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

auth = v3.Password(auth_url='https://192.168.250.1:5000/v3/auth/token?nocatalog', user_id='admin', password='contrail123', project_id='appformix')

sess = session.Session(auth=auth)
#print sess

keystone = client.Client(session=sess)

print keystone.get_token_data()
