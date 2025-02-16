# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow_addons as tfa

'''

train_xx=np.zeros((100,20,1))
a1=tf.convert_to_tensor(train_xx)
a2l=layers.MultiHeadAttention(
            num_heads=4, key_dim=2, dropout=0.1
        )
a2=a2l(a1,a1);
a0=a2.numpy()

ll=tf.keras.layers.Reshape((12,1), input_shape=(12,))
train_xx=np.zeros((100,12))
a1=tf.convert_to_tensor(train_xx)
a2=ll(a1)

'''


input_shape=(12);
num_classes=2;
num_seq=12;


num_heads=4;  #默认4
projection_dim=64;  #64
transformer_layers=2;
transformer_units = [
    projection_dim * 2,
    projection_dim,
]  # Size of the transformer layers
mlp_head_units = [2048, 1024]  # [2048, 1024]

def mlp(x, hidden_units, dropout_rate):
    for units in hidden_units:
        x = layers.Dense(units, activation=tf.nn.gelu)(x)
        x = layers.Dropout(dropout_rate)(x)
    return x

class transformers_PatchEncoder(layers.Layer):
    def __init__(self, num_patches, projection_dim):
        super().__init__()
        self.num_patches = num_patches
        self.projection = layers.Dense(units=projection_dim)
        self.position_embedding = layers.Embedding(
            input_dim=num_patches, output_dim=projection_dim
        )

    def call(self, patch):
        positions = tf.range(start=0, limit=self.num_patches, delta=1)
        #// 0~144
        encoded = self.projection(patch) + self.position_embedding(positions)
        #//                               144*64
        return encoded

class VWNormal(layers.Layer):
    
    def __init__(self):
        super().__init__()
        self.thev=tf.convert_to_tensor(-15.0);
        self.thew=tf.convert_to_tensor(-30.0);
    
    def call(self, theinput):
        
        result=(theinput-self.thew)/(self.thev-self.thew);
        
        return result;
    


class over_SPRIIndex(tf.keras.layers.Layer):
    def __init__(self):
        super(over_SPRIIndex, self).__init__();
        self.thev=tf.convert_to_tensor(-15.0);
        self.thew=tf.convert_to_tensor(-30.0);
                
    def getMinMax(self,data):
        p1=tf.reduce_min(data[:,2:5],1,keepdims=True);
        p2=tf.reduce_max(data[:,7:9],1,keepdims=True);
        
        '''
        rr1=tf.greater(data[:,5], data[:,4]);
        #1是水稻, 0不是水稻
        rr1z=tf.cast(rr1,dtype=tf.float32);
        
        rr2=tf.greater(data[:,6], data[:,4]);
        #1是水稻, 0不是水稻
        rr2z=tf.cast(rr2,dtype=tf.float32);
        
        rr3=tf.greater(tf.math.add(rr1z,rr2z),0);
        rr3z=tf.cast(rr3,dtype=tf.float32);
        rr3z=tf.expand_dims(rr3z,1);
        '''
        
        xp11=(p1-self.thew)/(self.thev-self.thew);
        pp12=tf.reduce_max(data[:,2:5],1,keepdims=True);
        xp12=(pp12-self.thew)/(self.thev-self.thew);
        
        xp21=(p2-self.thew)/(self.thev-self.thew);
        pp22=tf.reduce_min(data[:,7:9],1,keepdims=True);
        xp22=(pp22-self.thew)/(self.thev-self.thew);
        
        
        return [p1,p2,xp11,xp12,xp21,xp22];
    
    def SPRIIndex(self, value):
        v=self.thev;
        w=self.thew;
        [p1,p2,xp11,xp12,xp21,xp22]=self.getMinMax(value);
        D=p2-p1;
        fD=1.0/(1+tf.exp( (v-w)/2.0-D  ))
        WW=(p1-w)/(v-w);
        '''
        WW=0.0;
        if (p1>=v):
            WW=1.0;
        if (p1<v and p1>=w):
            WW=(p1-w)/(v-w);
        if (p1<w):
            WW=0.0;
        fW=1-WW*WW;
        '''
        
        lg1=tf.greater_equal(p1,v);
        lg1=tf.cast(lg1,dtype=tf.float32);
        lg2=tf.math.negative( tf.math.subtract(lg1,1));
        a1=lg1;
        a2=tf.math.multiply(WW,lg2);
        WW=tf.math.add(a1, a2);
        
        lg1=tf.less(p1,w);
        lg1=tf.cast(lg1,dtype=tf.float32);
        lg2=tf.math.negative( tf.math.subtract(lg1,1));
        a2=tf.math.multiply(WW,lg2);
        WW=a2;
        '''-------------------------------------------------'''
                
        fW=1-WW*WW;
        
        VV=(v-p2)/(v-w);
        
        
        '''
        if (p2<=w):
            VV=1.0;
        if (p2<=v and p2>w):
            VV=(v-p2)/(v-w);
        if (p2>v):
            VV=0.0;
        '''
        lg1=tf.less_equal(p2,w);
        lg1=tf.cast(lg1,dtype=tf.float32);
        lg2=tf.math.negative( tf.math.subtract(lg1,1));
        a1=lg1;
        a2=tf.math.multiply(VV,lg2);
        VV=tf.math.add(a1, a2);
        
        
        lg1=tf.greater(p2,v);
        lg1=tf.cast(lg1,dtype=tf.float32);
        lg2=tf.math.negative( tf.math.subtract(lg1,1));
        a1=lg1;
        a2=tf.math.multiply(VV,lg2);
        VV=a2;
        '''-------------------------------------------------'''
        
        
        fV=1-VV*VV;
        SPRI=fD*fW*fV;
        
        dec1=tf.less_equal(SPRI,0.5);
        dec2=tf.cast(dec1,dtype=tf.float32);
        dec3=tf.greater(SPRI,0.85);
        dec4=tf.cast(dec3,dtype=tf.float32);
        
        return [SPRI,fD,fW,fV, dec2,dec4];#,xp11,xp12,xp21,xp22];
    
    def call(self, inputs):
        pass;        
        return self.SPRIIndex(inputs);



def transformers_mlp(x, hidden_units, dropout_rate):
    for units in hidden_units:
        x = layers.Dense(units, activation=tf.nn.gelu)(x)
        x = layers.Dropout(dropout_rate)(x)
    return x

def create_transformer_classifier():
    
    
    inputs = layers.Input(shape=input_shape)
    '''
    输入是  (batch, input_shape), 要变形为(batch, input_shape，1)
    '''
    spri=over_SPRIIndex()(inputs);
    sprirep= tf.keras.layers.Concatenate()(spri);
   
    normal_input=VWNormal()(inputs);
    
    ee = tf.keras.layers.Concatenate()([normal_input,sprirep]);
    
   
    #接入编码
    encoded_patches=tf.keras.layers.Reshape((18,1), input_shape=(18,))(ee);
     
    encoded_patches=transformers_PatchEncoder(18,projection_dim)(encoded_patches);
    
    encoded_patches=transformers_PatchEncoder(18,projection_dim)(encoded_patches);
    
   
    
    '''
    #不接入编码
    encoded_patches=tf.keras.layers.Reshape((12,1), input_shape=(12,))(inputs);
    encoded_patches=transformers_PatchEncoder(12,projection_dim)(encoded_patches);
    encoded_patches=transformers_PatchEncoder(12,projection_dim)(encoded_patches);
    '''
    
    
    
    

    # Create multiple layers of the Transformer block.
    for _ in range(transformer_layers):
        # Layer normalization 1.
        x1 = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
        # Create a multi-head attention layer.
        attention_output = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=projection_dim, dropout=0.1
        )(x1, x1)
        # Skip connection 1.
        x2 = layers.Add()([attention_output, encoded_patches])
        # Layer normalization 2.
        x3 = layers.LayerNormalization(epsilon=1e-6)(x2)
        # MLP.
        x3 = mlp(x3, hidden_units=transformer_units, dropout_rate=0.1)
        # Skip connection 2.
        encoded_patches = layers.Add()([x3, x2])

    # Create a [batch_size, projection_dim] tensor.
    representation = layers.LayerNormalization(epsilon=1e-6)(encoded_patches)
    representation = layers.Flatten()(representation)
    representation = layers.Dropout(0.1)(representation)
    
    
    #print(tf.shape(spri));
    #print(tf.shape(representation));
   
    #将SPRI指数加进来
    
    representation = tf.keras.layers.Concatenate()([representation,sprirep]);
    
    # Add MLP.
    features = transformers_mlp(representation, hidden_units=mlp_head_units, dropout_rate=0.5)
    # Classify outputs.
    
    #features = tf.keras.layers.Concatenate()([features,sprirep]);
    
    #features = layers.Dense(2*num_classes+1, activation=tf.nn.gelu)(features)
    #将SPRI指数加进来
    #features = tf.keras.layers.Concatenate()([features,spri]);
    
    
    logits = layers.Dense(num_classes)(features)
    # Create the Keras model.
    model = keras.Model(inputs=inputs, outputs=logits)
    return model;


model=create_transformer_classifier();

learning_rate = 0.001
weight_decay = 0.0001
optimizer = tfa.optimizers.AdamW( learning_rate=learning_rate, weight_decay=weight_decay);
model.compile(optimizer=optimizer,loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True));

[alldata,alldecision,train_x,test_x,train_y1,train_y2,test_y1,test_y2]=dbdecision2021;
                     
r_x=train_x;
r_y=train_y2;
                                                  
model.fit(x=r_x, y=r_y, batch_size=100, epochs=600, validation_split=0.1);



      
