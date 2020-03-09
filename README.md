# DISCovery-RM07
Prototype code for RM07 Praxis II design project.

## Installation Instructions
1. Navigate to the folder you want to save the project to, then run:
    
       git clone https://github.com/HPrickettMorgan/DISCovery-RM07.git
2. From that folder, install the required libraries by running:
       
       pip3 install -r requirements.txt
3. Start the jupyter notebook server by running:

       jupyter notebook

You should now be able to view and modify all the jupyter notebooks in the project.

## Troubleshooting Installation
If imports complain about not being able to find `libmagic` or `ffmpeg` you may need to install those dependencies.

### On Mac OS X
1. Install the hombrew package manager:
    
       /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
2. If you are missing `libmagic`:
 
       brew install libmagic
     
3. If you are missing `ffmpeg`:
 
       brew install ffmpeg
