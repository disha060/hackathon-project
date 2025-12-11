import os
import json
import asyncio
from sqlalchemy.orm import Session
from typing import List
import schemas
import models

# Template-based content generation (fallback when API unavailable)
CONTENT_TEMPLATES = {
    "assignment": {
        1: {
            "title": "{concept} Fundamentals Quiz",
            "description": "Test your understanding of basic {concept} concepts including {topics}",
            "objectives": [
                "Identify key {concept} principles",
                "Apply basic {concept} techniques",
                "Solve simple {concept} problems"
            ]
        },
        2: {
            "title": "{concept} Practice Exercises",
            "description": "Practice applying {concept} through hands-on exercises covering {topics}",
            "objectives": [
                "Implement {concept} solutions",
                "Debug common {concept} issues",
                "Optimize {concept} performance"
            ]
        },
        3: {
            "title": "{concept} Advanced Challenges",
            "description": "Tackle complex {concept} problems requiring deep understanding of {topics}",
            "objectives": [
                "Design sophisticated {concept} systems",
                "Analyze {concept} trade-offs",
                "Evaluate {concept} best practices"
            ]
        }
    },
    "project": {
        "app_development": {
            "title": "{skill_area} Application Project",
            "description": "Build a complete {skill_area} application that demonstrates core concepts",
            "outcomes": [
                "Apply {skill_area} design patterns",
                "Implement user authentication",
                "Deploy a production-ready application"
            ]
        },
        "data_analysis": {
            "title": "{skill_area} Analytics Dashboard",
            "description": "Create a dashboard to visualize and analyze {skill_area} data trends",
            "outcomes": [
                "Process large datasets",
                "Create interactive visualizations",
                "Generate actionable insights"
            ]
        }
    }
}

def generate_assignment_prompt(concept_name: str, difficulty: int, topics: List[str]) -> str:
    """Generate prompt for assignment creation"""
    template = CONTENT_TEMPLATES["assignment"].get(difficulty, CONTENT_TEMPLATES["assignment"][2])
    topics_str = ", ".join(topics)
    
    return f"""
    Create a {concept_name} assignment for students.
    
    Title: {template['title'].format(concept=concept_name)}
    Description: {template['description'].format(concept=concept_name, topics=topics_str)}
    Difficulty Level: {difficulty}/5
    Estimated Time: {difficulty * 15 + 10} minutes
    
    Learning Objectives:
    {chr(10).join([f"- {obj.format(concept=concept_name)}" for obj in template['objectives']])}
    
    Please format the response as JSON with the following structure:
    {{
        "title": "Assignment Title",
        "description": "Detailed description",
        "difficulty_level": 1-5,
        "estimated_time": 15,
        "learning_objectives": ["objective1", "objective2", "objective3"]
    }}
    """

def generate_project_prompt(skill_area: str, project_type: str) -> str:
    """Generate prompt for project creation"""
    template = CONTENT_TEMPLATES["project"].get(project_type, CONTENT_TEMPLATES["project"]["app_development"])
    
    return f"""
    Create a {skill_area} project idea for students.
    
    Title: {template['title'].format(skill_area=skill_area)}
    Description: {template['description'].format(skill_area=skill_area)}
    Duration: {20 + len(skill_area) * 2} hours
    Team Size: {3 if 'app' in project_type else 4} members
    
    Learning Outcomes:
    {chr(10).join([f"- {outcome.format(skill_area=skill_area)}" for outcome in template['outcomes']])}
    
    Please format the response as JSON with the following structure:
    {{
        "title": "Project Title",
        "description": "Detailed description",
        "duration_hours": 20,
        "team_size": 3,
        "learning_outcomes": ["outcome1", "outcome2", "outcome3"]
    }}
    """

async def call_gemini_api(prompt: str, api_key: str = None) -> dict:
    """Call Gemini API to generate content"""
    # Use the provided API key or default to the one we have
    if not api_key:
        # Use the latest hardcoded API key
        api_key = "apikey"
    
    # Make actual API call to Gemini
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Create the model
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        
        # Generate content
        response = await model.generate_content_async(prompt)
        
        # Try to parse the JSON response
        import json
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured response from the text
            return {
                "topic": "Generated Content",
                "difficulty": 3,
                "questions": [
                    {
                        "id": 1,
                        "type": "Short Answer",
                        "question": response.text[:200] + "..." if len(response.text) > 200 else response.text,
                        "options": None,
                        "correct_answer": "See explanation above"
                    }
                ]
            }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        print(f"API Key used: {api_key[:10]}... (truncated for security)")
        # Only fallback to simulated response if there's a real error
        # In a production environment, we would handle this differently
        # For debugging, let's also return some information about the error
        error_response = simulate_gemini_response(prompt)
        error_response["error_note"] = f"Real API failed: {str(e)}. Using simulated responses."
        return error_response

def simulate_gemini_response(prompt: str) -> dict:
    """Simulate Gemini API response for demo purposes"""
    if "assignment" in prompt.lower():
        return {
            "title": "AI-Generated Assignment",
            "description": "This assignment was intelligently generated using advanced AI models to match your learning objectives",
            "difficulty_level": 3,
            "estimated_time": 45,
            "learning_objectives": [
                "Demonstrate understanding of core concepts",
                "Apply knowledge to solve practical problems",
                "Develop critical thinking skills"
            ]
        }
    elif "quiz" in prompt.lower():
        # Extract parameters from prompt
        import re
        # Extract topic from the prompt
        # Since we know the format, we can extract the topic directly
        # The prompt format is: "Generate X quiz questions about TOPIC at difficulty level Y"
        import re
        topic_match = re.search(r'Generate \d+ quiz questions about (.+?) at difficulty', prompt)
        topic = topic_match.group(1) if topic_match else "General Knowledge"
        
        count_match = re.search(r'(\d+) quiz questions', prompt)
        question_count = int(count_match.group(1)) if count_match else 5
        
        # Define topic-appropriate question templates
        if "java" in topic.lower() and "oop" in topic.lower():
            # Java OOP specific templates
            mcq_templates = [
                f"Which of the following is a fundamental principle of OOP in {topic}?",
                f"What is the primary purpose of encapsulation in {topic}?",
                f"Which keyword is used for inheritance in {topic}?",
                f"What does polymorphism allow in {topic}?",
                f"What is the main benefit of abstraction in {topic}?"
            ]
            
            tf_templates = [
                f"{topic} supports multiple inheritance through interfaces.",
                f"Encapsulation in {topic} helps protect data from unauthorized access.",
                f"Abstract classes in {topic} can be instantiated directly.",
                f"Method overriding is a form of polymorphism in {topic}.",
                f"Interfaces in {topic} can contain concrete method implementations."
            ]
            
            sa_templates = [
                f"Explain the four pillars of OOP in {topic}.",
                f"Describe how inheritance promotes code reusability in {topic}.",
                f"Compare and contrast abstract classes and interfaces in {topic}.",
                f"How does encapsulation improve security in {topic} programs?",
                f"Provide a real-world example demonstrating polymorphism in {topic}."
            ]
            
            fib_templates = [
                f"The _____ keyword is used to achieve inheritance in {topic}.",
                f"_____ refers to the ability of objects to take multiple forms in {topic}.",
                f"Data _____ is the technique of hiding internal details in {topic}.",
                f"An _____ class cannot be instantiated in {topic}.",
                f"_____ methods have the same signature but different implementations in {topic}."
            ]
            
            # Define realistic options and answers
            mcq_options = [
                ["Inheritance", "Compilation", "Execution", "Debugging"],
                ["Data hiding", "Code duplication", "Performance boost", "Syntax simplification"],
                ["extends", "implements", "inherits", "derives"],
                ["Different behaviors", "Same behavior", "Reduced code", "Faster execution"],
                ["Code simplicity", "Complexity increase", "Performance loss", "Memory reduction"]
            ]
            
            mcq_answers = ["Inheritance", "Data hiding", "extends", "Different behaviors", "Code simplicity"]
            tf_answers = ["True", "True", "False", "True", "False"]
            sa_answers = [
                f"The four pillars of OOP in {topic} are encapsulation, inheritance, polymorphism, and abstraction.",
                f"Inheritance in {topic} allows child classes to reuse code from parent classes, reducing redundancy.",
                f"Abstract classes in {topic} can have both abstract and concrete methods, while interfaces can only have abstract methods (before Java 8).",
                f"Encapsulation in {topic} protects data by controlling access through public/private modifiers.",
                f"Polymorphism in {topic} allows objects to behave differently based on their type, such as method overriding."
            ]
            fib_answers = ["extends", "polymorphism", "encapsulation", "abstract", "overriding"]
        else:
            # General knowledge templates
            mcq_templates = [
                f"Which process is primarily responsible for converting light energy into chemical energy in {topic}?",
                f"What is the primary function of {topic} in biological systems?",
                f"Which scientist is most associated with the discovery of {topic}?",
                f"What is a key characteristic that distinguishes {topic} from similar concepts?",
                f"In what cellular component does {topic} primarily occur?"
            ]
            
            tf_templates = [
                f"{topic} plays a crucial role in energy conversion processes.",
                f"The discovery of {topic} revolutionized our understanding of biological processes.",
                f"{topic} is exclusively found in plant cells.",
                f"ATP is a product of {topic}.",
                f"{topic} occurs only during daylight hours."
            ]
            
            sa_templates = [
                f"Explain the significance of {topic} in ecosystem dynamics.",
                f"Describe how {topic} contributes to cellular energy production.",
                f"Compare and contrast {topic} with cellular respiration.",
                f"Analyze the environmental factors that affect the rate of {topic}.",
                f"Discuss the evolutionary significance of {topic} in plant development."
            ]
            
            fib_templates = [
                f"The green pigment responsible for capturing light energy in {topic} is called _____ .",
                f"During {topic}, carbon dioxide is converted into _____ through a series of chemical reactions.",
                f"The _____ is the organelle where {topic} takes place in plant cells.",
                f"Oxygen is produced as a byproduct of {topic} when _____ molecules are split.",
                f"The Calvin cycle is the _____ stage of {topic} where glucose is synthesized."
            ]
            
            # Define realistic options and answers
            mcq_options = [
                ["Cellular Respiration", "Photosynthesis", "Glycolysis", "Fermentation"],
                ["Energy storage", "Energy conversion", "Waste removal", "Protein synthesis"],
                ["Gregor Mendel", "Jan Baptist van Helmont", "Joseph Priestley", "Melvin Calvin"],
                ["Light dependency", "Anaerobic nature", "Chlorophyll requirement", "Glucose production"],
                ["Mitochondria", "Nucleus", "Chloroplast", "Endoplasmic reticulum"]
            ]
            
            mcq_answers = ["Photosynthesis", "Energy conversion", "Melvin Calvin", "Chlorophyll requirement", "Chloroplast"]
            tf_answers = ["True", "True", "False", "True", "True"]
            sa_answers = [
                f"{topic} is crucial for converting solar energy into chemical energy, forming the foundation of food chains and producing oxygen essential for life.",
                f"{topic} converts light energy into chemical energy stored in glucose, providing fuel for cellular processes and releasing oxygen as a byproduct.",
                f"While {topic} produces glucose and oxygen using light energy, cellular respiration breaks down glucose to release energy, using oxygen and producing CO2.",
                f"Factors affecting {topic} include light intensity, temperature, and CO2 concentration, with optimal levels maximizing efficiency.",
                f"{topic} evolution enabled plants to harness solar energy, fundamentally changing Earth's atmosphere and supporting complex ecosystems."
            ]
            fib_answers = ["chlorophyll", "glucose", "chloroplast", "water", "light-independent"]
        
        questions = []
        question_types = ["Multiple Choice", "True or False", "Short Answer", "Fill in the Blank"]
        
        for i in range(min(question_count, 5)):  # Limit to 5 for realistic templates
            q_type = question_types[i % 4]
            
            if q_type == "Multiple Choice":
                questions.append({
                    "id": i+1,
                    "type": q_type,
                    "question": mcq_templates[i],
                    "options": mcq_options[i],
                    "correct_answer": mcq_answers[i]
                })
            elif q_type == "True or False":
                questions.append({
                    "id": i+1,
                    "type": q_type,
                    "question": tf_templates[i],
                    "options": None,
                    "correct_answer": tf_answers[i]
                })
            elif q_type == "Short Answer":
                questions.append({
                    "id": i+1,
                    "type": q_type,
                    "question": sa_templates[i],
                    "options": None,
                    "correct_answer": sa_answers[i]
                })
            else:  # Fill in the Blank
                questions.append({
                    "id": i+1,
                    "type": q_type,
                    "question": fib_templates[i],
                    "options": None,
                    "correct_answer": fib_answers[i]
                })
        
        # If more questions are needed, generate generic ones
        for i in range(len(questions), question_count):
            q_type = question_types[i % 4]
            base_index = i % 5
            
            if q_type == "Multiple Choice":
                questions.append({
                    "id": i+1,
                    "type": q_type,
                    "question": f"What is a key aspect of {topic}?",
                    "options": [f"Aspect {i+1}A", f"Aspect {i+1}B", f"Aspect {i+1}C", f"Aspect {i+1}D"],
                    "correct_answer": f"Aspect {i+1}B"
                })
            elif q_type == "True or False":
                questions.append({
                    "id": i+1,
                    "type": q_type,
                    "question": f"{topic} is an important subject.",
                    "options": None,
                    "correct_answer": "True"
                })
            else:
                questions.append({
                    "id": i+1,
                    "type": q_type,
                    "question": f"Explain a key concept of {topic}.",
                    "options": None,
                    "correct_answer": f"Key concept explanation for {topic}"
                })
        
        return {
            "topic": topic,
            "difficulty": 3,
            "questions": questions
        }
    else:
        return {
            "title": "AI-Generated Project",
            "description": "This project was designed using cutting-edge AI to provide an engaging learning experience",
            "duration_hours": 30,
            "team_size": 4,
            "learning_outcomes": [
                "Synthesize knowledge across multiple domains",
                "Collaborate effectively in team environments",
                "Create innovative solutions to real-world problems"
            ]
        }

def generate_assignments(concept_id: int, db: Session, api_key: str = None) -> List[schemas.AIGeneratedAssignment]:
    """
    Generate AI-suggested assignments for a concept using Gemini API or templates.
    """
    # Get concept details
    concept = db.query(models.Concepts).filter(models.Concepts.id == concept_id).first()
    if not concept:
        # Fallback to template-based generation
        template = CONTENT_TEMPLATES["assignment"][2]  # Medium difficulty
        assignments = [
            schemas.AIGeneratedAssignment(
                concept_id=concept_id,
                title=template["title"].format(concept="Programming"),
                description=template["description"].format(concept="Programming", topics="fundamentals"),
                difficulty_level=2,
                estimated_time=40,
                learning_objectives=template["objectives"]
            )
        ]
        return assignments
    
    # Generate assignments for different difficulty levels
    assignments = []
    topics = ["basics", "intermediate", "advanced"]
    
    for difficulty in [1, 2, 3]:
        # Try to call Gemini API
        prompt = generate_assignment_prompt(concept.name, difficulty, topics[:difficulty])
        
        try:
            # Call Gemini API with fallback
            response = asyncio.run(call_gemini_api(prompt, api_key))
            
            assignment = schemas.AIGeneratedAssignment(
                concept_id=concept_id,
                title=response["title"],
                description=response["description"],
                difficulty_level=response["difficulty_level"],
                estimated_time=response["estimated_time"],
                learning_objectives=response["learning_objectives"]
            )
            assignments.append(assignment)
        except Exception as e:
            # Fallback to template-based generation
            template = CONTENT_TEMPLATES["assignment"].get(difficulty, CONTENT_TEMPLATES["assignment"][2])
            fallback_assignment = schemas.AIGeneratedAssignment(
                concept_id=concept_id,
                title=template["title"].format(concept=concept.name),
                description=template["description"].format(concept=concept.name, topics=", ".join(topics[:difficulty])),
                difficulty_level=difficulty,
                estimated_time=difficulty * 15 + 10,
                learning_objectives=[obj.format(concept=concept.name) for obj in template["objectives"]]
            )
            assignments.append(fallback_assignment)
    
    return assignments

def generate_projects(skill_area: str, db: Session, api_key: str = None) -> List[schemas.AIGeneratedProject]:
    """
    Generate AI-suggested projects for a skill area using Gemini API or templates.
    """
    projects = []
    project_types = ["app_development", "data_analysis"]
    
    for project_type in project_types:
        # Try to call Gemini API
        prompt = generate_project_prompt(skill_area, project_type)
        
        try:
            # Call Gemini API with fallback
            response = asyncio.run(call_gemini_api(prompt, api_key))
            
            project = schemas.AIGeneratedProject(
                title=response["title"],
                description=response["description"],
                skill_area=skill_area,
                duration_hours=response["duration_hours"],
                team_size=response["team_size"],
                learning_outcomes=response["learning_outcomes"]
            )
            projects.append(project)
        except Exception as e:
            # Fallback to template-based generation
            template = CONTENT_TEMPLATES["project"].get(project_type, CONTENT_TEMPLATES["project"]["app_development"])
            fallback_project = schemas.AIGeneratedProject(
                title=template["title"].format(skill_area=skill_area),
                description=template["description"].format(skill_area=skill_area),
                skill_area=skill_area,
                duration_hours=20 + len(skill_area) * 2,
                team_size=3 if 'app' in project_type else 4,
                learning_outcomes=[outcome.format(skill_area=skill_area) for outcome in template["outcomes"]]
            )
            projects.append(fallback_project)
    
    return projects