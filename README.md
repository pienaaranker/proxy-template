# 🛡️ Secure API Proxy Example

This repository demonstrates a secure way to interact with AI APIs (like Google's Gemini) by implementing a proxy server. It serves as an educational example of why you should never expose API keys directly in your frontend code.

## 🤔 Why Use a Proxy?

### The Wrong Way (Dangerous! ⚠️)
```javascript
// DON'T DO THIS in your frontend code!
const apiKey = "your-api-key-here";
fetch("https://api.example.com/v1/generate", {
  headers: { Authorization: `Bearer ${apiKey}` }
});
```

When you include API keys directly in your frontend code:
- 🔓 Your API key is visible to anyone who inspects your website's source code
- 💸 Bad actors can steal and abuse your API key, potentially leading to huge bills
- 🚫 You have limited control over API usage and rate limiting

### The Right Way (Using this Proxy ✅)
```javascript
// Safe frontend code
fetch("https://your-proxy.com/api/gemini", {
  method: "POST",
  body: JSON.stringify({ prompt: "Hello, AI!" })
});
```

Benefits of using this proxy:
- 🔒 API keys are securely stored on the server
- 🔍 Request validation and sanitization
- 📊 Rate limiting capabilities
- 🚦 Usage monitoring and logging
- 🛠️ Ability to add middleware and custom logic

## 🚀 Features

- FastAPI-based proxy server
- CORS configuration for security
- Error handling and logging
- Environment variable management
- Ready for deployment

## 🛠️ Setup

1. Clone this repository
2. Create a `.env` file with your API keys:
   ```
   GEMINI_API_KEY=your-key-here
   GEMINI_MODEL=gemini-2.5-flash
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure allowed origins:
   - Open `api/index.py`
   - Locate the CORS middleware configuration
   - Add your frontend domain to the `allow_origins` list:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "https://your-frontend-domain.com",  # Add your domain here
           "http://localhost:3000",  # For local development
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
5. Run the server:
   ```bash
   uvicorn api.index:app --reload
   ```

## 🔐 Security Best Practices Demonstrated

1. API keys stored in environment variables
2. Configured CORS to restrict access to specific domains
3. Error handling that doesn't leak sensitive information
4. Request validation using Pydantic models
5. Comprehensive logging for monitoring

## 🌐 API Endpoints

- `GET /` - Health check endpoint
- `POST /api/gemini` - Proxy endpoint for Gemini AI API

## ⚠️ Important Note

This is a demonstration project. For production use, consider adding:
- Authentication
- Rate limiting
- Request validation
- Monitoring and analytics
- Additional security measures

### CORS Security ⚠️
The CORS configuration is crucial for security:
- Only add domains you trust to `allow_origins`
- Avoid using `["*"]` in production as it allows any site to access your API
- Consider using environment variables for different origins in different environments
- Remember to update the origins when deploying to production

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API Documentation](https://ai.google.dev/)
- [Web Security Best Practices](https://owasp.org/www-project-top-ten/)
- [CORS Security Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

## 🤝 Contributing

Feel free to contribute to this project by opening issues or submitting pull requests. Let's make the web more secure together!

## 📜 License

MIT License - feel free to use this code to learn and build secure applications! 