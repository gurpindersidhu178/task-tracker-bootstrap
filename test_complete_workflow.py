#!/usr/bin/env python3
"""
Complete workflow test script for the CV submission system
Tests: CV upload, parsing, profile generation, and email assignment
"""

import requests
import json
import time
import os
from pathlib import Path

def test_complete_workflow():
    print("🚀 Testing Complete CV Submission Workflow")
    print("=" * 50)
    
    # Test 1: API Health Check
    print("\n1️⃣ Testing API Health...")
    try:
        response = requests.get("http://localhost:5050/healthz")
        if response.status_code == 200:
            print("✅ API is healthy")
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return
    
    # Test 2: CV Upload with Real PDF
    print("\n2️⃣ Testing CV Upload with Real PDF...")
    test_pdf_path = "test_cv.pdf"
    
    if not os.path.exists(test_pdf_path):
        print(f"❌ Test PDF not found: {test_pdf_path}")
        return
    
    try:
        with open(test_pdf_path, 'rb') as f:
            files = {'file': ('test_cv.pdf', f, 'application/pdf')}
            data = {
                'name': 'John Doe',
                'email': 'john.doe@test.com',
                'skills': 'JavaScript, React, Node.js, Python, MongoDB'
            }
            
            response = requests.post("http://localhost:5050/upload", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ CV uploaded successfully")
                print(f"   📄 Parsed text length: {len(result.get('parsed_text', ''))} characters")
                print(f"   🎯 Extracted skills: {result.get('extracted_skills', [])}")
                print(f"   📧 Email sent: {result.get('email_sent', False)}")
                
                # Test 3: Check if profile was created
                print("\n3️⃣ Checking Profile Generation...")
                # Look for profile files in the parse_and_assign_api directory
                profile_dir = Path("parse_and_assign_api")
                profile_files = list(profile_dir.glob("*_full_profile.json")) + list(profile_dir.glob("*_profile.json"))
                
                if profile_files:
                    latest_profile = max(profile_files, key=lambda p: p.stat().st_mtime)
                    print(f"✅ Profile JSON file found: {latest_profile.name}")
                    with open(latest_profile, 'r') as f:
                        profile = json.load(f)
                    print(f"   📋 Profile contains {len(profile)} fields")
                    print(f"   🎯 Skills in profile: {profile.get('skills', [])}")
                    print(f"   📧 Email: {profile.get('email', 'N/A')}")
                else:
                    print("❌ Profile JSON file not found")
                    
            else:
                print(f"❌ CV upload failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
    except Exception as e:
        print(f"❌ CV upload error: {e}")
    
    # Test 4: Test with different skill combinations
    print("\n4️⃣ Testing Skill Extraction...")
    test_skills = [
        "JavaScript, React, Node.js",
        "Python, Django, PostgreSQL", 
        "Java, Spring Boot, MySQL",
        "DevOps, Docker, AWS"
    ]
    
    for skills in test_skills:
        try:
            with open(test_pdf_path, 'rb') as f:
                files = {'file': ('test_cv.pdf', f, 'application/pdf')}
                data = {
                    'name': f'Test User {skills[:10]}',
                    'email': f'test.{skills[:10].lower().replace(", ", "_")}@example.com',
                    'skills': skills
                }
                
                response = requests.post("http://localhost:5050/upload", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Skills '{skills}': Upload successful")
                    print(f"   🎯 Extracted: {result.get('extracted_skills', [])}")
                else:
                    print(f"❌ Skills '{skills}': Failed - {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Skills '{skills}': Error - {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Complete Workflow Test Finished!")
    print("\n📋 Next Steps:")
    print("1. Check email inbox for assignment emails")
    print("2. Verify profile JSON files in /tmp/")
    print("3. Test the main career form at http://localhost:3000")
    print("4. Review server logs for any errors")

if __name__ == "__main__":
    test_complete_workflow() 