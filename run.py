# run.py

from Welcome_page import User_IF

if __name__ == "__main__":
    try:
        User_IF.greet()
        User_IF.welcome_menu()
    
    except ValueError as e:
        print(f"Error: {e}")
        
    finally:
        User_IF.farewell()