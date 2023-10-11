from flask import Blueprint, redirect, render_template, request, flash, session
from flask import current_app as app
from flask_login import login_required, current_user
from . import database
from .models import Item, Order
import os
from werkzeug.utils import secure_filename
from PIL import Image
from datetime import datetime

perspectives = Blueprint("perspectives", __name__)


# HELPER METHODS
def resize_image(filename):
    image = Image.open("website/static/original_images/"+filename)
    resized_image = image.resize((500,500))
    resized_image.save("website/static/resized_images/"+filename)

def merge_dicts(d1, d2):
    return dict(list(d1.items()) + list(d2.items()))

def set_settings(s2change, s):
    if "Settings" in session:
        session["Settings"] = merge_dicts(session["Settings"], {s2change: s})
    else:
        session["Settings"] = {
        "sort_type_home": "id", 
        "sort_type_mc": "id", 
        "sort_type_helmets": "id", 
        "sort_type_clothing": "id",
        "sort_type_allitems": "id"
        }

def base_route(sort_type_setting, items, template):
    if request.method == "POST":
        set_settings(sort_type_setting, request.form.get("sortby"))
    
    if "Settings" not in session: set_settings("placeholder", "placeholder")

    return render_template(template, user=current_user, content=items, sort_type=session["Settings"][sort_type_setting])

def calc_total(dict):
    TOTAL = 0
    if dict in session:
        for item in session[dict]:
            TOTAL += session[dict][item]["price"] * int(session[dict][item]["quantity"])
    return TOTAL

def update_database(data):
    for item in data:
        current_item = Item.query.filter_by(id=item).first()
        current_item.stock = current_item.stock - int(data[item]["quantity"])
        database.session.commit()

def check_item_stock(dict):
    sold_out_items = []
    if dict in session:
        for item in session[dict]:
            current_item = Item.query.filter_by(id=item).first()
            session.modified = True
            session["ItemBasket"][item]["stock"] = current_item.stock
            if current_item.stock < int(session[dict][item]["quantity"]):
                sold_out_items.append(item)
        if len(sold_out_items) != 0:
            return [False, sold_out_items]
    return [True, sold_out_items]

@perspectives.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        set_settings("sort_type_home", request.form.get("sortby"))
        
    if "Settings" not in session: set_settings("placeholder", "placeholder")

    return render_template("home.html",
                            user=current_user,
                            content=Item.query.filter_by(exclusive="0").order_by(Item.id.desc()).limit(8),
                            content2=Item.query.filter_by(exclusive="1").limit(4),
                            sort_type=session["Settings"]["sort_type_home"]
                            )

@perspectives.route("/model_cars", methods=["GET", "POST"])
def model_cars():
    return base_route("sort_type_mc", Item.query.filter_by(item_type="Model Car", exclusive="0"), "model_cars.html")

@perspectives.route("/helmets", methods=["GET", "POST"])
def helmets():
    return base_route("sort_type_helmets", Item.query.filter_by(item_type="Helmet", exclusive="0"), "helmets.html")

@perspectives.route("/clothes", methods=["GET", "POST"])
def clothes():
    return base_route("sort_type_clothing", Item.query.filter_by(item_type="Clothing", exclusive="0"), "clothes.html")

@perspectives.route("/allitems", methods=["GET", "POST"])
def all_items():
    return base_route("sort_type_allitems", Item.query.all(), "allitems.html")

@perspectives.route("/basket")
def basket():
    return render_template("basket.html", user=current_user, TOTAL=calc_total("ItemBasket"), 
                        success=check_item_stock("ItemBasket")[0], 
                        out_of_stock_items=check_item_stock("ItemBasket")[1]) 
     
@perspectives.route("/checkout")
def checkout():
    return render_template("checkout.html", user=current_user, TOTAL=calc_total("ItemBasket"))

@perspectives.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_authenticated and current_user.id == 1:
        items = Item.query.all()
        if request.method == "POST":
            file = request.files['file']
            name = request.form.get("name")
            price = request.form.get("price")
            env_impact = request.form.get("env_impact")
            desc = request.form.get("desc")
            stock = request.form.get("stock")
            item_type = request.form.get("item_type")
            exclusive = request.form.get("exclusive")
            
            filename = secure_filename(file.filename)
            if filename:
                file.save(os.path.join(app.static_folder, ("original_images/"+filename)))
                resize_image(filename)
            
            if file and name and price and env_impact and desc and stock and item_type and exclusive and filename:
                new_item = Item(name=name, price=price, env_impact=env_impact, desc=desc, filename=file.filename, stock=stock, item_type=item_type, exclusive=exclusive)
                database.session.add(new_item)
                database.session.commit()
                return redirect(request.referrer)
            
        return render_template('admin.html', user=current_user, content=items)
    return redirect("/")

@perspectives.route("/addbasket", methods=["POST"])
def add_basket():
    # check if there has been a press of the add basket button
    if request.method == "POST":
        item_id = request.form.get("item_id")
        quantity = request.form.get("quantity")
        if item_id and quantity:
            item = Item.query.filter_by(id=item_id).first()
            items_dict = {
                item_id: {"name": item.name,
                            "price": item.price,
                            "filename": item.filename,
                            "quantity": quantity,
                            "id": item_id,
                            "stock": item.stock}
            }   
            # Add the basket to the session if its not already in it
            if "ItemBasket" in session:
                # Is the item already in the basket?
                if item_id in session["ItemBasket"]:
                    flash("Item is already in basket.", category="invalid")
                else:
                    # Add item to basket
                    session["ItemBasket"] = merge_dicts(d1=session["ItemBasket"], d2=items_dict) 
            else:
                session["ItemBasket"] = items_dict
    return redirect(request.referrer)

@perspectives.route("/updatebasket", methods=["POST"])
def update_basket():
    if "ItemBasket" in session:
        if request.method == "POST":
            new_quantity = request.form.get("quantity")
            item_id = request.form.get("item_id")

            # Ensure changes maintain
            temp = session["ItemBasket"][item_id]
            temp["quantity"] = new_quantity
            session["ItemBasket"] = merge_dicts(session["ItemBasket"], {str(item_id): temp})
    return redirect("/basket")        

@perspectives.route("/removeitem", methods=["POST"])
def remove_item():
    if "ItemBasket" in session and len(session["ItemBasket"]) > 0:
        if request.method == "POST":
            item_id = request.form.get("item_id")
            if item_id in session["ItemBasket"]:

                # Ensure changes maintain
                session.modified = True
                session["ItemBasket"].pop(item_id)
    return redirect("/basket")

@perspectives.route("/receipt", methods=["GET", "POST"])
def receipt():
    if "ItemBasket" in session and len(session["ItemBasket"]) > 0:
        dt=str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        if request.method == "POST":
            session["Receipt"] = session["ItemBasket"].copy()
            total=calc_total("Receipt")
            
            # Is there enough stock for the quantity?
            enough_stock = check_item_stock("Receipt")[0]
            if enough_stock:
                # Update stock
                update_database(session["Receipt"])
                session.pop("ItemBasket", default=None)

                # add to order
                if total and dt:
                    if current_user.is_authenticated:
                        new_order = Order(user_id=current_user.id, order_json=session["Receipt"], datetime=dt, total=total)
                    else:
                        new_order = Order(user_id=None, order_json=session["Receipt"], datetime=dt, total=total)
                    database.session.add(new_order)
                    database.session.commit()
                    return render_template("receipt.html", user=current_user, TOTAL=total, datetime=dt, success=enough_stock, order_num=new_order.id)
            else:
                return render_template("receipt.html", user=current_user, TOTAL=total, datetime=dt, success=enough_stock)
    return redirect("/")

@perspectives.route("/<int:id>")
def item_page(id):
    item = Item.query.get(id)
    if item:
        return render_template("item.html", user=current_user, item=item)
    return redirect("/")

@perspectives.route("/orders")
def orders():
    if current_user.is_authenticated:
        content = Order.query.filter_by(user_id=current_user.id).all()
        if content:
            return render_template("orders.html", user=current_user, content=content)
    return redirect("/")
