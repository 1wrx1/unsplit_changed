import collections

import torch
import torch.nn as nn

class MnistNet(nn.Module):
    def __init__(self, n_channels=1):
        super(MnistNet, self).__init__()
        self.features = []
        self.initial = None
        self.classifier = []
        self.layers = collections.OrderedDict()

        self.conv1 = nn.Conv2d(
            in_channels=n_channels,
            out_channels=8,
            kernel_size=5
        )
        self.features.append(self.conv1)
        self.layers['conv1'] = self.conv1

        self.ReLU1 = nn.ReLU(False)
        self.features.append(self.ReLU1)
        self.layers['ReLU1'] = self.ReLU1

        self.pool1 = nn.MaxPool2d(2, 2)
        self.features.append(self.pool1)
        self.layers['pool1'] = self.pool1

        self.conv2 = nn.Conv2d(
            in_channels=8,
            out_channels=16,
            kernel_size=5
        )
        self.features.append(self.conv2)
        self.layers['conv2'] = self.conv2

        self.ReLU2 = nn.ReLU(False)
        self.features.append(self.ReLU2)
        self.layers['ReLU2'] = self.ReLU2

        self.pool2 = nn.MaxPool2d(2, 2)
        self.features.append(self.pool2)
        self.layers['pool2'] = self.pool2

        self.feature_dims = 16 * 4 * 4
        self.fc1 = nn.Linear(self.feature_dims, 120)
        self.classifier.append(self.fc1)
        self.layers['fc1'] = self.fc1
     
        self.fc1act = nn.ReLU(False)
        self.classifier.append(self.fc1act)
        self.layers['fc1act'] = self.fc1act
     
        self.fc2 = nn.Linear(120, 84)
        self.classifier.append(self.fc2)
        self.layers['fc2'] = self.fc2
     
        self.fc2act = nn.ReLU(False)
        self.classifier.append(self.fc2act)
        self.layers['fc2act'] = self.fc2act
     
        self.fc3 = nn.Linear(84, 10)
        self.classifier.append(self.fc3)
        self.layers['fc3'] = self.fc3
        
        self.initial_params = [param.clone().detach().data for param in self.parameters()]

    def forward(self, x, start=0, end=10):
        if start <= 5: # start in self.features
            for idx, layer in enumerate(self.features[start:]):
                x = layer(x)
                if idx == end:
                    return x
            x = x.view(-1, self.feature_dims)
            for idx, layer in enumerate(self.classifier):
                x = layer(x)
                if idx + 6 == end:
                    return x
        else:
            if start == 6:
                x = x.view(-1, self.feature_dims)
            for idx, layer in enumerate(self.classifier):
                if idx >= start - 6:
                    x = layer(x)
                if idx + 6 == end:
                    return x
                
    def get_params(self, end=10):
        params = []
        for layer in list(self.layers.values())[:end+1]:
            params += list(layer.parameters())
        return params

    def restore_initial_params(self):
        for param, initial in zip(self.parameters(), self.initial_params):
            param.data = initial.requires_grad_(True)
            

class CifarNet(nn.Module):
    def __init__(self, n_channels=3):
        super(CifarNet, self).__init__()
        self.features = []
        self.initial = None
        self.classifier = []
        self.layers = collections.OrderedDict()

        self.conv11 = nn.Conv2d(
            in_channels=n_channels,
            out_channels=64,
            kernel_size=3,
            padding=1
        )
        self.features.append(self.conv11)
        self.layers['conv11'] = self.conv11

        self.ReLU11 = nn.ReLU(True)
        self.features.append(self.ReLU11)
        self.layers['ReLU11'] = self.ReLU11
        
        self.conv12 = nn.Conv2d(
            in_channels=64,
            out_channels=64,
            kernel_size=3,
            padding=1
        )
        self.features.append(self.conv12)
        self.layers['conv12'] = self.conv12
        
        self.ReLU12 = nn.ReLU(True)
        self.features.append(self.ReLU12)
        self.layers['ReLU12'] = self.ReLU12

        self.pool1 = nn.MaxPool2d(2, 2)
        self.features.append(self.pool1)
        self.layers['pool1'] = self.pool1

        self.conv21 = nn.Conv2d(
            in_channels=64,
            out_channels=128,
            kernel_size=3,
            padding=1
        )
        self.features.append(self.conv21)
        self.layers['conv21'] = self.conv21

        self.ReLU21 = nn.ReLU(True)
        self.features.append(self.ReLU21)
        self.layers['ReLU21'] = self.ReLU21
        
        self.conv22 = nn.Conv2d(
            in_channels=128,
            out_channels=128,
            kernel_size=3,
            padding=1
        )
        self.features.append(self.conv22)
        self.layers['conv22'] = self.conv22
        
        self.ReLU22 = nn.ReLU(True)
        self.features.append(self.ReLU22)
        self.layers['ReLU22'] = self.ReLU22

        self.pool2 = nn.MaxPool2d(2, 2)
        self.features.append(self.pool2)
        self.layers['pool2'] = self.pool2
        
        self.conv31 = nn.Conv2d(
            in_channels=128,
            out_channels=128,
            kernel_size=3,
            padding=1
        )
        self.features.append(self.conv31)
        self.layers['conv31'] = self.conv31
        
        self.ReLU31 = nn.ReLU(True)
        self.features.append(self.ReLU31)
        self.layers['ReLU31'] = self.ReLU31
        
        self.conv32 = nn.Conv2d(
            in_channels=128,
            out_channels=128,
            kernel_size=3,
            padding=1
        )
        self.features.append(self.conv32)
        self.layers['conv32'] = self.conv32
        
        self.ReLU32 = nn.ReLU(True)
        self.features.append(self.ReLU32)
        self.layers['ReLU32'] = self.ReLU32
        
        self.pool3 = nn.MaxPool2d(2, 2)
        self.features.append(self.pool3)
        self.layers['pool3'] = self.pool3
    
        self.feature_dims = 4 * 4 * 128
        self.fc1 = nn.Linear(self.feature_dims, 512)
        self.classifier.append(self.fc1)
        self.layers['fc1'] = self.fc1

        self.fc1act = nn.Sigmoid()
        self.classifier.append(self.fc1act)
        self.layers['fc1act'] = self.fc1act

        self.fc2 = nn.Linear(512, 10)
        self.classifier.append(self.fc2)
        self.layers['fc2'] = self.fc2

        self.initial_params = [param.data for param in self.parameters()]

    def forward(self, x, start=0, end=17):
        if start <= len(self.features)-1: # start in self.features
            for idx, layer in enumerate(self.features[start:]):
                x = layer(x)
                if idx == end:
                    return x
            x = x.view(-1, self.feature_dims)
            for idx, layer in enumerate(self.classifier):
                x = layer(x)
                if idx + 15 == end:
                    return x
        else:
            if start == 15:
                x = x.view(-1, self.feature_dims)
            for idx, layer in enumerate(self.classifier):
                if idx >= start - 15:
                    x = layer(x)
                if idx + 15 == end:
                    return x

    def get_params(self, end=17):
        params = []
        for layer in list(self.layers.values())[:end+1]:
            params += list(layer.parameters())
        return params

    def restore_initial_params(self):
        for param, initial in zip(self.parameters(), self.initial_params):
            param.data = initial
            

# 定义基本的卷积块
class BasicBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1):
        super(BasicBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
    
    def forward(self, x):
        identity = x
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)
        
        out += self.shortcut(identity)
        out = self.relu(out)
        
        return out
            

class ResNet18(nn.Module):
    def __init__(self, block, layers, num_classes=10):
        super(ResNet18, self).__init__()
        self.features = []
        self.initial = None
        self.classifier = []
        self.layers = collections.OrderedDict()
        self.in_channels = 64

        self.conv11 = nn.Conv2d(
            in_channels=3,
            out_channels=64,
            kernel_size=7,
            stride=2,
            padding=3,
            bias = False
        )
        self.features.append(self.conv11)
        self.layers['conv11'] = self.conv11
        
        self.bn1 = nn.BatchNorm2d(64)
        self.features.append(self.bn1)
        self.layers['BN1'] = self.bn1

        self.ReLU11 = nn.ReLU(True)
        self.features.append(self.ReLU11)
        self.layers['ReLU11'] = self.ReLU11
        
        self.maxpool = nn.MaxPool2d(
            kernel_size=3,
            stride=2,
            padding=1
        )
        self.features.append(self.maxpool)
        self.layers['maxpool'] = self.maxpool
        
        self.layer1 = self._make_layer(
            block,
            64,
            layers[0],
            stride=1
        )
        self.features.append(self.layer1)
        self.layers['layer1'] = self.layer1
        
        self.layer2 = self._make_layer(
            block,
            128,
            layers[1],
            stride=2
        )
        self.features.append(self.layer2)
        self.layers['layer2'] = self.layer2
        
        self.layer3 = self._make_layer(
            block,
            256,
            layers[2],
            stride=2
        )
        self.features.append(self.layer3)
        self.layers['layer3'] = self.layer3
        
        self.layer4 = self._make_layer(
            block,
            512,
            layers[3],
            stride=2
        )
        self.features.append(self.layer4)
        self.layers['layer4'] = self.layer4
        
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.features.append(self.avgpool)
        self.layers['avgpool'] = self.avgpool
    
        self.feature_dims = 512
        self.fc = nn.Linear(self.feature_dims, num_classes)
        self.classifier.append(self.fc)
        self.layers['fc'] = self.fc

        self.initial_params = [param.data for param in self.parameters()]
        
    def _make_layer(self, block, out_channels, blocks, stride=1):
        layer_res = []
        layer_res.append(block(self.in_channels, out_channels, stride))
        self.in_channels = out_channels
        
        for _ in range(1, blocks):
            layer_res.append(block(out_channels, out_channels))
        
        return nn.Sequential(*layer_res)

    def forward(self, x, start=0, end=9):
        if start <= len(self.features)-1: # start in self.features
            for idx, layer in enumerate(self.features[start:]):
                x = layer(x)
                if idx == end:
                    return x
            x = x.view(-1, self.feature_dims)
            for idx, layer in enumerate(self.classifier):
                x = layer(x)
                if idx + 9 == end:
                    return x
        else:
            if start == 9:
                x = x.view(-1, self.feature_dims)
            for idx, layer in enumerate(self.classifier):
                if idx >= start - 9:
                    x = layer(x)
                if idx + 9 == end:
                    return x

    def get_params(self, end=9):
        params = []
        for layer in list(self.layers.values())[:end+1]:
            params += list(layer.parameters())
        return params

    def restore_initial_params(self):
        for param, initial in zip(self.parameters(), self.initial_params):
            param.data = initial