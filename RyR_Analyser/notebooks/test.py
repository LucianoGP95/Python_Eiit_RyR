import configparser

for j in range(3):  # This outer loop controls the 'j' iteration
    for i in range(2):  # This inner loop controls the 'i' iteration, iterating twice for each 'j'
        print(f"j={j}, i={i}")
