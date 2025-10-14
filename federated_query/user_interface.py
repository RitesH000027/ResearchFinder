# Handles user input and output

def get_user_query():
    query = input("Enter your research query: ")
    return query

# For testing/demo purposes
if __name__ == "__main__":
    print(get_user_query())