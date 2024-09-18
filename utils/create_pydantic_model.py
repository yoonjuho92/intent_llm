from pydantic import BaseModel, create_model
from typing import List, Dict, Any

class Entity(BaseModel):
    keyword: str = ""

def create_output_model(entity_names: List[str]):
    print(entity_names)
    try:
        # Create the Entities model
        entity_fields: Dict[str, Any] = {
            "names": (List[str], ...)
        }
        for name in entity_names:
            entity_fields[name] = (Entity, {"keyword":""})
        
        DynamicEntities = create_model("Entities", **entity_fields)

        # Create the Data model
        DataModel = create_model(
            "Data",
            intent=(str, ...),
            entities=(DynamicEntities, ...),
            tail=(str, ...)
        )

        # Create the OutputModel
        OutputModel = create_model(
            "OutputModel",
            data=(DataModel, ...) 
        )

        return OutputModel

    except Exception as e:
        print(f"An error occurred in create_output_model: {str(e)}")
        raise

# Export the create_output_model function
__all__ = ['create_output_model']