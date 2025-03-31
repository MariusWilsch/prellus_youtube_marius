#!/usr/bin/env python3
"""
Generate Test Transcript

This script generates a test transcript of specified size for testing the large
transcript processing feature. It creates structured content with multiple topics
and natural paragraph breaks to simulate a real transcript.

Usage:
    python generate_test_transcript.py --output=<output_file> --size=<size_in_chars>

Example:
    python generate_test_transcript.py --output=data/transcripts/test_large/raw/transcript.txt --size=200000
"""

import argparse
import os
import random
import time
from typing import List, Tuple

def generate_paragraph(topic: str, min_length: int = 200, max_length: int = 800) -> str:
    """
    Generate a paragraph about a specific topic with natural language patterns.
    
    Args:
        topic: The topic of the paragraph
        min_length: Minimum length of the paragraph in characters
        max_length: Maximum length of the paragraph in characters
        
    Returns:
        A paragraph as a string
    """
    # Define templates for sentence generation
    templates = [
        f"Let's talk about {topic}. ",
        f"Now, regarding {topic}, there are several important aspects to consider. ",
        f"One fascinating thing about {topic} is its historical development. ",
        f"When we examine {topic} more closely, we can observe various patterns. ",
        f"The key principles of {topic} are worth discussing in detail. ",
        f"Many people misunderstand {topic}, but let me clarify. ",
        f"The evolution of {topic} over time reveals interesting trends. ",
        f"Experts in the field of {topic} often debate about its fundamental nature. ",
        f"Understanding {topic} requires looking at it from multiple perspectives. ",
        f"Recent developments in {topic} have changed how we think about it. "
    ]
    
    # List of connecting phrases to make the text flow naturally
    connectors = [
        "Furthermore, ", "Additionally, ", "Moreover, ", "In addition, ", 
        "However, ", "Nevertheless, ", "On the other hand, ", "Conversely, ",
        "As a result, ", "Consequently, ", "Therefore, ", "Thus, ",
        "For example, ", "For instance, ", "To illustrate, ", "As an example, ",
        "In particular, ", "Specifically, ", "Notably, ", "Especially, "
    ]
    
    # Facts and details that can be used for any topic
    generic_facts = [
        f"there are several schools of thought within {topic}. ",
        f"the historical context of {topic} is often overlooked. ",
        f"researchers have identified key patterns in {topic}. ",
        f"there are practical applications of {topic} in everyday life. ",
        f"cultural differences affect how {topic} is perceived. ",
        f"technological advances have transformed our understanding of {topic}. ",
        f"theoretical frameworks help us conceptualize {topic} more effectively. ",
        f"comparative studies of {topic} reveal cultural variations. ",
        f"longitudinal research on {topic} shows evolving patterns. ",
        f"critical analysis of {topic} challenges conventional wisdom. ",
        f"interdisciplinary approaches to {topic} offer new insights. ",
        f"the relationship between theory and practice in {topic} is complex. ",
        f"ethical considerations are important when discussing {topic}. ",
        f"global perspectives on {topic} differ from Western viewpoints. ",
        f"social contexts influence how we interpret {topic}. "
    ]
    
    # Begin with a template
    paragraph = random.choice(templates)
    current_length = len(paragraph)
    target_length = random.randint(min_length, max_length)
    
    # Add sentences until we reach the target length
    while current_length < target_length:
        # 70% chance to add a connector
        if random.random() < 0.7:
            next_part = random.choice(connectors)
        else:
            next_part = ""
            
        next_part += random.choice(generic_facts)
        paragraph += next_part
        current_length = len(paragraph)
    
    return paragraph

def generate_topic_section(topic: str, subtopics: List[str], target_length: int) -> str:
    """
    Generate a section about a topic with multiple paragraphs covering subtopics.
    
    Args:
        topic: The main topic
        subtopics: List of subtopics to cover
        target_length: Target length of the section in characters
        
    Returns:
        A multi-paragraph section as a string
    """
    section = f"== {topic} ==\n\n"
    current_length = len(section)
    
    # Add an introductory paragraph about the main topic
    intro = generate_paragraph(topic, 300, 600)
    section += intro + "\n\n"
    current_length = len(section)
    
    # Add paragraphs for each subtopic
    for subtopic in subtopics:
        # If we've already exceeded the target length, stop adding paragraphs
        if current_length >= target_length:
            break
            
        # Generate 1-3 paragraphs for each subtopic
        num_paragraphs = random.randint(1, 3)
        for _ in range(num_paragraphs):
            if current_length >= target_length:
                break
                
            paragraph = generate_paragraph(subtopic)
            section += paragraph + "\n\n"
            current_length = len(section)
    
    # If we still need more content, add general paragraphs
    while current_length < target_length:
        paragraph = generate_paragraph(random.choice(subtopics))
        section += paragraph + "\n\n"
        current_length = len(section)
    
    return section

def generate_transcript(topics: List[Tuple[str, List[str]]], target_size: int) -> str:
    """
    Generate a full transcript with multiple topics and subtopics.
    
    Args:
        topics: List of (topic, [subtopics]) tuples
        target_size: Target size of the transcript in characters
        
    Returns:
        A complete transcript as a string
    """
    transcript = "# Test Transcript for Large Processing\n\n"
    current_size = len(transcript)
    
    # Calculate approximate size per topic
    size_per_topic = target_size / len(topics)
    
    # Generate content for each topic
    for topic, subtopics in topics:
        section = generate_topic_section(topic, subtopics, size_per_topic)
        transcript += section
        current_size = len(transcript)
    
    # If we're under the target size, add additional content
    while current_size < target_size:
        # Choose a random topic to expand
        topic, subtopics = random.choice(topics)
        
        # Generate a paragraph on a random subtopic
        subtopic = random.choice(subtopics)
        paragraph = generate_paragraph(subtopic)
        
        transcript += f"Additional thoughts on {subtopic}:\n\n{paragraph}\n\n"
        current_size = len(transcript)
    
    return transcript

def main():
    """Main function to generate a test transcript."""
    parser = argparse.ArgumentParser(description="Generate a test transcript for large processing")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--size", type=int, default=200000, help="Target size in characters (default: 200000)")
    args = parser.parse_args()
    
    # Define topics and subtopics for a diverse transcript
    topics = [
        ("History of Computing", [
            "Early Mechanical Computers", 
            "Electronic Computing Era", 
            "Personal Computing Revolution",
            "Internet Age",
            "Mobile Computing",
            "Cloud Computing"
        ]),
        ("Artificial Intelligence", [
            "Machine Learning Foundations", 
            "Neural Networks", 
            "Natural Language Processing",
            "Computer Vision",
            "AI Ethics",
            "Reinforcement Learning"
        ]),
        ("Software Engineering", [
            "Development Methodologies", 
            "Software Architecture", 
            "Testing and Quality Assurance",
            "DevOps Practices",
            "Code Optimization",
            "Software Maintenance"
        ]),
        ("Data Science", [
            "Statistical Analysis", 
            "Data Visualization", 
            "Big Data Technologies",
            "Predictive Modeling",
            "Data Ethics",
            "Data Engineering"
        ]),
        ("Cybersecurity", [
            "Network Security", 
            "Cryptography", 
            "Ethical Hacking",
            "Security Policies",
            "Threat Intelligence",
            "Incident Response"
        ])
    ]
    
    start_time = time.time()
    print(f"Generating test transcript of approximately {args.size} characters...")
    
    # Generate the transcript
    transcript = generate_transcript(topics, args.size)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Write to file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(transcript)
    
    generation_time = time.time() - start_time
    actual_size = len(transcript)
    
    print(f"Generated transcript of {actual_size} characters in {generation_time:.2f} seconds")
    print(f"Saved to: {args.output}")

if __name__ == "__main__":
    main() 