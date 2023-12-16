# Flask Server Example

This is a simple example of a Python Flask server. It includes instructions on how to start the server and use it.

## Prerequisites

- Python 3.x installed
- Flask library installed (`pip install Flask`)

## Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/Harri200191/kitaabkhoj-BE-Python.git

2. **Create a virtual environment (optional but recommended):**

    ```bash 
    python -m venv venv   

3. **Activate the virtual environment:**

    - On Windows:

        ```bash 
        venv\Scripts\activate
    - On macOS/Linux:

        ```bash
        source venv/bin/activate

4. **Run the Flask server:**

    ```bash 
    python app.py
    ```

   This will start the server on http://127.0.0.1:5000/.
   
   Open your web browser and go to http://127.0.0.1:5000/. You should see a simple message indicating that the server is running.

5. **Contributing**
   
   Contributions are welcome! If you find a bug or have an improvement, please open an issue or create a pull request.

6. **Usage**:
   
   Can be used in React frontend like:

   ```code
   const response = await fetch(http://localhost:5000/process_text?txt=${<input text>}); 
   const data = await response.json();
   const author = data.author
   const book = data.book
   ```
