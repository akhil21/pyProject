import numpy as np

def normalize_histogram(histogram):
    total = np.sum(list(histogram.values()))
    for key in histogram.keys():
        histogram[key]/= total
    return histogram

def write_dataset(registry, dataset, result, projector):
    data_dict = result.get_iq_data_dict()
    hist_dict = projector.get_histogram_dict(data_dict)
    dataset.reset()
    for key, histogram in zip(registry.queue.keys(), hist_dict):
        result = {
            "type"      : "experiment",
            "histogram" : normalize_histogram(histogram),
            "shot"      : 1000,
            "hist_std"  : None
        }
        dataset.save(key,result)