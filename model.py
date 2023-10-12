import torch.nn as nn
import torch
from torchsummary import summary
from game import State

DN_RESIDUAL_NUM = 16
DN_INPUT_SHAPE = (8, 17, 17) # player 1 말위치 + player 1이 놓은 벽
DN_OUTPUT_SIZE = 136

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
            nn.Linear(256, 4)  
        )

        self.policy_net = nn.Sequential(
            nn.Conv2d(512, 2, kernel_size = 3, stride = 1, padding = 1, bias=False),
            nn.BatchNorm2d(2),
            nn.ReLU(inplace=True),
            nn.Flatten(),
            nn.Linear(2*17*17, DN_OUTPUT_SIZE)
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
    # summary(model, DN_INPUT_SHAPE, device=device.type)

    state = State()
    a, b, c = DN_INPUT_SHAPE

    x = state.get_input_state() # 회전한 input을 받는다
    x =  torch.tensor(x, dtype=torch.float32)
    x = x.reshape(1, a, b, c)

    pred = model(x) 

    # make_dot(pred, params=dict(model.named_parameters())).render("model_graph", format="png")