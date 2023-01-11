from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import os
import json

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
        
    def delete_all(self):
        with self.driver.session(database="neo4j") as session:
            session.run("MATCH (n) DETACH DELETE n")
  
    def create_initNode(self, node1_name, node2_name, node3_name,count):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._create_and_return_applyment, node1_name, node2_name, node3_name,count)
            for row in result:
                print("Created friendship between: {p1}, {p2},{p3}".format(p1=row['p1'], p2=row['p2'], p3=row['p3']))        
    
    @staticmethod
    def _create_and_return_applyment(tx, node1_name, node2_name,node3_name,count):
        label="BaseNode"+str(count)
        query = (
            "CREATE (p1:"+eval(repr(label))+" { name: $node1_name }) "
            "CREATE (p2:"+eval(repr(label))+" { name: $node2_name }) "
            "CREATE (p3:"+eval(repr(label))+" { name: $node3_name }) "
            "CREATE (p1)-[:作用]->(p3) "
            "CREATE (p2)-[:作用]->(p3) "
            "RETURN p1, p2, p3"
        )
        result = tx.run(query, node1_name=node1_name, node2_name=node2_name,node3_name=node3_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"],"p3": row["p3"]["name"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
        
    def create_affect(self, key, value_text,count):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._create_and_return_affect, key, value_text,count)
        for row in result:
            print("Created node: {p1}".format(p1=row['p1'])) 
    
    @staticmethod
    def _create_and_return_affect(tx, key, value,count):
        label="BaseNode"+str(count)
        print("MERGE (p2)-[:"+eval(repr(key))+"]->(p1)")
        query = (
            "CREATE (p1:Node { name: $value }) "
            "WITH true as pass "
            "MATCH (p1:Node {name: $value}) "
            "MATCH (p2:"+eval(repr(label))+" { name: $base }) "
            "MERGE (p2)-[:"+eval(repr(key))+"]->(p1)"
        )
        result = tx.run(query, value=value, base="承灾体")
        try:
            return [{"p1": row["p1"]["name"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            
    def create_environment(self, key, value_text,count):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._create_and_return_environment, key, value_text,count)
        for row in result:
            print("Created node: {p1}".format(p1=row['p1'])) 
    
    @staticmethod
    def _create_and_return_environment(tx, key, value,count):
        print("MERGE (p2)-[:"+eval(repr(key))+"]->(p1)")
        label="BaseNode"+str(count)
        query = (
            "CREATE (p1:Node { name: $value }) "
            "WITH true as pass "
            "MATCH (p1:Node {name: $value}) "
            "MATCH (p2:"+eval(repr(label))+" { name: $base }) "
            "MERGE (p2)-[:"+eval(repr(key))+"]->(p1)"
        )
        result = tx.run(query, value=value, base="孕灾环境")
        try:
            return [{"p1": row["p1"]["name"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))

    def create_factor(self, key, value_text,count):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(
                self._create_and_return_factor, key, value_text,count)
        for row in result:
            print("Created node: {p1}".format(p1=row['p1'])) 
    
    @staticmethod
    def _create_and_return_factor(tx, key, value,count):
        print("MERGE (p2)-[:"+eval(repr(key))+"]->(p1)")
        label="BaseNode"+str(count)
        query = (
            "CREATE (p1:Node { name: $value }) "
            "WITH true as pass "
            "MATCH (p1:Node {name: $value}) "
            "MATCH (p2:"+eval(repr(label))+" { name: $base }) "
            "MERGE (p2)-[:"+eval(repr(key))+"]->(p1)"
        )
        result = tx.run(query, value=value, base="致灾因子")
        try:
            return [{"p1": row["p1"]["name"]}
                    for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
    
if __name__ == "__main__":
    uri = "bolt://121.5.136.152:7687"
    user = ""
    password = ""
    app = App(uri, user, password)
    app.delete_all()
    files = os.listdir('./json')
    for i in range(0,len(files)-3):
        count=i
        app.create_initNode("致灾因子","孕灾环境","承灾体",count)
        filename="json/result"+str(i)+".json"
        with open(filename,'r',encoding='utf8')as json_file:
            data = json.load(json_file)
            for i in data[0].items():
                key=i[0]
                value=i[1]
                value_text=value[0]['text']
                value_probability=value[0]['probability']
                if key in ['死亡','失踪','受伤','轻伤','重伤','受灾人数','房屋损坏','房屋倒塌','损坏','倒塌','农作物','受灾面积','万公顷','公顷','绝收','亩','千亩','万亩','经济损失','元','万元','亿元','地区']:
                    app.create_affect(key,value_text,count)                    
                if key in ['台风名称','灾害','致灾因子','台风']:
                    app.create_factor(key,value_text,count)    
                if key in ['风速','风力','时间','东经','北纬','降雨','半径','大风级数']:
                    app.create_environment(key,value_text,count)
    app.close()