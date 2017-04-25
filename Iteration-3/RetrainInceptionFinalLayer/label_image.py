import tensorflow as tf, sys
import os

def get_class(image_path):

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("data/sorevision_output_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("data/sorevision_output_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        retstr = ''

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            retstr = retstr + '%s (score = %.5f)' % (human_string, score) + '\n'

    return retstr

image_dir = 'data/test/cankersore/'
image_path = ''

for filename in os.listdir(image_dir):
    if filename.endswith(".jpg"):
        image_path = os.path.join(image_dir, filename)
        print(image_path + ":\n" + get_class(image_path))
    else:
        continue

image_dir = 'data/test/coldsore/'
image_path = ''

for filename in os.listdir(image_dir):
    if filename.endswith(".jpg"):
        image_path = os.path.join(image_dir, filename)
        print(image_path + ":\n" + get_class(image_path))
    else:
        continue