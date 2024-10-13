
from fastapi import APIRouter
import random
from typing import Dict, Literal, Union, List
from pydantic import BaseModel
import math
import logging

# Router for endpoints
router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define difficulty levels and their corresponding points
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
DIFFICULTY_POINTS = {"easy": 1, "medium": 2, "hard": 3}

# Function to generate a geometry question
def generate_geometry_question(difficulty: str) -> Dict[str, str]:
    shapes = ["square", "rectangle", "circle", "triangle"]
    shape = random.choice(shapes)
    
    if difficulty == "easy":
        range_start, range_end = 1, 5
    elif difficulty == "medium":
        range_start, range_end = 5, 10
    else:  # hard
        range_start, range_end = 10, 20
    
    if shape == "square":
        side = random.randint(range_start, range_end)
        area = side ** 2
        question = f"What is the area of a square with side length {side}?"
        answer = str(area)
    elif shape == "rectangle":
        length = random.randint(range_start, range_end)
        width = random.randint(range_start, range_end)
        area = length * width
        question = f"What is the area of a rectangle with length {length} and width {width}?"
        answer = str(area)
    elif shape == "circle":
        radius = random.randint(range_start, range_end)
        area = round(math.pi * radius ** 2, 2)
        question = f"What is the area of a circle with radius {radius}? (Round to 2 decimal places)"
        answer = str(area)
    else:  # triangle
        base = random.randint(range_start, range_end)
        height = random.randint(range_start, range_end)
        area = round(0.5 * base * height, 2)
        question = f"What is the area of a triangle with base {base} and height {height}?"
        answer = str(area)
    
    return {
        "question": question,
        "answer": answer,
        "difficulty": difficulty
    }

# Function to generate a trigonometry question
def generate_trigonometry_question(difficulty: str) -> Dict[str, str]:
    functions = ["sin", "cos", "tan"]
    function = random.choice(functions)
    
    if difficulty == "easy":
        angles = [0, 30, 45, 60, 90]
    elif difficulty == "medium":
        angles = [0, 30, 45, 60, 90, 120, 150, 180]
    else:  # hard
        angles = list(range(0, 361, 15))  # All angles from 0 to 360 in 15-degree increments
    
    angle = random.choice(angles)
    
    if function == "sin":
        result = round(math.sin(math.radians(angle)), 2)
    elif function == "cos":
        result = round(math.cos(math.radians(angle)), 2)
    else:
        result = round(math.tan(math.radians(angle)), 2)
    
    question = f"What is the {function} of {angle} degrees? (Round to 2 decimal places)"
    answer = str(result)
    
    return {
        "question": question,
        "answer": answer,
        "difficulty": difficulty
    }

# Function to generate an algebraic equation
def generate_algebraic_equation(difficulty: str) -> Dict[str, Union[int, str]]:
    a = random.randint(1, 5) if difficulty == "easy" else random.randint(1, 10)
    b = random.randint(1, 5) if difficulty == "easy" else random.randint(1, 10)
    x = random.randint(1, 5) if difficulty == "easy" else random.randint(1, 10)
    c = a * x + b
    
    return {
        "a": a,
        "b": b,
        "c": c,
        "x": x,
        "difficulty": difficulty
    }

# Function to generate a calculus question
def generate_calculus_question(difficulty: str) -> Dict[str, str]:
    question_type = random.choice(["derivative", "integral"])
    
    if difficulty == "easy":
        functions = ["x^2", "x^3", "sin(x)", "cos(x)"]
    elif difficulty == "medium":
        functions = ["x^2", "x^3", "sin(x)", "cos(x)", "e^x", "ln(x)"]
    else:  # hard
        functions = ["x^2", "x^3", "sin(x)", "cos(x)", "e^x", "ln(x)", "tan(x)", "x^4", "sqrt(x)"]
    
    try:
        function = random.choice(functions)
        if question_type == "derivative":
            question = f"What is the derivative of {function} with respect to x?"
            answer = "Derivative of " + function
        else:  # integral
            question = f"What is the indefinite integral of {function} with respect to x? (Ignore the constant of integration)"
            answer = "Integral of " + function
    
        logger.info(f"Successfully generated calculus question: {question}")
        return {
            "question": question,
            "answer": answer,
            "difficulty": difficulty
        }
    except Exception as e:
        logger.error(f"Unexpected error in generate_calculus_question: {e}")
        return {
            "question": "An unexpected error occurred while generating the calculus question.",
            "answer": "N/A",
            "difficulty": difficulty
        }

# Function to generate a math question
def generate_math_question() -> Dict[str, Union[str, Literal["algebra", "geometry", "trigonometry", "calculus"], int]]:
    topic = random.choice(["algebra", "geometry", "trigonometry", "calculus"])
    difficulty = random.choice(DIFFICULTY_LEVELS)
    
    try:
        if topic == "algebra":
            equation = generate_algebraic_equation(difficulty)
            question = f"{equation['a']}x + {equation['b']} = {equation['c']}"
            answer = str(equation['x'])
        elif topic == "geometry":
            question_data = generate_geometry_question(difficulty)
            question = question_data["question"]
            answer = question_data["answer"]
        elif topic == "trigonometry":
            question_data = generate_trigonometry_question(difficulty)
            question = question_data["question"]
            answer = question_data["answer"]
        else:  # calculus
            question_data = generate_calculus_question(difficulty)
            question = question_data["question"]
            answer = question_data["answer"]
            
            # If there was an error generating the calculus question, fall back to algebra
            if question == "An unexpected error occurred while generating the calculus question.":
                logger.warning("Failed to generate calculus question. Falling back to algebra.")
                topic = "algebra"
                equation = generate_algebraic_equation(difficulty)
                question = f"{equation['a']}x + {equation['b']} = {equation['c']}"
                answer = str(equation['x'])
        
        logger.info(f"Successfully generated {topic} question: {question}")
        return {
            "question": question,
            "answer": answer,
            "topic": topic,
            "difficulty": difficulty,
            "points": DIFFICULTY_POINTS[difficulty]
        }
    except Exception as e:
        logger.error(f"Unexpected error in generate_math_question: {e}")
        # Fallback to a simple addition question
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        return {
            "question": f"What is {a} + {b}?",
            "answer": str(a + b),
            "topic": "arithmetic",
            "difficulty": "easy",
            "points": DIFFICULTY_POINTS["easy"]
        }

class MathQuestionResponse(BaseModel):
    question: str
    answer: str
    topic: Literal["algebra", "geometry", "trigonometry", "calculus", "arithmetic"]
    difficulty: Literal["easy", "medium", "hard"]
    points: int

# FastAPI route for math question API
@router.get("/api/math-question")
def get_math_question() -> MathQuestionResponse:
    question_data = generate_math_question()
    logger.info(f"Returning math question: {question_data}")
    return MathQuestionResponse(
        question=question_data["question"],
        answer=question_data["answer"],
        topic=question_data["topic"],
        difficulty=question_data["difficulty"],
        points=question_data["points"]
    )
