# Vietnamese Finance & Policy News Aggregator

A modern web application that aggregates Vietnamese finance and policy news from multiple RSS feeds, similar to Techmeme. Features real-time updates, AI-powered summarization, and a clean, responsive interface.

## ✨ Features

- **Real-time RSS Aggregation**: Fetches news from 6 major Vietnamese financial news sources
- **Auto-refresh**: Updates every 10 minutes automatically
- **AI Summarization**: Optional OpenAI-powered one-sentence summaries in Vietnamese
- **Responsive Design**: Clean, modern UI that works on all devices
- **Source Filtering**: Only shows finance and policy-related articles
- **Live Updates**: Real-time refresh without page reload
- **Free Deployment**: Ready for Vercel, Render, or Netlify

## News Sources

- **VnExpress** - Kinh doanh section
- **Cafef** - Financial news
- **NDH** - Business news
- **Báo Đầu Tư** - Investment news
- **VietnamPlus** - Economic news
- **Thời Báo Tài Chính** - Financial times

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Local Installation

1. **Clone or download the project**

   ```bash
   git clone <repository-url>
   cd vietnamese-finance-news-aggerator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional)**

   ```bash
   cp env.example .env
   # Edit .env and add your OpenAI API key if you want AI summarization
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### With Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI API Key for AI summarization (optional)
OPENAI_API_KEY=your_openai_api_key_here

# Flask configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### RSS Feeds

You can modify the RSS feeds in `app.py`:

```python
RSS_FEEDS = [
    "https://vnexpress.net/rss/kinh-doanh.rss",
    "https://cafef.vn/home.rss",
    # Add more feeds here
]
```

## Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI**

   ```bash
   npm i -g vercel
   ```

2. **Deploy**

   ```bash
   vercel
   ```

3. **Set environment variables** in Vercel dashboard:
   - `OPENAI_API_KEY` (optional)

### Option 2: Render

1. **Connect your GitHub repository** to Render
2. **Create a new Web Service**
3. **Use these settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment: `Python 3`

### Option 3: Netlify

1. **Install Netlify CLI**

   ```bash
   npm i -g netlify-cli
   ```

2. **Build and deploy**
   ```bash
   netlify deploy --prod
   ```

### Option 4: Heroku

1. **Install Heroku CLI**
2. **Login and create app**

   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Deploy**
   ```bash
   git push heroku main
   ```

## 🤖 AI Summarization

The app includes optional AI-powered summarization using OpenAI's GPT models:

1. **Get an OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **Set the environment variable**:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
3. **Restart the application**

Without an API key, the app will use rule-based summarization.

## 📁 Project Structure

```
vietnamese-finance-news-aggerator/
├── app.py                 # Main Flask application
├── summarizer.py          # AI summarization module
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/               # Static assets (if any)
├── vercel.json          # Vercel deployment config
├── render.yaml          # Render deployment config
├── Procfile             # Heroku deployment config
├── env.example          # Environment variables example
└── README.md            # This file
```

## How It Works

1. **RSS Fetching**: The app fetches RSS feeds every 10 minutes in a background thread
2. **Content Filtering**: Only finance and policy-related articles are processed
3. **AI Summarization**: Each article gets a one-sentence summary in Vietnamese
4. **Real-time Updates**: The frontend automatically refreshes every minute
5. **Responsive Display**: Articles are displayed in a clean, Techmeme-like layout

## Customization

### Adding New RSS Feeds

Edit the `RSS_FEEDS` list in `app.py`:

```python
RSS_FEEDS = [
    "https://vnexpress.net/rss/kinh-doanh.rss",
    "https://your-new-feed.rss",
    # Add more feeds
]
```

### Modifying Update Frequency

Change the update interval in `app.py`:

```python
# Wait 10 minutes before next update
time.sleep(600)  # 600 seconds = 10 minutes
```

### Customizing the UI

Edit `templates/index.html` to modify the appearance and layout.

## 🐛 Troubleshooting

### Common Issues

1. **RSS feeds not loading**

   - Check your internet connection
   - Verify RSS feed URLs are accessible
   - Check the console for error messages

2. **AI summarization not working**

   - Verify your OpenAI API key is correct
   - Check if you have sufficient API credits
   - The app will fall back to rule-based summarization

3. **Deployment issues**
   - Ensure all dependencies are in `requirements.txt`
   - Check environment variables are set correctly
   - Verify the deployment platform supports Python/Flask

### Debug Mode

Run with debug mode for detailed error messages:

```bash
export FLASK_DEBUG=True
python app.py
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Built for the Vietnamese financial news community**
