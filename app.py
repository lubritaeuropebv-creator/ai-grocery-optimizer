import streamlit as st
import tempfile
from core.recipe_ai import generate_recipe
from core.ingredients import scale_ingredients
from core.pdf_parser import parse_flyer
from core.optimizer import best_carts

st.set_page_config(page_title="AI Grocery Optimizer", layout="wide")
st.title("🛒 AI Grocery Optimizer")

persons = st.number_input("Number of persons", 1, 20, 2)
dish = st.text_input("What do you want to cook?")

uploaded = st.file_uploader(
    "Upload shop flyers (PDF)",
    type="pdf",
    accept_multiple_files=True
)

if st.button("Optimize cart") and dish and uploaded:
    with st.spinner("Generating recipe & optimizing prices..."):
        recipe = generate_recipe(dish, persons)
        ingredients = scale_ingredients(recipe, persons)

        shop_products = {}

        for file in uploaded:
            shop = file.name.replace(".pdf", "")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            shop_products[shop] = parse_flyer(tmp_path, shop)

        results = best_carts(ingredients, shop_products)

    for k, res in results.items():
        if res:
            total, cart, shops = res
            st.subheader(f"Best {k.replace('_', ' ')} option")
            st.write(f"**Shops:** {', '.join(shops)}")
            st.success(f"Total: €{total:.2f}")
            st.table(cart)

