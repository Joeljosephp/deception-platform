def generate_report(risk, threat, findings):

    report = "\n"
    report += "=" * 60 + "\n"
    report += "           INCIDENT REPORT\n"
    report += "=" * 60 + "\n"

    report += f"Threat Level : {threat}\n"
    report += f"Risk Score   : {risk}\n\n"

    report += "Evidence:\n"

    # If no findings
    if len(findings) == 0:
        report += " • No suspicious activity detected\n"
    else:
        for item in findings:
            report += f" • {item}\n"

    report += "\nMITRE ATT&CK Mapping\n"

    if "Honeytoken Access" in findings:
        report += " • T1552 - Unsecured Credentials\n"

    if "Fake Document Opened" in findings:
        report += " • T1213 - Data from Information Repositories\n"

    if "Admin API Scan" in findings:
        report += " • T1595 - Active Scanning\n"

    report += "\nRecommended Actions\n"

    if risk >= 80:
        report += " • Isolate Session\n"
        report += " • Alert Administrator\n"
        report += " • Investigate User\n"

    elif risk >= 50:
        report += " • Monitor User Activity\n"

    elif risk >= 20:
        report += " • Increase Monitoring\n"

    else:
        report += " • Continue Monitoring\n"

    report += "=" * 60

    return report