from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import random
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
import math

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Enhanced flag data with additional information for AI features
FLAGS_DATA = {
    'usa.png': {
        'name': 'United States',
        'continent': 'americas',
        'difficulty': 1,
        'hints': ['Stars and stripes', 'Red, white, and blue', '50 stars for 50 states'],
        'facts': ['Has 13 stripes representing the original colonies', 'The current design dates from 1960']
    },
    'uk.png': {
        'name': 'United Kingdom',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Union Jack', 'Combines three crosses', 'Red, white, and blue'],
        'facts': ['Combines flags of England, Scotland, and Ireland', 'One of the oldest flag designs']
    },
    'france.png': {
        'name': 'France',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Tricolor', 'Vertical stripes', 'Blue, white, red'],
        'facts': ['Adopted during French Revolution', 'Colors represent liberty, equality, fraternity']
    },
    'germany.png': {
        'name': 'Germany',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Horizontal stripes', 'Black, red, gold', 'Three equal bands'],
        'facts': ['Colors date back to 1848', 'Represents unity and justice']
    },
    'japan.png': {
        'name': 'Japan',
        'continent': 'asia',
        'difficulty': 1,
        'hints': ['Rising sun', 'Red circle', 'White background'],
        'facts': ['Called Hinomaru', 'One of the simplest flag designs']
    },
    'canada.png': {
        'name': 'Canada',
        'continent': 'americas',
        'difficulty': 2,
        'hints': ['Maple leaf', 'Red and white', 'Eleven points on leaf'],
        'facts': ['Adopted in 1965', 'Replaced the Red Ensign']
    },
    'australia.png': {
        'name': 'Australia',
        'continent': 'oceania',
        'difficulty': 3,
        'hints': ['Southern Cross', 'Union Jack in corner', 'Blue background'],
        'facts': ['Features constellation visible from Southern Hemisphere', 'Has six stars']
    },
    'brazil.png': {
        'name': 'Brazil',
        'continent': 'americas',
        'difficulty': 3,
        'hints': ['Green and yellow', 'Blue circle', 'Stars and banner'],
        'facts': ['Green represents forests', 'Yellow represents mineral wealth']
    },
    'india.png': {
        'name': 'India',
        'continent': 'asia',
        'difficulty': 2,
        'hints': ['Tricolor', 'Wheel in center', 'Saffron, white, green'],
        'facts': ['Wheel is called Ashoka Chakra', 'Has 24 spokes']
    },
    'china.png': {
        'name': 'China',
        'continent': 'asia',
        'difficulty': 2,
        'hints': ['Red background', 'Five stars', 'Yellow stars'],
        'facts': ['Large star represents Communist Party', 'Four smaller stars represent social classes']
    },
    'italy.png': {
        'name': 'Italy',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Tricolor', 'Vertical stripes', 'Green, white, red'],
        'facts': ['Inspired by French flag', 'Green represents hope']
    },
    'spain.png': {
        'name': 'Spain',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Red and yellow', 'Coat of arms', 'Horizontal stripes'],
        'facts': ['Yellow stripe is twice as wide', 'Current design from 1981']
    },
    'russia.png': {
        'name': 'Russia',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Tricolor', 'White, blue, red', 'Horizontal stripes'],
        'facts': ['Adopted by Peter the Great', 'Colors represent nobility and courage']
    },
    'mexico.png': {
        'name': 'Mexico',
        'continent': 'americas',
        'difficulty': 3,
        'hints': ['Eagle on cactus', 'Green, white, red', 'Vertical stripes'],
        'facts': ['Eagle eating snake represents Aztec legend', 'Symbol of Tenochtitlan founding']
    },
    'south_africa.png': {
        'name': 'South Africa',
        'continent': 'africa',
        'difficulty': 4,
        'hints': ['Y-shaped design', 'Six colors', 'Unique pattern'],
        'facts': ['Adopted in 1994', 'Combines colors of major political parties']
    },
    'argentina.png': {
        'name': 'Argentina',
        'continent': 'americas',
        'difficulty': 3,
        'hints': ['Sun symbol', 'Light blue and white', 'Horizontal stripes'],
        'facts': ['Sun represents Inca sun god', 'Colors represent sky and clouds']
    },
    'egypt.png': {
        'name': 'Egypt',
        'continent': 'africa',
        'difficulty': 3,
        'hints': ['Eagle symbol', 'Red, white, black', 'Horizontal stripes'],
        'facts': ['Eagle of Saladin', 'Pan-Arab colors']
    },
    'sweden.png': {
        'name': 'Sweden',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Nordic cross', 'Blue and yellow', 'Cross offset to left'],
        'facts': ['Based on Danish flag design', 'Yellow cross on blue field']
    },
    'norway.png': {
        'name': 'Norway',
        'continent': 'europe',
        'difficulty': 3,
        'hints': ['Nordic cross', 'Red, white, blue', 'Cross within cross'],
        'facts': ['Combines Danish and Swedish elements', 'White cross outlined in blue']
    },
    'netherlands.png': {
        'name': 'Netherlands',
        'continent': 'europe',
        'difficulty': 2,
        'hints': ['Tricolor', 'Red, white, blue', 'Horizontal stripes'],
        'facts': ['One of oldest tricolor flags', 'Originally orange instead of red']
    }
}

# AI-powered quiz categories
QUIZ_CATEGORIES = {
    'adaptive': 'Adaptive Learning Quiz',
    'all_flags': 'All World Flags',
    'europe': 'European Flags',
    'asia': 'Asian Flags',
    'americas': 'Flags of the Americas',
    'africa': 'African Flags',
    'oceania': 'Oceania Flags',
    'easy': 'Easy Flags',
    'medium': 'Medium Flags',
    'hard': 'Hard Flags',
    'mistake_review': 'Review Your Mistakes'
}

class AIQuizEngine:
    """AI-powered quiz engine with adaptive learning"""
    
    def __init__(self):
        self.performance_weight = 0.3
        self.time_weight = 0.2
        self.difficulty_weight = 0.5
    
    def calculate_user_skill_level(self, session_data):
        """Calculate user's current skill level based on performance"""
        if not session_data.get('answer_history'):
            return 2  # Default medium difficulty
        
        recent_answers = session_data['answer_history'][-10:]  # Last 10 answers
        correct_ratio = sum(1 for a in recent_answers if a['correct']) / len(recent_answers)
        avg_time = sum(a.get('time_taken', 10) for a in recent_answers) / len(recent_answers)
        
        # Skill level from 1 (easy) to 4 (hard)
        skill_level = 1 + (correct_ratio * 2) + (1 if avg_time < 5 else 0)
        return min(4, max(1, round(skill_level)))
    
    def get_adaptive_flags(self, session_data):
        """Get flags based on user's performance and learning gaps"""
        skill_level = self.calculate_user_skill_level(session_data)
        
        # Get flags that match user's skill level
        suitable_flags = {}
        for flag, data in FLAGS_DATA.items():
            if abs(data['difficulty'] - skill_level) <= 1:
                suitable_flags[flag] = data
        
        # Prioritize flags user has struggled with
        mistake_flags = session_data.get('mistake_patterns', {})
        
        # Combine suitable flags with mistake review
        if mistake_flags and random.random() < 0.4:  # 40% chance to review mistakes
            flag_pool = {k: v for k, v in suitable_flags.items() if k in mistake_flags}
            if flag_pool:
                return flag_pool
        
        return suitable_flags if suitable_flags else FLAGS_DATA
    
    def generate_smart_distractors(self, correct_answer, flag_data):
        """Generate intelligent wrong answers based on flag characteristics"""
        correct_data = flag_data[correct_answer]
        
        # Group flags by similarity
        similar_flags = []
        different_flags = []
        
        for flag, data in FLAGS_DATA.items():
            if flag == correct_answer:
                continue
                
            similarity_score = 0
            
            # Same continent
            if data['continent'] == correct_data['continent']:
                similarity_score += 2
            
            # Similar difficulty
            if abs(data['difficulty'] - correct_data['difficulty']) <= 1:
                similarity_score += 1
            
            if similarity_score >= 2:
                similar_flags.append(data['name'])
            else:
                different_flags.append(data['name'])
        
        # Mix of similar and different flags for balanced difficulty
        distractors = []
        if similar_flags:
            distractors.extend(random.sample(similar_flags, min(2, len(similar_flags))))
        if different_flags:
            distractors.extend(random.sample(different_flags, min(2, len(different_flags))))
        
        # Ensure we have enough distractors
        all_other_flags = [data['name'] for flag, data in FLAGS_DATA.items() if flag != correct_answer]
        while len(distractors) < 3 and len(distractors) < len(all_other_flags):
            remaining = [f for f in all_other_flags if f not in distractors]
            if remaining:
                distractors.append(random.choice(remaining))
        
        return distractors[:3]

def get_flag_files():
    """Get list of flag files from the static/flags directory"""
    flags_dir = os.path.join(app.static_folder, 'flags')
    if not os.path.exists(flags_dir):
        os.makedirs(flags_dir)
        return []
    
    flag_files = []
    for filename in os.listdir(flags_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            flag_files.append(filename)
    
    return flag_files

def initialize_session():
    """Initialize session data for AI features"""
    if 'ai_data' not in session:
        session['ai_data'] = {
            'answer_history': [],
            'mistake_patterns': {},
            'learning_progress': {},
            'session_start': time.time(),
            'hints_used': 0,
            'streak': 0,
            'best_streak': 0
        }

def update_learning_analytics(flag_name, correct, time_taken, hint_used):
    """Update AI learning analytics"""
    if 'ai_data' not in session:
        initialize_session()
    
    ai_data = session['ai_data']
    
    # Update answer history
    answer_record = {
        'flag': flag_name,
        'correct': correct,
        'time_taken': time_taken,
        'hint_used': hint_used,
        'timestamp': time.time()
    }
    ai_data['answer_history'].append(answer_record)
    
    # Keep only last 50 answers
    if len(ai_data['answer_history']) > 50:
        ai_data['answer_history'] = ai_data['answer_history'][-50:]
    
    # Update mistake patterns
    if not correct:
        ai_data['mistake_patterns'][flag_name] = ai_data['mistake_patterns'].get(flag_name, 0) + 1
        ai_data['streak'] = 0
    else:
        ai_data['streak'] += 1
        ai_data['best_streak'] = max(ai_data['best_streak'], ai_data['streak'])
        # Reduce mistake count if user gets it right
        if flag_name in ai_data['mistake_patterns']:
            ai_data['mistake_patterns'][flag_name] = max(0, ai_data['mistake_patterns'][flag_name] - 1)
    
    # Update learning progress
    if flag_name not in ai_data['learning_progress']:
        ai_data['learning_progress'][flag_name] = {'attempts': 0, 'correct': 0}
    
    ai_data['learning_progress'][flag_name]['attempts'] += 1
    if correct:
        ai_data['learning_progress'][flag_name]['correct'] += 1
    
    session['ai_data'] = ai_data

def generate_quiz_question(category='all_flags'):
    """Generate a quiz question with AI-powered adaptive selection"""
    initialize_session()
    
    ai_engine = AIQuizEngine()
    
    # Get available flags based on category and AI recommendations
    if category == 'adaptive':
        available_flags = ai_engine.get_adaptive_flags(session['ai_data'])
    elif category == 'mistake_review':
        mistake_flags = session['ai_data'].get('mistake_patterns', {})
        available_flags = {flag: FLAGS_DATA[flag] for flag in mistake_flags.keys() if flag in FLAGS_DATA}
        if not available_flags:
            available_flags = FLAGS_DATA
    elif category in ['easy', 'medium', 'hard']:
        difficulty_map = {'easy': 1, 'medium': 2, 'hard': 3}
        target_difficulty = difficulty_map[category]
        available_flags = {flag: data for flag, data in FLAGS_DATA.items() 
                         if data['difficulty'] == target_difficulty}
    else:
        # Filter by continent
        continent_filter = {
            'europe': 'europe',
            'asia': 'asia', 
            'americas': 'americas',
            'africa': 'africa',
            'oceania': 'oceania'
        }
        
        if category in continent_filter:
            available_flags = {flag: data for flag, data in FLAGS_DATA.items() 
                             if data['continent'] == continent_filter[category]}
        else:
            available_flags = FLAGS_DATA
    
    if not available_flags:
        return None
    
    # Select correct answer
    flag_files = list(available_flags.keys())
    correct_flag = random.choice(flag_files)
    correct_data = available_flags[correct_flag]
    correct_answer = correct_data['name']
    
    # Generate smart distractors
    wrong_answers = ai_engine.generate_smart_distractors(correct_flag, {correct_flag: correct_data})
    
    # Combine and shuffle options
    options = [correct_answer] + wrong_answers[:3]
    random.shuffle(options)
    
    return {
        'flag_image': correct_flag,
        'correct_answer': correct_answer,
        'options': options,
        'hints': correct_data.get('hints', []),
        'facts': correct_data.get('facts', []),
        'difficulty': correct_data.get('difficulty', 2)
    }

@app.route('/')
def welcome():
    """Welcome page to select quiz category"""
    initialize_session()
    
    # Get AI insights for display
    ai_data = session.get('ai_data', {})
    insights = {
        'total_questions': len(ai_data.get('answer_history', [])),
        'current_streak': ai_data.get('streak', 0),
        'best_streak': ai_data.get('best_streak', 0),
        'skill_level': AIQuizEngine().calculate_user_skill_level(ai_data)
    }
    
    return render_template('welcome.html', categories=QUIZ_CATEGORIES, insights=insights)

@app.route('/quiz/<category>')
def index(category):
    """Main quiz page with AI features"""
    session['current_quiz_category'] = category
    session['question_start_time'] = time.time()
    return render_template('index.html', category=category)

@app.route('/api/question')
def get_question():
    """API endpoint to get a new quiz question with AI selection"""
    current_category = session.get('current_quiz_category', 'all_flags')
    question = generate_quiz_question(category=current_category)
    if not question:
        return jsonify({'error': 'No flags available'}), 400
    
    # Store question data in session
    session['current_question'] = question
    session['question_start_time'] = time.time()
    session['hint_used'] = False
    
    return jsonify({
        'flag_image': question['flag_image'],
        'options': question['options'],
        'difficulty': question['difficulty'],
        'has_hints': len(question['hints']) > 0
    })

@app.route('/api/hint')
def get_hint():
    """API endpoint to get a hint for current question"""
    current_question = session.get('current_question')
    if not current_question or not current_question.get('hints'):
        return jsonify({'error': 'No hints available'}), 400
    
    hints = current_question['hints']
    hint_index = session.get('current_hint_index', 0)
    
    if hint_index >= len(hints):
        return jsonify({'hint': 'No more hints available!', 'last_hint': True})
    
    hint = hints[hint_index]
    session['current_hint_index'] = hint_index + 1
    session['hint_used'] = True
    
    return jsonify({
        'hint': hint,
        'hint_number': hint_index + 1,
        'total_hints': len(hints),
        'last_hint': hint_index + 1 >= len(hints)
    })

@app.route('/api/answer', methods=['POST'])
def check_answer():
    """API endpoint to check answer with AI learning updates"""
    data = request.get_json()
    user_answer = data.get('answer')
    current_question = session.get('current_question')
    
    if not user_answer or not current_question:
        return jsonify({'error': 'Invalid request'}), 400
    
    correct_answer = current_question['correct_answer']
    is_correct = user_answer == correct_answer
    
    # Calculate time taken
    time_taken = time.time() - session.get('question_start_time', time.time())
    hint_used = session.get('hint_used', False)
    
    # Update AI learning analytics
    flag_name = current_question['flag_image']
    update_learning_analytics(flag_name, is_correct, time_taken, hint_used)
    
    # Update traditional score
    if 'score' not in session:
        session['score'] = 0
        session['total_questions'] = 0
    
    session['total_questions'] += 1
    if is_correct:
        session['score'] += 1
    
    # Reset hint index for next question
    session['current_hint_index'] = 0
    
    # Get interesting fact
    facts = current_question.get('facts', [])
    fun_fact = random.choice(facts) if facts else None
    
    # Calculate performance insights
    ai_data = session.get('ai_data', {})
    recent_performance = ai_data.get('answer_history', [])[-5:]  # Last 5 answers
    recent_accuracy = sum(1 for a in recent_performance if a['correct']) / len(recent_performance) if recent_performance else 0
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer,
        'score': session['score'],
        'total': session['total_questions'],
        'time_taken': round(time_taken, 1),
        'hint_used': hint_used,
        'fun_fact': fun_fact,
        'current_streak': ai_data.get('streak', 0),
        'recent_accuracy': round(recent_accuracy * 100, 1)
    })

@app.route('/api/score')
def get_score():
    """API endpoint to get current score and AI insights"""
    ai_data = session.get('ai_data', {})
    skill_level = AIQuizEngine().calculate_user_skill_level(ai_data)
    
    skill_names = {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced', 4: 'Expert'}
    
    return jsonify({
        'score': session.get('score', 0),
        'total': session.get('total_questions', 0),
        'current_streak': ai_data.get('streak', 0),
        'best_streak': ai_data.get('best_streak', 0),
        'skill_level': skill_names.get(skill_level, 'Intermediate'),
        'hints_used': ai_data.get('hints_used', 0)
    })

@app.route('/api/analytics')
def get_analytics():
    """API endpoint to get detailed learning analytics"""
    ai_data = session.get('ai_data', {})
    
    # Calculate various metrics
    answer_history = ai_data.get('answer_history', [])
    if not answer_history:
        return jsonify({'message': 'No data available yet'})
    
    # Performance over time
    recent_10 = answer_history[-10:] if len(answer_history) >= 10 else answer_history
    accuracy = sum(1 for a in recent_10 if a['correct']) / len(recent_10) * 100
    
    # Average response time
    avg_time = sum(a.get('time_taken', 10) for a in recent_10) / len(recent_10)
    
    # Most challenging flags
    mistake_patterns = ai_data.get('mistake_patterns', {})
    challenging_flags = sorted(mistake_patterns.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Learning progress
    learning_progress = ai_data.get('learning_progress', {})
    mastered_flags = [flag for flag, data in learning_progress.items() 
                     if data['attempts'] >= 3 and data['correct'] / data['attempts'] >= 0.8]
    
    return jsonify({
        'accuracy': round(accuracy, 1),
        'avg_response_time': round(avg_time, 1),
        'challenging_flags': [{'flag': FLAGS_DATA.get(flag, {}).get('name', flag), 'mistakes': count} 
                             for flag, count in challenging_flags],
        'mastered_count': len(mastered_flags),
        'total_flags_seen': len(learning_progress),
        'session_duration': round((time.time() - ai_data.get('session_start', time.time())) / 60, 1)
    })

@app.route('/api/reset')
def reset_score():
    """API endpoint to reset the score and optionally AI data"""
    reset_ai = request.args.get('reset_ai', 'false').lower() == 'true'
    
    session['score'] = 0
    session['total_questions'] = 0
    
    if reset_ai:
        session['ai_data'] = {
            'answer_history': [],
            'mistake_patterns': {},
            'learning_progress': {},
            'session_start': time.time(),
            'hints_used': 0,
            'streak': 0,
            'best_streak': 0
        }
    
    return jsonify({'message': 'Score reset', 'ai_reset': reset_ai})

# Template creation with enhanced AI features
def create_templates():
    """Create enhanced template files with AI features"""
    templates_dir = 'templates'
    static_dir = 'static'
    flags_dir = os.path.join(static_dir, 'flags')
    
    os.makedirs(templates_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(flags_dir, exist_ok=True)
    
    # Enhanced index.html with AI features
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Flag Quiz</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .quiz-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            text-align: center;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .ai-badge {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            margin: 5px;
        }
        .difficulty-indicator {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .difficulty-star {
            color: #feca57;
            font-size: 18px;
        }
        .flag-image {
            max-width: 350px;
            max-height: 250px;
            border: 4px solid #333;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .option-btn {
            padding: 18px;
            font-size: 16px;
            border: 2px solid #667eea;
            background: rgba(102, 126, 234, 0.1);
            color: #333;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .option-btn:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }
        .option-btn.correct {
            background: #51cf66;
            color: white;
            border-color: #51cf66;
        }
        .option-btn.incorrect {
            background: #ff6b6b;
            color: white;
            border-color: #ff6b6b;
        }
        .score-display {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .score-item {
            background: rgba(102, 126, 234, 0.1);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(102, 126, 234, 0.3);
        }
        .score-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        .score-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            flex-wrap: wrap;
            justify-content: center;
        }
        .btn {
            padding: 12px 24px;
            font-size: 16px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 500;
        }
        .btn-primary {
            background: #667eea;
            color: white;
        }
        .btn-primary:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        .btn-secondary {
            background: #a0aec0;
            color: white;
        }
        .btn-secondary:hover {
            background: #718096;
        }
        .btn-hint {
            background: #feca57;
            color: white;
        }
        .btn-hint:hover {
            background: #ffd93d;
        }
        .btn-analytics {
            background: #ff6b6b;
            color: white;
        }
        .btn-analytics:hover {
            background: #fa5252;
        }
        .feedback {
            margin: 20px 0;
            padding: 20px;
            border-radius: 10px;
            font-weight: bold;
            backdrop-filter: blur(10px);
        }
        .feedback.correct {
            background: rgba(81, 207, 102, 0.2);
            color: #2b8a3e;
            border: 2px solid #51cf66;
        }
        .feedback.incorrect {
            background: rgba(255, 107, 107, 0.2);
            color: #c92a2a;
            border: 2px solid #ff6b6b;
        }
        .hint-box {
            background: rgba(254, 202, 87, 0.2);
            border: 2px solid #feca57;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            color: #b7791f;
        }
        .fun-fact {
            background: rgba(102, 126, 234, 0.1);
            border: 2px solid #667eea;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            color: #4c51bf;
            font-style: italic;
        }
        .analytics-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        }
        .analytics-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 30px;
            border-radius: 20px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
        }
        .close-btn {
            position: absolute;
            top: 15px;
            right: 20px;
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: #666;
        }
        .loading {
            color: #667eea;
            font-style: italic;
            font-size: 18px;
        }
        .streak-display {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
        }
        @media (max-width: 768px) {
            .header {
                flex-direction: column;
                gap: 15px;
            }
            .score-display {
                grid-template-columns: repeat(2, 1fr);
            }
            .controls {
                flex-direction: column;
                align-items: center;
            }
            .btn {
                width: 100%;
                max-width: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="quiz-container">
        <div class="header">
            <h1>🤖 AI-Powered Flag Quiz</h1>
            <div class="ai-badge">AI Learning Mode</div>
        </div>
        
        <div class="score-display" id="scoreDisplay">
            <div class="score-item">
                <div class="score-value" id="score">0/0</div>
                <div class="score-label">Score</div>
            </div>
            <div class="score-item">
                <div class="score-value" id="streak">0</div>
                <div class="score-label">Current Streak</div>
            </div>
            <div class="score-item">
                <div class="score-value" id="skillLevel">-</div>
                <div class="score-label">Skill Level</div>
            </div>
        </div>
        
        <div id="quiz-content">
            <div class="loading">🧠 AI is preparing your personalized question...</div>
        </div>
        
        <div class="controls">
            <button class="btn btn-primary" onclick="loadNewQuestion()">New Question</button>
            <button class="btn btn-hint" onclick="getHint()" id="hintBtn">💡 Get Hint</button>
            <button class="btn btn-analytics" onclick="showAnalytics()">📊 Analytics</button>
            <button class="btn btn-secondary" onclick="resetScore()">Reset Score</button>
            <button class="btn btn-secondary" onclick="window.location.href='/'">Back to Welcome</button>
        </div>
    </div>

    <!-- Analytics Modal -->
    <div id="analyticsModal" class="analytics-modal">
        <div class="analytics-content">
            <button class="close-btn" onclick="hideAnalytics()">&times;</button>
            <h2>📊 Your Learning Analytics</h2>
            <div id="analyticsContent">
                <div class="loading">Loading your progress...</div>
            </div>
        </div>
    </div>

    <script>
        let currentQuestion = null;
        let answered = false;
        let questionStartTime = null;

        async function loadNewQuestion() {
            try {
                document.getElementById('quiz-content').innerHTML = '<div class="loading">🧠 AI is selecting your next challenge...</div>';
                answered = false;
                questionStartTime = Date.now();
                
                const response = await fetch('/api/question');
                const data = await response.json();
                
                if (data.error) {
                    document.getElementById('quiz-content').innerHTML = 
                        '<div class="feedback incorrect">Error: ' + data.error + '</div>' +
                        '<p>Please make sure flag images are placed in the static/flags/ directory.</p>';
                    return;
                }
                
                currentQuestion = data;
                displayQuestion(data);
                updateScore();
                
                // Update hint button
                const hintBtn = document.getElementById('hintBtn');
                hintBtn.disabled = !data.has_hints;
                hintBtn.style.opacity = data.has_hints ? '1' : '0.5';
                
            } catch (error) {
                console.error('Error loading question:', error);
                document.getElementById('quiz-content').innerHTML = 
                    '<div class="feedback incorrect">Error loading question. Please try again.</div>';
            }
        }

        function displayQuestion(question) {
            // Generate difficulty stars
            const difficultyStars = '★'.repeat(question.difficulty) + '☆'.repeat(4 - question.difficulty);
            
            const optionsHtml = question.options.map(option => 
                `<button class="option-btn" onclick="selectAnswer('${option.replace(/'/g, "\\'")}')">
                    ${option}
                </button>`
            ).join('');
            
            document.getElementById('quiz-content').innerHTML = `
                <div class="difficulty-indicator">
                    <span>Difficulty: </span>
                    <span class="difficulty-star">${difficultyStars}</span>
                </div>
                <img src="/static/flags/${question.flag_image}" alt="Flag" class="flag-image" 
                     onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Y4ZjlmYSIgc3Ryb2tlPSIjZGVlMmU2IiBzdHJva2Utd2lkdGg9IjIiLz48dGV4dCB4PSIxNTAiIHk9IjEwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzZjNzU3ZCI+RmxhZyBub3QgZm91bmQ8L3RleHQ+PC9zdmc+'">
                <p><strong>🌍 Which country does this flag belong to?</strong></p>
                <div class="options">
                    ${optionsHtml}
                </div>
            `;
        }

        async function selectAnswer(answer) {
            if (answered) return;
            answered = true;
            
            try {
                const response = await fetch('/api/answer', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ answer: answer })
                });
                
                const result = await response.json();
                displayResult(result, answer);
                updateScore();
            } catch (error) {
                console.error('Error checking answer:', error);
            }
        }

        function displayResult(result, userAnswer) {
            const buttons = document.querySelectorAll('.option-btn');
            buttons.forEach(btn => {
                btn.disabled = true;
                if (btn.textContent.trim() === result.correct_answer) {
                    btn.classList.add('correct');
                } else if (btn.textContent.trim() === userAnswer && !result.correct) {
                    btn.classList.add('incorrect');
                }
            });
            
            const feedbackClass = result.correct ? 'correct' : 'incorrect';
            const emoji = result.correct ? '🎉' : '❌';
            const feedbackText = result.correct ? 
                `${emoji} Excellent! You got it right!` : 
                `${emoji} Not quite! The correct answer is: ${result.correct_answer}`;
            
            let additionalInfo = '';
            
            // Add performance info
            if (result.time_taken) {
                additionalInfo += `<br><small>⏱️ Time: ${result.time_taken}s`;
                if (result.hint_used) {
                    additionalInfo += ' (hint used)';
                }
                additionalInfo += '</small>';
            }
            
            // Add streak info
            if (result.current_streak > 0) {
                additionalInfo += `<br><small>🔥 Current streak: ${result.current_streak}</small>`;
            }
            
            // Add recent accuracy
            if (result.recent_accuracy !== undefined) {
                additionalInfo += `<br><small>📈 Recent accuracy: ${result.recent_accuracy}%</small>`;
            }
            
            const feedbackHtml = `<div class="feedback ${feedbackClass}">${feedbackText}${additionalInfo}</div>`;
            
            // Add fun fact if available
            if (result.fun_fact) {
                const factHtml = `<div class="fun-fact">💡 Did you know? ${result.fun_fact}</div>`;
                document.getElementById('quiz-content').innerHTML += feedbackHtml + factHtml;
            } else {
                document.getElementById('quiz-content').innerHTML += feedbackHtml;
            }
        }

        async function getHint() {
            if (answered) return;
            
            try {
                const response = await fetch('/api/hint');
                const data = await response.json();
                
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                // Remove existing hint box
                const existingHint = document.querySelector('.hint-box');
                if (existingHint) {
                    existingHint.remove();
                }
                
                const hintHtml = `<div class="hint-box">
                    💡 Hint ${data.hint_number}/${data.total_hints}: ${data.hint}
                </div>`;
                
                document.getElementById('quiz-content').innerHTML += hintHtml;
                
                // Update hint button
                const hintBtn = document.getElementById('hintBtn');
                if (data.last_hint) {
                    hintBtn.disabled = true;
                    hintBtn.textContent = 'No more hints';
                    hintBtn.style.opacity = '0.5';
                }
                
            } catch (error) {
                console.error('Error getting hint:', error);
            }
        }

        async function updateScore() {
            try {
                const response = await fetch('/api/score');
                const data = await response.json();
                
                document.getElementById('score').textContent = `${data.score}/${data.total}`;
                document.getElementById('streak').textContent = data.current_streak;
                document.getElementById('skillLevel').textContent = data.skill_level;
                
            } catch (error) {
                console.error('Error updating score:', error);
            }
        }

        async function showAnalytics() {
            document.getElementById('analyticsModal').style.display = 'block';
            
            try {
                const response = await fetch('/api/analytics');
                const data = await response.json();
                
                if (data.message) {
                    document.getElementById('analyticsContent').innerHTML = 
                        `<p>${data.message}</p><p>Start answering questions to see your progress!</p>`;
                    return;
                }
                
                const challengingFlagsHtml = data.challenging_flags.length > 0 ? 
                    data.challenging_flags.map(flag => 
                        `<li>${flag.flag} (${flag.mistakes} mistakes)</li>`
                    ).join('') : '<li>None yet - keep practicing!</li>';
                
                document.getElementById('analyticsContent').innerHTML = `
                    <div style="text-align: left;">
                        <h3>📊 Performance Overview</h3>
                        <p><strong>Overall Accuracy:</strong> ${data.accuracy}%</p>
                        <p><strong>Average Response Time:</strong> ${data.avg_response_time}s</p>
                        <p><strong>Session Duration:</strong> ${data.session_duration} minutes</p>
                        
                        <h3>🎯 Learning Progress</h3>
                        <p><strong>Flags Mastered:</strong> ${data.mastered_count}/${data.total_flags_seen}</p>
                        
                        <h3>💪 Most Challenging Flags</h3>
                        <ul>${challengingFlagsHtml}</ul>
                        
                        <p style="margin-top: 20px; font-size: 14px; color: #666;">
                            💡 The AI adapts questions based on your performance to optimize learning!
                        </p>
                    </div>
                `;
                
            } catch (error) {
                console.error('Error loading analytics:', error);
                document.getElementById('analyticsContent').innerHTML = 
                    '<p>Error loading analytics. Please try again.</p>';
            }
        }

        function hideAnalytics() {
            document.getElementById('analyticsModal').style.display = 'none';
        }

        async function resetScore() {
            const resetAI = confirm('Reset learning data too? (This will clear your AI progress and start fresh)');
            
            try {
                const url = resetAI ? '/api/reset?reset_ai=true' : '/api/reset';
                await fetch(url);
                updateScore();
                document.getElementById('quiz-content').innerHTML = 
                    '<div class="loading">Click "New Question" to start your ' + 
                    (resetAI ? 'fresh learning journey' : 'quiz') + '!</div>';
                
                // Reset hint button
                const hintBtn = document.getElementById('hintBtn');
                hintBtn.disabled = false;
                hintBtn.textContent = '💡 Get Hint';
                hintBtn.style.opacity = '1';
                
            } catch (error) {
                console.error('Error resetting score:', error);
            }
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('analyticsModal');
            if (event.target === modal) {
                hideAnalytics();
            }
        }

        // Load first question when page loads
        window.onload = function() {
            updateScore();
            loadNewQuestion();
        };
    </script>
</body>
</html>'''

    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

    # Enhanced welcome.html with AI insights
    welcome_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Powered Flag Quiz - Welcome</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        .welcome-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            text-align: center;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 2.5em;
        }
        .ai-features {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 30px 0;
        }
        .ai-features h2 {
            margin-top: 0;
            font-size: 1.8em;
        }
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .feature-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            text-align: left;
        }
        .feature-item h4 {
            margin: 0 0 10px 0;
            color: #feca57;
        }
        .insights-panel {
            background: rgba(102, 126, 234, 0.1);
            border: 2px solid rgba(102, 126, 234, 0.3);
            border-radius: 15px;
            padding: 20px;
            margin: 30px 0;
        }
        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .insight-item {
            text-align: center;
        }
        .insight-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .insight-label {
            color: #666;
            font-size: 0.9em;
        }
        .quiz-blocks {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        .quiz-block-btn {
            padding: 25px;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #667eea;
            background: rgba(102, 126, 234, 0.1);
            color: #333;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: block;
            position: relative;
            overflow: hidden;
        }
        .quiz-block-btn:hover {
            background: #667eea;
            color: white;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }
        .quiz-block-btn.recommended {
            border-color: #feca57;
            background: rgba(254, 202, 87, 0.2);
        }
        .quiz-block-btn.recommended::before {
            content: "🤖 AI Recommended";
            position: absolute;
            top: 5px;
            right: 10px;
            font-size: 12px;
            background: #feca57;
            color: white;
            padding: 3px 8px;
            border-radius: 10px;
        }
        .instructions {
            margin-top: 40px;
            font-size: 16px;
            color: #666;
            line-height: 1.6;
        }
        .instructions p {
            margin: 10px 0;
        }
        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }
            .features-grid {
                grid-template-columns: 1fr;
            }
            .insights-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .quiz-blocks {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="welcome-container">
        <h1>🤖 Welcome to AI-Powered Flag Quiz! 🌎</h1>
        
        <div class="ai-features">
            <h2>🧠 Smart Learning Features</h2>
            <div class="features-grid">
                <div class="feature-item">
                    <h4>📈 Adaptive Difficulty</h4>
                    <p>AI adjusts question difficulty based on your performance</p>
                </div>
                <div class="feature-item">
                    <h4>💡 Intelligent Hints</h4>
                    <p>Context-aware hints to guide your learning</p>
                </div>
                <div class="feature-item">
                    <h4>📊 Learning Analytics</h4>
                    <p>Track your progress and identify improvement areas</p>
                </div>
                <div class="feature-item">
                    <h4>🎯 Mistake Review</h4>
                    <p>Focus on flags you find challenging</p>
                </div>
            </div>
        </div>
        
        {% if insights.total_questions > 0 %}
        <div class="insights-panel">
            <h3>📊 Your Learning Journey</h3>
            <div class="insights-grid">
                <div class="insight-item">
                    <div class="insight-value">{{ insights.total_questions }}</div>
                    <div class="insight-label">Questions Answered</div>
                </div>
                <div class="insight-item">
                    <div class="insight-value">{{ insights.current_streak }}</div>
                    <div class="insight-label">Current Streak</div>
                </div>
                <div class="insight-item">
                    <div class="insight-value">{{ insights.best_streak }}</div>
                    <div class="insight-label">Best Streak</div>
                </div>
                <div class="insight-item">
                    <div class="insight-value">Lv.{{ insights.skill_level }}</div>
                    <div class="insight-label">Skill Level</div>
                </div>
            </div>
        </div>
        {% endif %}
        
        <p style="font-size: 1.2em; margin: 30px 0;">Select a quiz mode to begin your learning adventure:</p>
        
        <div class="quiz-blocks">
            {% for key, value in categories.items() %}
                {% if key == 'adaptive' %}
                    <a href="/quiz/{{ key }}" class="quiz-block-btn recommended">
                        {{ value }}<br>
                        <small style="font-weight: normal; opacity: 0.8;">
                            Personalized questions based on your skill level
                        </small>
                    </a>
                {% elif key == 'mistake_review' and insights.total_questions > 5 %}
                    <a href="/quiz/{{ key }}" class="quiz-block-btn">
                        {{ value }}<br>
                        <small style="font-weight: normal; opacity: 0.8;">
                            Practice flags you've struggled with
                        </small>
                    </a>
                {% elif key not in ['adaptive', 'mistake_review'] %}
                    <a href="/quiz/{{ key }}" class="quiz-block-btn">
                        {{ value }}
                    </a>
                {% endif %}
            {% endfor %}
        </div>
        
        <div class="instructions">
            <h3>🚀 Getting Started</h3>
            <p><strong>New to flag quizzes?</strong> Start with "Adaptive Learning Quiz" - our AI will adjust to your skill level!</p>
            <p><strong>Want a challenge?</strong> Try the difficulty-based modes or continental quizzes.</p>
            <p><strong>Need to improve?</strong> Use "Review Your Mistakes" after answering some questions.</p>
            <p style="font-size: 14px; margin-top: 30px;">
                💡 <strong>Pro tip:</strong> The AI learns from your responses to provide better questions and hints!
            </p>
            <p style="font-size: 14px; color: #888;">
                Ensure flag images are in the <code>static/flags/</code> directory for the quiz to function correctly.
            </p>
        </div>
    </div>
</body>
</html>'''

    with open(os.path.join(templates_dir, 'welcome.html'), 'w', encoding='utf-8') as f:
        f.write(welcome_html)
    
    # Enhanced README
    readme_content = ''' '''

    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

if __name__ == '__main__':
    create_templates()
    print("🚀 Starting Flag Quiz App...")
    print("📁 Make sure to add flag images to the 'static/flags/' directory")
    print("🌐 Visit http://localhost:5000 to play the quiz")
    app.run(debug=True, port=5000)