def generate_ai_messages(

    score,
    attendance,
    study_hours,
    sleep_hours,
    assignment_completion,
    class_participation,

    education_type=None,
    stream=None,
    branch=None,
    semester=None,
    board=None,
    specialization=None

):

    messages = []

    # =====================================================
    # 1. AI MENTOR
    # =====================================================

    if score >= 85:

        mentor_msg = """
Excellent Performance 🌟

• Maintain consistency
• Practice mock tests
• Continue revision
"""

    elif score >= 60:

        mentor_msg = """
Good Progress 👍

• Focus weak subjects
• Increase revision
• Practice daily
"""

    else:

        mentor_msg = """
Performance Needs Improvement 💙

• Follow study routine
• Improve attendance
• Focus on basics
"""

    messages.append({

        "icon":"fa-solid fa-robot",

        "color":"msg-blue",

        "title":"AI Mentor",

        "message":mentor_msg

    })

    # =====================================================
    # 2. SUBJECT GUIDANCE
    # =====================================================

    guidance_msg = ""

    # =====================================================
    # BTECH
    # =====================================================

    if education_type == "BTech":

        # CSE

        if branch == "CSE":

            guidance_msg = """
CSE Subject Guidance 💻

• Practice DSA daily
• Revise DBMS queries
• Improve OS concepts
• Build mini projects
"""

        # ECE

        elif branch == "ECE":

            guidance_msg = """
ECE Subject Guidance 📡

• Practice Digital Electronics
• Improve Communication Systems
• Revise Microprocessors
• Focus Circuit Theory
"""

        # EE

        elif branch == "EE":

            guidance_msg = """
Electrical Subject Guidance ⚡

• Focus Power Systems
• Practice Machines
• Improve Control Systems
• Solve Numericals
"""

        # ME

        elif branch == "ME":

            guidance_msg = """
Mechanical Subject Guidance ⚙️

• Revise Thermodynamics
• Practice CAD concepts
• Improve Machine Design
• Solve Numericals
"""

        # CIVIL

        elif branch == "Civil":

            guidance_msg = """
Civil Subject Guidance 🏗️

• Improve RCC Design
• Revise Surveying
• Practice Numericals
• Focus Structures
"""

        else:

            guidance_msg = """
Engineering Guidance 🚀

• Improve technical concepts
• Practice numericals
• Build practical skills
"""

    # =====================================================
    # 10TH
    # =====================================================

    elif education_type == "10th":

        guidance_msg = """
10th Subject Guidance 📘

• Practice Mathematics
• Revise Science
• Improve SST writing
• Solve sample papers
"""

    # =====================================================
    # 12TH
    # =====================================================

    elif education_type == "12th":

        # SCIENCE

        if stream == "Science":

            # PCM

            if specialization == "PCM":

                guidance_msg = """
PCM Subject Guidance 🔬

• Practice Physics numericals
• Revise Maths formulas
• Focus Organic Chemistry
• Solve mock tests
"""

            # PCB

            elif specialization == "PCB":

                guidance_msg = """
PCB Subject Guidance 🧬

• Focus NCERT Biology
• Practice diagrams
• Revise Chemistry
• Improve theory revision
"""

            else:

                guidance_msg = """
Science Subject Guidance ⚛️

• Revise formulas
• Practice numericals
• Solve mock tests
"""

        # COMMERCE

        elif stream == "Commerce":

            guidance_msg = """
Commerce Subject Guidance 📈

• Practice Accounts
• Revise Economics
• Improve BST answers
• Focus presentation
"""

        # ARTS

        elif stream == "Arts":

            guidance_msg = """
Arts Subject Guidance 📝

• Revise History notes
• Improve Political Science
• Practice Geography maps
• Improve answer writing
"""

    # =====================================================
    # DEFAULT
    # =====================================================

    else:

        guidance_msg = """
Smart Study Guidance 🎯

• Revise daily
• Practice weak topics
• Stay consistent
"""

    messages.append({

        "icon":"fa-solid fa-graduation-cap",

        "color":"msg-green",

        "title":"Personalized Guidance",

        "message":guidance_msg

    })

    # =====================================================
    # 3. ATTENDANCE
    # =====================================================

    if attendance < 75:

        messages.append({

            "icon":"fa-solid fa-triangle-exclamation",

            "color":"msg-red",

            "title":"Attendance Alert",

            "message":f"""

Attendance is {attendance}% 🚨

• Attend classes regularly
• Avoid missing practicals
• Revise classroom topics
"""

        })

    # =====================================================
    # 4. STUDY HOURS
    # =====================================================

    if study_hours < 5:

        messages.append({

            "icon":"fa-solid fa-book",

            "color":"msg-blue",

            "title":"Study Strategy",

            "message":"""

Study hours are low 📚

• Follow study schedule
• Solve PYQs
• Revise weak topics
"""

        })

    # =====================================================
    # 5. SLEEP
    # =====================================================

    if sleep_hours < 6:

        messages.append({

            "icon":"fa-solid fa-heart",

            "color":"msg-purple",

            "title":"Health & Focus",

            "message":"""

Sleep schedule is weak 😴

• Sleep 7–8 hours
• Avoid late-night mobile use
• Follow fixed routine
"""

        })

    # =====================================================
    # 6. ASSIGNMENTS
    # =====================================================

    if assignment_completion <= 5:

        messages.append({

            "icon":"fa-solid fa-file-lines",

            "color":"msg-orange",

            "title":"Assignment Guidance",

            "message":"""

Assignments need improvement 📝

• Submit before deadlines
• Improve presentation
• Practice writing
"""

        })

    # =====================================================
    # 7. PARTICIPATION
    # =====================================================

    if class_participation == 1:

        messages.append({

            "icon":"fa-solid fa-users",

            "color":"msg-green",

            "title":"Class Participation",

            "message":"""

Participation is low 🎯

• Ask doubts confidently
• Join discussions
• Engage practically
"""

        })

    # =====================================================
    # 8. SEMESTER GUIDANCE
    # =====================================================

    if education_type == "BTech":

        if semester in ["1","2"]:

            sem_msg = """
Semester Focus 🎯

• Improve programming basics
• Focus Mathematics
• Build fundamentals
"""

        elif semester in ["3","4","5"]:

            sem_msg = """
Mid Semester Focus 🚀

• Start projects
• Improve coding
• Build communication
"""

        else:

            sem_msg = """
Placement Preparation 💼

• Practice aptitude
• Build resume
• Prepare interviews
"""

        messages.append({

            "icon":"fa-solid fa-code",

            "color":"msg-purple",

            "title":"Semester Guidance",

            "message":sem_msg

        })

    # =====================================================
    # 9. DAILY ROUTINE
    # =====================================================

    messages.append({

        "icon":"fa-solid fa-calendar-days",

        "color":"msg-blue",

        "title":"Suggested Routine",

        "message":"""

Daily Routine ⏰

6 AM → Wake Up
7 AM → Revision
8 AM → School/College
6 PM → Practice
8 PM → Weak Subject
"""

    })

    # =====================================================
    # 10. MOTIVATION
    # =====================================================

    if score <= 75:

        messages.append({

            "icon":"fa-solid fa-lightbulb",

            "color":"msg-green",

            "title":"Motivation",

            "message":"""

Stay consistent 💪

• Improve daily
• Avoid comparison
• Focus smart learning
"""

        })

    # =====================================================
    # LIMIT TO BEST 6
    # =====================================================

    return messages[:6]