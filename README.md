# haiku-generator
A command-line program to generate haiku using Markov chains.

> O Grave, where was thy   
> sting? O Grave, where was thy sting?  
> O Grave, where was I?

(Source text: Walden)

> caw! caw! caw! caw! caw!  
> caw! caw! caw! caw! caw! caw! caw!  
> caw! caw! caw! caw! caw!

(Source text: Moby Dick)

## Install
You'll need to install [Python 3](https://www.python.org/downloads/). 

    pip3 install -r requirements.txt
    python3 -m nltk.downloader cmudict punkt #download required nltk data
    
If you're on OS X and these commands give you a CERTIFICATE_VERIFY_FAILED error, [read this](https://bugs.python.org/msg283984) for help fixing it.
     
## Test
    python3 -m unittest discover
    
## Usage

    ./haiku.py                   # Generate a haiku with default options (prefix length = 2, source text is corpus/moby_dick.txt)
    ./haiku.py corpus/walden.txt # Use Walden as source text
    ./haiku.py -l 4              # Use prefix length of 3 for Markov chain generation

## Input files

There are several sample source texts in the ``corpus`` directory, or you can use one of your own. 
For best results, use long passages of text with punctuation, and remove chapter headings, footnotes, etc.
