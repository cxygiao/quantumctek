import math

import numpy as np
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import torch.nn.functional as F

class PositionalEncoding(nn.Module):
    def __init__(self, hidden_size, dropout=0.1, max_len=5000):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, hidden_size, 2) * -(math.log(10000.0) / hidden_size))
        pe = torch.zeros(max_len, hidden_size)
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)  # shape: (max_len, 1, hidden_size)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return self.dropout(x)
class Transformer(nn.Module):
    """
        Parameters：
        - input_size: feature size
        - hidden_size: number of hidden units
        - output_size: number of output
        - num_layers: number of layers
        - num_heads: number of heads
        - dropout: dropout probability
    """

    def __init__(self, input_size, hidden_size=1, output_size=1, num_layers=2, num_heads=1, dropout=0.1):
        super().__init__()

        self.embedding = nn.Linear(input_size, hidden_size)
        self.positional_encoding = PositionalEncoding(hidden_size, dropout)
        self.transformer = nn.Transformer(
            d_model=hidden_size,
            nhead=num_heads,
            num_encoder_layers=num_layers,
            num_decoder_layers=num_layers,
            dim_feedforward=hidden_size*4,
            dropout=dropout
        )
        self.output_layer = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.embedding(x)
        x = self.positional_encoding(x)
        x = self.transformer(x, x) # self-attention
        x = self.output_layer(x)
        return x
class LstmRNN(nn.Module):

    def __init__(self, input_size, hidden_size=1, output_size=1, num_layers=2):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers)
        self.dropout = nn.Dropout(p=0.9)  # p is the probability of dropping out a neuron 第二列

        # self.lstm = nn.LSTM(input_size, hidden_size, num_layers)  # utilize the LSTM model in torch.nn
        self.forwardCalculation = nn.Sequential(nn.Linear(hidden_size, output_size))

    def forward(self, _x):
        x, _ = self.lstm(_x)  # _x is input, size (seq_len, batch, input_size)
        x = self.dropout(x)
        s, b, h = x.shape  # x is output, size (seq_len, batch, hidden_size)
        x = x.view(s * b, h)
        x = self.forwardCalculation(x)
        x = x.view(s, b, -1)
        return x

# class LstmRNN(nn.Module):
#     """
#         Parameters：
#         - input_size: feature size
#         - hidden_size: number of hidden units
#         - output_size: number of output
#         - num_layers: layers of LSTM to stack
#     """
#
#     def __init__(self, input_size, hidden_size=1, output_size=1, num_layers=2):
#         super().__init__()
#
#         self.lstm = nn.RNN(input_size, hidden_size, num_layers)  # utilize the LSTM model in torch.nn
#         self.forwardCalculation = nn.Sequential(nn.Linear(hidden_size, output_size))
#
#     def forward(self, _x):
#         x, _ = self.lstm(_x)  # _x is input, size (seq_len, batch, input_size)
#         s, b, h = x.shape  # x is output, size (seq_len, batch, hidden_size)
#         x = x.view(s * b, h)
#         x = self.forwardCalculation(x)
#         x = x.view(s, b, -1)
#         return x
class DualLstmRNN(nn.Module):
    def __init__(self, input_size=6, hidden_size=16, output_size=1, num_layers=1, dual_weight=0.1):
        super().__init__()
#第一列
        self.lstm = LstmRNN(input_size, hidden_size, output_size, num_layers)
        self.dual_weight = dual_weight

    def forward(self, _x, y):
        y_hat = self.lstm(_x)
        mse = torch.mean((y_hat - y)**2)
        loss = mse + self.dual_weight * torch.mean((y_hat.mean(0) - y.mean(0))**2, dim=0)
        return loss
# from keras import backend as K
# def r2(y_true, y_pred):
#     """
#     r2 returns the coefficient of determination R^2
#
#     The parameters are the target values y_true and the values predicted by the neural
#     network y_pred
#     """
#     # print(type(y_true))
#     # print(type(y_pred))
#     # y_true = y_true.detach().numpy()
#     # y_pred = y_true.detach().numpy()
#     SS_res = K.sum(K.square(y_true - y_pred))
#     SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
#     return (1 - SS_res / SS_tot)

if __name__ == '__main__':
    # create database

    class DiabetesDataset(Dataset):
        def __init__(self, filepath):
            xy = np.loadtxt('data/train_2.csv', delimiter=',', dtype=np.float32)
            self.len = xy.shape[0]
            self.t = xy[:, 0]
            self.x_data = xy[:,: 6]
            self.y_data = xy[:,-1]

        # 以上数据为np

        def __len__(self):
            return self.len


    Data = DiabetesDataset('data/train_2.csv')

    data_len = Data.len
    t = Data.t
    dataset = np.zeros((data_len, 7))
    dataset[:,: 6] = Data.x_data
    dataset[:, -1] = Data.y_data
    dataset = dataset.astype('float32')

    # # tensor的元素作归一化
    # in_max = dataset[:,: 6].max()
    # in_min = dataset[:,: 6].min()
    # out_max = dataset[:, -1].max()
    # out_min = dataset[:, -1].min()
    # dataset_normal = np.zeros((data_len,7))
    # dataset_normal[:,: 6] = (dataset[:,: 6]) / in_max
    # dataset_normal[:, -1] = dataset[:, -1] / 0.85
    # # dataset_normal[:, -1] = dataset[:, -1]
    # dataset_normal = dataset_normal.astype('float32')

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))  # 将数据归一到0到1，可以根据数据特点归一到-1到1
    dataset_normal = scaler.fit_transform(dataset[:,: 6])  # 归一化
    dataset_normal = dataset_normal.astype('float32')


    # # 将数据划分为训练集和测试集
    train_data_ratio = 0.7  # Choose 30% of the data for testing
    train_data_len = int(data_len * train_data_ratio)+1
    test_data_len = int(data_len * (1-train_data_ratio))
    train_x = dataset_normal[:train_data_len,:6]
    train_y = dataset_normal[:train_data_len, -1]
    INPUT_FEATURES_NUM = 6
    OUTPUT_FEATURES_NUM = 1
    # t_for_training = t[:train_data_len]

    test_x = dataset_normal[test_data_len:, : 6]
    test_y = dataset_normal[test_data_len:, -1]
    # t_for_testing = t[train_data_len:]

    # ----------------- train -------------------
    train_x_tensor = train_x.reshape(-1, 5, INPUT_FEATURES_NUM)  # set batch size to 5
    train_y_tensor = train_y.reshape(-1, 5, OUTPUT_FEATURES_NUM)  # set batch size to 5

    # transfer data to pytorch tensor
    train_x_tensor = torch.from_numpy(train_x_tensor)
    train_y_tensor = torch.from_numpy(train_y_tensor)
    # test_x_tensor = torch.from_numpy(test_x)

    lstm_model = LstmRNN(INPUT_FEATURES_NUM, 16, output_size=OUTPUT_FEATURES_NUM, num_layers=2)  # 16 hidden units
    loss_model = DualLstmRNN(INPUT_FEATURES_NUM, 16, output_size=OUTPUT_FEATURES_NUM, num_layers=2, dual_weight=0.1)  # 16 hidden units
    # print('LSTM model:', lstm_model)
    # print('model.parameters:', lstm_model.parameters)


    loss_function = nn.MSELoss()
    # loss_function=nn.CrossEntropyLoss()
    # loss_function = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(lstm_model.parameters(), lr=0.01)

    max_epochs = 100
    for epoch in range(max_epochs):
        output = lstm_model(train_x_tensor)
        # loss = torch.nn.CrossEntropyLoss(train_x_tensor,train_y_tensor)
        # loss = F.cross_entropy(train_x_tensor,train_y_tensor)
        loss = loss_function(output, train_y_tensor)
        loss1= loss_model(train_x_tensor,output)
        loss = loss + loss1
        # print("loss:::",loss)
        # print("output:::::::::::::", output)
        # print(type(output))

        # output = output.detach().numpy()
        # print(type(output))
        # train_y_tensor= train_y_tensor.detach().numpy()
        # train_y_tensor = train_y_tensor.squeeze()
        # output= output.squeeze()

        # print("train.shape",train_y_tensor.shape)
        # print("output.shape:::",output.shape)



        # bput = np.clip(output.detach().numpy().squeeze(), 0, 0.86)
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(0, 0.86))  # 将数据归一到0到1，可以根据数据特点归一到-1到1
        bput = scaler.fit_transform(output.detach().numpy().squeeze())  # 归一化

        from sklearn.metrics import r2_score
        r_2 = r2_score(train_y_tensor.detach().numpy().squeeze(), bput)


        # print("boutput::::::::::",bput)
        print("r2::::::{}     loss   {} ".format(r_2,loss))
        from math import sqrt
        if r_2 > 0.99:
            print('Epoch [{}/{}], Loss: {:.5f}      r2{}'.format(epoch + 1, max_epochs, loss.item(),r_2))
            print("The r2 value is reached")
            break

        # print("output.shape::::::",output.shape)
        # print("train_y_tensor.shape::::::", train_y_tensor)

        # output_epoch = output.detach().numpy()
        # train_y_tensor_epoch = train_y_tensor.detach().numpy()
        # output_epoch.reshape(350, 1, 1)  # set batch size to 5
        # train_y_tensor_epoch.reshape(350, 1, 1)  # set batch size to 5
        # print("output.shape::::::", type(output_epoch))
        # print("train_y_tensor.shape::::::", type(train_y_tensor_epoch))
        # print("output.shape::::::", output_epoch.shape)
        # print("train_y_tensor.shape::::::", train_y_tensor_epoch.shape)

        #print('Epoch [{}/{}], Loss: {:.5f},r2::{}'.format(epoch + 1, max_epochs, loss.item(), r2(train_y_tensor,output)))


        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if loss.item() < 1e-4:
            print('Epoch [{}/{}], Loss: {:.5f}'.format(epoch + 1, max_epochs, loss.item()))
            print("The loss value is reached")
            break
        elif (epoch + 1) % 10 == 0:
            print('Epoch: [{}/{}], Loss:{:.5f}'.format(epoch + 1, max_epochs, loss.item()))
