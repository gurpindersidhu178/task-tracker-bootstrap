#!/usr/bin/env python3
"""
Simple script to create a test PDF CV for testing the parsing functionality
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_test_pdf():
    # Read the CV content
    with open('test_cv.txt', 'r') as f:
        cv_content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate("test_cv.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=12
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        spaceBefore=8
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # Parse content and create paragraphs
    story = []
    
    lines = cv_content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.isupper() and len(line) < 50:  # Likely a title
            story.append(Paragraph(line, title_style))
        elif line.endswith(':') or (line.isupper() and len(line) < 30):  # Likely a heading
            story.append(Paragraph(line, heading_style))
        else:
            story.append(Paragraph(line, normal_style))
        
        story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    print("✅ Test CV PDF created: test_cv.pdf")

if __name__ == "__main__":
    create_test_pdf() 