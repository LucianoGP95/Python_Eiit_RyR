mean_fbx = [1, 2, 3, 4, 5]
lenses_per_nest = 3

for index in range(lenses_per_nest):
    specific_lens_values = mean_fbx[index::lenses_per_nest]
    print(specific_lens_values)