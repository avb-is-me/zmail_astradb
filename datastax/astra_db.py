""" Astra Database Helper Functions """
import os
import astrapy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the DataStax Astra DataAPIClient
ASTRA_DB_APPLICATION_TOKEN=os.environ["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_API_ENDPOINT=os.environ["ASTRA_DB_API_ENDPOINT"]

# Initialize the Langflow API
LANGFLOW_BASE_API_URL=os.environ["LANGFLOW_BASE_API_URL"]
LANGFLOW_FLOW_ENDPOINT=os.environ["LANGFLOW_FLOW_ENDPOINT"]
LANGFLOW_FLOW_ID=os.environ["LANGFLOW_FLOW_ID"]
LANGFLOW_APPLICATION_TOKEN=os.environ["LANGFLOW_APPLICATION_TOKEN"]

client = astrapy.DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
database = client.get_database(ASTRA_DB_API_ENDPOINT)

def create_collection(collection_name, embedding_and_chunk_size):
    """
    Create a collection in the Astra database with the specified name and embedding model dimension.

    Args:
        collection_name (str): The name of the collection to create.
        embedding_and_chunk_size (int): The dimension of the embedding model and chunk size.

    Returns:
        Collection: The created collection object.

    Raises:
        astrapy.exceptions.CollectionAlreadyExistsException: If the collection already exists.
    """
    print(f"Creating Astra database collection '{collection_name}'...")

    # Create collection with Nvidia's NV-Embed-QA embedding model
    try:
        collection = database.create_collection(
            collection_name,
            dimension=embedding_and_chunk_size,
            service={"provider": "nvidia", "modelName": "NV-Embed-QA"},
            metric=astrapy.constants.VectorMetric.COSINE,
            check_exists=True,
        )
        return collection
    except astrapy.exceptions.CollectionAlreadyExistsException:
        print(f"Astra database collection '{collection_name}' already exists, moving on...")
        return database.get_collection(collection_name)

def get_collection(collection_name):
    """
    Retrieve a collection from the Astra database with the specified name.

    Args:
        collection_name (str): The name of the collection to retrieve.

    Returns:
        Collection: The retrieved collection object.
    """
    return database.get_collection(collection_name)
