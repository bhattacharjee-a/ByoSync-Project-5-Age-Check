# Age Check with Boolean Privacy Demo

## ByoSync Internship Project - Project 5

A privacy-focused age verification system that determines whether a user is above a specified age threshold without exposing the exact estimated age to normal users.

---

## Project Objective

Traditional age estimation systems reveal a user's exact predicted age, which may expose unnecessary personal information.

This project follows a **Boolean Privacy** approach:

- User uploads an image
- System estimates age internally
- User receives only:
  - PASS
  - FAIL
  - INCONCLUSIVE
- Exact age is hidden from normal users

Example response:

```json
{
  "threshold": 21,
  "is_above_threshold": true,
  "confidence": 0.65,
  "decision": "PASS"
}
```

---

## Features

### Age Verification
Supports:

- 18+
- 21+
- 60+

### Face Detection
- OpenCV Haar Cascade Face Detection
- Rejects images with:
  - No face detected
  - Multiple faces detected

### Privacy Protection
Normal users receive:

- Threshold
- Pass / Fail / Inconclusive
- Confidence Score

Normal users never receive:

- Predicted Age
- Face Embeddings
- Biometric Templates

### Debug/Admin Mode

When `DEBUG_MODE=True`:

- Predicted age becomes visible
- Face detection visualization is enabled
- Additional logs are generated

### Logging

Application activity is logged using Python Logging.

### Local Storage

Verification results are stored locally using JSON.

No database is required.

## Stretch Goals Completed

### Multiple Boolean Age Checks

The system supports evaluating a single image against multiple age thresholds in one request.

Example thresholds:
- 18+
- 21+
- 60+

Features:
- Upload one image and evaluate multiple thresholds simultaneously.
- Public API returns only boolean decisions and confidence values.
- Exact age remains hidden from public users.
- Admin/Debug mode can display estimated age for testing.
- Reduces repeated uploads and improves usability.

Example:

```json
{
  "results": [
    {
      "threshold": 18,
      "is_above_threshold": true,
      "decision": "PASS"
    },
    {
      "threshold": 21,
      "is_above_threshold": true,
      "decision": "PASS"
    },
    {
      "threshold": 60,
      "is_above_threshold": false,
      "decision": "FAIL"
    }
  ]
}

```

---
## Project Structure

```text
ByoSync-Project-5-Age-Check/

│
├── ML_models/
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_default.xml
│   └── haarcascade_smile.xml
│
├── app/
│   ├── main.py
│   └── schemas.py
│
├── tests/
│   ├── test_api.py
│   └── test_security.py
│
├── User_interface.py
├── Welcome_page.py
├── constants.py
├── final_draft.py
├── model.py
├── repository.py
├── project_log.py
├── requirements.txt
├── project_blueprint.txt
└── .gitignore
```

---

## Technology Stack

- Python 3.12
- OpenCV
- DeepFace
- FastAPI
- NumPy
- JSON
- Pytest

---

## Installation

Clone repository:

```bash
git clone https://github.com/bhattacharjee-a/ByoSync-Project-5-Age-Check.git
```

Move into project directory:

```bash
cd ByoSync-Project-5-Age-Check
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Console Version

```bash
python final_draft.py
```

### FastAPI Version

```bash
uvicorn app.main:app --reload
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Verification Logic

### Input

- Image
- Threshold

### Internal Processing

1. Detect face
2. Estimate age using DeepFace
3. Compare age with threshold
4. Calculate confidence
5. Generate decision

### Decision Rules

PASS

```text
Predicted Age >= Threshold
```

FAIL

```text
Predicted Age < Threshold
```

INCONCLUSIVE

```text
Difference <= 2 years
```

---

## Example Output

```json
{
  "threshold": 18,
  "is_above_threshold": true,
  "confidence": 0.50,
  "decision": "PASS"
}
```

---

## Privacy Considerations

This project demonstrates a privacy-preserving design pattern.

Normal users cannot access:

- Exact age
- Face embeddings
- Raw biometric templates

Only threshold-based verification is returned.

---

## Testing

Run tests:

```bash
pytest
```

Current tests:

- API Validation
- Security Validation
- Input Validation

---

## Future Improvements

- Streamlit User Interface
- InsightFace integration
- Activity log dashboard
- Batch image processing

---

## Team Members

### Abhiroop Bhattacharjee
- Project Architecture
- Age Detection Module
- Face Detection Module
- Repository Layer
- Logging System
- Verification Logic
- Testing
- Documentation

### Ukarsh Tyagi
- FastAPI Development
- Integration Support
- Streamlit Support
- Testing Support

### Akankhya
- UI Design Planning
- User Experience Review

### Deshna
- Dataset Analysis
- Testing
- Validation Support

### Shubhangi
- Project Reporting
- Documentation Support

### Harshita
- Team Member

---

## Disclaimer

This project was developed as part of the ByoSync Internship Program for educational and learning purposes.

It is not intended for production deployment and does not claim compliance with commercial privacy, biometric, or regulatory standards.
