from neo4j import GraphDatabase
import json

from view import View


class Neo4jServer(object):
    def __init__(self):
        self.__driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "123"))
        # self.__truncate_db()

    def close(self):
        self.__driver.close()

    def __truncate_db(self):
        with self.__driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def registration(self, username, redis_id):
        with self.__driver.session() as session:
            session.run("MERGE (u:user {name: $username, redis_id: $redis_id})"
                        "ON CREATE SET u.online = false", username=username, redis_id=redis_id)

    def sign_in(self, redis_id):
        with self.__driver.session() as session:
            session.run("MATCH (u:user {redis_id: $redis_id}) SET u.online = true", redis_id=redis_id)

    def sign_out(self, redis_id):
        with self.__driver.session() as session:
            session.run("MATCH (u:user {redis_id: $redis_id}) SET u.online = false", redis_id=redis_id)

    def create_message(self, sender_id, consumer_id, message: dict):
        with self.__driver.session() as session:
            try:
                # session.write_transaction(self.__create_message_as_node, message["id"], message["tags"])
                session.write_transaction(self.__create_message_as_relation, int(sender_id), int(consumer_id),
                                          message["id"], message["tags"])
            except Exception as e:
                View.show_error(str(e))

    @staticmethod
    def __create_message_as_node(tx, message_id, tags: list):
        res = tx.run("MATCH (m:messages {redis_id: $message_id}) RETURN m", message_id=message_id)
        if res.peek() is not None:
            raise Exception(f"Message with id: {message_id} already exists")

        tx.run("MERGE (m:messages {redis_id: $message_id})"
               "ON CREATE SET m.tags = $tags, m.delivered = false, m.spam = false", message_id=message_id, tags=tags)

    @staticmethod
    def __create_message_as_relation(tx, sender_id, consumer_id, message_id, tags: list):
        tx.run("MATCH(a: user {redis_id: $sender_id}), (b:user {redis_id: $consumer_id})"
               "MERGE(a) - [r: messages]->(b)"
               "ON CREATE SET r += {all: [$message_id], spam: [], tags: $tags}"
               "ON MATCH SET r.all = r.all + 2, r.tags = r.tags + $tags",
               sender_id=sender_id, consumer_id=consumer_id, message_id=message_id, tags=tags)

    def deliver_message(self, redis_id):
        with self.__driver.session() as session:
            session.run("MATCH (m:messages {redis_id: $redis_id }) SET m.delivered = true", redis_id=redis_id)

    def mark_message_as_spam(self, redis_id):
        with self.__driver.session() as session:
            # session.run("MATCH (m:messages {redis_id: $redis_id }) SET m.spam = true", redis_id=redis_id)
            session.run("MATCH (u1:user)-[r:messages]->(u2:user) "
                        "WHERE $redis_id IN r.all AND NOT $redis_id IN r.spam "
                        "SET r.spam = r.spam + $redis_id", redis_id=redis_id)

    def get_users_with_tagged_messages(self, tags: list):
        with self.__driver.session() as session:
            query = "MATCH (m:messages) WHERE"
            for tag in tags:
                query += f" \'{tag}\' IN m.tags AND"

            query = query[:-3] + "MATCH (u1:user)-[r:messages]->(u2:user) " \
                                 "WHERE m.redis_id IN r.list " \
                                 "RETURN u1"
            res = session.run(query)
            return list(res)
