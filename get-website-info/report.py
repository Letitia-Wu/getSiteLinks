#!/usr/bin/env python3

import os
import sys
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(attachment, title, paragraph):
    print("Generating report ...")
    report = SimpleDocTemplate(attachment)
    styles = getSampleStyleSheet()
    report_title = Paragraph(title, styles["h1"])
    empty_line = Spacer(1, 20)
    report_info = Paragraph(paragraph, styles["BodyText"])
    report.build([report_title, empty_line, report_info])
    print("Report generated")
