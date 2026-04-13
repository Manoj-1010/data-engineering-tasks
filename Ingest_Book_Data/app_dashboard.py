import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page configuration for the dashboard
st.set_page_config(page_title="Book Analytics Dashboard", page_icon="📚", layout="wide")

@st.cache_data
def load_data():
    """Loads the transformed dataset. Cached to improve dashboard performance."""
    file_path = "new_data/transformed/books/books_transformed.csv"
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return None

def main():
    st.title("📚 Book Analytics Dashboard")
    st.markdown("Explore insights, pricing patterns, and top-rated picks from the scraped book dataset.")

    # Load the data
    df = load_data()

    if df is None:
        st.error("⚠️ 'books_transformed.csv' not found. Please run `transform_data.py` first to generate the data.")
        return
    elif df.empty:
        st.warning("⚠️ The dataset is empty. Please check your data ingestion pipeline.")
        return

    # --- THE SIDEBAR FILTERS ---
    st.sidebar.header("⚙️ Dashboard Controls")
    
    # Start with the full dataframe
    filtered_df = df.copy()

    # 1. Price Range Slider
    if 'price' in filtered_df.columns and not filtered_df.empty:
        min_price = float(filtered_df['price'].min())
        max_price = float(filtered_df['price'].max())
        
        # Only show the slider if we have a valid price range
        if min_price < max_price:
            price_range = st.sidebar.slider(
                "💰 Price Range (£):",
                min_value=min_price,
                max_value=max_price,
                value=(min_price, max_price) # Default to showing all prices
            )
            filtered_df = filtered_df[
                (filtered_df['price'] >= price_range[0]) & 
                (filtered_df['price'] <= price_range[1])
            ]

    # 2. Minimum Rating Filter
    if 'rating' in filtered_df.columns:
        min_rating = st.sidebar.slider(
            "⭐ Minimum Star Rating:", 
            min_value=1, max_value=5, value=1
        )
        filtered_df = filtered_df[filtered_df['rating'] >= min_rating]

    # 3. Availability Filter
    if 'availability' in filtered_df.columns:
        stock_filter = st.sidebar.radio(
            "📦 Stock Status:",
            options=["Show All", "In Stock Only", "Out of Stock Only"]
        )
        if stock_filter == "In Stock Only":
            filtered_df = filtered_df[filtered_df['availability'] == 1]
        elif stock_filter == "Out of Stock Only":
            filtered_df = filtered_df[filtered_df['availability'] == 0]

    # If filters return no data, show a friendly warning and stop rendering charts
    if filtered_df.empty:
        st.sidebar.warning("No books match your current filters!")
        st.warning("No books match the selected filters. Please adjust your criteria.")
        return

    st.markdown("---")

    # --- TOP ROW: High-Level Metrics ---
    st.header("Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    total_books = len(filtered_df)
    avg_price = filtered_df['price'].mean() if 'price' in filtered_df.columns else 0
    in_stock_pct = (filtered_df['availability'].mean() * 100) if 'availability' in filtered_df.columns else 0
    avg_rating = filtered_df['rating'].mean() if 'rating' in filtered_df.columns else 0

    col1.metric("Books Showing", f"{total_books:,}")
    col2.metric("Average Price", f"£{avg_price:.2f}")
    col3.metric("Average Rating", f"{avg_rating:.1f} / 5.0")
    col4.metric("In Stock", f"{in_stock_pct:.1f}%")

    st.markdown("---")

    # --- MIDDLE ROW: Charts for Price and Ratings ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("💰 Pricing Patterns")
        if 'price' in filtered_df.columns:
            fig_price = px.histogram(
                filtered_df, 
                x="price", 
                nbins=20, 
                title="Distribution of Book Prices",
                labels={"price": "Price (£)", "count": "Number of Books"},
                color_discrete_sequence=["#3366CC"]
            )
            fig_price.update_layout(bargap=0.1)
            st.plotly_chart(fig_price, width="stretch")

    with col_chart2:
        st.subheader("⭐ Rating Distributions")
        if 'rating' in filtered_df.columns:
            rating_counts = filtered_df['rating'].value_counts().sort_index()
            fig_rating = px.bar(
                x=rating_counts.index, 
                y=rating_counts.values, 
                title="Count of Books by Star Rating",
                labels={"x": "Star Rating", "y": "Number of Books"},
                color_discrete_sequence=["#FF9900"]
            )
            fig_rating.update_xaxes(tickvals=[1, 2, 3, 4, 5])
            st.plotly_chart(fig_rating, width="stretch")

    st.markdown("---")

    # --- BOTTOM ROW: Donut Chart and Top Books ---
    col_chart3, col_chart4 = st.columns(2)

    with col_chart3:
        st.subheader("🍩 Price Categories")
        st.markdown("Proportion of books in different price tiers.")
        
        if 'price' in filtered_df.columns:
            bins = [0, 20, 40, float('inf')]
            labels = ['Budget (< £20)', 'Mid-Range (£20-£40)', 'Premium (> £40)']
            
            tier_data = pd.cut(filtered_df['price'], bins=bins, labels=labels).value_counts().reset_index()
            tier_data.columns = ['Tier', 'Count']
            
            fig_donut = px.pie(
                tier_data, 
                values='Count', 
                names='Tier', 
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Teal
            )
            st.plotly_chart(fig_donut, width="stretch")

    with col_chart4:
        st.subheader("🏆 Top-Performing Books")
        st.markdown("Highest rated books based on your current filters.")
        
        if 'rating' in filtered_df.columns and 'price' in filtered_df.columns:
            # Sort by rating first, then price, to get the absolute best books at the top
            top_books = filtered_df.sort_values(by=['rating', 'price'], ascending=[False, False])
            
            desired_cols = ['title', 'price', 'availability', 'url']
            display_cols = [col for col in desired_cols if col in filtered_df.columns]
            
            st.dataframe(
                top_books[display_cols].head(10),
                column_config={
                    "title": "Book Title",
                    "price": st.column_config.NumberColumn("Price (£)", format="£%.2f"),
                    "availability": st.column_config.CheckboxColumn("In Stock?", default=False),
                    "url": st.column_config.LinkColumn("Store Link", display_text="View Book")
                },
                hide_index=True,
                width="stretch"
            )

if __name__ == "__main__":
    main()