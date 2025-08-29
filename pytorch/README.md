# PyTorch Source Files

Wherever we begin to host, whether it be through the cloud or locally, this folder serves as a source for all of our PyTorch files.

NOTE: If you import something into your scripts, add your library to the ``requirements.txt`` file. That way, when installing libraries, you can use ``pip install -r requirements.txt`` to get every required library to run code in this folder.

# Setting up Your Virtual Environment (for running locally)

This is the best way to have our Python code run EXACTLY the way it runs on your PC, just as it runs on mine.

## On Windows
- Use ``Ctrl + ` ``to open the terminal (if it's not opened already)

From the VS Code terminal:
- Navigate to the pytorch folder using ``cd pytorch``
- Run the command ``python3 -m venv .venv`` to create it
- To activate it, run ``.\.venv\Scripts\activate.ps1`` 
    - If you're using CMD, run ``.\.venv\Scripts\activate.bat`` instead
- Use ``pip install torch`` to install the PyTorch library (replace/add to "torch" with other libraries if need be)
## On Linux/Mac
From the terminal:
- Navigate to the pytorch folder using ``cd pytorch``
- Run the command ``python3 -m venv .venv`` to create it
- To activate it, run ``source .venv/bin/activate``
    - Your terminal should look something like this now: ``(.venv) ┌─[nick@archer] - [~/Software-Engineering-25-26/pytorch]``
- Use ``pip install torch`` to install the PyTorch library (replace/add to "torch" with other libraries if need be)