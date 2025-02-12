def parseKeyPair(items:list[str], keyType, valueType) -> dict:
    """
        Parses and cast a series of key-value pairs and returns a dictionary.
        Adapted from : https://stackoverflow.com/a/65692916

        Args:
            items : The list of strings to parse in the following format `["0=Value 1", "1=Value 2"]`
            keyType : The type used for casting the keys
            valueType : The type used for casting the values

        Raises:
            ValueError : If there is no equal sign dividing the key and value pair
    """
    dictionnary = {}

    for item in items:
        if "=" in item:
            split_string = item.split("=")

            key = (keyType)(split_string[0].strip())
            value = (valueType)(split_string[1].strip())

            dictionnary[key] = value
        else:
            raise ValueError(f"Invalid argument provided - {item}")
        
    return dictionnary
