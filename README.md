# coin-price-bot
A wechat robot querying coin prices and more...
## 功能
- 发送BTC、bitcoin、ETH等关键词时，返回当前价格（目前支持coinmarketcap能够查到的上千个币种）
- 发送以太坊地址时，返回该地址上所有ether和token的余额
- 发送GBI、GBI7、GBI30，返回区块链全球指数7天或30天走势
- 其他调侃回复
- 限制每分钟查询两次价格，防止刷屏

## 依赖
`itchat, pygal, cairosvg, lxml, tinycss, cssselect`

## 使用方法
将机器人微信号加入群聊中，运行程序，扫码登录即可

## 提示
建议用小号操作，频繁登录（主要是调试时）或发送重复消息可能导致被限制web登录
