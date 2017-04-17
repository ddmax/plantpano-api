import tensorflow as tf
import numpy as np
import os
import logging

from settings import TF_DATA_FOLDER


class PlantClassifier:
    default_args = {
        'model_graph_def_file': os.path.join(TF_DATA_FOLDER, 'model.pb'),
        'class_labels_file': os.path.join(TF_DATA_FOLDER, 'labels.txt')
    }
    for k, v in default_args.items():
        if not os.path.exists(v):
            raise Exception("File {} not found at {}".format(k, v))

    def __init__(self, model_graph_def_file, class_labels_file):
        logging.info('Loading model data and labels...')

        # Read model
        self.graph = self.load_graph(model_graph_def_file)
        # Read labels
        self.labels = self.load_labels(class_labels_file)

    def load_graph(self, model_graph_def_file):
        with tf.gfile.FastGFile(model_graph_def_file, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name='')
        return graph

    def load_labels(self, class_labels_file):
        labels_file = open(class_labels_file, encoding='utf-8')
        lines = labels_file.read().splitlines()
        return [str(w) for w in lines]

    def classify_image(self, image, from_file=False):
        result = list()

        image_data = tf.gfile.FastGFile(image, 'rb').read() if from_file else image

        with tf.Session(graph=self.graph) as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)

            top_k = predictions.argsort()[-5:][::-1]

            for node_id in top_k:
                plant_name = self.labels[node_id]
                score = format(predictions[node_id], '.4f')
                result.append({
                    'name': plant_name,
                    'score': score
                })

            return result

clf = PlantClassifier(**PlantClassifier.default_args)
