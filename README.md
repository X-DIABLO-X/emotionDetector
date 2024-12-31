# 🌟 Smart Mirror: Emotion Detector with Compliments 💬✨

Welcome to **Smart Mirror**! This project is an emotion-detecting application that uses AI to recognize your emotions and offers compliments based on your mood. It’s like having a personal cheerleader that never misses a beat! 🪞🤖

## 🚀 Features

- 🎭 **Emotion Detection**: Recognizes emotions like happiness, sadness, anger, surprise, and fear.
- 🎤 **Voice Feedback**: Speaks personalized compliments to brighten your day.
- 🧑‍🦳 **Age & Gender Detection**: Provides additional information about detected faces.
- 🎨 **Enhanced UI**: Displays emotions with vibrant colors and clean visuals.
- 🖥️ **Real-Time Processing**: Works seamlessly with your webcam to process emotions live.

---

## 🛠️ Technologies Used

- **Python** 🐍
- **OpenCV** 🔍: For real-time video processing and visualization.
- **FER** 🤗: Facial emotion recognition library for emotion detection.
- **pyttsx3** 🗣️: Text-to-speech engine for voice feedback.
- **Pretrained Models**: Age and gender detection using Caffe.

---

## 🎬 How It Works

1. **Detect Emotions**:
   - The app uses your webcam to detect faces and analyze emotions.
2. **Categorize Mood**:
   - Emotions are categorized as "very" (e.g., very happy) or moderate (e.g., sad).
3. **Compliments Generator**:
   - Depending on the mood, the app speaks tailored compliments to boost morale.
4. **Enhanced Visualization**:
   - Color-coded emotion rectangles and text overlays make the experience interactive and engaging.

---

## 🖥️ Setup & Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/X-DIABLO-X/emotionDetector.git
   cd smart-mirror
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the pretrained models:
   - **Age Model**:
     - `age_deploy.prototxt`
     - `age_net.caffemodel`
   - **Gender Model**:
     - `gender_deploy.prototxt`
     - `gender_net.caffemodel`
   
   Place these files in the appropriate directory.

4. Run the app:
   ```bash
   python smart_mirror.py
   ```

---

## 🎮 Controls

| Key | Action          |
|-----|-----------------|
| `Q` | Quit the app    |
| `S` | Toggle speech   |
| `H` | Help and info   |

---

## 📸 Screenshots

- **Emotion Detection in Action**:
  - Real-time emotion and age detection with colorful overlays.

---

## 🎉 Compliments List

Here’s a sneak peek at how Smart Mirror lifts your spirits:

- **Angry**: "Stay calm, you've got this!"
- **Sad**: "It’s okay to feel this way. Better days are coming!"
- **Happy**: "Your smile lights up the room!"
- **Surprised**: "Wow, what a pleasant surprise!"
- **Feared**: "You are braver than you think!"

---

## 🧠 How It’s Built

### Core Components

1. **Emotion Detection**: Using the FER library for precise emotion recognition.
2. **Age & Gender Models**: Caffe-based deep learning models.
3. **Speech Feedback**: pyttsx3 for dynamic voice output.
4. **Interactive UI**: Enhanced with OpenCV for visual feedback.

---

## 💡 Ideas for Future Enhancements

- 🌐 **Cloud Integration**: Save user emotion history for analytics.
- 🤝 **Multi-User Support**: Personalize responses for multiple users.
- 📈 **Emotion Trends**: Display mood trends over time.
- 📱 **Mobile App**: Bring the Smart Mirror experience to smartphones.

---

## 🙌 Contribution Guidelines

We welcome contributions! 🎉

1. Fork the repo.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Create a pull request.

---

## 📜 License

This project is licensed under the Scaler School of Technology. 📝

---

## 🤗 Feedback & Support

If you enjoy using **Smart Mirror**, give it a ⭐! For issues or suggestions, open an issue or drop us an email at **harshit.tiwari080805@gmail.com**.

---

### 🌟 Remember: "Your reflection isn't just what you see; it's how you feel!"

