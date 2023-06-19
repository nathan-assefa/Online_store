#!/usr/bin/python3
""" This is backend engine for the MySQL database """


from models.base_model import BaseModel, Base
from models.user import User
from models.category import Category
from models.product import Product
from models.review import Review
from models.cart import Cart
from models.cart_item import CartItem
from models.order import Order
from models.order_item import OrderItem
from sqlalchemy import create_engine
from os import getenv


class_names = [
        User,
        Category,
        Product,
        Review,
        Cart,
        CartItem
        ]


class DBStorage:
    """ an engine for backend """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        ONLINE_STORE_MYSQL_USER = getenv('ONLINE_STORE_MYSQL_USER')
        ONLINE_STORE_MYSQL_PWD = getenv('ONLINE_STORE_MYSQL_PWD')
        ONLINE_STORE_MYSQL_HOST = getenv('ONLINE_STORE_MYSQL_HOST')
        ONLINE_STORE_MYSQL_DB = getenv('ONLINE_STORE_MYSQL_DB')
        ONLINE_STORE_ENV = getenv('ONLINE_STORE_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(ONLINE_STORE_MYSQL_USER,
                                             ONLINE_STORE_MYSQL_PWD,
                                             ONLINE_STORE_MYSQL_HOST,
                                             ONLINE_STORE_MYSQL_DB),
                                      pool_pre_ping=True)
        if ONLINE_STORE_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        # let us first compile a list of class so that we
        # query via loop
        query_classes = class_names if not cls else [cls]

        # making query for each class using list comprehension

        list_obj = [
                obj for query_class in query_classes
                for obj in self.__session.query(query_class)
                ]

        return {f"{type(obj).__name__}.{obj.id}": obj for obj in list_obj}

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def close(self):
        self.__session.close()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def get(self, cls, id):
        """Returns the object based on the class and its ID, or None"""
        if cls and id and type(id) is str:
            if type(cls) is not str:
                cls = cls.__name__
            return self.all().get(cls + "." + id)
        return None

    def count(self, cls=None):
        """ Counting the number of objects in the database"""
        all_objects = self.all().values()
        if cls:
            if type(cls) is not str:
                cls = cls.__name__
            return len(self.all(cls))
        else:
            return len(self.all())

    def retrieve_cart_items(self, user_id):
        try:
            # Retrieve the user's cart items
            cart_items = (
                self.__session.query(CartItem)
                .join(Cart)
                .filter(Cart.user_id == user_id)
                .all()
            )

            # Merge the associated Product objects with the session
            for cart_item in cart_items:
                self.__session.merge(cart_item.product)

            '''
                ************* why merge function? *****************
                The merge function in SQLAlchemy is used to merge the
                state of detached objects into the session, allowing
                updates to be synchronized with the database

                it mainly resolves the error message "the parent instance
                (CartItem) is not bound to a session", meaning this error
                typically occurs when you're trying to access a lazy-loaded
                attribute outside of an active session.

                All in all, the merge function is used here since the
                'cart_item.product' is going to be used in other sessions, so
                by merging it before closing the current session, we can make
                sure that the 'product' attribute can still be accecced in
                another session.
            '''

            return cart_items
        except Exception:
            pass

        finally:
            self.close()
    

    def create_order_items(self, user_id, order_id):
        try:
            cart_items = self.retrieve_cart_items(user_id)
            order_items = []
            for cart_item in cart_items:
                order_item = OrderItem()
                order_items.append(order_item)
            
            for order_item, cart_item in zip(order_items, cart_items):
                order_item.quantity = cart_item.quantity
                order_item.product_id = cart_item.product_id
                order_item.price = cart_item.product.price
                order_item.order_id = order_id

            self.__session.add_all(order_items)  # Use add_all() to add all objects

            self.save()
            '''
                 ******************why zip function?**************
                 the zip() function is used to iterate over both order_items and
                 cart_items simultaneously, allowing you to assign the corresponding
                 values to the order_item attributes.
            '''
        except Exception as e:
            print(e)

        finally:
            self.close()


    def total_price(self, user_id):
        try:
            cart_items = self.retrieve_cart_items(user_id)
            total_price = 0

            for cart_item in cart_items:
                item_price = cart_item.price * cart_item.quantity
                total_price += item_price
            return total_price

            # The `total_price` variable now holds the cumulative
            # cost of all items in the cart
        except Exception:
            pass


    def reload(self):
        from sqlalchemy.orm import sessionmaker, scoped_session

        Base.metadata.create_all(self.__engine)

        # create a new database session
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

        """ why 'scoped_session' is required in this context ?
        In SQLAlchemy, scoped_session is a utility function that creates
        a thread-local scope for a session. It provides a way to manage
        sessions within a web application or multi-threaded environment,
        ensuring that each thread has its own unique session instance.

        The scoped_session function takes a session factory as an argument
        and returns a new session object. This new session is associated with
        the current thread and can be accessed using the same syntax as a
        regular session.

        The main advantage of using scoped_session is that it simplifies
        the management of sessions in multi-threaded scenarios. Each thread
        can access its own unique session without interfering with other
        threads. It provides a thread-local scope, meaning that sessions are
        stored in a thread-local variable, ensuring that each thread operates
        with its own isolated session.

        By using scoped_session, you can avoid issues related to thread-safety
        and ensure that each thread has its own dedicated session for performing
        database operations.
        """

        """ What is thread then? 
        In computer programming, a thread is the smallest unit of execution
        within a process. A thread is a sequence of instructions that can be
        executed independently and concurrently with other threads within
        the same process.

        Threads are lightweight compared to processes because they share
        the same memory space and resources of the parent process. Multiple
        threads within a process can execute concurrently, allowing for parallel
        execution and efficient utilization of system resources.

        Threads are commonly used in concurrent programming to achieve
        multitasking and improve application performance. By dividing
        the program into multiple threads, different parts of the program can
        execute simultaneously, making it possible to perform multiple 
        tasks concurrently.

        Threads can communicate and share data with each other through shared
        memory or message passing mechanisms. However, since threads operate
        in the same memory space, they need to synchronize access to shared
        resources to avoid conflicts and ensure data integrity.

        In summary, a thread is an independent sequence of instructions that
        can execute concurrently with other threads within a process, allowing
        for multitasking and parallel execution.

        In the context of web services, threads can be used to handle multiple
        concurrent requests and improve the scalability and responsiveness of
        the service. Here are a few points to consider regarding threads in web services:

            Concurrent request handling: When a web service receives multiple 
            requests simultaneously, each request can be assigned to a separate
            thread for processing. This allows the service to handle multiple
            requests concurrently, ensuring that one request does not block others
            from being processed.

            Improved responsiveness: By using threads, a web service can respond
            to requests more quickly. While one thread is performing a time-consuming
            operation, such as accessing a database or making an external API call,
            other threads can continue processing other requests.
            This helps to prevent delays and ensures that the service remains
            responsive to incoming requests.

            Scalability: Threads enable a web service to scale horizontally by
            handling multiple requests concurrently. As the load on the service
            increases, more threads can be created to handle additional requests,
            allowing the service to accommodate more clients and distribute the
            workload across multiple threads.
        """

        """ why 'bind' is required is sessionmaker?
        When you create a session using sessionmaker, you can pass the bind
        argument to associate the session with a specific engine. This allows
        the session to use the engine for database operations such as querying,
        inserting, updating, and deleting data.

        By binding a session to an engine, you ensure that all database
        operations performed through that session are executed on the specified
        database connection. This helps maintain consistency and allows multiple
        sessions to work with different database connections concurrently.
        """
                

