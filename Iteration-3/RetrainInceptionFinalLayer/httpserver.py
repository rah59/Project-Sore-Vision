#!/usr/bin/python

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
from flask import Flask, request
import simplejson
import base64
import tensorflow as tf, sys
import os
from PIL import Image

PORT_NUMBER = 8080


# This class will handles any incoming request from
# the browser
class myHandler(BaseHTTPRequestHandler):

    def get_class(self):

        # Read in the image_data
        image_data = tf.gfile.FastGFile("imageToSave.jpg", 'rb').read()

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

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response)

    # Handler for the POST requests
    def do_POST(self):
        if self.path == "/get_custom":

            #self._set_headers()
            #print("in post method")
            #self.data_string = self.rfile.read(int(self.headers['Content-Length']))

            #self.send_response(200)
            #self.end_headers()

            #data = simplejson.loads(self.data_string)

            #data = data[data.find(",") + 1:]

            #decodeddata = base64.b64decode(data)
            #image_binary = base64.b64encode(data)

            #data = request.POST('data')

            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)  # <--- Gets the data itself

            #post_data = post_data[post_data.find(",") + 1:]

            image_binary = base64.decodebytes(post_data)

            with open("imageToSave.png", "wb") as fh:
                fh.write(image_binary)

            im = Image.open("imageToSave.png")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, im)
            bg.save("imageToSave.jpg")

            #open("inputimage.jpg", "wb").write(decodeddata)

            #with open("test123456.json", "w") as outfile:
            #    simplejson.dump(data, outfile)
            #print("{}".format(data))

            predictiontext = self.get_class()
            #return predictiontext

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type", "text")
            self.send_header("Content-length", str(len(predictiontext)))
            self.end_headers()
            self.wfile.write(bytes(predictiontext, 'utf8'))


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print ('Started httpserver on port ', PORT_NUMBER)

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print ('^C received, shutting down the web server')
    server.socket.close()