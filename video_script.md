# 🎬 Video Presentation Script
## Diabetes Risk & Lifestyle Advisor — Essentials of AI Group Project

> **Total Duration:** ~14 minutes  
> **Members:** 4  
> **Format:** Screen recording with presenter view (slides + webcam)

---

## 📌 Recording Setup Checklist
- [ ] Open the presentation slides (HTML file in browser, fullscreen)
- [ ] Enable presenter webcam overlay (ensure face is visible)
- [ ] Use screen recording software (OBS, Zoom, Teams, or built-in recorder)
- [ ] Test audio before recording
- [ ] Each member records their section (or record together in one session)

---

---

## 👤 MEMBER 1 — Introduction, Problem Statement & Dataset
**Slides:** 1, 2, 3 | **Duration:** ~3 minutes

---

### 🔹 Slide 1 — Title Slide

> "Hello everyone, and welcome to our group presentation for the Essentials of Artificial Intelligence course."
>
> "Our project is called the **Diabetes Risk and Lifestyle Advisor** — an AI-powered decision support system that predicts diabetes risk and provides personalized lifestyle recommendations."
>
> "My name is [Member 1], and I'll be covering the problem statement and the dataset we used. After me, [Member 2] will explain the system architecture and neural network, [Member 3] will cover fuzzy logic, the rule engine, and the web interface, and [Member 4] will walk you through the demo, testing, and our conclusions."
>
> "Let's get started."

*[Click → Slide 2]*

---

### 🔹 Slide 2 — Problem Statement

> "So, why did we choose this project?"
>
> "Diabetes is one of the biggest health challenges worldwide. According to the International Diabetes Federation, **537 million adults** are living with diabetes globally — and nearly **half of them don't even know they have it**."
>
> "Research shows that early detection and lifestyle changes can **reduce the risk of developing Type 2 diabetes by up to 58 percent**. That's a huge number."
>
> "So our goal was to build a system that can help with early screening. Our solution is a **hybrid AI system** that combines three different AI techniques:"
>
> "First, a **Neural Network** that predicts risk from health data. Second, **Fuzzy Logic** that categorizes that risk in a nuanced way. And third, a **Rule-Based Engine** that generates personalized lifestyle recommendations."
>
> "We also built an **interactive web interface** so anyone can use it easily."

*[Click → Slide 3]*

---

### 🔹 Slide 3 — Dataset

> "For our training data, we used the **Pima Indians Diabetes Dataset**, which is one of the most well-known datasets in medical machine learning."
>
> "It comes from the **National Institute of Diabetes and Digestive and Kidney Diseases** and is hosted on the **UCI Machine Learning Repository**. The dataset contains **768 patient records** with **8 health metric features** and one binary outcome — whether the patient has diabetes or not."
>
> "The 8 features include: Pregnancies, Glucose level, Blood Pressure, Skin Thickness, Insulin level, BMI, a Diabetes Pedigree Function which represents family history, and Age."
>
> "Now, this dataset does have some quality issues — several features contain **zeros that are biologically impossible**, like a blood pressure of zero. So during preprocessing, we **replaced those zeros with NaN values** and then **imputed them using column medians**."
>
> "We also applied **StandardScaler normalization** to bring all features to the same scale, and used an **80/20 stratified train-test split** to ensure balanced class representation."
>
> "I'll now hand over to [Member 2], who will explain how our system architecture works."

---

---

## 👤 MEMBER 2 — System Architecture & Neural Network
**Slides:** 4, 5 | **Duration:** ~3.5 minutes

---

### 🔹 Slide 4 — System Architecture

> "Thank you, [Member 1]. I'm [Member 2], and I'll walk you through our system architecture and the Neural Network component."
>
> "Our system uses a **three-stage sequential pipeline** — each stage feeds its output into the next stage."
>
> "In **Stage 1**, the Neural Network takes raw patient health data — things like glucose level, BMI, age, and blood pressure — and outputs a **continuous risk probability** between 0 and 1."
>
> "In **Stage 2**, the Fuzzy Logic Engine takes that probability along with BMI and the patient's self-reported activity level, and produces a **nuanced risk category**: Low, Moderate, High, or Severe."
>
> "In **Stage 3**, the Rule-Based Engine takes the category plus the original patient metrics and generates a **personalized list of lifestyle and medical recommendations**."
>
> "What makes this design powerful is that each stage contributes something different. The Neural Network is **data-driven** — it learns patterns from real patient records. The Fuzzy Logic is **expert-informed** — it encodes domain knowledge. And the Rule Engine provides **actionable output** — specific advice the patient can follow."
>
> "Let me now dive into Stage 1 in detail."

*[Click → Slide 5]*

---

### 🔹 Slide 5 — Neural Network (Stage 1)

> "For our Neural Network, we used scikit-learn's **MLPClassifier**, which stands for Multi-Layer Perceptron."
>
> "The model has **two hidden layers** — the first with **16 neurons** and the second with **8 neurons**. We use the **ReLU activation function** and the **Adam optimizer**, which is an adaptive learning rate optimizer that works well for this type of problem."
>
> "The model is trained for up to **500 iterations** with a fixed random state of 42 for reproducibility."
>
> "As you can see in the network diagram on the right, the data flows from the **8 input features** through the two hidden layers and finally to a **single output neuron** that gives us the probability of diabetes."
>
> "We use `predict_proba` to get the probability rather than a binary classification — this gives us a much more nuanced output that the fuzzy logic engine can work with."
>
> "For model persistence, we save both the trained model and the scaler using **joblib** — so we don't need to retrain every time. If the saved model isn't found, the system **automatically trains a new one**."
>
> "During training, we evaluate the model using **Accuracy, Precision, Recall, F1 Score, and the Confusion Matrix** to ensure it performs well."
>
> "On the bottom right, you can see our preprocessing code — replacing impossible zero values and applying StandardScaler normalization."
>
> "I'll now hand over to [Member 3] to explain the Fuzzy Logic and Rule-Based components."

---

---

## 👤 MEMBER 3 — Fuzzy Logic, Rule-Based Engine & Web Interface
**Slides:** 6, 7, 8 | **Duration:** ~4 minutes

---

### 🔹 Slide 6 — Fuzzy Logic Engine (Stage 2)

> "Thanks, [Member 2]. I'm [Member 3], and I'll cover the Fuzzy Logic Engine, the Rule-Based Engine, and our web interface."
>
> "So why did we add Fuzzy Logic on top of the Neural Network? The answer is **nuance**."
>
> "A neural network gives us a number — say, 0.52. But what does that mean? Is it moderate risk or high risk? The boundary is sharp and arbitrary."
>
> "Fuzzy Logic solves this by modeling **degrees of truth**. For example, if a patient has a BMI of 29.5, they're not just 'overweight' or 'obese' — they're **partially both**. Fuzzy logic handles this naturally with overlapping membership functions."
>
> "Our fuzzy system has **three input variables**: the neural network's risk probability, the patient's BMI, and their self-reported activity level."
>
> "For the output, we get a **risk category score from 0 to 100**, which maps to four categories: Low if it's 25 or below, Moderate up to 50, High up to 75, and Severe above 75."
>
> "We defined **36 fuzzy rules** — one for every combination of the three input variables. We use a mix of **trapezoidal and triangular membership functions** with overlapping boundaries for smooth transitions."
>
> "The system also has built-in safety features: **input clamping** to avoid edge-case crashes, and a **fallback mechanism** in case no rules fire."

*[Click → Slide 7]*

---

### 🔹 Slide 7 — Rule-Based Engine (Stage 3)

> "The third and final stage is the **Rule-Based Engine**. This is where the AI output gets translated into something **actionable** — real lifestyle and medical recommendations the patient can follow."
>
> "The engine uses **deterministic if/elif logic** in pure Python. Based on the risk category from the fuzzy engine, it generates a **base set of recommendations**:"
>
> "For **Low Risk**, there are 4 maintenance recommendations — things like maintaining your current lifestyle and getting annual check-ups."
>
> "For **Moderate Risk**, there are 4 proactive recommendations — like getting a fasting glucose test and exercising 150 minutes per week."
>
> "For **High Risk**, there are 5 urgent recommendations — including seeing a doctor within 2 weeks and daily glucose monitoring."
>
> "And for **Severe Risk**, there are 5 critical recommendations — like immediate medical consultation and mandatory daily monitoring."
>
> "But it doesn't stop there. We also have **6 metric-specific modifiers** that add extra recommendations based on individual values — such as high glucose, high BMI, elevated blood pressure, high insulin, age, and family history."
>
> "In total, the system can select from roughly **25 to 30 distinct recommendations** per patient, making the advice truly personalized."
>
> "And importantly, the **very first recommendation is always a medical disclaimer** — reminding users that this is a screening tool, not a medical diagnosis."

*[Click → Slide 8]*

---

### 🔹 Slide 8 — Web Interface

> "For the user interface, we built an **interactive web dashboard using Streamlit**."
>
> "The interface features a clean **input form with 9 health metric fields** arranged in a 3-column layout. Users enter their health data — things like glucose level, BMI, blood pressure, age, and activity level."
>
> "On the sidebar, there's information about the system, the dataset, known limitations, and the tech stack."
>
> "When the user clicks **'Analyze Risk'**, the system runs all three stages of the pipeline and displays the results with **color-coded risk badges** — green for Low, yellow for Moderate, red for High, and dark red for Severe."
>
> "The recommendations are displayed with **context-aware icons** — a running emoji for exercise tips, a salad for diet advice, a hospital for medical recommendations, and so on."
>
> "There's also an **expandable detailed breakdown** that shows the JSON inputs and outputs for each pipeline stage — useful for debugging and understanding how the system arrived at its conclusions."
>
> "Our tech stack includes Streamlit for the web framework, scikit-learn for the neural network, scikit-fuzzy for the fuzzy logic, pandas and numpy for data processing, and joblib for model serialization."
>
> "I'll now hand over to [Member 4] for the live demo and our conclusions."

---

---

## 👤 MEMBER 4 — Demo, Testing, Limitations & Conclusion
**Slides:** 9, 10, 11, 12 | **Duration:** ~3.5 minutes

---

### 🔹 Slide 9 — Live Demo

> "Thank you, [Member 3]. I'm [Member 4], and I'll demonstrate the system in action, walk through our testing, discuss limitations, and wrap up."
>
> "Let me switch to a screen share to show you the running application."

*[Switch to screen share showing the Streamlit app running]*

> "Here you can see our Streamlit dashboard. I'll enter some sample data for a test patient. Let's say: 1 pregnancy, glucose of 120, blood pressure of 72, skin thickness of 29, insulin of 125, BMI of 28, a family history score of 0.3725, age of 33, and an activity level of 5 out of 10."
>
> "Now I'll click **'Analyze Risk'** — and you can see the three stages running in sequence."
>
> "The results show the **neural network probability**, the **fuzzy logic category** with its color-coded badge, and a list of **personalized recommendations**."
>
> "Let me also try a high-risk profile to show the contrast..."
>
> *[Enter high-risk data and show the difference in results]*
>
> "As you can see, the system correctly identifies this as a higher risk case and generates more urgent, specific recommendations."

*[Switch back to presentation slides → Slide 10]*

---

### 🔹 Slide 10 — Testing & Validation

> "For testing, we created a comprehensive **test pipeline with 10 diverse patient profiles** — covering everything from a healthy young woman to an extreme high-risk case."
>
> "Each profile was tested against **all three stages individually** and then through the **full end-to-end pipeline**."
>
> "For the Neural Network, we verify that the output probability is always between 0 and 1. For the Fuzzy Engine, we check that the output contains valid category and score values. And for the Rules Engine, we verify that it always returns at least 2 recommendations and that the first one always contains the disclaimer."
>
> "All 10 profiles passed all assertions, and the system produces **clinically sensible results** — healthy profiles get Low risk, high-risk profiles get High or Severe, and borderline cases fall in between."

*[Click → Slide 11]*

---

### 🔹 Slide 11 — Limitations & Ethical Considerations

> "Now, no system is perfect, and it's important to be transparent about our limitations."
>
> "The biggest limitation is **dataset bias**. Our model was trained exclusively on Pima Native American women from a 1960s study — so it may not generalize well to men, other ethnicities, or younger populations."
>
> "We also only use **8 health metrics** — a real clinical assessment would consider many more factors like HbA1c levels, lifestyle history, and genetic markers."
>
> "And with only **768 records**, our dataset is quite small compared to modern clinical AI systems."
>
> "However, we've built in important **ethical safeguards**. The system is explicitly framed as an **educational screening tool, not a medical diagnosis**. No patient data is stored — everything is processed locally. And we always acknowledge the **potential for errors**, recommending professional consultation alongside every assessment."

*[Click → Slide 12]*

---

### 🔹 Slide 12 — Conclusion

> "To wrap up, here's what we achieved:"
>
> "We built a **hybrid AI system** that successfully combines three different AI techniques — neural networks, fuzzy logic, and rule-based reasoning — into a cohesive pipeline."
>
> "We created an **interactive web interface** using Streamlit that makes the system accessible and easy to use."
>
> "The system provides **personalized risk assessments and lifestyle recommendations**, and we validated it with **10 comprehensive test profiles**."
>
> "We also integrated **ethical considerations from the start** — including disclaimers, privacy safeguards, and transparency about limitations."
>
> "For future work, we'd like to use a **larger and more diverse dataset**, explore **deep learning architectures** like CNNs or LSTMs, integrate **real-time health data from wearables**, add **multi-language support**, and eventually seek **clinical validation with healthcare professionals**."
>
> "Our source code is available on our **GitHub repository**, and you're welcome to try the live demo."
>
> "Thank you for watching our presentation. We're happy to answer any questions!"

---

---

## ⏱️ Time Allocation Summary

| Member | Slides | Topics | Duration |
|--------|--------|--------|----------|
| **Member 1** | 1, 2, 3 | Title, Problem Statement, Dataset | ~3 min |
| **Member 2** | 4, 5 | Architecture, Neural Network | ~3.5 min |
| **Member 3** | 6, 7, 8 | Fuzzy Logic, Rule Engine, Web Interface | ~4 min |
| **Member 4** | 9, 10, 11, 12 | Demo, Testing, Limitations, Conclusion | ~3.5 min |
| **Total** | 12 slides | — | **~14 min** |

---

## 💡 Tips for Recording

1. **Practice** your part 2-3 times before recording
2. **Speak slowly and clearly** — slightly slower than normal conversation
3. **Keep the presenter view visible** as per the submission guidelines
4. **Use a quiet room** with minimal background noise
5. **Look at the camera** occasionally, not just the slides
6. For the **demo section** (Member 4): have the Streamlit app pre-loaded and ready
7. **Smooth transitions**: Each member should briefly introduce the next speaker
8. Consider using **Zoom or Teams** to record — easy to enable presenter + screen share view
