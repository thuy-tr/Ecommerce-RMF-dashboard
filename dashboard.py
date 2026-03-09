import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide", page_icon="🛒")

@st.cache_data
def load_data():
    df = pd.read_excel("Online Retail.xlsx")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    
    # Calculate return rate before cleaning
    total_invoices = df["InvoiceNo"].nunique()
    cancelled_invoices = df["InvoiceNo"].astype(str).str.startswith("C", na=False).sum()
    return_rate = cancelled_invoices / total_invoices if total_invoices > 0 else 0
    
    # Cleaning
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean.dropna(subset=["CustomerID"])
    df_clean = df_clean[~df_clean["InvoiceNo"].astype(str).str.startswith("C", na=False)]
    df_clean = df_clean[(df_clean["Quantity"] > 0) & (df_clean["UnitPrice"] > 0)]
    df_clean["Revenue"] = df_clean["Quantity"] * df_clean["UnitPrice"]
    
    def get_category(desc):
        if pd.isna(desc):
            return "Miscellaneous"
        d = str(desc).upper()
        if "POSTAGE" in d or d.strip() == "MANUAL":
            return "Postage & fees"
        if "JUMBO BAG" in d or ("BAG" in d and "JUMBO" in d):
            return "Bags and packaging"
        if any(x in d for x in [" BAG ", "BAG ", " BAG", "BAGS ", " TOTE ", "PACKAGING", "CELLOPHANE", "WRAP ", " GIFT WRAP", "RIBBON REEL", "RIBBON REELS", "ROUND SNACK BAG", "LUNCH BAG", "BOTTLE BAG", "CARRIER BAG", "SHOPPING BAG", "PAPER BAG", "PLASTIC BAG", "METAL BAG"]):
            return "Bags and packaging"
        if "BAG" in d:
            return "Bags and packaging"
        if any(x in d for x in ["JAM ", " JAM", "JAM JAR", "MARMALADE", "HONEY ", "CHOCOLATE", "BISCUIT", "COOKIE", "SWEET", "CANDY", "TEA COSY", "TEA COZIE", "COFFEE ", " SUGAR ", "MILK BOTTLE", "CREAM JUG", "RECIPE BOOK", "COOKBOOK"]):
            return "Food and beverage"
        if "JAM" in d:
            return "Food and beverage"
        if any(x in d for x in ["CAKE TIN", "CAKESTAND", "CAKE STAND", "CAKE CASE", "CAKE CASES", "CAKE MOULD", "CAKE PLATE", "JELLY MOULD", "PANTRY JELLY", "BAKING ", "OVEN ", "KITCHEN ", "CUTLERY", "TEAPOT", "TEACUP", " MUG ", " MUGS", "EGG CUP", "EGG RING", "PIE FUNNEL", "BREAD BIN", "BREAD BASKET", "SCALES ", "KITCHEN SCALE", "COASTER", "COASTERS", "NAPKIN RING", "POT HOLDER", "OVEN GLOVE", "APRON ", "TEA TOWEL", "TOWEL ", "JUG ", " BOWL", "BOWLS ", "PLATE ", " PLATES", "CUP AND SAUCER", "TRIVET", "STORAGE JAR", "JAR ", " JARS", "BOTTLE ", " BOTTLES", "FLASK", "TRAY ", " TRAYS", "STORAGE BOX", "LUNCH BOX", "TIN ", " TINS"]):
            return "Kitchenware"
        if "JAR" in d or "STORAGE" in d:
            return "Kitchenware"
        if "CAKE" in d:
            return "Kitchenware"
        if any(x in d for x in ["PEN ", " PENS", "PENCIL", "NOTEBOOK", "NOTEPAD", "NOTE PAD", "ENVELOPE", "LABEL ", " LABELS", "STICKER ", "RULER ", "ERASER", "HIGHLIGHTER", "CLIP ", " PAPERCLIP", "FILE ", " FOLDER", "DESK ", "ORGANISER", "ORGANIZER", "DIARY ", "CALENDAR", "ADVENT CALENDAR", "BOOKMARK", "MAGNET ", " LETTER ", "POSTCARD", "CARD HOLDER", "TISSUE BOX", "TISSUES ", " TISSUE "]):
            return "Stationery"
        if "TISSUE" in d:
            return "Stationery"
        if any(x in d for x in ["BUNTING", "BALLOON", "POPCORN ", "PARTY ", "CONFETTI", "CELEBRATION", "PAPER CHAIN", "TABLE CLOTH", "PAPER PLATE", "PAPER CUP", "CHRISTMAS CRACKER", "CRACKER ", " FAN "]):
            return "Party supplies"
        if "HOLDER" in d and any(x in d for x in ["CANDLE", "T-LIGHT", "NIGHT LIGHT", "TEA LIGHT", "POPCORN"]):
            return "Party supplies"
        if "FAN" in d and "PAPER" in d:
            return "Party supplies"
        if any(x in d for x in ["PAINT SET", "PAINT BRUSH", "PAINT ", "CRAFT ", "PAPER CRAFT", "GLITTER", "GLUE ", " SEQUIN", "SEQUINS", "RIBBON ", " RIBBONS", "COLOUR ", "COLOR ", "STAMP ", " INK PAD", "SEWING ", "KNITTING", "SCRAPBOOK", "FELTCRAFT", "CARD KIT", "STICKER SHEET", "DECOUPAGE"]):
            return "Craft supplies"
        if "PAINT" in d:
            return "Craft supplies"
        if "SET" in d and any(x in d for x in ["CRAFT", "PAINT", "RIBBON", "COLOUR", "COLOURED", "SEWING", "STAMP", "PAPER", "CARD "]):
            return "Craft supplies"
        if any(x in d for x in ["PICNIC", "GARDEN ", " PLANTER", "PLANTERS", "FLOWER POT", "FLOWERPOT", "SEED ", " BULB ", "BULBS ", "LAWN ", "SHED ", "GREENHOUSE", "OUTDOOR", "PATIO", "BIRD BATH", "FAIRY ", "GNOME ", "FROG ", "WOODEN SKIP", "BASKET "]):
            return "Garden and outdoor"
        if "BASKET" in d or "PICNIC" in d:
            return "Garden and outdoor"
        if any(x in d for x in ["T-LIGHT", "NIGHT LIGHT", "LANTERN", "CHILLI LIGHT", "LIGHTS ", " LIGHTS", "DECORATIVE LIGHT", "CANDLE ", "CANDLES", "LAMP ", " LAMPS"]):
            return "Home decor"
        if "LIGHT" in d:
            return "Home decor"
        if any(x in d for x in ["ORNAMENT", "FIGURINE", " BIRD ", "BIRDS ", " RABBIT", "RABBITS", "DOLL ", "HEART ", "HEARTS ", "FAIRY", "GNOME", "SCULPTURE", "DECORATION", "TRINKET BOX", "VASE ", " VASES", "MIRROR ", "CLOCK ", "CLOCKS", "PICTURE ", "PHOTO FRAME", "WALL ART", "SIGN ", "CHALK BOARD", "BLACKBOARD", "DOOR STOP", "HANGING ", "COAT HANGER", "BLANKET ", "CUSHION ", "CURTAIN", "LAVENDER", "POTPOURRI", "BATHROOM SET", "HANGER ", "DOLL "]):
            return "Home decor"
        if "FRAME" in d or "BOARD" in d:
            return "Home decor"
        if "DOORMAT" in d or " DOOR MAT" in d:
            return "Home decor"
        if " MAT " in d or d.endswith(" MAT"):
            return "Home decor"
        if "BUNTING" in d:
            return "Home decor"
        if "ORNAMENT" in d or "BIRD" in d or "RABBIT" in d:
            return "Home decor"
        if any(x in d for x in ["PURSE ", " WALLET", "KEY RING", "KEYRING", "KEY FOB", "RING BINDER", "HAND WARMER", "UMBRELLA", "GLASSES CASE", "CARD WALLET"]):
            return "Miscellaneous"
        if "PURSE" in d or "RING " in d:
            return "Miscellaneous"
        if any(x in d for x in ["HARMONICA", "MUSIC BOX", "TOY ", " TOYS", "DOLL ", "TEDDY", "PLUSH", "PUZZLE ", "GAME "]):
            return "Miscellaneous"
        if "MUSIC" in d:
            return "Miscellaneous"
        if "SET" in d:
            return "Craft supplies"
        return "Miscellaneous"

    df_clean["Category"] = df_clean["Description"].apply(get_category)
    return df_clean, return_rate

@st.cache_data
def calculate_rfm(df_clean):
    reference_date = df_clean["InvoiceDate"].max() + pd.Timedelta(days=1)
    
    rfm = df_clean.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum"),
        FirstPurchase=("InvoiceDate", "min"),
        LastPurchase=("InvoiceDate", "max")
    ).reset_index()
    
    # Get most frequent country for each customer
    customer_country = df_clean.groupby("CustomerID")["Country"].agg(lambda x: x.mode()[0] if not x.empty else "Unknown").reset_index()
    rfm = rfm.merge(customer_country, on="CustomerID", how="left")
    
    rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method="first"), q=5, labels=[5, 4, 3, 2, 1], duplicates="drop").astype(int)
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop").astype(int)
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5], duplicates="drop").astype(int)
    
    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    rfm["RFM_Sum"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]
    
    def rfm_segment(row):
        r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]
        if r >= 4 and (f + m) >= 8:
            return "Champions"
        if r >= 3 and (f + m) >= 6:
            return "Loyal"
        if r >= 3 and (f + m) <= 4:
            return "Potential"
        if r <= 2 and (f + m) >= 6:
            return "At Risk"
        if r <= 2 and (f + m) <= 4:
            return "Lost"
        return "Other"

    rfm["Segment"] = rfm.apply(rfm_segment, axis=1)
    return rfm

# Load data
with st.spinner("Loading and processing data..."):
    df_clean, return_rate = load_data()
    rfm = calculate_rfm(df_clean)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Business Overview", "Customer RFM Analysis"])

if page == "Business Overview":
    st.title("📈 Business Overview")
    
    # Top-level metrics
    total_revenue = df_clean["Revenue"].sum()
    total_customers = df_clean["CustomerID"].nunique()
    total_orders = df_clean["InvoiceNo"].nunique()
    aov = total_revenue / total_orders if total_orders > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"£{total_revenue:,.2f}")
    col2.metric("Total Customers", f"{total_customers:,}")
    col3.metric("Average Order Value (AOV)", f"£{aov:,.2f}")
    col4.metric("Return Rate", f"{return_rate*100:.2f}%")
    
    st.markdown("---")
    
    # Revenue Trends
    st.subheader("Revenue Trends")
    df_clean["YearMonth"] = df_clean["InvoiceDate"].dt.to_period("M").astype(str)
    monthly_rev = df_clean.groupby("YearMonth")["Revenue"].sum().reset_index()
    fig_rev = px.line(monthly_rev, x="YearMonth", y="Revenue", markers=True, title="Monthly Revenue", labels={"Revenue": "Revenue (£)", "YearMonth": "Month"})
    fig_rev.update_layout(xaxis_title="Month", yaxis_title="Revenue (£)")
    st.plotly_chart(fig_rev, use_container_width=True)
    
    st.markdown("---")
    
    # Geographic analysis
    st.subheader("🌍 Geographic analysis")
    col_geo_bar, col_geo_pie = st.columns(2)
    
    country_rev = df_clean.groupby("Country")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False).head(10)
    
    with col_geo_bar:
        fig_country = px.bar(country_rev, x="Revenue", y="Country", orientation='h', title="Top 10 Countries by Revenue", labels={"Revenue": "Revenue (£)"})
        fig_country.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_country, use_container_width=True)
        
    with col_geo_pie:
        fig_country_pie = px.pie(country_rev, values="Revenue", names="Country", title="Revenue Distribution - Top 10 Countries")
        fig_country_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_country_pie, use_container_width=True)

    st.markdown("---")
    
    # Product Performance
    st.subheader("🛍️ Product Performance")
    col_prod_bar, col_cat_bar = st.columns(2)
    
    with col_prod_bar:
        prod_rev = df_clean.groupby("Description")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False).head(10)
        fig_prod = px.bar(prod_rev, x="Revenue", y="Description", orientation='h', title="Top 10 Products by Revenue", labels={"Revenue": "Revenue (£)"})
        fig_prod.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_prod, use_container_width=True)
        
    with col_cat_bar:
        cat_rev = df_clean.groupby("Category")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
        fig_cat = px.bar(cat_rev, x="Revenue", y="Category", orientation='h', title="Top Categories by Revenue", labels={"Revenue": "Revenue (£)"})
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)

elif page == "Customer RFM Analysis":
    st.title("🎯 Customer RFM Analysis")
    
    # Recommendations Dictionary
    recommendations = {
        "Champions": {
            "priority": "Critical",
            "action": "VIP program, exclusives, referral incentives",
            "impact": "Retain 67% revenue; grow share of wallet",
            "desc": "Protect and reward: VIP/loyalty program, early access or exclusive offers, referral incentives. Aim to retain and increase share of wallet.",
            "color": "#2ca02c" # green
        },
        "Loyal": {
            "priority": "High",
            "action": "Engagement, cross-sell, upsell",
            "impact": "Prevent slip to At Risk; sustain ~15% revenue",
            "desc": "Keep engaged with relevant communication and offers so they do not slip to At Risk. Consider light cross-sell/upsell.",
            "color": "#1f77b4" # blue
        },
        "Potential": {
            "priority": "Medium",
            "action": "Recommendations, second-purchase offer, bundles",
            "impact": "Convert to Loyal; grow from 1.8% revenue",
            "desc": "Nurture: product recommendations, 'second purchase' or bundle offers, simple loyalty perks to increase frequency and spend.",
            "color": "#ff7f0e" # orange
        },
        "At Risk": {
            "priority": "High",
            "action": "Win-back emails, limited-time offer, 'we miss you'",
            "impact": "Recover ~11% revenue at risk of churn",
            "desc": "Prioritize reactivation: personalized win-back emails, limited-time discount or free shipping, 'we miss you' messaging. Track response and ROI.",
            "color": "#d62728" # red
        },
        "Lost": {
            "priority": "Low",
            "action": "Low-cost win-back or accept churn",
            "impact": "Avoid wasted spend; optional recovery of 2.75%",
            "desc": "Either low-cost reactivation (e.g. one-off win-back campaign) or accept churn and avoid costly mass marketing. Use budget where ROI is higher.",
            "color": "#7f7f7f" # gray
        },
        "Other": {
            "priority": "Medium",
            "action": "Refine rules, segment-specific campaigns",
            "impact": "Reclassify or unlock incremental value",
            "desc": "Review behavior (e.g. by RFM_Score or country) to refine rules or target with segment-specific campaigns.",
            "color": "#9467bd" # purple
        }
    }
    
    # Customer Selector
    customer_list = rfm["CustomerID"].astype(int).astype(str).tolist()
    selected_customer_str = st.selectbox("Search for a Customer ID", customer_list)
    
    if selected_customer_str:
        selected_customer = float(selected_customer_str)
        cust_data = rfm[rfm["CustomerID"] == selected_customer].iloc[0]
        segment = cust_data["Segment"]
        rec = recommendations.get(segment, recommendations["Other"])
        
        # Segment Banner (fixed text color for visibility)
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #f0f2f6; border-left: 10px solid {rec['color']}; color: #333333;">
            <h2 style="margin-top: 0; color: #333333;">Segment: {segment}</h2>
            <p style="color: #333333; margin-bottom: 5px;"><strong>Priority:</strong> {rec['priority']}</p>
            <p style="color: #333333; margin-bottom: 5px;"><strong>Recommended Action:</strong> {rec['action']}</p>
            <p style="color: #333333; margin-bottom: 5px;"><strong>Expected Impact:</strong> {rec['impact']}</p>
            <p style="color: #333333; margin-top: 10px;"><em>{rec['desc']}</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Customer Profile & Financials
        st.subheader("👤 Customer Profile & Financial Summary")
        
        # Calculate AOV for this customer
        cust_aov = cust_data["Monetary"] / cust_data["Frequency"] if cust_data["Frequency"] > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Location", cust_data["Country"])
        col2.metric("Total Revenue", f"£{cust_data['Monetary']:,.2f}")
        col3.metric("Transactions", f"{cust_data['Frequency']}")
        col4.metric("AOV", f"£{cust_aov:,.2f}")
        
        st.write(f"**First Purchase:** {cust_data['FirstPurchase'].strftime('%Y-%m-%d')} | **Last Purchase:** {cust_data['LastPurchase'].strftime('%Y-%m-%d')}")
        
        st.markdown("---")
        
        # RFM Scores
        st.subheader("📊 RFM Scores")
        col_r, col_f, col_m = st.columns(3)
        
        with col_r:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e6e6e6;">
                <h4 style="color: #555; margin-bottom: 5px;">Recency Score</h4>
                <h1 style="color: #1f77b4; margin: 0;">{cust_data['R_Score']} <span style="font-size: 18px; color: #aaa;">/ 5</span></h1>
                <p style="color: #777; margin-top: 5px; font-size: 14px;"><strong>{cust_data['Recency']} days</strong> since last purchase</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_f:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e6e6e6;">
                <h4 style="color: #555; margin-bottom: 5px;">Frequency Score</h4>
                <h1 style="color: #ff7f0e; margin: 0;">{cust_data['F_Score']} <span style="font-size: 18px; color: #aaa;">/ 5</span></h1>
                <p style="color: #777; margin-top: 5px; font-size: 14px;"><strong>{cust_data['Frequency']}</strong> total orders</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col_m:
            st.markdown(f"""
            <div style="text-align: center; padding: 15px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border: 1px solid #e6e6e6;">
                <h4 style="color: #555; margin-bottom: 5px;">Monetary Score</h4>
                <h1 style="color: #2ca02c; margin: 0;">{cust_data['M_Score']} <span style="font-size: 18px; color: #aaa;">/ 5</span></h1>
                <p style="color: #777; margin-top: 5px; font-size: 14px;"><strong>£{cust_data['Monetary']:,.2f}</strong> total spent</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Customer specific product data
        st.subheader("🛒 Purchase History")
        cust_orders = df_clean[df_clean["CustomerID"] == selected_customer]
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            top_products = cust_orders.groupby("Description")["Quantity"].sum().reset_index().sort_values("Quantity", ascending=False).head(10)
            if not top_products.empty:
                fig_prod = px.bar(top_products, x="Quantity", y="Description", orientation='h', title="Top 10 Products Purchased")
                fig_prod.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_prod, use_container_width=True)
            else:
                st.info("No product data available.")
                
        with col_chart2:
            cat_dist = cust_orders.groupby("Category")["Revenue"].sum().reset_index()
            if not cat_dist.empty:
                fig_cat_pie = px.pie(cat_dist, values="Revenue", names="Category", hole=0.4, title="Revenue by Product Category")
                fig_cat_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_cat_pie, use_container_width=True)
            else:
                st.info("No category data available.")
                
        st.markdown("---")
        
        # Purchase Timeline
        st.subheader("📈 Purchase Timeline")
        timeline_df = cust_orders.groupby(cust_orders["InvoiceDate"].dt.date)["Revenue"].sum().reset_index()
        if not timeline_df.empty:
            fig_timeline = px.line(timeline_df, x="InvoiceDate", y="Revenue", markers=True, title="Revenue Over Time", labels={"Revenue": "Revenue (£)", "InvoiceDate": "Date"})
            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No timeline data available.")
