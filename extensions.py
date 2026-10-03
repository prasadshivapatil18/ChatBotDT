from flask_socketio import SocketIO
from flask_login import LoginManager
from ai.chatbot import AIChatbot

socketio = SocketIO(cors_allowed_origins="*", async_mode='threading')
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# Global AI Chatbot instance
ai_bot = AIChatbot()
