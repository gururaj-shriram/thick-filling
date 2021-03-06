#
# adaboost_test.py
# 
# date last modified: 28 nov 2017
# modified last by: jerry
# 
#

import math
import operator
import numpy as np
import matplotlib.pyplot as plt
import re
from matplotlib.colors import ListedColormap
from random import randint
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree 
from perceptron import PerceptronClassifier
from sklearn.linear_model import perceptron
from sklearn.ensemble import AdaBoostClassifier
from adaboost import AdaBoost
from adaboost import classifier_error_rate

# once again, change this to switch datasets; 
# don't forget to toggle load_dataset() as well 

#FILENAME = "dataset/default.csv" 
#FILENAME = "dataset/ionosphere.dat" 
#FILENAME = "dataset/musk.dat"  
#FILENAME = "dataset/heart.dat"  
#FILENAME = "dataset/spambase.dat" 
#FILENAME = "dataset/animals.dat" 
#FILENAME = "dataset/ecoli.dat"
#FILENAME = "dataset/fertility.dat"
#FILENAME = "dataset/magic04.dat"
FILENAME = "dataset/occupancy.dat"

FILENAME_LIST = [
	#"dataset/kidney.dat",
	# "dataset/cancer.dat"]
	#"dataset/occupancy.dat"]	
	"dataset/ionosphere.dat"]
	#"dataset/musk.dat"]
	#"dataset/heart.dat", 
	#"dataset/spambase.dat", 
	#"dataset/animals.dat", 
	#"dataset/ecoli.dat"]
	#"dataset/fertility.dat",
	#"dataset/magic04.dat"]

# probability of an example being in the training set 
PROBABILITY_TRAINING_SET = 0.65

# learning rate for perceptron 
ETA = 0.05
# learning rate for adaboost when adjusting weights of classifiers 
ETA_WEIGHTS = 0.0001
# desired threshold for error rate; 0.2 --> 20% 
THRESHOLD = 0.05
# maximum number of epochs for training
UPPER_BOUND = 500
# verbose flag 
IS_VERBOSE = True 
# number of classifiers to induce in Adaboost
NUM_OF_CLASSIFIERS = 20

def split_dataset(examples, prob_training):
	"""
	receives list of examples  
	returns a tuple consisting of a training set and testing set 
	"""
	training_set = []
	testing_set = []

	# generate a random number [1,100]. if it is greater than 
	# prob_training then add the example to the 
	# testing set; otherwise add it to the training set 
	percent_training = prob_training * 100; 
	for example in examples:
		result = randint(1, 100) 
		# if the result is a number less than percent_training, 
		# add to training set; else add it to the testing set 
		if (result < percent_training):
			training_set.append(example)
		else:
			testing_set.append(example)

	return (training_set, testing_set)

def load_dataset(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split(",") # a row in the data-set 
		dataset.append(list(map(float, example[:]))) # append it to the 2D array

	return dataset 


def load_dataset_ionosphere(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split(",") # a row in the data-set 
		if example[-1] == 'g':
			example[-1] = 1
		else:
			example[-1] = 0
		dataset.append(list(map(float, example[:]))) # append it to the 2D array

	return dataset 

def load_dataset_cancer(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split(",") # a row in the data-set 
		if '?' in example:
			continue
		if example[-1] == '2':
			example[-1] = 1
		else:
			example[-1] = 0
		dataset.append(list(map(float, example[:]))) # append it to the 2D array

	return dataset 

def load_dataset_kidney(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split(",") # a row in the data-set 
		if '?' in example:
			continue

		dataset.append(list(map(float, example[:]))) # append it to the 2D array

	return dataset 


def load_dataset_musk(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split(",") # a row in the data-set 
		dataset.append(list(map(float, example[2:]))) # append it to the 2D array

	return dataset 

def load_dataset_ecoli(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split("  ") # a row in the data-set 
		dataset.append(list(map(float, example[1:]))) # append it to the 2D array

	return dataset 

def load_dataset_heart(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split(" ") # a row in the data-set 
		if example[-1] == '2':
			example[-1] = 1
		else:
			example[-1] = 0
		dataset.append(list(map(float, example[:]))) # append it to the 2D array

	return dataset 

def load_dataset_magic(filename):
	"""
	given a filename that points to a file containing the data-set, 
	load it into memory and return an array containing this data-set
	"""
	dataset = []
	# open the data-set file
	file = open(filename, "r")
	# we want to load this data-set into a 2D array 
	# where each row is an example and each column is 
	# an attribute. 
	for line in file: 
		example = line.strip().split(",") # a row in the data-set 
		if example[-1] == 'g':
			example[-1] = 1
		else:
			example[-1] = 0
		dataset.append(list(map(float, example[:]))) # append it to the 2D array

	return dataset 

def load_any_dataset(filename):
	tmp = filename.split('/')
	title = tmp[1].split('.')[0].lower()

	if title == "ionosphere":
		return load_dataset_ionosphere(filename)
	elif title == "musk":
		return load_dataset_musk(filename)
	elif title == "heart":
		return load_dataset_heart(filename)
	elif title == "ecoli":
		return load_dataset_ecoli(filename)
	elif title == "magic04":
		return load_dataset_magic(filename)
	elif title == "cancer":
		return load_dataset_cancer(filename)
	elif title == "kidney":
		return load_dataset_kidney(filename)
	else:
		return load_dataset(filename)

def split_attribute_and_label(dataset):
	"""
	split attribute vectors from their class-labels 
	"""

	# add 0.1 because values are processed as floats and we may have 0.999...
	class_labels = [round(row[-1]) for row in dataset]
	attributes = [row[:-1] for row in dataset]
	return (attributes, class_labels)

def calculate_error(class_labels, hypothesis_list):
	"""
	calculates simple error rate on a dataset
	:param class_labels: list of given class-labels 
	:param hypothesis_list: list of classifier predictions for examples
	"""
	num_errors = 0
	for i in range(len(class_labels)):
		if class_labels[i] != hypothesis_list[i]:
			num_errors += 1

	return (num_errors / len(class_labels))

class ErrorWrapper:
	def __init__(self, num_classifiers, train_error, test_error, scikit_error):
		self.num_classifiers = num_classifiers
		self.train_error = train_error
		self.test_error = test_error
		self.scikit_error = scikit_error

	def __str__(self):
		return "# of Classifiers {0}, Train Error: {1}, Test Error: {2}, Scikit Error: {3}".format(
			self.num_classifiers, self.train_error, self.test_error, self.scikit_error)

def perceptron_avg_run(avg_num_of_run, training_set, testing_set):
	(train_x, train_y) = split_attribute_and_label(training_set)
	(test_x, test_y) = split_attribute_and_label(testing_set)

	perceptron_error = []
	
	for i in range(avg_num_of_run):

		p = perceptron.Perceptron(max_iter=UPPER_BOUND, verbose=0, random_state=None, 
								fit_intercept=True, eta0=ETA)
		p.fit(train_x, train_y)
		result_list = p.predict(test_x)
		perceptron_error.append(calculate_error(test_y, result_list))

	return sum(perceptron_error) / len(perceptron_error)

def decision_tree_avg_run(avg_num_of_run, training_set, testing_set):
	(train_x, train_y) = split_attribute_and_label(training_set)
	(test_x, test_y) = split_attribute_and_label(testing_set)

	# run decision tree classifier avg_num_of_run times
	decision_tree_error = []
	for i in range(avg_num_of_run):
		clf = tree.DecisionTreeClassifier()
		clf = clf.fit(train_x, train_y)
		decision_tree_result_list = clf.predict(test_x)
		decision_tree_error.append(calculate_error(test_y, decision_tree_result_list))

	return sum(decision_tree_error) / len(decision_tree_error)

def adaboost_avg_run(max_classes, avg_num_of_run, training_set, testing_set):
	testing_error_list = []
	all_error_list = []

	# because datasets sometimes place the class attribute at the end or even 
	# at the beginning or the middle, we'll separate the attribute vector from
	# the class-label. also note that this is the way scikit-learn does it. 
	# train_x: the attribute vector; train_y: the class_label  
	(train_x, train_y) = split_attribute_and_label(training_set)
	(test_x, test_y) = split_attribute_and_label(testing_set)
	# print(len(train_x))	
	train_subset_num = int(len(train_y) * 0.2) 

	for cl in range(1, max_classes+1, 2):
		train_error = []
		testing_error = []
		scikit_error = []
		for i in range(avg_num_of_run):
			
			ada_obj = AdaBoost(cl, train_subset_num, THRESHOLD, ETA, UPPER_BOUND, ETA_WEIGHTS, False)
			ada_obj.fit(train_x, train_y)

			hypothesis_list = ada_obj.predict(train_x)
			mistakes = ada_obj.xor_tuples(train_y, hypothesis_list)
			error_rate_train = classifier_error_rate(mistakes)

			hypothesis_list = ada_obj.predict(test_x)
			mistakes = ada_obj.xor_tuples(test_y, hypothesis_list)
			error_rate_test = classifier_error_rate(mistakes)
			train_error.append(error_rate_train)
			testing_error.append(error_rate_test)

			pada = perceptron.Perceptron(max_iter=UPPER_BOUND, verbose=0, random_state=None, 
							fit_intercept=True, eta0=ETA)

			bdt = AdaBoostClassifier(pada,algorithm="SAMME",n_estimators=cl)
			bdt.fit(train_x, train_y)
			result_list = bdt.predict(test_x)
			scikit_error.append(calculate_error(test_y, result_list))

		errors = ErrorWrapper(
			cl, 
			sum(train_error)/len(train_error), 
			sum(testing_error)/len(testing_error), 
			sum(scikit_error)/len(scikit_error))

		all_error_list.append(errors)
		print("Train avg for %s   %s"%(cl, errors.train_error))
		print("Testing avg for %s   %s"%(cl, errors.test_error))
		testing_error_list.append((sum(testing_error)/len(testing_error)) * 100)
		print("Scikit adaboost avg for %s   %s"%(cl, errors.scikit_error))

	#return testing_error_list
	return all_error_list

def adaboost_avg_run_new(max_classes, avg_num_of_run, training_set, testing_set):
	all_error_list = []

	# because datasets sometimes place the class attribute at the end or even 
	# at the beginning or the middle, we'll separate the attribute vector from
	# the class-label. also note that this is the way scikit-learn does it. 
	# train_x: the attribute vector; train_y: the class_label  
	(train_x, train_y) = split_attribute_and_label(training_set)
	(test_x, test_y) = split_attribute_and_label(testing_set)
	# print(len(train_x))	
	train_subset_num = int(len(train_y) * 0.2) 

	our_ada_training_errors = {}
	our_ada_testing_errors = {}

	# init dict of num classifier to error list
	for i in range(1, max_classes+1):
		our_ada_training_errors[i] = []
		our_ada_testing_errors[i] = []

	# run ada num_runs times
	for i in range(avg_num_of_run):
		ada_obj = AdaBoost(max_classes, train_subset_num, THRESHOLD, ETA, UPPER_BOUND, ETA_WEIGHTS, False)
		ada_obj.fit_with_errors(train_x, train_y, test_x, test_y)

		for j in range(max_classes):
			our_ada_training_errors[j+1].append(ada_obj.training_error[j])
			our_ada_testing_errors[j+1].append(ada_obj.testing_error[j])

	for cl in range(1, max_classes+1):
		scikit_error = []
		for i in range(avg_num_of_run):
			pada = perceptron.Perceptron(max_iter=UPPER_BOUND, verbose=0, random_state=None, 
							fit_intercept=True, eta0=ETA)

			bdt = AdaBoostClassifier(pada,algorithm="SAMME",n_estimators=cl)
			bdt.fit(train_x, train_y)
			result_list = bdt.predict(test_x)
			scikit_error.append(calculate_error(test_y, result_list))

		errors = ErrorWrapper(
			cl, 
			sum(our_ada_training_errors[cl])/len(our_ada_training_errors[cl]), 
			sum(our_ada_testing_errors[cl])/len(our_ada_testing_errors[cl]), 
			sum(scikit_error)/len(scikit_error))

		all_error_list.append(errors)
		print("Train avg for %s   %s"%(cl, errors.train_error))
		print("Testing avg for %s   %s"%(cl, errors.test_error))
		print("Scikit adaboost avg for %s   %s"%(cl, errors.scikit_error))

	return all_error_list

def plot_errors(filename, count, error_list):
	num_classifiers_list = []
	train_error_list = []
	test_error_list = []
	scikit_error_list = []

	tmp = filename.split('/')
	title = tmp[1].split('.')[0].title()
	new_filename = 'graphs/' + title + '_' + str(count)
	
	for error in error_list:
		num_classifiers_list.append(error.num_classifiers)
		train_error_list.append(error.train_error)
		test_error_list.append(error.test_error)
		scikit_error_list.append(error.scikit_error)

	plt.plot(num_classifiers_list, train_error_list, 'r-')
	plt.plot(num_classifiers_list, test_error_list, 'g-')
	plt.plot(num_classifiers_list, scikit_error_list, 'b-')
	plt.legend(['Training Set Error', 'Testing Set Error', 'Scikit Error'], loc = 'upper right')
	plt.xlabel('Number of Classifiers')
	plt.ylabel('Error Rate')
	plt.title('Adaboost Error Rates on the {0} Dataset'.format(title))
	plt.savefig('{0}.png'.format(new_filename))
	plt.gcf().clear()

def plot_testing_set_errors(filename, count, error_list, decision_tree_avg_error, perceptron_avg_error):
	num_classifiers_list = []
	test_error_list = []

	tmp = filename.split('/')
	title = tmp[1].split('.')[0].title()
	new_filename = 'graphs/' + title 
	
	for error in error_list:
		num_classifiers_list.append(error.num_classifiers)
		test_error_list.append(error.test_error)

	plt.plot(num_classifiers_list, test_error_list, 'r-')
	plt.axhline(y=decision_tree_avg_error, color='g')
	plt.axhline(y=perceptron_avg_error, color='b')

	plt.legend(['Testing Set Error', 'Average Error using a Decision Tree', 'Average Error using a Single Perceptron Classifier'], loc = 'upper right')
	plt.xlabel('Number of Classifiers')
	plt.ylabel('Error Rate')
	plt.title('Error Rates with Different Classifiers on the {0} Dataset'.format(title))
	plt.savefig('{0}_different_classifiers_{1}.png'.format(new_filename, str(count)))
	plt.gcf().clear()

def get_class_labels(dataset):
	"""
	calculates the number of class labels in the dataset
	returns a dictionary from class label to a random index used for plotting
	"""
	class_labels = {}
	i = 0
	for row in dataset:
		if row[-1] not in class_labels:
			class_labels[row[-1]] = i
			i += 1

	return class_labels

def plot_color_map(filename, training_set):
	"""
	Most of the code used to plot is from an example from scikit
	http://scikit-learn.org/stable/auto_examples/neighbors/plot_classification.html
	"""
	tmp = filename.split('/')
	title = tmp[1].split('.')[0].title()
	new_filename = 'graphs/' + title 

	train_X = [row[0:-1] for row in training_set]
	train_y = [row[-1] for row in training_set]

	# Convert the training tuples into np arrays to use for plotting
	class_labels = get_class_labels(training_set)
	temp_X = np.array(train_X).astype(np.float)
	temp_y = []

	for data in train_y:
		temp_y.append(int(data))

	# change this for interesting attributes
	attribute_1_index = 0
	attribute_2_index = 1

	# get subset of training set with the attributes at the calculated indexes
	X = np.array(temp_X[:,attribute_1_index:attribute_2_index+1])
	y = np.array(temp_y)

	pada = perceptron.Perceptron(max_iter=UPPER_BOUND, verbose=0, random_state=None, 
							fit_intercept=True, eta0=ETA)

	bdt = AdaBoostClassifier(pada,algorithm="SAMME",n_estimators=50)
	bdt.fit(X, y)

	num_classes = len(class_labels)
	h = 0.02 # step size

	# create a random color map for data points and classes
	c_map_1 = plt.get_cmap("magma_r")
	c_map_2 = ListedColormap(['#FFFFFF'])
	# Plot the decision boundary. For that, we will assign a color to each
	# point in the mesh [x_min, x_max]x[y_min, y_max].
	x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
		np.arange(y_min, y_max, h))
	
	Z = bdt.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.figure()
	plt.pcolormesh(xx, yy, Z, cmap=c_map_1)

	# Plot also the training points
	plt.scatter(X[:, 0], X[:, 1], c=y, cmap=c_map_2,
		edgecolor='k', s=20)
	plt.xlim(xx.min(), xx.max())
	plt.ylim(yy.min(), yy.max())
	plt.xlabel('Attribute 1')
	plt.ylabel('Attribute 2')
	plt.title("Training data in the {0} Dataset".format(title))
	plt.savefig("{0}_colormap.png".format(new_filename))

def run_all(num_times = 1):
	for i in range(num_times):
		j = 0
		while j < len(FILENAME_LIST):
			filename = FILENAME_LIST[j]
			j += 1

			dataset = load_any_dataset(filename)
			(training_set,testing_set) = split_dataset(dataset, PROBABILITY_TRAINING_SET)

			try:
				error_list = adaboost_avg_run_new(50, 5, training_set, testing_set)
				decision_tree_avg_error = decision_tree_avg_run(5, training_set, testing_set)
				perceptron_avg_error = perceptron_avg_run(5, training_set, testing_set)
			except Exception as e:
				#print(str(e))
				j = 0
				continue
			
			plot_errors(filename, i+1, error_list)
			plot_testing_set_errors(filename, i+1, error_list, decision_tree_avg_error, perceptron_avg_error)

			# Change attribute parameters in plot_color_map for good results
			#plot_color_map(filename, training_set)


# preprocessing: load in the dataset and split into a training and testing set 
#dataset = load_dataset(FILENAME) 
#dataset =load_dataset_ionosphere(FILENAME)
#dataset =load_dataset_musk(FILENAME)
#dataset =load_dataset_heart(FILENAME)
#dataset =load_dataset_ecoli(FILENAME)
#dataset = load_dataset_magic(FILENAME)

# (training_set,testing_set) = split_dataset(dataset, PROBABILITY_TRAINING_SET)

# if IS_VERBOSE:
# 	print("training set size: %s testing set size: %s num instances: %s" % 
# 		(len(training_set), len(testing_set), len(dataset)))

# because datasets sometimes place the class attribute at the end or even 
# at the beginning or the middle, we'll separate the attribute vector from
# the class-label. also note that this is the way scikit-learn does it. 
# train_x: the attribute vector; train_y: the class_label  
# (train_x, train_y) = split_attribute_and_label(training_set)
# (test_x, test_y) = split_attribute_and_label(testing_set)


# # create the perceptron classifier 
#linear_classifier = PerceptronClassifier(ETA, THRESHOLD, UPPER_BOUND, False)
# # train the classifier 
#linear_classifier.fit(train_x, train_y)
#print("Training error rate %s" % linear_classifier.training_error_rate)
# #print(linear_classifier.weights)

# # test the trained classifier on the testing set 
#result_list = linear_classifier.predict(test_x)
# print("=========")
#print("our perceptron error rate on test: %s" % calculate_error(test_y, result_list))
# print("=========")

# test their perceptron and adaboost for comparison 
# p = perceptron.Perceptron(max_iter=UPPER_BOUND, verbose=0, random_state=None, 
# 							fit_intercept=True, eta0=ETA)
# p.fit(train_x, train_y)
# result_list = p.predict(test_x)
# print("their perceptron error on test: %s" % calculate_error(test_y, result_list))

# pada = perceptron.Perceptron(max_iter=UPPER_BOUND, verbose=0, random_state=None, 
# 							fit_intercept=True, eta0=ETA)


# bdt = AdaBoostClassifier(p,algorithm="SAMME",n_estimators=NUM_OF_CLASSIFIERS)
# bdt.fit(train_x, train_y)
# result_list = bdt.predict(test_x)
# print("their adaboost error on test: %s" % calculate_error(test_y, result_list))

# # test a decision tree 
# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(train_x, train_y)
# decision_tree_result_list = clf.predict(test_x)
# print("=========")
# print("single tree error rate on testing set: %s" % calculate_error(test_y, decision_tree_result_list))
# print("=========")

# # Create the perceptron object (net)
# #net = perceptron.Perceptron(max_iter=UPPER_BOUND, verbose=0, random_state=None, fit_intercept=True, eta0=ETA)

# # Train the perceptron object (net)
# #net.fit(train_x,train_y)

# #pred = net.predict(train_x)
# #print("scikit-learn perceptron training error rate %s" % calculate_error(train_y, pred))

# #pred_t = net.predict(test_x)
# #print("scikit-learn perceptron testing error rate %s" % calculate_error(test_y, pred_t))

# # need to find good number for training subset size
# train_subset_num = int(len(train_y)*.5) #int(len(train_y)*10/NUM_OF_CLASSIFIERS)
# print("num examples in training subset : " + str(train_subset_num))

# ada_obj = AdaBoost(NUM_OF_CLASSIFIERS, train_subset_num, THRESHOLD, ETA, UPPER_BOUND, ETA_WEIGHTS, IS_VERBOSE)
# ada_obj.fit(train_x, train_y)
# print(ada_obj.classifiers_weights)

# hypothesis_list = ada_obj.predict(train_x)
# mistakes = ada_obj.xor_tuples(train_y, hypothesis_list)
# error_rate = ada_obj.classifier_error_rate(mistakes)

# print('training error rate %f'%error_rate)

# hypothesis_list = ada_obj.predict(test_x)
# mistakes = ada_obj.xor_tuples(test_y, hypothesis_list)
# error_rate = ada_obj.classifier_error_rate(mistakes)

# print('testing error rate %f'%error_rate)

# #(average_train, average_test) = average_for_runs(10, train_subset_num, NUM_OF_CLASSIFIERS)

# #print('average train error rate %f'%average_train)
# #print('average test error rate %f'%average_test)

# #average_error_rate = average_for_runs(10, train_subset_num, 10)
# #print("average error rate : %f" % average_error_rate) 

# split dataset only once
# (training_set,testing_set) = split_dataset(dataset, PROBABILITY_TRAINING_SET)
# error_list = adaboost_avg_run(50, 5, training_set, testing_set)
# #error_list = adaboost_avg_run(20, 1, training_set, testing_set)
# decision_tree_avg_error = decision_tree_avg_run(5, training_set, testing_set)
# perceptron_avg_error = perceptron_avg_run(5, training_set, testing_set)
# plot_errors(FILENAME, error_list)
# plot_testing_set_errors(FILENAME, error_list, decision_tree_avg_error, perceptron_avg_error)

run_all()
