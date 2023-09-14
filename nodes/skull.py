
def mask_auto_threshold(img_file, operation, index):
    import os
    import numpy as np
    import nibabel as nib
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    from nipype.utils.filemanip import split_filename as split_f

    ## Mean function
    def calculate_mean(data):
        total = sum(data)
        count = len(data)
        mean = total / count
        return mean

    img_nii = nib.load(img_file)
    img_arr = np.array(img_nii.dataobj)

    # Reshape data to a 1D array (required by k-means)
    X = np.copy(img_arr).flatten().reshape(-1, 1)

    print("X shape : ", X.shape)

    # Create a k-means clustering model with 3 clusters
    # using k-means++ initialization

    num_clusters = 3

    kmeans = KMeans(n_clusters=num_clusters, random_state=0)

    # Fit the model to the data and predict cluster labels
    cluster_labels = kmeans.fit_predict(X)

    # Split data into groups based on cluster labels
    groups = [X[cluster_labels == i].flatten() for i in range(num_clusters)]

    avail_operations = ["min", "mean", "max"]

    assert operation in avail_operations, "Error, \
        {} is not in {}".format(operation, avail_operations)

    assert 0 <= index and index < num_clusters-1, "Error \
        with index {}".format(index)

    # We must define : the minimum of the second group for the headmask
    # we create minimums array, we sort and then take the middle value
    minimums_array = np.array([np.amin(group) for group in groups])
    min_sorted = np.sort(minimums_array)

    print("Min : {}".format(" ".join(str(val) for val in min_sorted)))

    # We must define :  mean of the second group for the skull extraction
    # we create means array, we sort and then take the middle value
    means_array = np.array([calculate_mean(group) for group in groups])
    mean_sorted = np.sort(means_array)

    index_sorted = np.argsort(means_array)

    print("Mean : {}".format(" ".join(str(int(val)) for val in mean_sorted)))

    print("Index = {}".format(" ".join(str(int(val)) for val in index_sorted)))

    print("Index mid group : ", index_sorted[index])
    print("Min/max mid group : ", np.amin(groups[index_sorted[index]]),
          np.amax(groups[index_sorted[index]]))

    maximums_array = np.array([np.amax(group) for group in groups])
    max_sorted = np.sort(maximums_array)

    print("Max : {}".format(" ".join(str(val) for val in max_sorted)))

    if operation == "min":  # for head mask
        mask_threshold = min_sorted[index]
        print("headmask_threshold : ", mask_threshold)

    elif operation == "mean":  # for skull mask

        mask_threshold = mean_sorted[index]
        print("skull_extraction_threshold : ", mask_threshold)

    elif operation == "max":  # unused

        mask_threshold = max_sorted[index]
        print("max threshold : ", mask_threshold)

    return mask_threshold


def mask_auto_img(img_file, operation, index, sample_bins, distance):

    import os
    import numpy as np
    import nibabel as nib
    import matplotlib.pyplot as plt

    from scipy.signal import find_peaks

    from nipype.utils.filemanip import split_filename as split_f

    def compute_Kmeans(img_arr, operation, index=1, num_clusters=3):
        import os
        import numpy as np
        import nibabel as nib
        import matplotlib.pyplot as plt
        from sklearn.cluster import KMeans
        ## Mean function
        def calculate_mean(data):
            total = sum(data)
            count = len(data)
            mean = total / count
            return mean

        g = open(os.path.abspath("kmeans.log"), "w+")

        print("Running Kmeans with : ", operation, index, num_clusters)

        g.write("Running Kmeans with : {} {} {}".format(
            operation, index, num_clusters))


        # Reshape data to a 1D array (required by k-means)
        X = np.copy(img_arr).flatten().reshape(-1, 1)

        kmeans = KMeans(n_clusters=num_clusters, random_state=0)

        # Fit the model to the data and predict cluster labels
        cluster_labels = kmeans.fit_predict(X)

        # Split data into groups based on cluster labels
        groups = [X[cluster_labels == i].flatten() for i in range(num_clusters)]

        avail_operations = ["min", "interval", "max"]

        assert operation in avail_operations, "Error, \
            {} is not in {}".format(operation, avail_operations)

        assert 0 <= index and index < num_clusters-1, "Error \
            with index {}".format(index)

        # We must define : the minimum of the second group for the headmask
        # we create minimums array, we sort and then take the middle value
        minimums_array = np.array([np.amin(group) for group in groups])
        min_sorted = np.sort(minimums_array)

        print("Min : {}".format(" ".join(str(val) for val in min_sorted)))
        g.write("Min : {}".format(" ".join(str(val) for val in min_sorted)))

        # We must define :  mean of the second group for the skull extraction
        # we create means array, we sort and then take the middle value
        means_array = np.array([calculate_mean(group) for group in groups])
        mean_sorted = np.sort(means_array)

        index_sorted = np.argsort(means_array)

        print("Mean : {}".format(" ".join(str(int(val)) for val in mean_sorted)))
        g.write("Mean : {}".format(" ".join(str(int(val)) for val in mean_sorted)))

        print("Index = {}".format(" ".join(str(int(val)) for val in index_sorted)))
        g.write("Index = {}".format(" ".join(str(int(val)) for val in index_sorted)))

        print("Index mid group : ", index_sorted[index])
        g.write("Index mid group : {}".format(index_sorted[index]))

        min_thresh = np.amin(groups[index_sorted[index]])
        max_thresh = np.amax(groups[index_sorted[index]])

        print("Min/max mid group : {} {}".format( min_thresh, max_thresh))
        g.write("Min/max mid group : {} {}".format( min_thresh, max_thresh))

        if operation == "min":

            fiter_array = min_thresh < img_arr

        elif operation == "max":

            fiter_array = img_arr < max_thresh

        elif operation == "interval":

            fiter_array = np.logical_and(min_thresh < img_arr, img_arr < max_thresh)

        g.close()

        return fiter_array

    path, fname, ext = split_f(img_file)

    log_file = os.path.abspath(fname + ".log")

    f = open(log_file, "w+")


    print("Running local minimas with : ", operation, index, sample_bins, distance)

    f.write("Running local minimas with : {} {} {} {}\n".format(operation, index, sample_bins, distance))

    img_nii = nib.load(img_file)
    img_arr = np.array(img_nii.dataobj)

    # Reshape data to a 1D array (required by k-means)
    X = np.copy(img_arr).flatten().reshape(-1, 1)

    print("X shape : ", X.shape)

    print("X max : ", np.round(np.max(X)))
    nb_bins = (np.rint(np.max(X)/sample_bins)).astype(int)
    print("Nb bins: ", nb_bins)

    f.write("X shape : {}\n".format(X.shape))
    f.write("X max : {}\n".format(np.round(np.max(X))))
    f.write("Nb bins: {}\n".format(nb_bins))

    # Create a histogram
    hist, bins, _ = plt.hist(X, bins=nb_bins,
                             alpha=0.5, color='b', label='Histogram')

    # Add labels and a legend
    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.title('Histogram')
    plt.legend()

    # Save the figure as a PNG file
    plt.savefig(os.path.abspath('histogram.png'))

    # Find local minima in the histogram
    peaks, _ = find_peaks(-hist, distance = distance)  # Use negative histogram for minima

    print("peaks indexes :", peaks)

    print("peak_hist :", hist[peaks])
    print("peak_bins :", bins[peaks])

    f.write("peaks indexes : {}\n".format(peaks))
    f.write("peak_hist : {}\n".format(hist[peaks]))
    f.write("peak_bins : {}\n".format(bins[peaks]))


    # filtering
    new_mask_data = np.zeros(img_arr.shape, dtype=img_arr.dtype)

    assert operation in ["higher", "interval", "lower"], \
        "Error in operation {}".format(operation)

    proceed = True

    if operation == "interval":
        if not (isinstance(index, list) and len(index) == 2):
            print("Error, index {} should be a list for interval".format(
                index))
            proceed = False

        if not (peaks.shape[0] > 1):
            print("Error, could not find at least two local minima")
            proceed = False

        if index[0] < 0 or len(bins[peaks]) <= index[0]:
            print("Error, index 0 {} out of peak indexes ".format(index[0]))
            proceed = False

        if index[1] < index[0] or len(bins[peaks]) <= index[1]:
            print("Error, index 1 {} out of peak indexes ".format(index[1]))
            proceed = False

        if proceed:
            index_peak_min = bins[peaks][index[0]]
            index_peak_max = bins[peaks][index[1]]

            print("Keeping interval between {} and {}".format(index_peak_min,
                                                          index_peak_max))

            f.write("Keeping interval between {} and {}\n".format(
                index_peak_min, index_peak_max))

            filter_arr = np.logical_and(index_peak_min < img_arr,
                                    img_arr < index_peak_max)

        else:

            filter_arr = compute_Kmeans(img_arr, operation="interval", index=index)

            f.write("Running Kmeans with interval\n")

    elif operation == "higher":
        if not isinstance(index, int):
            print("Error, index {} should be a integer for higher".format(
                index))
            proceed = False

        if index < 0 or len(bins[peaks]) <= index:

            print("Error, {} out of peak indexes ".format(index))
            proceed = False

        if proceed:
            index_peak_min = bins[peaks][index]
            print("Keeping higher than {}".format(index_peak_min))
            f.write("Keeping higher than {}\n".format(index_peak_min))

            filter_arr = index_peak_min < img_arr

        else:

            filter_arr = compute_Kmeans(img_arr, operation="min", index=index)

            f.write("Running Kmeans with min\n")

    elif operation == "lower":
        if not isinstance(index, int):
            print("Error, index {} should be a integer for higher".format(
                index))
            proceed = False

        if index < 0 or len(bins[peaks]) <= index:

            print("Error, {} out of peak indexes ".format(index))
            proceed = False

        if proceed:
            index_peak_max = bins[peaks][index]
            print("Keeping lower than {} ".format(index_peak_max))
            f.write("Keeping lower than {}\n".format(index_peak_max))

            filter_arr = img_arr < index_peak_max
        else:
            f.write("Running Kmeans with max\n")
            filter_arr = compute_Kmeans(img_arr, operation="max",index = index)


    new_mask_data[filter_arr] = img_arr[filter_arr]

    print(np.sum(new_mask_data))

    # saving mask as nii
    mask_img_file = os.path.abspath(fname + "_autothresh" + ext)

    mask_img = nib.Nifti1Image(dataobj=new_mask_data,
                               header=img_nii.header,
                               affine=img_nii.affine)
    nib.save(mask_img, mask_img_file)

    f.close()

    return mask_img_file


def pad_zero_mri(img_file, pad_val=10):

    import os
    import nibabel as nib
    import numpy as np

    from nipype.utils.filemanip import split_filename as split_f

    img = nib.load(img_file)
    img_arr = np.array(img.dataobj)
    img_arr_copy = np.copy(img_arr)

    img_arr_copy_padded = np.pad(
        img_arr_copy,
        pad_width=[(pad_val, pad_val), (pad_val, pad_val), (pad_val, pad_val)],
        mode='constant',
        constant_values=[(0, 0), (0, 0), (0, 0)])

    img_padded = nib.Nifti1Image(img_arr_copy_padded,
                                 header=img.header,
                                 affine=img.affine)

    path, fname, ext = split_f(img_file)

    img_padded_file = os.path.abspath("padded_" + fname + ext)

    nib.save(img_padded, img_padded_file)

    return img_padded_file


def keep_gcc(nii_file):

    import os
    import nibabel as nib
    import numpy as np

    from nipype.utils.filemanip import split_filename as split_f

    def getLargestCC(segmentation):

        from skimage.measure import label

        labels = label(segmentation)
        assert labels.max() != 0  # assume at least 1 CC
        largestCC = labels == np.argmax(np.bincount(labels.flat)[1:])+1
        return largestCC

    # nibabel (nifti -> np.array)
    img = nib.load(nii_file)
    data = img.get_fdata().astype("int32")
    print(data.shape)

    # numpy
    data[data > 0] = 1
    binary = np.array(data, dtype="bool")

    # skimage

    # skimage GCC
    new_data = getLargestCC(binary)

    # nibabel (np.array -> nifti)
    new_img = nib.Nifti1Image(dataobj=new_data,
                              header=img.header,
                              affine=img.affine)

    path, fname, ext = split_f(nii_file)

    gcc_nii_file = os.path.abspath(fname + "_gcc" + ext)

    nib.save(new_img, gcc_nii_file)
    return gcc_nii_file



def wrap_nii2mesh_old(nii_file):

    import os
    from nipype.utils.filemanip import split_filename as split_f

    path, fname, ext = split_f(nii_file)

    stl_file = os.path.abspath(fname + ".stl")

    cmd = "nii2mesh_old_gcc {} {}".format(nii_file, stl_file)

    ret = os.system(cmd)

    print(ret)

    assert ret == 0, "Error, cmd {} did not work".format(cmd)
    return stl_file

def wrap_nii2mesh(nii_file):

    import os
    from nipype.utils.filemanip import split_filename as split_f

    path, fname, ext = split_f(nii_file)

    stl_file = os.path.abspath(fname + ".stl")

    cmd = "nii2mesh {} {}".format(nii_file, stl_file)

    ret = os.system(cmd)

    print(ret)

    assert ret == 0, "Error, cmd {} did not work".format(cmd)
    return stl_file

