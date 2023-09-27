import torch.nn as nn

class ResidualBlock(nn.Module):
    # ResNet Basic Block으로 18, 34 layer에 들어가는 것들이다.
    # dimension 이 달라지는 경우
    dimension_expansion = 1  
    # size 축소시에 stride=2로 전달받음
    def __init__(self,in_channels, out_channels, stride=1):
        super().__init__()
        # stride = 1인 경우 size 유지, stride가 2 인 경우 size 2로 나눠짐
        self.residual_function = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3,stride=stride,padding=1,bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels * ResidualBlock.dimension_expansion, kernel_size=3,stride=1,padding=1,bias=False),
            nn.BatchNorm2d(out_channels * ResidualBlock.dimension_expansion),
        )
        # Shortcut 
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels * ResidualBlock.dimension_expansion:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels * ResidualBlock.dimension_expansion, kernel_size = 1,stride = stride, bias=False),
                nn.BatchNorm2d(out_channels * ResidualBlock.dimension_expansion),
            )
        # input, output 결합
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self,x):
        out = self.residual_function(x) + self.shortcut(x)
        out = self.relu(out)
        return out