def render_html(profile: dict) -> str:
    """
    Renders the CV template with the provided profile data.
    
    Args:
        profile (dict): Dictionary containing the user's profile information
        
    Returns:
        str: Rendered HTML content
    """
    with open("templates/cv_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    experience_html = ''.join([
        f"<li><b>{exp['title']}</b> en {exp['company']} ({exp['start_date']} - {exp.get('end_date', 'actual')}): {exp['description']}</li>"
        for exp in profile['experiences']
    ])

    education_html = ''.join([
        f"<li>{edu['degree']} - {edu['institution']} ({edu['year']})</li>"
        for edu in profile['education']
    ])

    return template.format(
        name=profile['name'],
        email=profile['email'],
        phone=profile['phone'],
        location=profile['location'],
        experiences=experience_html,
        education=education_html,
        skills=', '.join(profile['skills']),
        languages=', '.join(profile['languages'])
    )
