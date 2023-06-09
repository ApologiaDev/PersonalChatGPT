
import os
from argparse import ArgumentParser
from time import time
from glob import glob

from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAIKEY')


def construct_index(directory_path, outputdir):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTVectorStoreIndex.from_documents(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.storage_context.persist(persist_dir=outputdir)

    return index


def get_argparser():
    argparser = ArgumentParser(description='Train GPT index from documents')
    argparser.add_argument('corpusdir', help='directory of the training data')
    argparser.add_argument('outputdir', help='directory of output index')
    return argparser


def get_directory_books(corpusdir):
    for bookpath in glob(os.path.join(corpusdir, "*.pdf")):
        bookfilename = os.path.basename(bookpath)
        yield bookfilename


if __name__ == '__main__':
    args = get_argparser().parse_args()
    starttime = time()
    _ = construct_index(args.corpusdir, args.outputdir)
    endtime = time()
    print('Time elapsed: {} sec'.format(endtime-starttime))

    # write book file name
    f = open(os.path.join(args.outputdir, 'traincorpus.txt'), 'w')
    for bookfilename in get_directory_books(args.corpusdir):
        f.write(bookfilename+'\n')
    f.close()
