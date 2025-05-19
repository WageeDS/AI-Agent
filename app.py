import streamlit as st
import json
from datetime import datetime
import os
import base64
from utils.gemini_client import generate_recipe
from utils.recipe_parser import parse_recipe, extract_grocery_list

# IMPORTANT: set_page_config must be the FIRST Streamlit command
st.set_page_config(
    page_title="AI Recipe & Grocery List Assistant",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main {
        background-color: #f9f7f0;
        padding: 20px;
    }
    .stButton>button {
        background-color: #FF6B6B !important;
        color: white !important;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        border: none !important;
    }
    h1 {
        color: #2E8B57;
        border-bottom: 2px solid #FF6B6B;
        padding-bottom: 10px;
    }
    h2 {
        color: #5F9EA0;
        margin-top: 20px;
    }
    .recipe-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .shopping-card {
        background-color: #f0fff4;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .ingredient-item {
        margin-bottom: 8px;
        padding-left: 20px;
        position: relative;
    }
    .ingredient-item:before {
        content: "•";
        position: absolute;
        left: 0;
        color: #FF6B6B;
        font-weight: bold;
    }
    .instruction-item {
        margin-bottom: 12px;
        padding-left: 30px;
        position: relative;
    }
    .instruction-number {
        position: absolute;
        left: 0;
        background-color: #FF6B6B;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        text-align: center;
        line-height: 24px;
        font-weight: bold;
    }
    .header-image {
        width: 100%;  # Change from 100% to any percentage you want
        height: 20%; # Set a fixed height
        max-width: 800px; # Add a maximum width
        margin: 0 auto; # Center the image
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        display: block; # Helps with centering
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        font-weight: 600;
        white-space: pre-wrap;
        background-color: grey;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6B6B !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def save_recipe_to_history(recipe, ingredients, dietary_preferences, grocery_list):
    """Save the recipe to history JSON file"""
    history_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": recipe.get('title', 'Untitled Recipe'),
        "ingredients_used": ingredients,
        "dietary_preferences": dietary_preferences,
        "recipe": recipe,
        "grocery_list": grocery_list
    }
    
    # Create history directory if it doesn't exist
    os.makedirs('history', exist_ok=True)
    
    # Save to JSON file
    history_file = 'history/recipe_history.json'
    try:
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError:
                    history = []
        else:
            history = []
        
        # Add new entry
        history.append(history_entry)
        
        # Save back to file
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        st.error(f"Error saving recipe to history: {str(e)}")

def display_recipe_history():
    """Display recipe history from JSON file with nicer formatting"""
    history_file = 'history/recipe_history.json'
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                try:
                    history = json.load(f)
                    
                    if not history:
                        st.info("No recipe history available.")
                        return
                    
                    # Display each recipe in history (newest first)
                    for entry in reversed(history):
                        with st.expander(f"🍽️ {entry['title']} - {entry['timestamp']}"):
                            st.markdown(f"""
                            **Ingredients used:** {entry['ingredients_used']}  
                            **Dietary preferences:** {entry['dietary_preferences']}
                            """)
                            
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                # Display recipe details
                                if st.button("📖 Show Full Recipe", key=f"show_{entry['timestamp']}"):
                                    st.session_state.selected_recipe = entry
                                    st.experimental_rerun()
                            with col2:
                                # Add delete button
                                if st.button("🗑️", key=f"delete_{entry['timestamp']}"):
                                    # Would implement deletion functionality here
                                    st.info("Delete functionality would remove this recipe")
                    
                except json.JSONDecodeError:
                    st.info("No recipe history available.")
        else:
            st.info("No recipe history available.")
    except Exception as e:
        st.error(f"Error loading recipe history: {str(e)}")

def add_header_image(image_path=None):
    """Display header image from file or URL"""
    # Default to the local shakshuka image
    if not image_path:
        image_path = "assets/shakshuka.jpg"
    
    # Try to load local image first
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            img_src = f"data:image/jpeg;base64,{img_data}"
            st.markdown(f"""
            <img src="{img_src}" class="header-image" alt="Delicious Food Image">
            """, unsafe_allow_html=True)
    else:
        # Fallback to displaying a placeholder or the URL directly
        st.image("https://images.unsplash.com/photo-1588957659793-59407442d82b", 
                 caption="Delicious Food", use_column_width=True)

# UI code starts here
# Title and description
st.title("🍲 AI Recipe & Grocery List Assistant")
add_header_image()  # Add the function call to display the shakshuka image
st.write("Enter your ingredients and dietary preferences to get a personalized recipe!")

# Create tabs
tab1, tab2, tab3 = st.tabs(["💡 Generate Recipe", "📚 Recipe History", "ℹ️ About"])

with tab1:
    # User input section
    st.subheader("What's in your kitchen?")
    ingredients = st.text_area("Enter ingredients (comma-separated):", 
                            help="Example: eggs, tomatoes, onions, garlic, feta cheese, cilantro",
                            placeholder="eggs, tomatoes, onion, garlic, feta cheese")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dietary Preferences")
        dietary_preferences = st.selectbox("Select:", 
                                    ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Low-Carb"])
    with col2:
        st.subheader("Cuisine Style (Optional)")
        cuisine = st.selectbox("Select:", 
                    ["Any", "Mediterranean", "Italian", "Mexican", "Asian", "French", "Indian"])
    
    # Recipe generation
    if st.button("🧙‍♂️ Generate Recipe", use_container_width=True, type="primary"):
        if not ingredients:
            st.error("Please enter at least one ingredient.")
        else:
            with st.status("👨‍🍳 Your AI chef is cooking up something delicious...") as status:
                try:
                    status.update(label="Analyzing your ingredients...")
                    # Include cuisine in the recipe generation if specified
                    full_preferences = f"{dietary_preferences}, {cuisine} cuisine" if cuisine != "Any" else dietary_preferences
                    recipe_text = generate_recipe(ingredients, full_preferences)
                    
                    status.update(label="Creating your recipe...")
                    recipe = parse_recipe(recipe_text)
                    
                    status.update(label="Preparing shopping list...")
                    grocery_list = extract_grocery_list(recipe_text)
                    
                    status.update(label="✅ Recipe ready!", state="complete")
                    
                    # Display recipe in a nice format with cards
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h1>🍳 {recipe['title']}</h1>
                        <h2>Ingredients</h2>
                        <div>
                    """, unsafe_allow_html=True)
                    
                    for ingredient in recipe.get('ingredients', []):
                        st.markdown(f'<div class="ingredient-item">{ingredient}</div>', unsafe_allow_html=True)
                    
                    st.markdown("<h2>Instructions</h2>", unsafe_allow_html=True)
                    
                    for i, step in enumerate(recipe.get('instructions', [])):
                        st.markdown(f"""
                        <div class="instruction-item">
                            <span class="instruction-number">{i+1}</span>
                            {step}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Display shopping list with checkboxes
                    st.markdown("""
                    <div class="shopping-card">
                        <h2>🛒 Shopping List</h2>
                    """, unsafe_allow_html=True)
                    
                    for i, item in enumerate(grocery_list):
                        key = f"item_{i}_{datetime.now().strftime('%H%M%S')}"
                        is_checked = st.checkbox(item, key=key)
                    
                    if grocery_list:
                        # Add Print Shopping List button
                        shopping_list_text = "\n".join([f"- {item}" for item in grocery_list])
                        st.download_button(
                            label="📄 Download Shopping List",
                            data=shopping_list_text,
                            file_name="shopping_list.txt",
                            mime="text/plain"
                        )
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add rating and save features
                    with st.expander("Rate & Save This Recipe"):
                        col1, col2 = st.columns(2)
                        with col1:
                            rating = st.slider("How would you rate this recipe?", 1, 5, 3)
                        with col2:
                            st.button("❤️ Save to Favorites", type="secondary")
                    
                    # Save recipe to history
                    save_recipe_to_history(recipe, ingredients, dietary_preferences, grocery_list)
                    
                except Exception as e:
                    status.update(label="❌ Recipe generation failed", state="error")
                    st.error(f"Error generating recipe: {str(e)}")

with tab2:
    st.subheader("Your Recipe Collection")
    st.write("View your previously generated recipes")
    if st.button("📂 Load Recipe History", use_container_width=True):
        display_recipe_history()
    
    # Display selected recipe from history if any
    if 'selected_recipe' in st.session_state:
        entry = st.session_state.selected_recipe
        
        st.markdown(f"""
        <div class="recipe-card">
            <h1>🍳 {entry['recipe']['title']}</h1>
            <p><em>Created on: {entry['timestamp']}</em></p>
            <h2>Ingredients</h2>
        """, unsafe_allow_html=True)
        
        for ingredient in entry['recipe'].get('ingredients', []):
            st.markdown(f'<div class="ingredient-item">{ingredient}</div>', unsafe_allow_html=True)
        
        st.markdown("<h2>Instructions</h2>", unsafe_allow_html=True)
        
        for i, step in enumerate(entry['recipe'].get('instructions', [])):
            st.markdown(f"""
            <div class="instruction-item">
                <span class="instruction-number">{i+1}</span>
                {step}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Shopping list for history item
        st.markdown("""
        <div class="shopping-card">
            <h2>🛒 Shopping List</h2>
        """, unsafe_allow_html=True)
        
        for item in entry['grocery_list']:
            st.markdown(f'<div class="ingredient-item">{item}</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.subheader("About This App")
    st.markdown("""
    ### 🍲 AI Recipe & Grocery List Assistant
    
    This AI-powered Recipe Assistant helps you:
    
    * **Create delicious meals** with ingredients you already have
    * **Discover new recipe ideas** based on your dietary preferences
    * **Generate shopping lists** for missing ingredients
    * **Save your favorite recipes** for later
    
    #### How It Works
    1. Enter the ingredients you have available
    2. Select any dietary preferences
    3. Click "Generate Recipe" and let AI do the rest!
    
    #### Technologies Used
    - **Frontend**: Streamlit
    - **AI**: Google's Gemini AI
    - **Backend**: Python
    
    #### Developed By
    Wageesha Sammani
    
    **Note**: The app uses Google's Gemini API to generate recipes and requires an internet connection.
    """)
    
    # Show example image
    add_header_image()  # Add the shakshuka image again in the About tab