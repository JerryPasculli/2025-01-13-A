from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction
from model.nodo import Nodo


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM classification"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_local():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """SELECT distinct Localization
                            FROM classification
                            order by Localization ASC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row)

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodi(tipo):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select c.GeneID, g.Essential
from classification c, genes g  where Localization = %s and c.GeneID = g.GeneID 
group by c.GeneID, g.Essential """
            cursor.execute(query, [tipo])

            for row in cursor:
                result.append(Nodo(**row))

            cursor.close()
            cnx.close()
        return result



    @staticmethod
    def get_archi(tipo):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """with nodi as (select *
from classification c where Localization = %s),
geni as (select GeneID1, GeneID2
from interactions i 
group by GeneID1, GeneID2),
coppie as (select n1.GeneId primo, n1.Localization lprimo, n2.GeneId secondo, n2.Localization lsecondo
from nodi n1, nodi n2, geni g
where n1.GeneId>n2.GeneId and (n1.GeneId = g.GeneId1 or  n1.GeneId = g.GeneId2)
and (n2.GeneId = g.GeneId1 or  n2.GeneId = g.GeneId2)
group by n1.GeneId, n1.Localization, n2.GeneId, n2.Localization),
crom as (select g.GeneId, g.Chromosome
from genes g, nodi n
where g.GeneId = n.GeneId
group by g.GeneId)


select  c.*, sum(distinct(Chromosome)) peso
from coppie c, crom c1
where primo = c1.GeneId or secondo = c1.GeneId
group by primo, lprimo, secondo, lsecondo
ORDER by peso ASC"""
            cursor.execute(query, [tipo])

            for row in cursor:
                result.append([row[0], row[2], row[4]])

            cursor.close()
            cnx.close()
        return result
