from database.DB_connect import DBConnect
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategory(): #1 - poi aggiungere questo nel model

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from  categories c "

        cursor.execute(query)

        for row in cursor:
            results.append(row["category_name"])


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllProduct(category):  # 1 - poi aggiungere questo nel model

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select p.product_id, p.product_name, p.brand_id, p.category_id, p.model_year, p.list_price 
                    from categories c , products p 
                    where c.category_id = p.category_id and c.category_name = %s
                    order by p.product_name ASC

                """

        cursor.execute(query, (category,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVenditeProdotto(category, startDate, endDate):  # 1 - poi aggiungere questo nel model

        conn = DBConnect.get_connection()



        cursor = conn.cursor(dictionary=True)
        query = """ 
                select p.product_id , p.product_name , SUM(oi.quantity ) as vendite
                from categories c, products p, order_items oi ,orders o 
                where c.category_id = p.category_id and p.product_id = oi.product_id and o.order_id = oi.order_id 
                and c.category_name = %s
                and o.order_date between  %s  and  %s
                group by p.product_name, p.product_id  

                """

        cursor.execute(query, (category,startDate,endDate))
        idMapVendite = {}

        for row in cursor:
            idMapVendite[row["product_id"]] = row["vendite"]


        cursor.close()
        conn.close()
        return idMapVendite