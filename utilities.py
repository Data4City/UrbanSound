import os.path as p
import gc


def plot_spectrogram(filename):
    plt.interactive(False)
    filename, _ = build_path(filename)
    clip, sample_rate = librosa.load(filename, sr=None)
    fig, ax = plt.subplots()
    S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    plt.show()

    
def create_spectrogram(filename):
    plt.interactive(False)
    filename, fold_id =build_path(filename)
    clip, sample_rate = librosa.load(filename, sr=None)
    fig = plt.figure(figsize=[0.72,0.72])
    ax = fig.add_subplot(111)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
    curr_path = p.join(spectro_path, folds[fold_id])
    savefile  = p.join(curr_path, "{}.jpg".format(p.basename(filename).split(".")[0] ))
    plt.savefig(savefile, dpi=400, bbox_inches='tight',pad_inches=0)
    plt.close()    
    fig.clf()
    plt.close(fig)
    plt.close('all')
    del filename,clip,sample_rate,fig,ax,S,savefile
    
def build_path(file_name, spectrogram = False):
    file= file_name.split(".")
    source = spectro_path if spectrogram else audio_source
    file_name = file[0] + ".jpg" if spectrogram else file[0] +".wav"
    fsID= int(file_name.split("-")[0])
    frame = metadata.loc[fsID]
    fold_id = 0
    try:
        fold_id = frame["fold"].values[0]-1
    except:
        fold_id = frame["fold"] -1
    file_with_fold = p.join(folds[fold_id], file_name)
    return p.join(source,file_with_fold), fold_id


def add_spectrogram_to_metadata(metadata):
    counter = 0
    errors =0
    for index, row in metadata.iterrows():
        counter += 1
        if counter%2000 ==0:
            gc.collect()
        try:
            file_name = row["slice_file_name"]
            s,_ = build_path(file_name, True)
            metadata.loc[index, "spectro_path"] = s
            if not p.exists(s): create_spectrogram(row["slice_file_name"])
        except Exception as e:
            errors +=1

    print("Total: {} \nErrors: {}\nCorrect: {}".format(counter, errors, counter-errors))
    
    return metadata