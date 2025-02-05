import requests,json,asyncio
from web3 import Web3
import secrets

import string

def generate_random_name(length=6):
    """
    生成随机字母名字。
    
    参数:
        length (int): 名字的长度，默认为6
    
    返回:
        str: 随机生成的名字
    """
    # 生成随机字母
    letters = string.ascii_letters  # 包含大小写字母
    random_name = ''.join(secrets.choice(letters) for _ in range(length))
    return random_name



def generate_eth_wallets(n, output_file='account.txt'):
    """
    生成 n 个以太坊钱包，并将公钥和私钥写入指定文件。
    
    参数:
        n (int): 要生成的钱包数量
        output_file (str): 输出文件名，默认为 'account.txt'
    """
    # 创建 Web3 实例
    w3 = Web3()

    # 打开文件用于写入
    with open(output_file, 'w') as file:
        for _ in range(n):
            # 生成随机私钥
            private_key = secrets.token_hex(32)  # 32字节的随机私钥
            private_key = '0x' + private_key  # 添加 0x 前缀

            # 从私钥生成账户
            account = w3.eth.account.from_key(private_key)

            # 获取公钥（地址）
            public_key = account.address

            # 写入文件，格式为：公钥@私钥
            file.write(f"{public_key}@{private_key}\n")

    print(f"成功生成 {n} 个以太坊钱包，公钥和私钥已写入 {output_file}。")


def read_public_keys(file_path='account.txt'):
    """
    从指定文件中读取公钥，并返回一个包含所有公钥的列表。
    
    参数:
        file_path (str): 文件路径，默认为 'account.txt'
    
    返回:
        list: 包含所有公钥的列表
    """
    public_keys = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # 每行格式为：公钥@私钥，通过分割符 '@' 分割
                parts = line.strip().split('@')
                if len(parts) == 2:
                    public_key = parts[0]
                    public_keys.append(public_key)
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请确保文件路径正确。")
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
    
    return public_keys


def check_registration(wallet):

    url = f'https://kaleidofinance.xyz/api/testnet/check-registration?wallet={wallet}'
    result=requests.get(url=url)
    print()
    result=result.json()
    if result['isRegistered']==True:
        print('Wallet address already registered')
    else:
        print('Wallet address not registered')

async def register(wallet):
    
    url = 'https://kaleidofinance.xyz/api/testnet/register'
    # 生成一个随机名字    
    random_name = generate_random_name()
    #s使用了2925邮箱
    email="liam10628_{}@2925.com".format(random_name)
    data={"email":email,"walletAddress":wallet,"socialTasks":{"twitter":True,"telegram":True,"discord":True},"agreedToTerms":True,"referralCode":"4SIQAZF5","referralCount":0,"referralBonus":0,"xUsername":random_name,"referredBy":"4SIQAZF5"}
    headers = {'Content-Type': 'application/json'}
    result=requests.post(url=url,data=json.dumps(data))
    print(result.json())
    result=result.json()
    return result


async def main(public_keys_list):
    """
    异步处理公钥列表，调用 register 函数注册每个公钥。
    
    参数:
        public_keys_list (list): 公钥列表
    """
    # 创建一个任务列表
    tasks = [register(public_key) for public_key in public_keys_list]
    
    # 并发执行所有任务，捕获异常
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 处理结果
    for result in results:
        if isinstance(result, Exception):
            print(f"发生异常：{result}")
        else:
            print(result)

if __name__ == '__main__':
    #按需要设置生成的钱包数量
    generate_eth_wallets(100)
    # 示例：读取公钥
    public_keys_list = read_public_keys()
    print("生成钱包完成，开始注册...")
    # 运行异步主函数
    asyncio.run(main(public_keys_list))
    print("注册完成。")