import requests,os,hashlib,sys
def setup():
    print("AWACoin JMR特供版")
    print("该软件为虚拟钱包，非区块链服务，不提供兑现。完全符合中国民法典的规定。")
    print("没有检测到钱包文件，正在创建属于你的独一无二的钱包")
    server="http://s1.jiangmuran.com:8848/"
    print("正在验证...")
    try:
        assert requests.get(server+"api/v1/get_chunk_diff").json()["diff"] > 1
    except:
        print("这不是一个有效的服务器。")
        exit(1)
    print("验证成功！")

    print("正在创建awacoin账号...")
    try:
        data = requests.get(server+"api/v1/register").json()
        with open(".awacoin_wallet","w+") as f:
            f.write(server+"+"+data["account"]+"+"+data["password"])
    except:
        print("账号创建失败！")
        exit(1)
def mine(server,acc,pwd,diff):
    mine=requests.post(server+"api/v1/mine/create",data={"account":acc,"password":pwd}).json()
    mineid=mine["id"]
    salt=mine["salt"]
    md5=mine["hash"]
    result=None
    for i in range(0,diff+1):
        if hashlib.sha512((str(i)+salt).encode("utf-8")).hexdigest()[:450] == md5:
            result=i
            print(f"Chunk result: {result}")
            break
    if not result:
        print("ERR: INVAILD MINE")
        return
    return requests.post(server+"api/v1/mine/finish",data={"id":mineid,"answer":i}).json()
if not os.path.exists(".awacoin_wallet"):
    print("未找到钱包文件")
    setup()

with open(".awacoin_wallet","r") as f:
    server,acc,pwd=f.read().split("+")
print("欢迎来到awacoin 命令行！")
if len(sys.argv) > 1 and sys.argv[1] == "mine":
    print("正在获得区块难度")
    diff=requests.get(server+"/api/v1/get_chunk_diff").json()["diff"]
    print("开始挖掘...")
    while 1:
        try:
            result=mine(server,acc,pwd,diff)
        except Exception as e:
            print(f"失败: {e}")
        else:
            if result.get("error"):
                print(f"失败: {result['error']}")
            else:
                print(f"当前余额: {result['balance']}")
    exit(0)
while 1:
    op=input("(0) 挖掘\n(1) 获得我的钱包地址\n(2) 转账\n(3) 获得余额\n\n你的操作> ")
    if op == "0":
        print("正在获得区块难度")
        diff=requests.get(server+"/api/v1/get_chunk_diff").json()["diff"]
        print("开始挖掘...")
        while 1:
            try:
                result=mine(server,acc,pwd,diff)
            except Exception as e:
                print(f"失败: {e}")
            else:
                if result.get("error"):
                    print(f"失败: {result['error']}")
                else:
                    print(f"当前余额: {result['balance']}")
    if op == "1":
        print(f"你的钱包地址:{acc}")
    if op == "2":
        dest=input("目标钱包：")
        amount=input("数量：")
        amount=float(amount)
        result=requests.post(server+"/api/v1/transfer",data={"account":acc,"password":pwd,"to":dest,"amount":amount}).json()
        if result.get("error"):
            print(f"转账失败：{result['error']}")
        else:
            print(f"成功，转账后余额：{result['balance']}")
    if op == "3":
        wallet=input("钱包(留空为自己): ")
        if not wallet:
            wallet=acc
        result=requests.get(server+"/api/v1/getbalance",params={"account":wallet}).json()
        if result.get("error"):
            print(f"获得失败：{result['error']}")
        else:
            print(f"余额：{result['balance']}")
    
