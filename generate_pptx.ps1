# PowerShell Script to Generate 16:9 PowerPoint Presentation for Diabetes Risk AI Project
# With full-bleed dark slate background, proper alignment, high contrast & embedded screenshots

function Get-Rgb([int]$r, [int]$g, [int]$b) {
    return [int]($r + ($g * 256) + ($b * 65536))
}

# Color Palette (Modern Dark Theme)
$C_BG        = Get-Rgb 11 15 25      # Deep Slate #0B0F19
$C_CARD      = Get-Rgb 21 30 46      # Slate 900 #151E2E
$C_CARD_BRD  = Get-Rgb 42 56 82      # Slate 700 border #2A3852
$C_TEXT_PRI  = Get-Rgb 248 250 252   # Bright White #F8FAFC
$C_TEXT_MUT  = Get-Rgb 148 163 184   # Slate 400 #94A3B8
$C_BLUE      = Get-Rgb 56 189 248    # Sky Blue #38BDF8
$C_GREEN     = Get-Rgb 74 222 128    # Emerald Green #4ADE80
$C_AMBER     = Get-Rgb 251 191 36    # Amber Yellow #FBBF24
$C_RED       = Get-Rgb 248 113 113   # Rose Red #F87171
$C_PURPLE    = Get-Rgb 192 132 252   # Purple #C084FC

$outputPath = "c:\Users\USER\Downloads\Programs\AI project\Diabetes_AI_Presentation.pptx"

Write-Host "Initializing PowerPoint COM application..."
$ppt = New-Object -ComObject PowerPoint.Application
$pres = $ppt.Presentations.Add([Microsoft.Office.Core.MsoTriState]::msoTrue)

# Set 16:9 Widescreen (960 x 540 points)
$pres.PageSetup.SlideWidth = 960
$pres.PageSetup.SlideHeight = 540

function New-Slide([int]$slideNum) {
    $s = $pres.Slides.Add($slideNum, 12) # 12 = ppLayoutBlank
    # Add reliable full-bleed background rectangle
    $bg = $s.Shapes.AddShape(1, 0, 0, 960, 540) # 1 = msoShapeRectangle
    $bg.Fill.Solid()
    $bg.Fill.ForeColor.RGB = $C_BG
    $bg.Line.Visible = 0
    $bg.ZOrder(1) # 1 = msoSendToBack
    return $s
}

function Add-Header($slide, [string]$tag, [string]$title, [int]$accentColor) {
    # Category Tag
    $tbTag = $slide.Shapes.AddTextbox(1, 45, 20, 500, 18)
    $tbTag.TextFrame.MarginLeft = 0; $tbTag.TextFrame.MarginTop = 0
    $tbTag.TextFrame.TextRange.Text = $tag.ToUpper()
    $tbTag.TextFrame.TextRange.Font.Name = "Segoe UI"
    $tbTag.TextFrame.TextRange.Font.Size = 9.5
    $tbTag.TextFrame.TextRange.Font.Bold = -1
    $tbTag.TextFrame.TextRange.Font.Color.RGB = $accentColor
    
    # Title
    $tbTitle = $slide.Shapes.AddTextbox(1, 45, 38, 850, 36)
    $tbTitle.TextFrame.MarginLeft = 0; $tbTitle.TextFrame.MarginTop = 0
    $tbTitle.TextFrame.TextRange.Text = $title
    $tbTitle.TextFrame.TextRange.Font.Name = "Segoe UI"
    $tbTitle.TextFrame.TextRange.Font.Size = 21
    $tbTitle.TextFrame.TextRange.Font.Bold = -1
    $tbTitle.TextFrame.TextRange.Font.Color.RGB = $C_TEXT_PRI
    
    # Accent Underline Bar
    $bar = $slide.Shapes.AddShape(1, 45, 78, 55, 3) # 1 = msoShapeRectangle
    $bar.Fill.Solid()
    $bar.Fill.ForeColor.RGB = $accentColor
    $bar.Line.Visible = 0
}

function Add-Footer($slide, [int]$slideNum, [string]$speaker) {
    # Project & Course Label
    $tbLeft = $slide.Shapes.AddTextbox(1, 45, 502, 450, 20)
    $tbLeft.TextFrame.MarginLeft = 0; $tbLeft.TextFrame.MarginTop = 0
    $tbLeft.TextFrame.TextRange.Text = "Essentials of AI - Group Project | Diabetes Risk & Lifestyle Advisor"
    $tbLeft.TextFrame.TextRange.Font.Name = "Segoe UI"
    $tbLeft.TextFrame.TextRange.Font.Size = 9
    $tbLeft.TextFrame.TextRange.Font.Color.RGB = $C_TEXT_MUT
    
    # Speaker Tag
    $tbMid = $slide.Shapes.AddTextbox(1, 520, 502, 280, 20)
    $tbMid.TextFrame.MarginLeft = 0; $tbMid.TextFrame.MarginTop = 0
    $tbMid.TextFrame.TextRange.Text = "Speaker: " + $speaker
    $tbMid.TextFrame.TextRange.Font.Name = "Segoe UI"
    $tbMid.TextFrame.TextRange.Font.Size = 9
    $tbMid.TextFrame.TextRange.Font.Bold = -1
    $tbMid.TextFrame.TextRange.Font.Color.RGB = $C_BLUE
    
    # Slide Number
    $tbRight = $slide.Shapes.AddTextbox(1, 840, 502, 75, 20)
    $tbRight.TextFrame.MarginLeft = 0; $tbRight.TextFrame.MarginTop = 0
    $tbRight.TextFrame.TextRange.ParagraphFormat.Alignment = 3 # Right
    $tbRight.TextFrame.TextRange.Text = [string]$slideNum + " / 12"
    $tbRight.TextFrame.TextRange.Font.Name = "Segoe UI"
    $tbRight.TextFrame.TextRange.Font.Size = 9
    $tbRight.TextFrame.TextRange.Font.Color.RGB = $C_TEXT_MUT
}

function Add-Card($slide, [float]$x, [float]$y, [float]$w, [float]$h, [int]$fillColor, [int]$borderColor) {
    $card = $slide.Shapes.AddShape(5, $x, $y, $w, $h) # 5 = msoShapeRoundedRectangle
    $card.Fill.Solid()
    $card.Fill.ForeColor.RGB = $fillColor
    $card.Line.ForeColor.RGB = $borderColor
    $card.Line.Weight = 1
    $card.TextFrame.WordWrap = -1
    $card.TextFrame.MarginLeft = 16
    $card.TextFrame.MarginRight = 16
    $card.TextFrame.MarginTop = 14
    $card.TextFrame.MarginBottom = 12
    return $card
}

# ==========================================
# SLIDE 1: TITLE SLIDE
# ==========================================
Write-Host "Generating Slide 1: Title..."
$s1 = New-Slide 1

$tbTag1 = $s1.Shapes.AddTextbox(1, 45, 42, 870, 25)
$tbTag1.TextFrame.TextRange.ParagraphFormat.Alignment = 2 # Center
$tbTag1.TextFrame.TextRange.Text = "ESSENTIALS OF ARTIFICIAL INTELLIGENCE - FINAL GROUP PROJECT"
$tbTag1.TextFrame.TextRange.Font.Name = "Segoe UI"
$tbTag1.TextFrame.TextRange.Font.Size = 10
$tbTag1.TextFrame.TextRange.Font.Bold = -1
$tbTag1.TextFrame.TextRange.Font.Color.RGB = $C_BLUE

$tbTitle1 = $s1.Shapes.AddTextbox(1, 45, 72, 870, 55)
$tbTitle1.TextFrame.TextRange.ParagraphFormat.Alignment = 2 # Center
$tbTitle1.TextFrame.TextRange.Text = "Diabetes Risk & Lifestyle Advisor"
$tbTitle1.TextFrame.TextRange.Font.Name = "Segoe UI"
$tbTitle1.TextFrame.TextRange.Font.Size = 34
$tbTitle1.TextFrame.TextRange.Font.Bold = -1
$tbTitle1.TextFrame.TextRange.Font.Color.RGB = $C_TEXT_PRI

$tbSub1 = $s1.Shapes.AddTextbox(1, 45, 132, 870, 30)
$tbSub1.TextFrame.TextRange.ParagraphFormat.Alignment = 2 # Center
$tbSub1.TextFrame.TextRange.Text = "A Multi-Stage Decision Support System Combining Machine Learning, Fuzzy Logic & Expert Rules"
$tbSub1.TextFrame.TextRange.Font.Name = "Segoe UI"
$tbSub1.TextFrame.TextRange.Font.Size = 13
$tbSub1.TextFrame.TextRange.Font.Color.RGB = $C_TEXT_MUT

$pipeCard = Add-Card $s1 90 178 780 82 (Get-Rgb 16 28 48) $C_BLUE
$tfP = $pipeCard.TextFrame
$tfP.MarginLeft = 20; $tfP.MarginTop = 14; $tfP.MarginRight = 20
$trP = $tfP.TextRange
$trP.Text = "STAGE 1: Neural Network (MLP)     ->     STAGE 2: Fuzzy Logic Engine     ->     STAGE 3: Rule-Based Advisor`r`n[ Continuous Probability 0.0 - 1.0 ]          [ Linguistic Category: Low/Mod/High/Severe ]          [ 25+ Tailored Recommendations ]"
$trP.Font.Name = "Segoe UI"
$trP.Font.Size = 11.5
$trP.Font.Bold = -1
$trP.ParagraphFormat.Alignment = 2 # Center
$trP.Font.Color.RGB = $C_TEXT_PRI

$members = @(
    @{ Name="Member 1"; Role="Overview & Dataset"; Topics="* Problem Statement`r`n* Diabetes Burden & Early Care`r`n* Pima Indians Dataset`r`n* Data Preprocessing Pipeline" },
    @{ Name="Member 2"; Role="Architecture & NN"; Topics="* 3-Stage Sequential Flow`r`n* MLPClassifier Model Design`r`n* Training & Hyperparameters`r`n* Model Evaluation Metrics" },
    @{ Name="Member 3"; Role="Fuzzy Logic & Rules"; Topics="* Why Fuzzy Reasoning?`r`n* 36 Combinatorial Rules`r`n* Rule-Based Expert Advisor`r`n* Streamlit Web Architecture" },
    @{ Name="Member 4"; Role="Demo, Tests & Ethics"; Topics="* Live System Walkthrough`r`n* 10 Test Patient Profiles`r`n* Limitations & Dataset Bias`r`n* Ethical Safeguards & Summary" }
)

$mLefts = @(45, 267, 489, 711)
for ($i = 0; $i -lt 4; $i++) {
    $m = $members[$i]
    $mCard = Add-Card $s1 $mLefts[$i] 285 204 195 $C_CARD $C_CARD_BRD
    $tfM = $mCard.TextFrame
    $tfM.MarginLeft = 14; $tfM.MarginTop = 14; $tfM.MarginRight = 14
    $trM = $tfM.TextRange
    $trM.Text = $m.Name + "`r`n" + $m.Role + "`r`n`r`n" + $m.Topics
    $trM.Font.Name = "Segoe UI"
    $trM.Font.Size = 10.5
    $trM.ParagraphFormat.Alignment = 1 # Left align
    $trM.Font.Color.RGB = $C_TEXT_MUT
    
    $p1 = $trM.Paragraphs(1)
    $p1.Font.Bold = -1; $p1.Font.Size = 13; $p1.Font.Color.RGB = $C_BLUE
    $p2 = $trM.Paragraphs(2)
    $p2.Font.Size = 10; $p2.Font.Bold = -1; $p2.Font.Color.RGB = $C_TEXT_PRI
}

Add-Footer $s1 1 "All Members"

# ==========================================
# SLIDE 2: PROBLEM STATEMENT & MOTIVATION
# ==========================================
Write-Host "Generating Slide 2: Problem Statement..."
$s2 = New-Slide 2
Add-Header $s2 "Project Motivation & Scope" "Problem Statement & Project Goal" $C_RED

$c2_1 = Add-Card $s2 45 95 422 385 (Get-Rgb 35 18 24) (Get-Rgb 185 28 28)
$tf2_1 = $c2_1.TextFrame
$tf2_1.MarginLeft = 18; $tf2_1.MarginTop = 16; $tf2_1.MarginRight = 18
$tr2_1 = $tf2_1.TextRange
$tr2_1.ParagraphFormat.Alignment = 1
$tr2_1.Text = "The Global Diabetes Challenge`r`n`r`n" +
"* Massive Global Prevalence:`r`n  According to the International Diabetes Federation (IDF), over 537 million adults live with diabetes worldwide.`r`n`r`n" +
"* Undiagnosed Burden (~50%):`r`n  Nearly half of all individuals with diabetes remain undiagnosed, delaying essential care until complications arise.`r`n`r`n" +
"* Preventable with Timely Action:`r`n  Clinical studies prove early lifestyle intervention can reduce Type 2 diabetes risk by up to 58%.`r`n`r`n" +
"* Limitations of Standard AI Tools:`r`n  Pure black-box classifiers output raw probabilities (e.g. 0.62) with zero actionable guidance, leaving users without practical lifestyle steps."
$tr2_1.Font.Name = "Segoe UI"; $tr2_1.Font.Size = 10.5; $tr2_1.Font.Color.RGB = $C_TEXT_PRI
$tr2_1.Paragraphs(1).Font.Size = 13.5; $tr2_1.Paragraphs(1).Font.Bold = -1; $tr2_1.Paragraphs(1).Font.Color.RGB = $C_RED

$c2_2 = Add-Card $s2 493 95 422 385 (Get-Rgb 14 36 28) (Get-Rgb 22 163 74)
$tf2_2 = $c2_2.TextFrame
$tf2_2.MarginLeft = 18; $tf2_2.MarginTop = 16; $tf2_2.MarginRight = 18
$tr2_2 = $tf2_2.TextRange
$tr2_2.ParagraphFormat.Alignment = 1
$tr2_2.Text = "Our Hybrid AI Solution`r`n`r`n" +
"* Chained 3-Stage Pipeline:`r`n  Integrates predictive machine learning, fuzzy inference, and expert decision rules into a cohesive clinical workflow.`r`n`r`n" +
"* Nuanced Risk Categorization:`r`n  Instead of binary yes/no, fuzzy logic factors in BMI and physical activity to assess continuous real-world vulnerability.`r`n`r`n" +
"* Personalized Lifestyle Action Plans:`r`n  The expert engine provides 25-30 tailored nutritional, fitness, and medical recommendations customized to individual vitals.`r`n`r`n" +
"* Accessible & Educational:`r`n  Deployed as an interactive web dashboard with transparent disclaimers and immediate visual feedback."
$tr2_2.Font.Name = "Segoe UI"; $tr2_2.Font.Size = 10.5; $tr2_2.Font.Color.RGB = $C_TEXT_PRI
$tr2_2.Paragraphs(1).Font.Size = 13.5; $tr2_2.Paragraphs(1).Font.Bold = -1; $tr2_2.Paragraphs(1).Font.Color.RGB = $C_GREEN

Add-Footer $s2 2 "Member 1"

# ==========================================
# SLIDE 3: DATASET & PREPROCESSING
# ==========================================
Write-Host "Generating Slide 3: Dataset..."
$s3 = New-Slide 3
Add-Header $s3 "Data Engineering & Preparation" "Pima Indians Diabetes Dataset & Preprocessing" $C_AMBER

$c3_1 = Add-Card $s3 45 95 422 385 $C_CARD $C_CARD_BRD
$tf3_1 = $c3_1.TextFrame
$tf3_1.MarginLeft = 18; $tf3_1.MarginTop = 16; $tf3_1.MarginRight = 18
$tr3_1 = $tf3_1.TextRange
$tr3_1.ParagraphFormat.Alignment = 1
$tr3_1.Text = "Dataset Overview & Data Cleaning`r`n`r`n" +
"* Origin & Scope:`r`n  National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK), hosted on UCI Machine Learning Repository.`r`n`r`n" +
"* Cohort Characteristics:`r`n  768 female patients of Pima Native American heritage, aged 21 and older. Target: Outcome (0 = Healthy, 1 = Diabetic).`r`n`r`n" +
"* Biologically Impossible Zeros Imputation:`r`n  Features like Glucose, Blood Pressure, Skin Thickness, Insulin, and BMI had recorded values of 0 (physiologically invalid).`r`n  -> Handled by replacing 0 with NaN, then imputing with feature-specific column medians.`r`n`r`n" +
"* Normalization & Splitting:`r`n  Applied StandardScaler normalization. Split using an 80/20 stratified split to preserve class distribution."
$tr3_1.Font.Name = "Segoe UI"; $tr3_1.Font.Size = 10.5; $tr3_1.Font.Color.RGB = $C_TEXT_MUT
$tr3_1.Paragraphs(1).Font.Size = 13.5; $tr3_1.Paragraphs(1).Font.Bold = -1; $tr3_1.Paragraphs(1).Font.Color.RGB = $C_AMBER

$c3_2 = Add-Card $s3 493 95 422 385 $C_CARD $C_CARD_BRD
$tf3_2 = $c3_2.TextFrame
$tf3_2.MarginLeft = 18; $tf3_2.MarginTop = 16; $tf3_2.MarginRight = 18
$tr3_2 = $tf3_2.TextRange
$tr3_2.ParagraphFormat.Alignment = 1
$tr3_2.Text = "Clinical Features (8 Predictors)`r`n`r`n" +
"1. Pregnancies: Total number of gestation cycles`r`n`r`n" +
"2. Glucose: 2-hour plasma glucose concentration (mg/dL)`r`n`r`n" +
"3. BloodPressure: Diastolic blood pressure (mm Hg)`r`n`r`n" +
"4. SkinThickness: Triceps skinfold measurement (mm)`r`n`r`n" +
"5. Insulin: 2-Hour serum insulin level (uU/mL)`r`n`r`n" +
"6. BMI: Body Mass Index (weight in kg / (height in m)^2)`r`n`r`n" +
"7. DiabetesPedigree: Genetic predisposition score`r`n`r`n" +
"8. Age: Patient age in completed years"
$tr3_2.Font.Name = "Segoe UI"; $tr3_2.Font.Size = 10.5; $tr3_2.Font.Color.RGB = $C_TEXT_PRI
$tr3_2.Paragraphs(1).Font.Size = 13.5; $tr3_2.Paragraphs(1).Font.Bold = -1; $tr3_2.Paragraphs(1).Font.Color.RGB = $C_BLUE

Add-Footer $s3 3 "Member 1"

# ==========================================
# SLIDE 4: SYSTEM ARCHITECTURE
# ==========================================
Write-Host "Generating Slide 4: System Architecture..."
$s4 = New-Slide 4
Add-Header $s4 "Multi-Stage Pipeline" "System Architecture & End-to-End Pipeline" $C_PURPLE

$sBoxW = 272; $sBoxH = 150
$sLefts = @(45, 344, 643)

$box1 = Add-Card $s4 $sLefts[0] 95 $sBoxW $sBoxH (Get-Rgb 16 35 60) $C_BLUE
$tfB1 = $box1.TextFrame; $tfB1.MarginLeft = 14; $tfB1.MarginTop = 12; $tfB1.MarginRight = 14
$trB1 = $tfB1.TextRange
$trB1.ParagraphFormat.Alignment = 1
$trB1.Text = "STAGE 1: NEURAL NETWORK`r`nModel: MLPClassifier (scikit-learn)`r`n`r`n* Takes 8 normalized vitals`r`n* 2 Hidden Layers (16, 8 neurons)`r`n* Output: Risk Probability (0.0 - 1.0)"
$trB1.Font.Name = "Segoe UI"; $trB1.Font.Size = 10.5; $trB1.Font.Color.RGB = $C_TEXT_PRI
$trB1.Paragraphs(1).Font.Bold = -1; $trB1.Paragraphs(1).Font.Color.RGB = $C_BLUE

$box2 = Add-Card $s4 $sLefts[1] 95 $sBoxW $sBoxH (Get-Rgb 14 40 28) $C_GREEN
$tfB2 = $box2.TextFrame; $tfB2.MarginLeft = 14; $tfB2.MarginTop = 12; $tfB2.MarginRight = 14
$trB2 = $tfB2.TextRange
$trB2.ParagraphFormat.Alignment = 1
$trB2.Text = "STAGE 2: FUZZY LOGIC`r`nEngine: scikit-fuzzy (skfuzzy)`r`n`r`n* Combines Risk Prob + BMI + Activity`r`n* 36 Expert Fuzzy Rules (Centroid)`r`n* Output: Risk Category (0 - 100)"
$trB2.Font.Name = "Segoe UI"; $trB2.Font.Size = 10.5; $trB2.Font.Color.RGB = $C_TEXT_PRI
$trB2.Paragraphs(1).Font.Bold = -1; $trB2.Paragraphs(1).Font.Color.RGB = $C_GREEN

$box3 = Add-Card $s4 $sLefts[2] 95 $sBoxW $sBoxH (Get-Rgb 42 28 14) $C_AMBER
$tfB3 = $box3.TextFrame; $tfB3.MarginLeft = 14; $tfB3.MarginTop = 12; $tfB3.MarginRight = 14
$trB3 = $tfB3.TextRange
$trB3.ParagraphFormat.Alignment = 1
$trB3.Text = "STAGE 3: RULE-BASED ENGINE`r`nAdvisor: Python Expert Rules`r`n`r`n* 4 Risk Tiers (Low to Severe)`r`n* 6 Patient Metric Modifiers`r`n* Output: Tailored Advice + Disclaimer"
$trB3.Font.Name = "Segoe UI"; $trB3.Font.Size = 10.5; $trB3.Font.Color.RGB = $C_TEXT_PRI
$trB3.Paragraphs(1).Font.Bold = -1; $trB3.Paragraphs(1).Font.Color.RGB = $C_AMBER

$bBoxH = 215; $bY = 265

$syn1 = Add-Card $s4 $sLefts[0] $bY $sBoxW $bBoxH $C_CARD $C_CARD_BRD
$tfS1 = $syn1.TextFrame; $tfS1.MarginLeft = 14; $tfS1.MarginTop = 14; $tfS1.MarginRight = 14
$trS1 = $tfS1.TextRange
$trS1.ParagraphFormat.Alignment = 1
$trS1.Text = "Data-Driven Prediction`r`n`r`n* Learns complex non-linear clinical interactions across 768 patient records.`r`n* Provides fine-grained statistical calibration rather than arbitrary rules."
$trS1.Font.Name = "Segoe UI"; $trS1.Font.Size = 11; $trS1.Font.Color.RGB = $C_TEXT_MUT
$trS1.Paragraphs(1).Font.Bold = -1; $trS1.Paragraphs(1).Font.Color.RGB = $C_BLUE

$syn2 = Add-Card $s4 $sLefts[1] $bY $sBoxW $bBoxH $C_CARD $C_CARD_BRD
$tfS2 = $syn2.TextFrame; $tfS2.MarginLeft = 14; $tfS2.MarginTop = 14; $tfS2.MarginRight = 14
$trS2 = $tfS2.TextRange
$trS2.ParagraphFormat.Alignment = 1
$trS2.Text = "Nuanced Boundaries`r`n`r`n* Handles gray areas (e.g. BMI 29.8 vs 30.1) using continuous membership curves.`r`n* Balances raw ML risk with physical activity and lifestyle resilience."
$trS2.Font.Name = "Segoe UI"; $trS2.Font.Size = 11; $trS2.Font.Color.RGB = $C_TEXT_MUT
$trS2.Paragraphs(1).Font.Bold = -1; $trS2.Paragraphs(1).Font.Color.RGB = $C_GREEN

$syn3 = Add-Card $s4 $sLefts[2] $bY $sBoxW $bBoxH $C_CARD $C_CARD_BRD
$tfS3 = $syn3.TextFrame; $tfS3.MarginLeft = 14; $tfS3.MarginTop = 14; $tfS3.MarginRight = 14
$trS3 = $tfS3.TextRange
$trS3.ParagraphFormat.Alignment = 1
$trS3.Text = "Deterministic Actionability`r`n`r`n* Translates risk numbers into clear, practical lifestyle guidelines.`r`n* Guarantees consistent safety disclaimers and medical referrals when vitals spike."
$trS3.Font.Name = "Segoe UI"; $trS3.Font.Size = 11; $trS3.Font.Color.RGB = $C_TEXT_MUT
$trS3.Paragraphs(1).Font.Bold = -1; $trS3.Paragraphs(1).Font.Color.RGB = $C_AMBER

Add-Footer $s4 4 "Member 2"

# ==========================================
# SLIDE 5: STAGE 1 — NEURAL NETWORK
# ==========================================
Write-Host "Generating Slide 5: Neural Network..."
$s5 = New-Slide 5
Add-Header $s5 "Stage 1: Predictive Modeling" "Neural Network Model Architecture & Training" $C_BLUE

$c5_1 = Add-Card $s5 45 95 422 385 $C_CARD $C_CARD_BRD
$tf5_1 = $c5_1.TextFrame; $tf5_1.MarginLeft = 18; $tf5_1.MarginTop = 16; $tf5_1.MarginRight = 18
$tr5_1 = $tf5_1.TextRange
$tr5_1.ParagraphFormat.Alignment = 1
$tr5_1.Text = "Model Specifications (MLPClassifier)`r`n`r`n" +
"* Model Framework:`r`n  scikit-learn MLPClassifier (Multi-Layer Perceptron)`r`n`r`n" +
"* Network Topology:`r`n  - Input Layer: 8 neurons (standardized clinical features)`r`n  - Hidden Layer 1: 16 neurons with ReLU activation`r`n  - Hidden Layer 2: 8 neurons with ReLU activation`r`n  - Output Layer: Single probability score via logistic function`r`n`r`n" +
"* Optimization & Training:`r`n  - Solver: Adam (Adaptive Moment Estimation)`r`n  - Max Iterations: 500 epochs (early convergence)`r`n  - Reproducibility: Fixed random_state=42`r`n`r`n" +
"* Continuous Probability Output:`r`n  Invokes model.predict_proba(X)[0][1] to generate continuous risk (0.0 to 1.0) rather than coarse 0/1 binary labels."
$tr5_1.Font.Name = "Segoe UI"; $tr5_1.Font.Size = 10.5; $tr5_1.Font.Color.RGB = $C_TEXT_PRI
$tr5_1.Paragraphs(1).Font.Size = 13.5; $tr5_1.Paragraphs(1).Font.Bold = -1; $tr5_1.Paragraphs(1).Font.Color.RGB = $C_BLUE

$c5_2 = Add-Card $s5 493 95 422 385 $C_CARD $C_CARD_BRD
$tf5_2 = $c5_2.TextFrame; $tf5_2.MarginLeft = 18; $tf5_2.MarginTop = 16; $tf5_2.MarginRight = 18
$tr5_2 = $tf5_2.TextRange
$tr5_2.ParagraphFormat.Alignment = 1
$tr5_2.Text = "Pipeline Integration & Reliability`r`n`r`n" +
"* Preprocessing Guarantee:`r`n  Input patient features are scaled using the pre-fit StandardScaler (scaler.pkl) before inference, preventing feature distortion.`r`n`r`n" +
"* Model Persistence (joblib):`r`n  - Trained weights saved as model.pkl`r`n  - Fitted scaler saved as scaler.pkl`r`n`r`n" +
"* Self-Healing Auto-Training:`r`n  If model.pkl or scaler.pkl are absent when the web app initializes, nn_model.py automatically triggers training on diabetes.csv seamlessly.`r`n`r`n" +
"* Evaluation Metrics:`r`n  Monitored Accuracy, Precision, Recall, F1 Score, and Confusion Matrix during training to ensure balanced clinical sensitivity."
$tr5_2.Font.Name = "Segoe UI"; $tr5_2.Font.Size = 10.5; $tr5_2.Font.Color.RGB = $C_TEXT_MUT
$tr5_2.Paragraphs(1).Font.Size = 13.5; $tr5_2.Paragraphs(1).Font.Bold = -1; $tr5_2.Paragraphs(1).Font.Color.RGB = $C_GREEN

Add-Footer $s5 5 "Member 2"

# ==========================================
# SLIDE 6: STAGE 2 — FUZZY LOGIC
# ==========================================
Write-Host "Generating Slide 6: Fuzzy Logic..."
$s6 = New-Slide 6
Add-Header $s6 "Stage 2: Approximate Reasoning" "Fuzzy Logic Engine & Nuanced Categorization" $C_GREEN

$c6_1 = Add-Card $s6 45 95 422 385 $C_CARD $C_CARD_BRD
$tf6_1 = $c6_1.TextFrame; $tf6_1.MarginLeft = 18; $tf6_1.MarginTop = 16; $tf6_1.MarginRight = 18
$tr6_1 = $tf6_1.TextRange
$tr6_1.ParagraphFormat.Alignment = 1
$tr6_1.Text = "Why Fuzzy Logic & Input Variables`r`n`r`n" +
"* Solving the Crisp Boundary Problem:`r`n  Real-world risk isn't black or white. A patient with BMI 29.9 and another with 30.1 are virtually identical clinically. Fuzzy logic enables continuous degrees of membership.`r`n`r`n" +
"* 3 Antecedent Variables (Inputs):`r`n  1. Risk Probability (0.0 to 1.0): [Low, Medium, High]`r`n  2. BMI (0 to 60 kg/m2): [Underweight, Normal, Overweight, Obese]`r`n  3. Activity Level (0 to 10 scale): [Sedentary, Moderate, Active]`r`n`r`n" +
"* 1 Consequent Variable (Output):`r`n  Risk Category Score (0 to 100):`r`n  - Low: Score <= 25    |  - Moderate: Score 25 to 50`r`n  - High: Score 50 to 75 |  - Severe: Score > 75"
$tr6_1.Font.Name = "Segoe UI"; $tr6_1.Font.Size = 10.5; $tr6_1.Font.Color.RGB = $C_TEXT_PRI
$tr6_1.Paragraphs(1).Font.Size = 13.5; $tr6_1.Paragraphs(1).Font.Bold = -1; $tr6_1.Paragraphs(1).Font.Color.RGB = $C_GREEN

$c6_2 = Add-Card $s6 493 95 422 385 $C_CARD $C_CARD_BRD
$tf6_2 = $c6_2.TextFrame; $tf6_2.MarginLeft = 18; $tf6_2.MarginTop = 16; $tf6_2.MarginRight = 18
$tr6_2 = $tf6_2.TextRange
$tr6_2.ParagraphFormat.Alignment = 1
$tr6_2.Text = "36 Rules & Computational Robustness`r`n`r`n" +
"* 36 Combinatorial Rules:`r`n  Covers all combinations (3 risk levels x 4 BMI categories x 3 activity tiers = 36 rules) to guarantee complete rule coverage.`r`n`r`n" +
"* Membership Geometry:`r`n  Uses trapezoidal functions (trapmf) for extreme boundaries and triangular functions (trimf) with overlaps for intermediate zones.`r`n`r`n" +
"* Centroid Defuzzification:`r`n  Computes the center of gravity of the aggregated fuzzy output set for a smooth continuous risk score.`r`n`r`n" +
"* Production Safeguards:`r`n  - Input Clamping: Prevents out-of-universe exceptions.`r`n  - Cached singleton control system for sub-millisecond execution.`r`n  - Linear fallback mechanism if zero rules trigger."
$tr6_2.Font.Name = "Segoe UI"; $tr6_2.Font.Size = 10.5; $tr6_2.Font.Color.RGB = $C_TEXT_MUT
$tr6_2.Paragraphs(1).Font.Size = 13.5; $tr6_2.Paragraphs(1).Font.Bold = -1; $tr6_2.Paragraphs(1).Font.Color.RGB = $C_BLUE

Add-Footer $s6 6 "Member 3"

# ==========================================
# SLIDE 7: STAGE 3 — RULE-BASED ENGINE
# ==========================================
Write-Host "Generating Slide 7: Rule-Based Engine..."
$s7 = New-Slide 7
Add-Header $s7 "Stage 3: Actionable Advice" "Rule-Based Expert Engine & Personalization" $C_AMBER

$c7_1 = Add-Card $s7 45 95 422 385 $C_CARD $C_CARD_BRD
$tf7_1 = $c7_1.TextFrame; $tf7_1.MarginLeft = 18; $tf7_1.MarginTop = 16; $tf7_1.MarginRight = 18
$tr7_1 = $tf7_1.TextRange
$tr7_1.ParagraphFormat.Alignment = 1
$tr7_1.Text = "4-Tier Baseline Recommendations`r`n`r`n" +
"* Mandatory Disclaimer First:`r`n  Every output begins with an explicit medical disclaimer stating the educational nature of the tool.`r`n`r`n" +
"* Tier 1: Low Risk (4 Base Guidelines):`r`n  Maintain balanced lifestyle, routine annual checkup, hydration, nutritious whole-food diet.`r`n`r`n" +
"* Tier 2: Moderate Risk (4 Proactive Guidelines):`r`n  Schedule fasting plasma glucose test, achieve 150 min/wk moderate exercise, cut refined carbs, track BMI.`r`n`r`n" +
"* Tier 3: High Risk (5 Urgent Guidelines):`r`n  Consult physician within 2 weeks, begin daily glucose logs, adopt low-GI diet, structured daily workouts.`r`n`r`n" +
"* Tier 4: Severe Risk (5 Critical Guidelines):`r`n  Immediate clinical evaluation, mandatory daily logs, medical dietitian meal plan, assess clinical therapy."
$tr7_1.Font.Name = "Segoe UI"; $tr7_1.Font.Size = 10; $tr7_1.Font.Color.RGB = $C_TEXT_PRI
$tr7_1.Paragraphs(1).Font.Size = 13.5; $tr7_1.Paragraphs(1).Font.Bold = -1; $tr7_1.Paragraphs(1).Font.Color.RGB = $C_AMBER

$c7_2 = Add-Card $s7 493 95 422 385 $C_CARD $C_CARD_BRD
$tf7_2 = $c7_2.TextFrame; $tf7_2.MarginLeft = 18; $tf7_2.MarginTop = 16; $tf7_2.MarginRight = 18
$tr7_2 = $tf7_2.TextRange
$tr7_2.ParagraphFormat.Alignment = 1
$tr7_2.Text = "6 Dynamic Clinical Modifiers`r`n`r`n" +
"* Blood Glucose:`r`n  Additional alerts if Glucose > 140 mg/dL (prediabetes threshold) or > 180 mg/dL (acute hyperglycemia).`r`n`r`n" +
"* Body Mass Index (BMI):`r`n  Custom guidance for Underweight (< 18.5), Obese (> 30), and Severely Obese (> 35).`r`n`r`n" +
"* Blood Pressure (BP):`r`n  Cardiovascular warnings if diastolic BP > 90 or > 100 mm Hg.`r`n`r`n" +
"* Insulin & Age Milestones:`r`n  Hyperinsulinemia alerts (> 200 uU/mL) + specialized screening schedules for patients aged > 45 and > 60.`r`n`r`n" +
"* Family Genetic History (Pedigree):`r`n  Increased screening urgency if pedigree score > 0.5 or > 0.8.`r`n`r`n" +
"* Total: 25-30 contextually assembled clinical directives."
$tr7_2.Font.Name = "Segoe UI"; $tr7_2.Font.Size = 10; $tr7_2.Font.Color.RGB = $C_TEXT_MUT
$tr7_2.Paragraphs(1).Font.Size = 13.5; $tr7_2.Paragraphs(1).Font.Bold = -1; $tr7_2.Paragraphs(1).Font.Color.RGB = $C_BLUE

Add-Footer $s7 7 "Member 3"

# ==========================================
# SLIDE 8: WEB INTERFACE & TECH STACK
# ==========================================
Write-Host "Generating Slide 8: Web Interface..."
$s8 = New-Slide 8
Add-Header $s8 "User Experience & Implementation" "Interactive Web Dashboard & Tech Stack" $C_BLUE

$c8_1 = Add-Card $s8 45 95 400 385 $C_CARD $C_CARD_BRD
$tf8_1 = $c8_1.TextFrame; $tf8_1.MarginLeft = 16; $tf8_1.MarginTop = 14; $tf8_1.MarginRight = 16
$tr8_1 = $tf8_1.TextRange
$tr8_1.ParagraphFormat.Alignment = 1
$tr8_1.Text = "Dashboard Capabilities`r`n`r`n" +
"* Responsive 3-Column Input Grid:`r`n  Clean entry fields for all 9 health vitals with tooltips and slider for activity level.`r`n`r`n" +
"* Informative Sidebar Panel:`r`n  Provides pipeline explanation, dataset details, demographic caveats, and project disclaimer.`r`n`r`n" +
"* Asynchronous Execution Indicator:`r`n  Visual spinners show pipeline execution across NN, Fuzzy Logic, and Rule evaluation.`r`n`r`n" +
"* Technology Stack:`r`n  - Streamlit (v1.28+) : Web UI & reactivity`r`n  - scikit-learn : MLP neural network`r`n  - scikit-fuzzy : Fuzzy logic control systems`r`n  - pandas & numpy : Tabular data handling`r`n  - joblib : Scaler & weight serialization"
$tr8_1.Font.Name = "Segoe UI"; $tr8_1.Font.Size = 10; $tr8_1.Font.Color.RGB = $C_TEXT_PRI
$tr8_1.Paragraphs(1).Font.Size = 13.5; $tr8_1.Paragraphs(1).Font.Bold = -1; $tr8_1.Paragraphs(1).Font.Color.RGB = $C_BLUE

$imgFormPath = "c:\Users\USER\Downloads\Programs\AI project\screenshot_form.png"
if (Test-Path $imgFormPath) {
    # Clean card container
    $imgCard1 = Add-Card $s8 465 95 450 385 $C_CARD $C_CARD_BRD
    $pic1 = $s8.Shapes.AddPicture($imgFormPath, 0, -1, 475, 105, 430, 365)
}

Add-Footer $s8 8 "Member 3"

# ==========================================
# SLIDE 9: LIVE DEMO & RESULTS
# ==========================================
Write-Host "Generating Slide 9: Live Demo..."
$s9 = New-Slide 9
Add-Header $s9 "System in Action" "Live Demonstration & Output Synthesis" $C_PURPLE

$c9_1 = Add-Card $s9 45 95 400 385 $C_CARD $C_CARD_BRD
$tf9_1 = $c9_1.TextFrame; $tf9_1.MarginLeft = 16; $tf9_1.MarginTop = 14; $tf9_1.MarginRight = 16
$tr9_1 = $tf9_1.TextRange
$tr9_1.ParagraphFormat.Alignment = 1
$tr9_1.Text = "Sample Patient Assessment`r`n`r`n" +
"* Patient Vitals Input:`r`n  - Age: 33  |  Pregnancies: 1  |  Glucose: 120 mg/dL`r`n  - Blood Pressure: 72 mm Hg  |  Skin Thickness: 29 mm`r`n  - Insulin: 125 uU/mL  |  BMI: 28.0  |  Activity: 5/10`r`n`r`n" +
"* Pipeline Execution Trace:`r`n  1. Neural Network: 38.4% continuous probability`r`n  2. Fuzzy Logic: Synthesizes probability + BMI 28 + moderate activity -> Category Score 46.2 (Moderate Risk)`r`n  3. Rules Advisor: Generates 8 targeted guidelines`r`n`r`n" +
"* Rich UI Results Presentation:`r`n  - Color-coded badges (Green/Yellow/Red/Dark Red)`r`n  - Category icons: Fitness, Diet, Clinical`r`n  - Expandable JSON debug inspectability"
$tr9_1.Font.Name = "Segoe UI"; $tr9_1.Font.Size = 10; $tr9_1.Font.Color.RGB = $C_TEXT_PRI
$tr9_1.Paragraphs(1).Font.Size = 13.5; $tr9_1.Paragraphs(1).Font.Bold = -1; $tr9_1.Paragraphs(1).Font.Color.RGB = $C_PURPLE

$imgResPath = "c:\Users\USER\Downloads\Programs\AI project\screenshot_results.png"
if (Test-Path $imgResPath) {
    $imgCard2 = Add-Card $s9 465 95 450 385 $C_CARD $C_CARD_BRD
    $pic2 = $s9.Shapes.AddPicture($imgResPath, 0, -1, 475, 105, 430, 365)
}

Add-Footer $s9 9 "Member 4"

# ==========================================
# SLIDE 10: TESTING & PIPELINE VALIDATION
# ==========================================
Write-Host "Generating Slide 10: Testing..."
$s10 = New-Slide 10
Add-Header $s10 "Verification & Quality Assurance" "Testing Suite & Pipeline Validation" $C_GREEN

$c10_1 = Add-Card $s10 45 95 422 385 $C_CARD $C_CARD_BRD
$tf10_1 = $c10_1.TextFrame; $tf10_1.MarginLeft = 18; $tf10_1.MarginTop = 16; $tf10_1.MarginRight = 18
$tr10_1 = $tf10_1.TextRange
$tr10_1.ParagraphFormat.Alignment = 1
$tr10_1.Text = "10 Clinical Test Profiles (test_pipeline.py)`r`n`r`n" +
"* Healthy Young Woman (Age 22, BMI 21.5)  -> Low Risk [Passed]`r`n`r`n" +
"* Average Middle-Aged (Age 45, BMI 26.5)  -> Moderate [Passed]`r`n`r`n" +
"* Overweight Sedentary (BMI 32, Act 1/10)   -> Moderate [Passed]`r`n`r`n" +
"* High-Risk Elderly (Age 65, Gluc 155)      -> High Risk [Passed]`r`n`r`n" +
"* Borderline Profiles A & B (Cutoff tests)  -> Smooth curve [Passed]`r`n`r`n" +
"* Active + Family History (Pedigree 1.2)   -> Controlled [Passed]`r`n`r`n" +
"* Extreme High Risk (Gluc 198, BMI 42)    -> Severe Risk [Passed]`r`n`r`n" +
"* Young Underweight (BMI 17.5)             -> Low Risk [Passed]`r`n`r`n" +
"* Isolated Hypertension (BP 105, Gluc 95)  -> Targeted BP [Passed]"
$tr10_1.Font.Name = "Segoe UI"; $tr10_1.Font.Size = 9.5; $tr10_1.Font.Color.RGB = $C_TEXT_PRI
$tr10_1.Paragraphs(1).Font.Size = 13.5; $tr10_1.Paragraphs(1).Font.Bold = -1; $tr10_1.Paragraphs(1).Font.Color.RGB = $C_GREEN

$c10_2 = Add-Card $s10 493 95 422 385 $C_CARD $C_CARD_BRD
$tf10_2 = $c10_2.TextFrame; $tf10_2.MarginLeft = 18; $tf10_2.MarginTop = 16; $tf10_2.MarginRight = 18
$tr10_2 = $tf10_2.TextRange
$tr10_2.ParagraphFormat.Alignment = 1
$tr10_2.Text = "Validation Assertions & Rigor`r`n`r`n" +
"* Neural Network Bounds Assertion:`r`n  Probability strictly verified within [0.0, 1.0] across all profiles with no NaN or infinite results.`r`n`r`n" +
"* Fuzzy Engine Completeness Assertion:`r`n  Asserts category key exists in {'Low', 'Moderate', 'High', 'Severe'} and score is within [0, 100]. Confirms zero runtime crashes from edge metrics.`r`n`r`n" +
"* Rule Safety Invariant Assertion:`r`n  Verifies list contains >= 2 recommendations and the first item strictly matches the required medical disclaimer.`r`n`r`n" +
"* Clinical Coherence:`r`n  Verified that extreme risk profiles reliably elevate to High/Severe, and healthy profiles remain at Low."
$tr10_2.Font.Name = "Segoe UI"; $tr10_2.Font.Size = 10; $tr10_2.Font.Color.RGB = $C_TEXT_MUT
$tr10_2.Paragraphs(1).Font.Size = 13.5; $tr10_2.Paragraphs(1).Font.Bold = -1; $tr10_2.Paragraphs(1).Font.Color.RGB = $C_BLUE

Add-Footer $s10 10 "Member 4"

# ==========================================
# SLIDE 11: LIMITATIONS & ETHICS
# ==========================================
Write-Host "Generating Slide 11: Limitations & Ethics..."
$s11 = New-Slide 11
Add-Header $s11 "Responsible AI Principles" "Limitations & Ethical Considerations" $C_AMBER

$c11_1 = Add-Card $s11 45 95 422 385 (Get-Rgb 35 24 16) (Get-Rgb 217 119 6)
$tf11_1 = $c11_1.TextFrame; $tf11_1.MarginLeft = 18; $tf11_1.MarginTop = 16; $tf11_1.MarginRight = 18
$tr11_1 = $tf11_1.TextRange
$tr11_1.ParagraphFormat.Alignment = 1
$tr11_1.Text = "Identified Project Limitations`r`n`r`n" +
"* Demographic & Geographic Bias:`r`n  The Pima Indians dataset comprises solely adult females of Pima heritage from a historical study. Findings may not generalize accurately across male, pediatric, or diverse ethnic cohorts.`r`n`r`n" +
"* Limited Clinical Biomarkers:`r`n  The model relies on 8 basic metrics. Real clinical diagnoses evaluate HbA1c, continuous glucose telemetry, lipid panels, and comprehensive dietary histories.`r`n`r`n" +
"* Sample Volume Limitations:`r`n  768 records is relatively small for deep generalization, necessitating lightweight architectures to prevent overfitting."
$tr11_1.Font.Name = "Segoe UI"; $tr11_1.Font.Size = 10.5; $tr11_1.Font.Color.RGB = $C_TEXT_PRI
$tr11_1.Paragraphs(1).Font.Size = 13.5; $tr11_1.Paragraphs(1).Font.Bold = -1; $tr11_1.Paragraphs(1).Font.Color.RGB = $C_AMBER

$c11_2 = Add-Card $s11 493 95 422 385 (Get-Rgb 14 36 28) (Get-Rgb 22 163 74)
$tf11_2 = $c11_2.TextFrame; $tf11_2.MarginLeft = 18; $tf11_2.MarginTop = 16; $tf11_2.MarginRight = 18
$tr11_2 = $tf11_2.TextRange
$tr11_2.ParagraphFormat.Alignment = 1
$tr11_2.Text = "Proactive Ethical Safeguards`r`n`r`n" +
"* Educational Screening Tool Framing:`r`n  System explicitly self-identifies as an educational screener, never as a diagnostic authority. Disclaimers are displayed prominently.`r`n`r`n" +
"* Privacy by Design:`r`n  No patient data, identifiers, or prediction logs are saved to disk or transmitted to third-party APIs. Processing runs entirely in local ephemeral session memory.`r`n`r`n" +
"* Asymmetric Risk Mitigation:`r`n  High and Severe tiers mandate professional medical consultation within defined timeframes (e.g. 2 weeks or immediate).`r`n`r`n" +
"* Explainable Decision Logic:`r`n  Users can trace exactly how their vitals produced their risk category."
$tr11_2.Font.Name = "Segoe UI"; $tr11_2.Font.Size = 10.5; $tr11_2.Font.Color.RGB = $C_TEXT_PRI
$tr11_2.Paragraphs(1).Font.Size = 13.5; $tr11_2.Paragraphs(1).Font.Bold = -1; $tr11_2.Paragraphs(1).Font.Color.RGB = $C_GREEN

Add-Footer $s11 11 "Member 4"

# ==========================================
# SLIDE 12: CONCLUSION & FUTURE WORK
# ==========================================
Write-Host "Generating Slide 12: Conclusion..."
$s12 = New-Slide 12
Add-Header $s12 "Wrap-Up & Submission" "Conclusion, Future Work & Deliverables" $C_BLUE

$c12_1 = Add-Card $s12 45 95 422 385 $C_CARD $C_CARD_BRD
$tf12_1 = $c12_1.TextFrame; $tf12_1.MarginLeft = 18; $tf12_1.MarginTop = 16; $tf12_1.MarginRight = 18
$tr12_1 = $tf12_1.TextRange
$tr12_1.ParagraphFormat.Alignment = 1
$tr12_1.Text = "Key Project Achievements`r`n`r`n" +
"* Working Hybrid AI System:`r`n  Successfully chained a neural network (continuous risk), fuzzy logic (linguistic reasoning), and expert rules (custom lifestyle recommendations).`r`n`r`n" +
"* Interactive Web Interface:`r`n  Deployed a polished Streamlit dashboard with real-time risk classification and inspectable pipeline outputs.`r`n`r`n" +
"* Rigorous Automated Validation:`r`n  Validated on 10 synthetic patient profiles with 100% assertion pass rates across all individual stages.`r`n`r`n" +
"* Responsible Healthcare AI:`r`n  Built with medical disclaimers, input validation, and privacy-preserving ephemeral computation."
$tr12_1.Font.Name = "Segoe UI"; $tr12_1.Font.Size = 10.5; $tr12_1.Font.Color.RGB = $C_TEXT_PRI
$tr12_1.Paragraphs(1).Font.Size = 13.5; $tr12_1.Paragraphs(1).Font.Bold = -1; $tr12_1.Paragraphs(1).Font.Color.RGB = $C_BLUE

$c12_2 = Add-Card $s12 493 95 422 385 $C_CARD $C_CARD_BRD
$tf12_2 = $c12_2.TextFrame; $tf12_2.MarginLeft = 18; $tf12_2.MarginTop = 16; $tf12_2.MarginRight = 18
$tr12_2 = $tf12_2.TextRange
$tr12_2.ParagraphFormat.Alignment = 1
$tr12_2.Text = "Future Roadmap & Submission Checklist`r`n`r`n" +
"* Future Technical Roadmap:`r`n  - Retrain on diverse multi-ethnic datasets (NHANES, UK Biobank)`r`n  - Integrate wearable sensors (Fitbit, Apple Watch) for real-time telemetry`r`n  - Explore deep tabular architectures (TabNet, XGBoost)`r`n  - Multi-language localization for global accessibility`r`n`r`n" +
"* Submission Deliverables (Due Oct 9th):`r`n  - Recorded presentation video with presenter view visible`r`n  - Presentation slide deck (PPTX & HTML format)`r`n  - GitHub repository containing clean code, tests & documentation`r`n  - LMS video & repository submission link`r`n`r`n" +
"Thank You! Questions & Viva Discussion Welcome."
$tr12_2.Font.Name = "Segoe UI"; $tr12_2.Font.Size = 10; $tr12_2.Font.Color.RGB = $C_TEXT_MUT
$tr12_2.Paragraphs(1).Font.Size = 13.5; $tr12_2.Paragraphs(1).Font.Bold = -1; $tr12_2.Paragraphs(1).Font.Color.RGB = $C_GREEN
$tr12_2.Paragraphs($tr12_2.Paragraphs.Count).Font.Bold = -1
$tr12_2.Paragraphs($tr12_2.Paragraphs.Count).Font.Color.RGB = $C_BLUE

Add-Footer $s12 12 "All Members"

# Save presentation
Write-Host "Saving presentation to $outputPath..."
$pres.SaveAs($outputPath)
$pres.Close()
$ppt.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "PPTX Generation Complete! Successfully created $outputPath"
