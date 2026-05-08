# app.py

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# =====================================
# GENERATE TEST CASES
# =====================================

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
                "status": ""
            },

            {
                "scenario": "Invalid Login",
                "steps": "Enter wrong password",
                "expected": "Error message displayed",
                "status": ""
            },

            {
                "scenario": "Empty Fields",
                "steps": "Leave username and password blank",
                "expected": "Validation error shown",
                "status": ""
            }

        ]

    # EDI TEST CASES
    elif "edi" in requirement or "837" in requirement:

        test_cases = [

            {
                "scenario": "Validate ISA Segment",
                "steps": "Upload EDI file with ISA segment",
                "expected": "ISA segment validated",
                "status": ""
            },

            {
                "scenario": "Validate GS Segment",
                "steps": "Upload EDI file with GS segment",
                "expected": "GS segment validated",
                "status": ""
            },

            {
                "scenario": "Validate Claim Number",
                "steps": "Validate CLM segment",
                "expected": "Claim number extracted",
                "status": ""
            }

        ]

    # DEFAULT TEST CASES
    else:

        test_cases = [

            {
                "scenario": "Sample Test",
                "steps": "Execute sample flow",
                "expected": "Application works successfully",
                "status": ""
            }

        ]

    return jsonify(test_cases)

# =====================================
# EDI VALIDATION
# =====================================

@app.route('/validate_edi', methods=['POST'])
def validate_edi():

    file = request.files['file']

    content = file.read().decode('utf-8')

    results = []

    # ISA
    if "ISA*" in content:
        results.append("✅ ISA Segment Found")
    else:
        results.append("❌ ISA Segment Missing")

    # GS
    if "GS*" in content:
        results.append("✅ GS Segment Found")
    else:
        results.append("❌ GS Segment Missing")

    # ST
    if "ST*" in content:
        results.append("✅ ST Segment Found")
    else:
        results.append("❌ ST Segment Missing")

    # CLM
    if "CLM*" in content:

        try:

            claim_line = [
                line for line in content.split("~")
                if "CLM*" in line
            ][0]

            claim_number = claim_line.split("*")[1]

            results.append(
                f"✅ Claim Number Found: {claim_number}"
            )

        except:

            results.append(
                "❌ Claim Segment Error"
            )

    else:

        results.append(
            "❌ Claim Segment Missing"
        )

    return jsonify({
        "result": results
    })

# =====================================
# EXPORT EXCEL
# =====================================

@app.route('/export_excel', methods=['POST'])
def export_excel():

    data = request.json

    df = pd.DataFrame(data)

    filename = "QA_Test_Report.xlsx"

    try:

        if os.path.exists(filename):
            os.remove(filename)

    except:
        pass

    df.to_excel(filename, index=False)

    return send_file(
        filename,
        as_attachment=True,
        download_name="QA_Test_Report.xlsx"
    )

# =====================================
# START APPLICATION
# =====================================

if __name__ == '__main__':
    app.run(debug=True)