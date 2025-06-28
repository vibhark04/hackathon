# 🤖 AI-Powered Flag Quiz Application

An intelligent flag learning platform that adapts to your skill level and provides personalized learning experiences using advanced AI algorithms.

## 🌟 Features

### 🧠 AI-Powered Learning
- **Adaptive Difficulty**: AI automatically adjusts question difficulty based on your performance
- **Smart Question Selection**: Prioritizes flags you need to practice based on your learning gaps
- **Intelligent Distractors**: Generates contextually relevant wrong answers for balanced difficulty
- **Mistake Pattern Analysis**: Tracks and helps you focus on challenging flags

### 📊 Advanced Analytics
- **Real-time Performance Tracking**: Monitor accuracy, response times, and streaks
- **Learning Progress Visualization**: See which flags you've mastered
- **Skill Level Assessment**: Dynamic skill level calculation (Beginner → Expert)
- **Session Analytics**: Detailed insights into your learning session

### 💡 Learning Enhancement
- **Context-Aware Hints**: Multi-level hint system with progressive difficulty
- **Educational Facts**: Learn interesting facts about each flag
- **Streak Tracking**: Maintain motivation with streak counters
- **Review Mode**: Focus on previously missed flags

### 🎯 Quiz Modes
- **Adaptive Learning Quiz** (Recommended): AI-personalized questions
- **Continental Quizzes**: Europe, Asia, Americas, Africa, Oceania
- **Difficulty-Based**: Easy, Medium, Hard flags
- **Mistake Review**: Practice your challenging flags
- **All World Flags**: Complete flag collection

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Flask framework
- Modern web browser

### Installation

1. **Clone or download the application**
   ```bash
   # Save the provided code as app.py
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Set up flag images**
   ```bash
   mkdir -p static/flags
   # Add your flag images to this directory
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
flag-quiz/
├── app.py                 # Main Flask application
├── static/
│   └── flags/            # Flag images directory
│       ├── usa.png
│       ├── uk.png
│       ├── france.png
│       └── ...
├── templates/            # Auto-generated HTML templates
│   ├── welcome.html
│   └── index.html
└── README.md
```

## 🖼️ Adding Flag Images

1. **Supported formats**: PNG, JPG, JPEG, GIF
2. **Naming convention**: Use the exact filenames as defined in `FLAGS_DATA` in `app.py`
3. **Recommended size**: 300x200 pixels for optimal display
4. **Example filenames**:
   ```
   usa.png, uk.png, france.png, germany.png, japan.png,
   canada.png, australia.png, brazil.png, india.png, china.png,
   italy.png, spain.png, russia.png, mexico.png, south_africa.png,
   argentina.png, egypt.png, sweden.png, norway.png, netherlands.png
   ```

## 🎮 How to Play

### For Beginners
1. Start with **"Adaptive Learning Quiz"** - the AI will assess your skill level
2. Use hints when stuck (💡 button)
3. Review your analytics to track progress
4. The difficulty will automatically adjust as you improve

### For Advanced Users
1. Try **continent-specific** or **difficulty-based** quizzes
2. Use **"Review Your Mistakes"** to focus on challenging flags
3. Aim for high accuracy streaks
4. Monitor your skill level progression

## 🧠 AI Features Explained

### Adaptive Algorithm
The AI uses multiple factors to personalize your experience:
- **Performance Weight** (30%): Recent accuracy and correctness
- **Time Weight** (20%): Response speed analysis
- **Difficulty Weight** (50%): Flag difficulty matching

### Smart Question Selection
- Analyzes your performance history
- Identifies learning gaps and mistake patterns
- Balances review of difficult flags with new challenges
- Ensures optimal learning progression

### Intelligent Distractor Generation
- Groups flags by geographical and visual similarity
- Creates balanced multiple-choice options
- Adjusts difficulty based on your skill level
- Prevents easy elimination strategies

## 📊 Analytics Dashboard

Access detailed learning insights:
- **Overall Accuracy**: Your success rate across recent questions
- **Average Response Time**: Speed of decision-making
- **Session Duration**: Time spent learning
- **Flags Mastered**: Countries you've learned well
- **Most Challenging Flags**: Areas needing focus

## ⚙️ Configuration

### Adding New Flags
1. Add the flag image to `static/flags/`
2. Update `FLAGS_DATA` in `app.py`:
   ```python
   'newflag.png': {
       'name': 'Country Name',
       'continent': 'continent_name',
       'difficulty': 1-4,
       'hints': ['Hint 1', 'Hint 2'],
       'facts': ['Interesting fact about the flag']
   }
   ```

### Customizing Difficulty
Adjust AI parameters in the `AIQuizEngine` class:
```python
self.performance_weight = 0.3  # Performance influence
self.time_weight = 0.2         # Speed influence  
self.difficulty_weight = 0.5   # Difficulty matching
```

### Quiz Categories
Add new categories in `QUIZ_CATEGORIES`:
```python
'new_category': 'Display Name'
```

## 🔧 Technical Details

### Backend (Flask)
- **Session Management**: Stores user progress and AI data
- **RESTful API**: JSON endpoints for frontend communication
- **AI Engine**: Adaptive learning algorithm implementation
- **Analytics Engine**: Performance tracking and insights

### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Works on desktop and mobile
- **Modern UI**: Glassmorphism design with animations
- **Interactive Elements**: Smooth transitions and feedback
- **Real-time Updates**: Dynamic score and analytics display

### AI Algorithm Components
1. **Skill Assessment**: Calculates user proficiency (1-4 scale)
2. **Question Selection**: Chooses appropriate flags based on skill
3. **Distractor Generation**: Creates intelligent wrong answers
4. **Performance Tracking**: Monitors and analyzes user progress

## 🌐 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers

## 🐛 Troubleshooting

### Common Issues

**Flag images not displaying**
- Ensure images are in `static/flags/` directory
- Check filename matches exactly with `FLAGS_DATA` keys
- Verify image format is supported (PNG, JPG, JPEG, GIF)

**AI features not working**
- Check browser console for JavaScript errors
- Ensure Flask session is working properly
- Verify all API endpoints are responding

**Poor performance**
- Add more flag images for better variety
- Ensure stable internet connection
- Try refreshing the page to reset session

### Development Mode

Run with debug enabled:
```bash
python app.py
# Debug mode is enabled by default
```

## 📈 Future Enhancements

Potential improvements for the application:
- **User Accounts**: Persistent progress tracking
- **Multiplayer Mode**: Compete with friends
- **Additional Geography**: Capitals, landmarks, maps
- **Advanced AI**: Machine learning model integration
- **Mobile App**: Native iOS/Android versions
- **Gamification**: Achievements, levels, rewards

## 🤝 Contributing

To contribute to this project:
1. Add more flag images and data
2. Improve the AI algorithms
3. Enhance the user interface
4. Add new quiz modes
5. Implement additional analytics

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Flag image sources: Various public domain collections
- AI algorithms inspired by adaptive learning research
- UI design using modern web standards

---

**Ready to test your flag knowledge? Start your AI-powered learning journey today!** 🚀🌎
