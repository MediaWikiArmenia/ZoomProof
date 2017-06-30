from collections import Counter

def calculate_mean(numbers):
  """calculate the mean of a list of numbers"""
  return round(sum(numbers) / len(numbers), 3)

def calculate_median(numbers):
  """calculate the median of a list of numbers"""
  l = len(numbers)
  center_pos = (l - 1) // 2
  #if numbers has an odd length
  if l % 2 == 1: 
    #return center element
    return numbers[center_pos]
  #if numbers has an even length
  else:
    #return mean of two center elements
    return round((numbers[center_pos] + numbers[center_pos + 1]) / 2, 3)

def calculate_mode(numbers):
  """calculate the mode (the most common element) of numbers"""
  count = Counter(numbers)
  #return element of (element, count) that has the highest count
  return count.most_common(1)[0][0]
