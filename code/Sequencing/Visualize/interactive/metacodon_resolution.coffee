models = cb_obj.document._all_models_by_name._dict

lines = (v for k, v of models when k.startsWith('line_'))
x_ranges = (v for k, v of models when k.startsWith('x_range'))

resolution = cb_obj.labels[cb_obj.active][...-(' resolution'.length)]

for x_range in x_ranges
    if resolution == 'nucleotide'
        x_range.start = x_range.start * 3
        x_range.end = x_range.end * 3
    else
        x_range.start = x_range.start / 3
        x_range.end = x_range.end / 3

for line_group in lines
    if not Array.isArray(line_group)
        line_group = [line_group]
    for line in line_group
        name = line.name['line_'.length..]
        source = models['source_' + name + '_' + resolution]
        line.data_source.data = source.data
