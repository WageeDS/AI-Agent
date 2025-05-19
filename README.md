# 🍲 AI Recipe & Grocery List Assistant

A modern Streamlit web application that leverages Google's Gemini AI to generate personalized recipes and shopping lists based on ingredients you already have at home.

![Recipe Assistant Screenshot](assets/shakshuka.jpg)

## ✨ Features

- **AI-Powered Recipe Generation**: Create delicious meals using ingredients you already have
- **Dietary Preference Support**: Customize recipes for Vegetarian, Vegan, Gluten-Free, Keto, and more
- **Cuisine Selection**: Choose from various cuisine styles (Mediterranean, Italian, Mexican, etc.)
- **Smart Shopping Lists**: Automatically generate shopping lists for missing ingredients
- **Recipe History**: Save and access your previously generated recipes
- **Beautiful UI**: Enjoy a clean, modern interface with recipe cards and interactive elements
- **Export Functionality**: Download shopping lists as text files

## 🚀 Setup & Installation

1. Clone this repository
   ```
   git clone <repository-url>
   cd ai-recipe-assistant
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Gemini API key
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. Create an assets folder for images
   ```
   mkdir -p assets
   ```

5. Add recipe images to the assets folder (optional)

## 🔧 How to Run

```
streamlit run app.py
```

Visit `http://localhost:8501` in your web browser to use the application.

## 💡 How to Use

1. Enter ingredients you have available (comma-separated)
2. Select dietary preferences and cuisine style (optional)
3. Click "Generate Recipe" 
4. View your personalized recipe and shopping list
5. Rate recipes and save favorites
6. Access your recipe history anytime

## 🔍 Project Structure

```
ai-recipe-assistant/
├── app.py                  # Main Streamlit application
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── gemini_client.py    # Google Gemini API integration
│   └── recipe_parser.py    # Recipe parsing functions
├── assets/                 # Image assets
├── history/                # Recipe history storage
├── .env                    # API keys (not in version control)
└── requirements.txt        # Project dependencies
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI**: Google's Gemini API
- **Backend**: Python
- **Data Storage**: JSON

## 👩‍💻 Developed By

Wageesha Sammani
## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.