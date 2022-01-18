from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shopify.util.configUtil import ConfigUtil

class DefaultSessionFactory:

    def __init__(self):
        self.configUtil = ConfigUtil()
        connectionString = self.getConnectionString()
        self.engine = self.createEngine(connectionString)
        SessionFactory = sessionmaker(bind=self.engine)
        self.session = SessionFactory()

    def createEngine(self, connStr):
        return create_engine(connStr, connect_args={'charset': 'utf8'})

    def getSession(self):
        return self.session

    def getEngine(self):
        return self.engine

    def getConnectionString(self):
        dbDetails = self.configUtil.getConfig(['database'])
        if dbDetails is not None:
            dbType = dbDetails.get('type', None)
            userName = dbDetails.get('user', None)
            password = dbDetails.get('password', None)
            endpoint = dbDetails.get('endpoint', None)
            port = dbDetails.get('port', None)
            dbName = dbDetails.get('name', None)

        if dbDetails is None or None in [dbType, userName, password, endpoint, port, dbName]:
            raise Exception('Error while formulating the connection string for DB connection')

        self.dbType = dbType
        connectionStringTemplate = '{}://{}:{}@{}:{}/{}'
        return connectionStringTemplate.format(dbType, userName, password, endpoint, port, dbName)

if __name__ == '__main__':
    d = DefaultSessionFactory()
    s = d.getSession()
    s.execute("SELECT current_database();")







