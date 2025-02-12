def parseKeyPair(items:list[str]) -> dict:
    """
        Parses a series of key-value pairs and return a dictionary.
        Assumes that the keys are integers and the values are strings.
        Adapted from : https://stackoverflow.com/a/65692916

        Args:
            items : The list of strings to parse in the following format `["0=Value 1", "1=Value 2"]`

        Raises:
            ValueError : If there is no equal sign dividing the key and value pair
    """
    dictionnary = {}

    for item in items:
        if "=" in item:
            split_string = item.split("=")

            key = (int)(split_string[0].strip())
            value = split_string[1].strip()

            dictionnary[key] = value
        else:
            raise ValueError(f"Invalid argument provided - {item}")
        
    return dictionnary
