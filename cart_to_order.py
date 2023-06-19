from models import storage
from models.cart_item import CartItem

usr_id = '71d9d033-e990-4187-8ef4-8a3225e1a81c'
ord_id = '73b1c64e-d48c-4b1b-944d-e601a9bc4196'
#CartItem(quantity=12, product_id="1fd9f2de-a104-4421-b38c-0e9603499a82", cart_id="0169afcc-e0f6-4438-94a4-b42135ab3bd7")

#storage.try_create_order_items(usr_id, ord_id)
#storage.retrieve_cart_items(usr_id)
storage.create_order_items(usr_id, ord_id)
