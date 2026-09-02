#!/usr/bin/env -S uv run python

import os
from pathlib import Path
from anthropic import Anthropic

def main() -> None:
    anthropic = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    # Upload a DOCX file
    docx_file_path = Path("example.docx")
    
    # Check if the file exists first
    if not docx_file_path.exists():
        print(f"File {docx_file_path} does not exist. Creating a sample DOCX file for demonstration.")
        # In a real scenario, you would have an actual DOCX file to upload
        
        # For this example, we'll just demonstrate the method call structure
        print("To upload a DOCX file, use:")
        print("file = anthropic.beta.files.upload(file=Path('your_file.docx'))")
        return
    
    # Upload the DOCX file
    try:
        file = anthropic.beta.files.upload(
            file=docx_file_path,
        )
        print(f"Successfully uploaded file: {file.id}")
        print(f"File name: {file.filename}")
        print(f"File size: {file.size} bytes")
        print(f"File type: {file.type}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    main()
