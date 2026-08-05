from pymilvus import MilvusClient


class milvus_clerk:

    def __init__(self, db_name: str, collection_name: str, dimension: int, recreate: bool = False):
        self.collection_name = collection_name
        self.dimension = dimension

        # MilvusClient requires a URI/filepath or connection address
        self.client = MilvusClient(uri=db_name)
        
        if recreate:
            self._drop_collection()
        self._create_collection()

        # Load collection requires specifying which collection to load
        self.client.load_collection(collection_name=self.collection_name)

    def _drop_collection(self):
        """Drop collection if it exists."""
        collections = self.client.list_collections()
        if self.collection_name in collections:
            self.client.drop_collection(collection_name=self.collection_name)

    def _create_collection(self):
        """Creates collection if it doesn't already exist."""
        collections = self.client.list_collections()

        if self.collection_name not in collections:
            from pymilvus import DataType
            
            schema = self.client.create_schema(
                auto_id=True,
                enable_dynamic_field=True
            )
            schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
            schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=self.dimension)
            schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=65535)
            schema.add_field(field_name="metadata", datatype=DataType.JSON)
            
            index_params = self.client.prepare_index_params()
            index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")
            
            self.client.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params
            )

    def insert(self, vectors: list, texts: list, metadata: list):
        """INSERT VECTORS"""
        if not (len(vectors) == len(texts) == len(metadata)):
            raise ValueError("Vectors, texts, and metadata must have same length")

        entities = []
        for i, (vector, text, meta) in enumerate(zip(vectors, texts, metadata)):
            entity = {
                "vector": vector,
                "text": text,
                "metadata": meta
            }
            entities.append(entity)

        self.client.insert(
            collection_name=self.collection_name, data=entities
        )

    def search(
        self, vector: list, top_k: int = 2, output_fields: list | None = None
    ):
        if output_fields is None:
            output_fields = ["text"]

        return self.client.search(
            collection_name=self.collection_name,
            data=[vector],
            limit=top_k,
            output_fields=output_fields,
        )

    def query(self, filter_expr: str, output_fields: list | None = None):
        """Query elements using a scalar filter expression (e.g., 'id in [1, 2]')."""
        if output_fields is None:
            output_fields = ["text"]

        return self.client.query(
            collection_name=self.collection_name,
            filter=filter_expr,
            output_fields=output_fields,
        )

    def delete(self, collection_n: str | None = None):
        """Drops the specified collection, or defaults to the instance collection."""
        target_coll = collection_n or self.collection_name

        if self.client.has_collection(collection_name=target_coll):
            self.client.drop_collection(collection_name=target_coll)
            return {
                "msg": "successfully removed",
                "coll_name": target_coll
            }

        return {
            "msg": "collection does not exist",
            "coll_name": target_coll
        }

    def list(self):
        return self.client.list_collections()