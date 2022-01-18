import json
from datetime import datetime
from shopify.logger.logger import logger
from shopify.service.cache.inventoryCache import InventoryResponseCache
from shopify.service.handler.baseHandler import BaseHandler
from shopify.db.helper.inventoryDAOHelper import InventoryDAOHelper
from shopify.service.type.types import ResponseType
from shopify.util.csvUtil import CsvUtil

class InventoryControlHandler(BaseHandler):

    inventoryCache = InventoryResponseCache()

    async def get(self, slug=None):
        logger.info('[GET] Request - {}'.format(self.request.path))
        slug = slug.upper()
        try:
            if slug == 'LIST':
                response, state = self.getBasedOnFilters()
            elif slug == 'EXPORT':
                response, state = self.generateCSVBasedOnFilters()
                self.send_response_csv(response, state)
                return
            self.send_response(response, state)
            logger.info('[GET] Response - {}'.format(self.request.path))
        except Exception as e:
            logger.exception(e)
            self.throwError()

    async def post(self, slug=None):
        logger.info('[POST] Request - {}'.format(self.request.path))
        slug = slug.upper()
        try:
            if slug == 'CREATE':
                response, state = self.createItem()
            if slug == 'UPDATE':
                response, state = self.updateItem()
            self.send_response(response, state)
            logger.info('[POST] Response - {}'.format(self.request.path))
        except Exception as e:
            self.throwError()

    async def delete(self, slug=None):
        logger.info('[DEL] Request - {}'.format(self.request.path))
        slug = slug.upper()
        try:
            if slug == 'DELETE':
                response, state = self.deleteItem()
            self.send_response(response, state)
            logger.info('[DEL] Response - {}'.format(self.request.path))
        except Exception as e:
            self.throwError()

    def isArgumentsSafe(self, args):
        return True

    def generateCSVBasedOnFilters(self):
        state = ResponseType.SUCCESS
        filePath, fileName = '', ''
        try :
            data, _ = self.getBasedOnFilters()
            fileName = "export_{}.csv".format(datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S'))
            filePath = CsvUtil.generateCSV('export.csv', data)
        except Exception as _:
            state = ResponseType.SERVER_ERROR
        response = {
            'path': filePath,
            'name': fileName
        }
        return response, state

    def getBasedOnFilters(self):
        args = self.request.arguments
        state = ResponseType.SUCCESS
        f = InventoryDAOHelper.getQueryParams(**args)

        collectedFromCache = False
        if len(f) == 0:
            res = InventoryControlHandler.inventoryCache.getCache('all', None)
            if res is not None:
                collectedFromCache = True

        if not collectedFromCache:
            res = InventoryDAOHelper.get(f)
            if len(res) != 0:
                res = InventoryDAOHelper.to_dict(res)
            InventoryControlHandler.inventoryCache.setCache('all', res)
        else:
            logger.info('Serving the request from cached data...')

        return res, state

    def createItem(self):
        args = json.loads(self.request.body)
        state = ResponseType.SUCCESS
        try:
            res = InventoryDAOHelper.create(**args)
        except Exception as e:
            state = ResponseType.INVALID_ARGS
            InventoryDAOHelper.rollback()

        if state == ResponseType.SUCCESS:
            InventoryControlHandler.inventoryCache.setIsDirty()

        return {}, state

    def updateItem(self):
        args = json.loads(self.request.body)
        state = ResponseType.SUCCESS
        filterCriteria = {'inventoryId': args['inventoryId']}
        f = InventoryDAOHelper.getQueryParams(**filterCriteria)
        try:
            res = InventoryDAOHelper.update(f, args['updates'])
        except Exception as e:
            state = ResponseType.SERVER_ERROR
            InventoryDAOHelper.rollback()

        if state == ResponseType.SUCCESS:
            InventoryControlHandler.inventoryCache.setIsDirty()

        return {'operation': 'UPDATE',  'numberOfRows': res}, state

    def deleteItem(self):
        args = json.loads(self.request.body)
        state = ResponseType.SUCCESS
        f = InventoryDAOHelper.getQueryParams(**args)
        try:
            res = InventoryDAOHelper.delete(f)
        except Exception as e:
            state = ResponseType.SERVER_ERROR
            InventoryDAOHelper.rollback()

        if state == ResponseType.SUCCESS:
            InventoryControlHandler.inventoryCache.setIsDirty()

        return {'operation': 'DELETE',  'numberOfRows': res}, state



