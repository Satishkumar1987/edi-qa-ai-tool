from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# =========================================
# HOME ROUTE
# =========================================

@app.route('/')
def home():

    return '''
    <h1>EDI QA AI Tool is Running Successfully 🚀</h1>
    <p>Backend Deployment Successful</p>
    '''

# =========================================
# GENERATE TEST CASES
# =========================================

@app.route('/generate', methods=['POST'])
def generate_test_cases():

    data = request.json

    requirement = data.get("requirement", "").lower()

    # LOGIN TEST CASES

    if "login" in requirement:

        test_cases = [

            {
                "scenario": "Valid Login",
                "steps": "Enter valid username and password",
                "expected": "Login successful",
                "status": "PASS"
            },

            {
                "scenario": "Invalid Login",
                "steps": "Enter wrong password",
                "expected": "Error message displayed",
                "status": "FAIL"
            },

            {
                "scenario": "Empty Fields",
                "steps": "Leave username and password blank",
                "expected": "Validation error shown",
                "status": "FAIL"
            }

        ]

    # EDI TEST CASES

    elif "edi" in requirement or "837" in requirement:

        test_cases = [

            {
                "scenario": "Validate ISA Segment",
                "steps": "Check ISA segment exists",
                "expected": "ISA segment validated",
                "status": "PASS"
            },

            {
                "scenario": "Validate GS Segment",
                "steps": "Check GS segment exists",
                "expected": "GS segment validated",
                "status": "PASS"
            },

            {
                "scenario": "Validate Claim Data",
                "steps": "Verify CLM segment",
                "expected": "Claim processed correctly",
                "status": "FAIL"
            }

        ]

    # DEFAULT TEST CASES

    else:

        test_cases = [

            {
                "scenario": "Basic Validation",
                "steps": "Execute test flow",
                "expected": "System works properly",
                "status": "PASS"
            },

            {
                "scenario": "Negative Validation",
                "steps": "Execute invalid flow",
                "expected": "Validation message shown",
                "status": "FAIL"
            }

        ]

    return jsonify(test_cases)

# =========================================
# EXPORT EXCEL
# =========================================

@app.route('/export_excel', methods=['POST'])
def export_excel():

    try:

        data = request.json

        df = pd.DataFrame(data)

        filename = "QA_Test_Report.xlsx"

        df.to_excel(filename, index=False)

        return send_file(
            filename,
            as_attachment=True
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================================
# VALIDATE EDI FILE
# =========================================

@app.route('/validate_edi', methods=['POST'])
def validate_edi():

    try:

        file = request.files['file']

        content = file.read().decode('utf-8')

        results = []

        # ISA Validation

        if "ISA*" in content:
            results.append("✅ ISA Segment Found")
        else:
            results.append("❌ ISA Segment Missing")

        # GS Validation

        if "GS*" in content:
            results.append("✅ GS Segment Found")
        else:
            results.append("❌ GS Segment Missing")

        # ST Validation

        if "ST*" in content:
            results.append("✅ ST Segment Found")
        else:
            results.append("❌ ST Segment Missing")

        # CLM Validation

        if "CLM*" in content:
            results.append("✅ Claim Segment Found")
        else:
            results.append("❌ Claim Segment Missing")

        return jsonify({
            "result": results
        })

    except Exception as e:

        return jsonify({
            "result": [str(e)]
        })

# =========================================
# START APPLICATION
# =========================================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )