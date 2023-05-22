# PersonalChatGPT

## Installation

First, clone the git repository:

```bazaar
cd <targetdir>
git clone https://github.com/stephenhky/PersonalChatGPT.git
```

Then go to the directory.

```bazaar
cd PersonalChatCPT
```

Create a new conda environment:

```bazaar
conda env create -n <envname> -f environment.yml
```

Get your own OpenAI API (instruction found [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)). Then add
the file `.env` which contains the environment variable like this:

```bazaar
OPENAIKEY=<OpenAIAPIKey>
```

## Activate the Conda Environment

To run any of the following scripts, you have to activate
the conda environment by

```bazaar
conda activate <envname>
```

After you have finished running everything, to deactivate the 
environment, just enter 

```bazaar
conda deactivate 
```

## Running ChatGPT

First, activate the conda environment, and go to the 
directory of the git repository. Then type:

```bazaar
python run_terminal_chatgpt_35turbo.py
```

This will run the same ChatGPT as in the web version.

## Train Customized Model 

First, put all your training data files (*.txt, *.pdf etc.) in a directory.
Then activate your conda environment (if you have not done so).
Go to the directory of the git repository. Then type

```bazaar
python train_gpt_index_model.py <trainingdatadir> <modeldir>
```

After a certain amount of time (depending on the web speed and 
the number of documents), the final trained GPT model will
be stored in the directory under your specified `<modeldir>`.
There will be a few JSON files underneath it.

## Run the Customized Model

First, activate your conda environment (if you have not done so).
Then go to the directory of the git repository. Then type

```bazaar
python run_customized_gpt.py <modeldir>
```

