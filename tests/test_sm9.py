

from gmssl import sm9
import json
import pickle
if __name__ == '__main__':
    idA = 'a'
    idB = 'b'

    print ("-----------------test sign and verify---------------")

    master_public, master_secret = sm9.setup ('sign')
    # (mpk, msk) ← Setup(λ).已知系统安全参数λ,系统建立算法Setup以λ为输入,输出系统主
    # 公钥mpk和主私钥msk,其中mpk是公开的,msk由KGC秘密保存.此算法由KGC执行

    Da = sm9.private_key_extract ('sign', master_public, master_secret, idA)
    # skID ← KeyGen(mpk, msk,ID).已知标识ID,用户私钥
    # 生成算法KeyGen以系统主公私钥对 (mpk, msk) 和 ID 为输入, 输出用户 ID 的私钥 skID. 此算法由 KGC 执行.

    message = 'abc'
    signature = sm9.sign (master_public, Da, message)
    # σ ← Sign(mpk, M, skID).已知消息M, 签名算法Sign以系统主公钥mpk、M
    # 和签名者的私钥skID为输入, 输出M的签名σ.此算法由签名者执行.

    assert (sm9.verify (master_public, idA, message, signature))
    # 1/0 ← Verify(mpk, M, σ, ID).验证算法Verify以系统主公钥mpk、签名消息M及其签名σ和签名者的标识ID
    # 为输入, 输出“1”或者“0”.“1”表示签名有效,“0”表示签名无效.此算法由验证者执行.

    print ("\t\t\t success")

    # print ("-----------------test key agreement---------------")
    #
    # master_public, master_secret = sm9.setup ('keyagreement')
    #
    # Da = sm9.private_key_extract ('keyagreement', master_public, master_secret, idA)
    # Db = sm9.private_key_extract ('keyagreement', master_public, master_secret, idB)
    #
    # xa, Ra = sm9.generate_ephemeral (master_public, idB)
    # xb, Rb = sm9.generate_ephemeral (master_public, idA)
    #
    # ska = sm9.generate_session_key (idA, idB, Ra, Rb, Da, xa, master_public, 'A', 128)
    # skb = sm9.generate_session_key (idA, idB, Ra, Rb, Db, xb, master_public, 'B', 128)
    #
    # assert (ska == skb)
    #
    # print ("\t\t\t success")
    
    print ("-----------------test encrypt and decrypt---------------")

    master_public, master_secret = sm9.setup ('encrypt')

    Da = sm9.private_key_extract ('encrypt', master_public, master_secret, idA)

    message = 'abc'
    ct = sm9.kem_dem_enc (master_public, idA, message, 32)
    pt = sm9.kem_dem_dec (master_public, idA, Da, ct, 32)

    assert (message == pt)

    print ("\t\t\t success")

    # print(Da)
    # print(master_public)
    # print(master_secret)
    # print(ct)
    # print(pt)
    # print(type(Da), type(master_public), type(master_secret), type(ct), type(pt))
    #
    # test1 = pickle.dumps(Da)
    # print(test1)
    # print(type(test1))
    # print(len(test1))
    # test2 = pickle.loads(test1)
    # test3 = sm9.kem_dem_dec(master_public, idA, test2, ct, 32)
    # print(test3)
    # print(master_public[0])
    # print(str(master_public[0][0]))
    # print(type(master_public[0][0]))
    # print(type(Da[0]))


