from portal.solutions import *




def twoSum(nums, target):
    num_dict = {}

    for index, num in enumerate(nums):
        complement = target - num

        if complement in num_dict:
            return [num_dict[complement], index]

        num_dict[num] = index

    return []  # Inject user code

if __name__ == '__main__':
    from portal.solutions import *
    result = twoSum(**{'nums': [2, 7, 11, 15], 'target': 9})  # Pass input(s) dynamically
    
    if isinstance(result, pd.DataFrame):
        output = {
            "headers": result.columns.tolist(),
            "values": result.values.tolist()
        }
    elif isinstance(result, list) or isinstance(result, dict):
        output = json.dumps(result)  # Convert list or dict to JSON
    else:
        output = result  # For simple types like int, str, etc.
    try:
        print(json.dumps(output))
    except:
        print(output)
    