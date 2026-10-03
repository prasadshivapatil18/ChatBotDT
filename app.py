import os
from flask import Flask, render_template
from flask_socketio import join_room, leave_room, emit
from config import config
from database.database import db, init_db
from extensions import socketio, login_manager, ai_bot
from models.user import User
from models.knowledge_base import KnowledgeBase
from routes import auth_bp, customer_bp, chatbot_bp, agent_bp, admin_bp, analytics_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    # Initialize extensions
    init_db(app)
    socketio.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)

    # Prime AI Knowledge Base Retriever
    with app.app_context():
        try:
            faqs = KnowledgeBase.query.all()
            if faqs:
                ai_bot.refresh_kb(faqs)
        except Exception as e:
            app.logger.warning(f"Knowledge Base index initialization deferred: {e}")

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error_title="404 - Not Found", error_msg="The page you requested does not exist."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', error_title="500 - Server Error", error_msg="An unexpected error occurred. Please try again later."), 500

    return app

# SocketIO Event Handlers
@socketio.on('join')
def on_join(data):
    conv_id = data.get('conversation_id')
    if conv_id:
        room = f"conv_{conv_id}"
        join_room(room)
        emit('status', {'msg': f'Connected to room {room}'}, room=room)

@socketio.on('leave')
def on_leave(data):
    conv_id = data.get('conversation_id')
    if conv_id:
        room = f"conv_{conv_id}"
        leave_room(room)

@socketio.on('typing')
def on_typing(data):
    conv_id = data.get('conversation_id')
    sender = data.get('sender', 'User')
    is_typing = data.get('is_typing', True)
    if conv_id:
        room = f"conv_{conv_id}"
        emit('typing_status', {'sender': sender, 'is_typing': is_typing}, room=room, include_self=False)

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n========================================================")
    print(f"🚀 AI Customer Service Chatbot running on http://127.0.0.1:{port}")
    print(f"========================================================\n")
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
