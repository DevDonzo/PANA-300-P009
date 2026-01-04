#!/usr/bin/env python3

def hello_world():
    """Simple test script to validate the hook"""
    print("Hello from test script!")
    return "Success"

if __name__ == "__main__":
    result = hello_world()
    print(f"Result: {result}")
