import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, blue, red

def export_docs_as_pdf(state, output_dir="outputs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = state.get("project_docs", "No documentation")
    diagram = state.get("diagram_mermaid", "No diagram")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"{output_dir}/final_docs_{timestamp}.pdf"

    try:
        print("📄 Creating enhanced PDF with ReportLab...")
        
        # Create PDF document with better margins
        pdf_doc = SimpleDocTemplate(
            pdf_filename, 
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        # Enhanced styles
        styles = getSampleStyleSheet()
        
        # Custom styles for better formatting
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#2c3e50'),
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            spaceBefore=25,
            textColor=HexColor('#34495e'),
            borderWidth=1,
            borderColor=HexColor('#3498db'),
            borderPadding=10
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=HexColor('#2c3e50'),
            leftIndent=10
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            leftIndent=10,
            rightIndent=10
        )
        
        code_style = ParagraphStyle(
            'CustomCode',
            parent=styles['Code'],
            fontSize=9,
            spaceAfter=15,
            spaceBefore=10,
            backColor=HexColor('#f8f9fa'),
            borderWidth=1,
            borderColor=HexColor('#dee2e6'),
            borderPadding=10,
            fontName='Courier'
        )
        
        story = []
        
        # Add title with emoji
        title = Paragraph("📝 Project Documentation", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Add timestamp
        timestamp_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        timestamp_para = Paragraph(timestamp_text, styles['Normal'])
        story.append(timestamp_para)
        story.append(Spacer(1, 30))
        
        # Process content with better formatting
        formatted_content = format_markdown_to_paragraphs(doc, styles, heading_style, subheading_style, body_style, code_style)
        story.extend(formatted_content)
        
        # Add page break before diagram
        story.append(PageBreak())
        
        # Add diagram section with better styling
        diagram_title = Paragraph("🔍 Architecture Diagram", heading_style)
        story.append(diagram_title)
        story.append(Spacer(1, 15))
        
        if diagram and diagram.strip():
            # Clean mermaid code for better readability
            cleaned_diagram = diagram.replace('```mermaid', '').replace('```', '').strip()
            
            # Add diagram explanation
            diagram_intro = Paragraph(
                "📊 <b>Architecture Overview:</b><br/>The following represents the project's component structure and relationships.", 
                body_style
            )
            story.append(diagram_intro)
            story.append(Spacer(1, 10))
            
            # Format diagram as structured text instead of raw code
            diagram_lines = cleaned_diagram.split('\n')
            for line in diagram_lines:
                line = line.strip()
                if line:
                    if '-->' in line or '→' in line:
                        # Connection lines - format as flow
                        formatted_line = f"🔗 {line}"
                    elif line.startswith('subgraph') or line.startswith('graph'):
                        # Graph definitions - format as headers
                        formatted_line = f"📦 <b>{line.replace('subgraph', 'Module:').replace('graph TD', 'Diagram Type: Top-Down')}</b>"
                    else:
                        # Component names
                        formatted_line = f"⚡ {line}"
                    
                    para = Paragraph(formatted_line, body_style)
                    story.append(para)
                    story.append(Spacer(1, 5))
        else:
            no_diagram = Paragraph("⚠️ No architecture diagram available for this project.", body_style)
            story.append(no_diagram)
        
        # Add footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=HexColor('#7f8c8d'),
            alignment=TA_CENTER
        )
        footer = Paragraph("Generated by GitHub Repository Analyzer • Powered by AI Agents", footer_style)
        story.append(footer)
        
        # Build PDF
        pdf_doc.build(story)
        
        print(f"✅ Enhanced PDF created: {pdf_filename}")
        state["pdf_path"] = pdf_filename
        state["pdf_status"] = "success"
        
    except Exception as e:
        print(f"❌ PDF creation failed: {e}")
        import traceback
        traceback.print_exc()
        state["pdf_status"] = "error"

    return state

def format_markdown_to_paragraphs(content, styles, heading_style, subheading_style, body_style, code_style):
    """
    Convert markdown content to formatted paragraphs
    """
    paragraphs = []
    lines = content.split('\n')
    
    in_code_block = False
    code_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Handle code blocks
        if line.startswith('```'):
            if in_code_block:
                # End code block
                if code_lines:
                    code_content = '\n'.join(code_lines)
                    code_para = Paragraph(f"<pre>{code_content}</pre>", code_style)
                    paragraphs.append(code_para)
                code_lines = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            continue
        
        if in_code_block:
            code_lines.append(line)
            continue
        
        # Skip empty lines
        if not line:
            paragraphs.append(Spacer(1, 10))
            continue
        
        # Format headers
        if line.startswith('# '):
            text = line[2:].strip()
            para = Paragraph(text, heading_style)
            paragraphs.append(para)
        elif line.startswith('## '):
            text = line[3:].strip()
            para = Paragraph(text, subheading_style)
            paragraphs.append(para)
        elif line.startswith('### '):
            text = line[4:].strip()
            para = Paragraph(f"<b>{text}</b>", body_style)
            paragraphs.append(para)
        # Format lists
        elif line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            para = Paragraph(f"• {text}", body_style)
            paragraphs.append(para)
        # Format bold text
        elif line.startswith('**') and line.endswith('**'):
            text = line[2:-2].strip()
            para = Paragraph(f"<b>{text}</b>", subheading_style)
            paragraphs.append(para)
        # Regular paragraphs
        else:
            # Handle inline formatting
            formatted_line = line
            
            # Bold text
            import re
            formatted_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', formatted_line)
            
            # Inline code
            formatted_line = re.sub(r'`(.*?)`', r'<font name="Courier" backColor="#f1f2f6">\1</font>', formatted_line)
            
            para = Paragraph(formatted_line, body_style)
            paragraphs.append(para)
    
    return paragraphs