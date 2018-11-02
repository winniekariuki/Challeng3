from flask_restful import Api
from flask import Blueprint

from app.api.v2.views import UserAccount,LoginUser, Produce,Singleproduct,SaleRecord,SingleSaleRecord

version2 = Blueprint('api',__name__,url_prefix='/api/v2')

api=Api(version2)

api.add_resource(LoginUser,'/auth/login')
api.add_resource(UserAccount,'/auth/signup')
api.add_resource(Produce,'/products')
api.add_resource(Singleproduct,'/products/<id>')
api.add_resource(SaleRecord,'/sales')
api.add_resource(SingleSaleRecord,'/sales/<saleID>')
