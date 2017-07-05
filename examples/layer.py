import tensorflow as tf

def parameter_count( shape , name="") :
  print "Parametes ",shape,", Count :",reduce(lambda x, y: x*y, shape ),", Name",name

def weight_variable(shape, name="Weight_Variable"):
  parameter_count(shape,name)
  return tf.Variable( tf.truncated_normal(shape, stddev=0.01), name=name)

def bias_variable(shape, name="Bias_Variable"):
  return tf.Variable( tf.constant(0.1, shape=shape), name=name)

def max_pool(x,stride=2, padding='SAME'):
  return tf.nn.max_pool(x, ksize=[1, stride, stride, 1], strides=[1, stride, stride, 1], padding=padding)

def avg_pool(x,stride=2, padding='SAME', name="Avg_Pool"):
  return tf.nn.avg_pool(x, ksize=[1, stride, stride, 1], strides=[1, stride, stride, 1], padding=padding, name=name)

def conv( x , layers_in , layers_out , width=6 , stride=1, padding='SAME', name="conv" ):
  w = weight_variable( [width, width, layers_in, layers_out], name=(name + "_weight")) 
  b = bias_variable( [layers_out] ) 
  return tf.add( tf.nn.conv2d( x, w, strides= [1, stride, stride, 1], padding=padding ) , b , name=name)

def deconv( x , layers_in , layers_out , width , shape_as , stride=1, padding='VALID', name="deconv" ):
  w = weight_variable( [width, width, layers_out, layers_in], name=(name + "_weight")) 
  b = bias_variable( [layers_out] ) 
  return tf.add( tf.nn.conv2d_transpose( x, filter=w, output_shape=tf.shape(shape_as), strides=[1, stride, stride, 1], padding=padding ) , b , name=name)

def drop_conv( keep_prob, x , layers_in , layers_out , width=6 , stride=1, padding='SAME', name="drop_conv" ):
  w = weight_variable( [width, width, layers_in, layers_out], name=(name + "_weight") ) 
  w = tf.nn.dropout( w, keep_prob ) / keep_prob
  b = bias_variable( [layers_out] ) 
  return tf.add( tf.nn.conv2d( x, w, strides= [1, stride, stride, 1], padding=padding ) , b , name=name)

def conv_relu( x , layers_in , layers_out , width=6 , stride=1, padding='SAME', name="conv_relu" ):
  h = conv( x , layers_in , layers_out , width , stride, padding, name=(name + "_conv") )
  return tf.nn.relu( h , name=name)

def batch_normalization( x, training, momentum=0.9 ) :
  return tf.layers.batch_normalization( x, training=training, momentum=momentum )

def single_resnet_block( x, layers, width , training, momentum=0.9, name="single_resnet_block" ) :
  result = batch_normalization( x , training, momentum=momentum )
  result = tf.nn.relu(result)
  return conv( result, layers, layers, width=width, name=name )

def resnet_block( x, layers, width , training, momentum=0.9, name="resnet_block" ) :
  result = single_resnet_block( x,      layers, width, training, momentum=momentum, name=(name + "_1") )
  result = single_resnet_block( result, layers, width, training, momentum=momentum, name=(name + "_2") )
  return tf.add( x , result, name=name )

def resnet_narrow( x, layers, width , training, narrowing=2, name="resnet_narrow" ) :
  result = batch_normalization( x , training )
  result = tf.nn.relu(result)
  result = conv( result, layers, layers/narrowing, width=1, name=(name + "_narrowing") )
  result = tf.nn.relu(result)
  result = conv( result, layers/narrowing, layers/narrowing, width=width, name=(name + "_conv") )
  result = tf.nn.relu(result)
  result = conv( result, layers/narrowing, layers, width=1, name=(name + "_expand") )
  result = tf.nn.relu(result)
  return tf.add( x , result, name=name )

def fully_connected( x , size_in , size_out, name="fully_connected" ):
  W = weight_variable( [size_in, size_out], name=(name + "_weight") )
  b = bias_variable( [size_out] )
  return tf.add( tf.matmul(x, W) , b , name=name )
