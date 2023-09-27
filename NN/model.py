import torch.nn as nn
from torch.nn import BatchNorm2d
from block import ResidualBlock
import torch
from torchsummary import summary

class resnet(nn.Module):

    def __init__(self):
        super().__init__()
        self.in_channels = 64
        
        self.conv0 = nn.Sequential(
            nn.Conv2d(8, 64, kernel_size = 5, stride = 1, padding = 2, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)   
        )

        block_type = ResidualBlock
        num_blocks = [3, 4, 6, 3]

        self.layer0 = self.make_layer(block_type, 64, num_blocks[0], 1)
        self.layer1 = self.make_layer(block_type, 128, num_blocks[1], 1)
        self.layer2 = self.make_layer(block_type, 256, num_blocks[2], 1)
        self.layer3 = self.make_layer(block_type, 512, num_blocks[3], 1)
        self.avg_pool = nn.AdaptiveAvgPool2d((1,1))

        self.value_net = nn.Sequential(
            nn.Conv2d(512, 4, kernel_size = 3, stride = 1, padding = 1, bias=False),
            nn.BatchNorm2d(4),
            nn.ReLU(inplace=True),
            nn.Flatten(),
            nn.Linear(4*17*17, 256),
            nn.Linear(256, 1)  
        )

        self.policy_net = nn.Sequential(
            nn.Conv2d(512, 2, kernel_size = 3, stride = 1, padding = 1, bias=False),
            nn.BatchNorm2d(2),
            nn.ReLU(inplace=True),
            nn.Flatten(),
            nn.Linear(2*17*17, 136)
        )


    def make_layer(self, block_type, out_channels, num_block, stride):
        # stride가 2 일 경우 list 맨 앞만 2, 나머진 1
        strides = [stride] + [1] * (num_block-1)
        layers = []
        for stride in strides:
            layers.append(block_type(self.in_channels, out_channels, stride))
            self.in_channels = out_channels * block_type.dimension_expansion
        return nn.Sequential(*layers)


    def forward(self, x):
        out = self.conv0(x)
        out = self.layer0(out)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        value = self.value_net(out)
        policy = self.policy_net(out)
        return value, policy
    
if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(device)
    model = resnet().to(device)
    summary(model, (8, 17, 17), device=device.type)