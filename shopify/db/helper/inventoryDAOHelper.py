from datetime import datetime
from shopify.db.model.core import Inventory, InventoryType
from shopify.db.session.sessionFactory import DefaultSessionFactory
from shopify.util.validatorUtil import ValidatorUtil

class InventoryDAOHelper:

    session = DefaultSessionFactory().getSession()
    lowRange = 'low'
    highRange = 'high'
    rangeParams = {
        'priceHigh': {
            'column': 'price',
            'type': 'high'
        },
        'priceLow': {
            'column': 'price',
            'type': 'low'
        },
        'quantityHigh': {
            'column': 'quantity',
            'type': 'high'
        },
        'quantityLow': {
            'column': 'quantity',
            'type': 'Low'
        },
    }

    @staticmethod
    def setTimeVars(item, creation=True):
        t = datetime.now()
        if creation:
            setattr(item, 'creationTime', t)
        setattr(item, 'modifiedTime', t)

    @staticmethod
    def getQueryParams(inventoryId=None, name=None, code=None,
                       type=None, supplier=None, priceLow=None,
                       priceHigh=None, quantityLow=None, quantityHigh=None):
        args = {
            'inventoryId': inventoryId, 'name': name, 'code': code,
            'type': type, 'supplier': supplier, 'priceLow': priceLow,
            'priceHigh': priceHigh, 'quantityLow': quantityLow, 'quantityHigh': quantityHigh
        }
        queryParams = []

        for key in args:
            if args[key] is not None:
                if key in InventoryDAOHelper.rangeParams:
                    attrInstance = getattr(Inventory, InventoryDAOHelper.rangeParams[key].get('column'))
                    if InventoryDAOHelper.rangeParams[key].get('column') == InventoryDAOHelper.lowRange:
                        queryParams.append(attrInstance >= float(args[key]))
                    if InventoryDAOHelper.rangeParams[key].get('column') == InventoryDAOHelper.highRange:
                        queryParams.append(attrInstance <= float(args[key]))
                else:
                    attrInstance = getattr(Inventory, key)
                    if isinstance(args[key], list):
                        queryParams.append(attrInstance.in_(inventoryId))
                    else:
                        queryParams.append(attrInstance.in_([inventoryId]))
        return queryParams

    @staticmethod
    def get(filters):
        res = InventoryDAOHelper.session.query(Inventory).filter(*filters).all()
        return res

    @staticmethod
    def delete(filters):
        res = InventoryDAOHelper.session.query(Inventory).filter(*filters).delete(synchronize_session='fetch')
        InventoryDAOHelper.session.commit()
        return res

    @staticmethod
    def validateArgs(args):
        validationMapper = {
            'name': ValidatorUtil.isValidString,
            'code': ValidatorUtil.isValidCode,
            'type': ValidatorUtil.isValidInventoryItemType,
            'supplier': ValidatorUtil.isValidString,
            'description': ValidatorUtil.isValidString,
            'quantity': ValidatorUtil.isValidInt,
            'price': ValidatorUtil.isValidFloat,
        }
        isValid = True
        for key in args:
            val = args[key]
            if key in validationMapper:
                isValid &= validationMapper[key](val)
        return isValid

    @staticmethod
    def create(inventoryId=None, name=None, code=None,
               type=None, supplier=None,
               description=None, quantity=None, price=None):
        args = {
            'inventoryId': inventoryId, 'name': name, 'code': code,
            'type': type, 'supplier': supplier,
            'description': description, 'quantity': quantity, 'price': price
        }

        if not InventoryDAOHelper.validateArgs(args):
            raise Exception('Invalid arguments passed. Returning ...')

        i = Inventory()
        for key in args:
            if args[key] is not None:
                if key == 'type':
                    enumName = InventoryType(int(args[key]))
                    setattr(i, key, enumName)
                else:
                    setattr(i, key, args[key])
        InventoryDAOHelper.setTimeVars(i)
        InventoryDAOHelper.session.add(i)
        InventoryDAOHelper.session.commit()
        return i

    @staticmethod
    def update(filters, updateParams):
        formulatedParams = {}

        if not InventoryDAOHelper.validateArgs(updateParams):
            raise Exception('Invalid arguments passed. Returning ...')

        for key in updateParams:
            if hasattr(Inventory, key):
                if key == 'type':
                    enumName = InventoryType(int(updateParams[key]))
                    updateParams[key] = enumName
                formulatedParams[getattr(Inventory, key)] = updateParams[key]
        res = InventoryDAOHelper.session.query(Inventory).filter(*filters).update(formulatedParams, synchronize_session='fetch')
        InventoryDAOHelper.session.commit()
        return res

    @staticmethod
    def rollback():
        InventoryDAOHelper.session.rollback()

    @staticmethod
    def to_dict(listOfItems):
        op = []
        if not isinstance(listOfItems, list):
            listOfItems = [listOfItems]
        for item in listOfItems:
            op.append({c.name: getattr(item, c.name) for c in item.__table__.columns})
        return op



