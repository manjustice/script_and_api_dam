from datetime import datetime

from flask import request
from flask_restful import Resource

from config import api, app
from models import Date, DAMResult


class Main(Resource):
    def get(self):
        date_str = request.args.get("date")

        if date_str is None:
            return {"error": "Date should be in parameter"}, 400

        date_patterns = ("%d.%m.%Y", "%d-%m-%Y", "%Y.%m.%d", "%Y-%m-%d")

        valid_date = None

        for pattern in date_patterns:
            try:
                valid_date = datetime.strptime(date_str, pattern).date()
            except ValueError:
                pass
            else:
                break

        if valid_date is None:
            return {
                "error": 'Not valid date. Use this formats: "%d.%m.%Y",'
                         ' "%d-%m-%Y", "%Y.%m.%d", "%Y-%m-%d"',
            }, 400

        date_value = Date.query.filter_by(date_value=valid_date).first()

        if date_value:
            dam_results = DAMResult.query.filter_by(date_id=date_value.id).all()
            result = {
                "date": date_str,
                "dam_results": []
            }

            for result_row in dam_results:
                result["dam_results"].append({
                    "hour": result_row.hour,
                    "price": result_row.price,
                    "sales_volume": result_row.sales_volume,
                    "purchase_volume": result_row.purchase_volume,
                    "declared_sales_volume": result_row.declared_sales_volume,
                    "declared_purchase_volume": result_row.declared_purchase_volume
                })

            return result
        else:
            return {"message": "No data available for the provided date."}, 404


api.add_resource(Main, "/api/rdn-closure")
api.init_app(app)


if __name__ == '__main__':
    app.run(port=8000, host="127.0.0.1")
