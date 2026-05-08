import typer
import numpy
import os
from sentence_transformers import SentenceTransformer
import httpx
import gzip
from pathlib import Path

############################################################################################################################################################################################################################################
app = typer.Typer()


model = SentenceTransformer(
    "mixedbread-ai/mxbai-embed-large-v1",
    prompts={"retrieval": "Represent this sentence for searching relevant passages: "},
)



pinsy_path = Path(__file__).resolve().parent / "pinsy.csv"
bepen_path = Path(__file__).resolve().parent / "bepen.csv"
picab_path = Path(__file__).resolve().parent / "picab.csv"
tieton_path = Path(__file__).resolve().parent / "tieton.csv"
arabidopsis_path = Path(__file__).resolve().parent / "arabidopsis.csv"
potra_path = Path(__file__).resolve().parent / "potra.csv"

pinsy_lines = pinsy_path.read_text().splitlines()
picab_lines = picab_path.read_text().splitlines()
tieton_lines = tieton_path.read_text().splitlines()
bepen_lines = bepen_path.read_text().splitlines()
arabidopsis_lines = arabidopsis_path.read_text().splitlines()
potra_lines = potra_path.read_text().splitlines()


pinsy_ID = []
picab_ID=[]
tieton_ID=[]
bepen_ID=[]
arabidopsis_ID = []
potra_ID = []
pinsy_description = []
picab_description = []
tieton_description = []
bepen_description = []
arabidopsis_description =[]
potra_description = []




for line in pinsy_lines:
    id_, desc = line.split(",", 1)
    pinsy_ID.append(id_)
    pinsy_description.append(desc)


for line in picab_lines:
    id_, desc = line.split(",", 1)
    picab_ID.append(id_)
    picab_description.append(desc)


for line in tieton_lines:
    id_, desc = line.split(",", 1)
    tieton_ID.append(id_)
    tieton_description.append(desc)


for line in bepen_lines:
    id_, desc = line.split(",", 1)
    bepen_ID.append(id_)
    bepen_description.append(desc)


for line in arabidopsis_lines:
    id_, desc = line.split(",", 1)
    arabidopsis_ID.append(id_)
    arabidopsis_description.append(desc)


for line in potra_lines:
    id_, desc = line.split(",", 1)
    potra_ID.append(id_)
    potra_description.append(desc)




# print(f"These are the first 5 lines of IDs with their description for Pinsy: {list(zip(pinsy_ID, pinsy_description))[:5]}")
# print(f"These are the first 5 lines of IDs with their description for Picab: {list(zip(picab_ID, picab_description))[:5]}")
# print(f"These are the first 5 lines of IDs with their description for Tieton: {list(zip(tieton_ID, tieton_description))[:5]}")
# print(f"These are the first 5 lines of IDs with their description for Bepen: {list(zip(bepen_ID, bepen_description))[:5]}")
# print(f"These are the first 5 lines of IDs with their description for Arabidopsis: {list(zip(arabidopsis_ID, arabidopsis_description))[:5]}")
# print(f"These are the first 5 lines of IDs with their description for Potra: {list(zip(potra_ID, potra_description))[:5]}")


############################################################################################################################################################################################################################################

pinsy_gene_ids_file = "pinsy-gene-ids.npy"
pinsy_embeddings_file = "pinsy-embeddings.npy"

if os.path.exists(pinsy_embeddings_file):
    print("Loading embeddings from disk for pinsy...")
    pinsy_embeddings = numpy.load(pinsy_embeddings_file)
    pinsy_ids = list(numpy.load(pinsy_gene_ids_file, allow_pickle=True))
else:
    print(f"Something is wrong with the pinsy file... Compute the embeddings again")





bepen_gene_ids_file = "bepen-gene-ids.npy"
bepen_embeddings_file = "bepen-embeddings.npy"

if os.path.exists(bepen_embeddings_file):
    print("Loading embeddings from disk for bepen...")
    bepen_embeddings = numpy.load(bepen_embeddings_file)
    bepen_ids = list(numpy.load(bepen_gene_ids_file, allow_pickle=True))
else:
    print(f"Something is wrong with the bepen file... Compute the embeddings again")




tieton_gene_ids_file = "tieton-gene-ids.npy"
tieton_embeddings_file = "tieton-embeddings.npy"

if os.path.exists(tieton_embeddings_file):
    print("Loading embeddings from disk for tieton...")
    tieton_embeddings = numpy.load(tieton_embeddings_file)
    tieton_ids = list(numpy.load(tieton_gene_ids_file, allow_pickle=True))
else:
    print(f"Something is wrong with the tieton file... Compute the embeddings again")




picab_gene_ids_file = "picab-gene-ids.npy"
picab_embeddings_file = "picab-embeddings.npy"

if os.path.exists(picab_embeddings_file):
    print("Loading embeddings from disk for picab...")
    picab_embeddings = numpy.load(picab_embeddings_file)
    picab_ids = list(numpy.load(picab_gene_ids_file, allow_pickle=True))
else:
    print(f"Something is wrong with the picab file... Compute the embeddings again")



arabidopsis_gene_ids_file = "arabidopsis-gene-ids.npy"
arabidopsis_embeddings_file = "arabidopsis-embeddings.npy"

if os.path.exists(arabidopsis_embeddings_file):
    print("Loading embeddings from disk for arabidopsis...")
    arabidopsis_embeddings = numpy.load(arabidopsis_embeddings_file)
    arabidopsis_ids = list(numpy.load(arabidopsis_gene_ids_file, allow_pickle=True))
else:
    print(f"Something is wrong with the arabidopsis file... Compute the embeddings again")



potra_gene_ids_file = "potra-gene-ids.npy"
potra_embeddings_file = "potra-embeddings.npy"

if os.path.exists(potra_embeddings_file):
    print("Loading embeddings from disk for potra...")
    potra_embeddings = numpy.load(potra_embeddings_file)
    potra_ids = list(numpy.load(potra_gene_ids_file, allow_pickle=True))
else:
    print(f"Something is wrong with the potra file... Compute the embeddings again")




############################################################################################################################################################################################################################################


# def search(query, num_of_top_results):
#     """ Search for semantically similar genes based on a query with a desired number of top results to appear. """
#     query_embedding = model.encode_query(query, prompt= "Search: ")
#     similarities = model.similarity(query_embedding, embeddings).squeeze()
#     indices= similarities.argsort(descending=True).squeeze().tolist()
#     print(f"\nTop {num_of_top_results} results for \"{query}\": ")
#     for i in range(num_of_top_results):
#         index = indices[i]
#         score = similarities[index].item()
#         print(f"\nGene: {gene_ids[index]} \nIndices: {embeddings[index]} \nSimilarity score: {score} \nDescription: {description[index]}")




############################################################################################################################################################################################################################################

# app = typer.Typer()

# @app.command()
# def search(query: str, num_of_top_results:int = 10):
#     """ Search for semantically similar genes based on a query with a desired number of top results to appear. Automatically prints top 10 results unless specified. """
#     query_embedding = model.encode_query(query, prompt= "Search: ")
#     similarities = model.similarity(query_embedding, embeddings).squeeze()
#     indices= similarities.argsort(descending=True).squeeze().tolist()
#     print(f"\nTop {num_of_top_results} results for \"{query}\": ")
#     for i in range(num_of_top_results):
#         index = indices[i]
#         score = similarities[index].item()
#         print(f"\nGene: {gene_ids[index]} \nIndices: {embeddings[index]} \nSimilarity score: {score} \nDescription: {description[index]}")





############################################################################################################################################################################################################################################
 

@app.command()
def search(pinsy: bool = False, picab: bool = False, potra: bool = False, arabidopsis: bool = False, bepen: bool = False, tieton: bool = False):
    """Search a bioilogical process to find a desired number of genes among different species. Default output: Most relative genes from all available species. 
    Available options: --arabidopsis --pinsy --picab --potra --tieton --bepen, to search exclusively within these species. """
    if pinsy: 
        query= input("You are searching for Pinus Sylvestris. What kind of genes are you looking for?")
        number = int(input("How many results do you want to see? "))
        query_embedding = model.encode_query(query)
        similarities = model.similarity(query_embedding, pinsy_embeddings).squeeze()
        indices= similarities.argsort(descending=True).squeeze().tolist()
        print(f"\nTop {number} results for \"{query}\": ")
        for i in range(number):
            index = indices[i]
            score = similarities[index].item()
            print(f"\nGene: {pinsy_ids[index]} \nIndices: {pinsy_embeddings[index]} \nSimilarity score: {score} \nDescription: {pinsy_description[index]}")
    elif picab: 
        query= input("You are searching for Picea abies. What kind of genes are you looking for?")
        number = int(input("How many results do you want to see? "))
        query_embedding = model.encode_query(query)
        similarities = model.similarity(query_embedding, picab_embeddings).squeeze()
        indices= similarities.argsort(descending=True).squeeze().tolist()
        print(f"\nTop {number} results for \"{query}\": ")
        for i in range(number):
            index = indices[i]
            score = similarities[index].item()
            print(f"\nGene: {picab_ids[index]} \nIndices: {picab_embeddings[index]} \nSimilarity score: {score} \nDescription: {picab_description[index]}")
    elif potra:
        query= input("You are searching for Populus tremula. What kind of genes are you looking for?")
        number = int(input("How many results do you want to see? "))
        query_embedding = model.encode_query(query)
        similarities = model.similarity(query_embedding, potra_embeddings).squeeze()
        indices= similarities.argsort(descending=True).squeeze().tolist()
        print(f"\nTop {number} results for \"{query}\": ")
        for i in range(number):
            index = indices[i]
            score = similarities[index].item()
            print(f"\nGene: {potra_ids[index]} \nIndices: {potra_embeddings[index]} \nSimilarity score: {score} \nDescription: {potra_description[index]}")
    elif arabidopsis:
        query= input("You are searching for Arabidopsis thaliana. What kind of genes are you looking for?")
        number = int(input("How many results do you want to see? "))
        query_embedding = model.encode_query(query)
        similarities = model.similarity(query_embedding, arabidopsis_embeddings).squeeze()
        indices= similarities.argsort(descending=True).squeeze().tolist()
        print(f"\nTop {number} results for \"{query}\": ")
        for i in range(number):
            index = indices[i]
            score = similarities[index].item()
            print(f"\nGene: {arabidopsis_ids[index]} \nIndices: {arabidopsis_embeddings[index]} \nSimilarity score: {score} \nDescription: {arabidopsis_description[index]}")
    elif tieton:
        query= input("You are searching for Tilia tomentosa. What kind of genes are you looking for?")
        number = int(input("How many results do you want to see? "))
        query_embedding = model.encode_query(query)
        similarities = model.similarity(query_embedding, tieton_embeddings).squeeze()
        indices= similarities.argsort(descending=True).squeeze().tolist()
        print(f"\nTop {number} results for \"{query}\": ")
        for i in range(number):
            index = indices[i]
            score = similarities[index].item()
            print(f"\nGene: {tieton_ids[index]} \nIndices: {tieton_embeddings[index]} \nSimilarity score: {score} \nDescription: {tieton_description[index]}")
    elif bepen:
        query= input("You are searching for Betula pendula. What kind of genes are you looking for?")
        number = int(input("How many results do you want to see? "))
        query_embedding = model.encode_query(query)
        similarities = model.similarity(query_embedding, bepen_embeddings).squeeze()
        indices= similarities.argsort(descending=True).squeeze().tolist()
        print(f"\nTop {number} results for \"{query}\": ")
        for i in range(number):
            index = indices[i]
            score = similarities[index].item()
            print(f"\nGene: {bepen_ids[index]} \nIndices: {bepen_embeddings[index]} \nSimilarity score: {score} \nDescription: {bepen_description[index]}")
    else: 
        print("Choose between --pinsy --arabidopsis --potra --bepen --tieton and --picab. Write: python test_embeddings.py search --<species of choice>")




############################################################################################################################################################################################################################################


if __name__ == "__main__":
    app()

