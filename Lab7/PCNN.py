# -*- coding: utf-8 -*-

from .BasicModule import BasicModule
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class PCNN(BasicModule):
    '''
    the basic model
    Zeng 2014 "Relation Classification via Convolutional Deep Neural Network"
    '''

    def __init__(self, opt):
        super(PCNN, self).__init__()
        
        self.opt = opt

        self.model_name = 'PCNN'
        
        #单词的向量化表示
        self.word_embs = nn.Embedding(self.opt.vocab_size, self.opt.word_dim)
        self.init_word_emb()
        #句子的向量化表示，个数为100+2（左右各1）+1，维度为5
        self.pos1_embs = nn.Embedding(103, 5)
        self.pos2_embs = nn.Embedding(103, 5)
        self.convs = nn.Conv2d(in_channels   =  1,
                               out_channels  =  200,#通道数为200
                               kernel_size   =  (3, 50+5+5),#卷积核大小(3,50+5+5)
                               padding       =  (1, 0)) #same padding:补1个0，valid padding:不补0
        #全连接层1
        self.fc1 = nn.Linear(200, 100)
        #全连接层2
        self.fc2 = nn.Linear(100, 19)
        self.dropout = nn.Dropout(0.5)

    def init_word_emb(self):
        if self.opt.use_gpu:
            self.word_embs.weight.data.copy_(self.get_word_emb().cuda())
        else:
            self.word_embs.weight.data.copy_(self.get_word_emb())

    def get_word_emb(self):
        return torch.from_numpy(np.load(self.opt.w2v_path))

    def forward(self, x):
        lexical_feature, word_feature, left_pf, right_pf = x
        #数据处理，从int变成long
        lexical_feature=lexical_feature.long()
        word_feature = word_feature.long()
        left_pf = left_pf.long()
        right_pf =right_pf.long()

        # batch的大小由输入的size决定
        batch_size = lexical_feature.size(0)
        lexical_1 = self.word_embs(lexical_feature)
        # 改变lexical_1的形状
        lexical_1 = lexical_1.view(batch_size, -1)

        # sentence1
        word_emb = self.word_embs(word_feature)  
        left_emb = self.pos1_embs(left_pf)  
        right_emb = self.pos2_embs(right_pf) 
        #按维数2拼接
        sentence_1 = torch.cat([word_emb, left_emb, right_emb], 2) 

        #把s1升维
        sentence_1 = sentence_1.unsqueeze(1)
        sentence_1 = self.dropout(sentence_1)
        sentence_2 = F.relu(self.convs(sentence_1)).squeeze(3)
        sentence_3 = F.max_pool1d(sentence_2, sentence_2.size(2)).squeeze(2)
        sentence_3 = torch.cat([sentence_3], 1)
        #经过一个全连接层
        sentence_3 = self.fc1(sentence_3)
        output = torch.tanh(sentence_3)
        output = self.dropout(output)
        output = self.fc2(output)
        return output
