import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import boto3
from ..core.config import settings


async def generate_certificate_pdf(candidate, assignment, score, certificate_number):
    """Generate a PDF certificate for a completed assignment"""
    
    # Create PDF filename
    filename = f"certificate_{certificate_number}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = f"/tmp/{filename}"
    
    # Create PDF document
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkgreen
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        alignment=TA_LEFT
    )
    
    # Add certificate title
    story.append(Paragraph("Certificate of Completion", title_style))
    story.append(Spacer(1, 20))
    
    # Add company logo/name
    story.append(Paragraph("Logbiz Group", subtitle_style))
    story.append(Spacer(1, 30))
    
    # Add certificate content
    story.append(Paragraph(
        f"This is to certify that <b>{candidate.full_name}</b> has successfully completed the assignment:",
        body_style
    ))
    story.append(Spacer(1, 20))
    
    # Assignment details
    assignment_details = [
        ["Assignment:", assignment.title],
        ["Project:", assignment.project.name],
        ["Domain:", assignment.project.domain or "N/A"],
        ["Difficulty Level:", assignment.difficulty_level.title()],
        ["Skills Demonstrated:", ", ".join(assignment.skillsets)],
        ["Score Achieved:", f"{score}%"],
        ["Certificate Number:", certificate_number],
        ["Date Issued:", datetime.utcnow().strftime("%B %d, %Y")]
    ]
    
    assignment_table = Table(assignment_details, colWidths=[2*inch, 4*inch])
    assignment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ]))
    
    story.append(assignment_table)
    story.append(Spacer(1, 30))
    
    # Add completion message
    if score >= 70:
        story.append(Paragraph(
            f"Congratulations! {candidate.full_name} has demonstrated excellent proficiency in the required skills and has successfully completed this assignment with a score of {score}%.",
            body_style
        ))
    else:
        story.append(Paragraph(
            f"{candidate.full_name} has completed this assignment with a score of {score}%. While this represents progress, further development in the required skills is recommended.",
            body_style
        ))
    
    story.append(Spacer(1, 30))
    
    # Add signature section
    signature_data = [
        ["", "", ""],
        ["_________________", "_________________", "_________________"],
        ["HR Manager", "Technical Lead", "Date"],
    ]
    
    signature_table = Table(signature_data, colWidths=[2*inch, 2*inch, 2*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    story.append(signature_table)
    story.append(Spacer(1, 20))
    
    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Paragraph(
        "This certificate is issued by Logbiz Group. For verification, please visit our certificate verification portal.",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    
    # Upload to S3 if configured
    if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            with open(filepath, 'rb') as file:
                s3_client.upload_fileobj(
                    file,
                    settings.S3_BUCKET,
                    f"certificates/{filename}",
                    ExtraArgs={'ContentType': 'application/pdf'}
                )
            
            # Generate public URL
            pdf_url = f"https://{settings.S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/certificates/{filename}"
            
            # Clean up local file
            os.remove(filepath)
            
            return pdf_url
            
        except Exception as e:
            # If S3 upload fails, return local file path
            print(f"S3 upload failed: {e}")
            return f"file://{filepath}"
    else:
        # Return local file path if S3 not configured
        return f"file://{filepath}"


async def verify_certificate_number(certificate_number):
    """Verify if a certificate number is valid"""
    # This would typically check against the database
    # For now, just check the format
    if not certificate_number or not certificate_number.startswith("CERT-"):
        return False
    
    if len(certificate_number) != 13:  # CERT-XXXXXXXX
        return False
    
    return True 